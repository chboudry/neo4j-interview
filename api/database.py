import os
import csv
from neo4j import GraphDatabase
from typing import List
from models import Employee, EmployeeWithRelationships, Relationship

class Neo4jClient:   
    """Singleton class to manage Neo4j database connection and operations""" 
    def __init__(self):
        # Try to load local .env file for development outside container
        #if os.path.exists('.env.local'):
        #    from dotenv import load_dotenv
        #    load_dotenv('.env.local')
        
        # Check if we're in the dev container
        self.uri = os.getenv("NEO4J_URI")        
        self.username = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = os.getenv("NEO4J_DATABASE")
        self.driver = None
        
    def connect(self):
        try:
            self.driver = GraphDatabase.driver(
                self.uri, 
                auth=(self.username, self.password)
            )
            # Test the connection
            with self.driver.session(database=self.database) as session:
                session.run("RETURN 1")
            print(f"Connected to Neo4j at {self.uri}")
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            raise
    
    def close(self):
        if self.driver:
            self.driver.close()
    
    def get_employees(self) -> List[Employee]:
        """Fetch all employees from Neo4j database"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (e:Employee)
                RETURN e.name as name, 
                       e.id as id, 
                       e.email as email,
                       e.department as department,
                       e.position as position
                ORDER BY e.name
            """)
            
            employees = []
            for record in result:
                employee_data = {
                    "name": record["name"],
                    "id": record["id"],
                    "email": record["email"],
                    "department": record["department"],
                    "position": record["position"]
                }
                # Filter out None values
                employee_data = {k: v for k, v in employee_data.items() if v is not None}
                employees.append(Employee(**employee_data))
            
            return employees
    
    def get_employees_with_relationships(self) -> List[EmployeeWithRelationships]:
        """Fetch all employees with their relationships"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (e:Employee)
                OPTIONAL MATCH (e)-[:REPORTS_TO]->(boss:Employee)
                OPTIONAL MATCH (subordinate:Employee)-[:REPORTS_TO]->(e)
                OPTIONAL MATCH (e)-[:FRIENDS_WITH]-(friend:Employee)
                RETURN e.name as name,
                       e.id as id,
                       e.email as email,
                       e.department as department,
                       e.position as position,
                       e.hire_date as hire_date,
                       boss.name as boss_name,
                       COLLECT(DISTINCT subordinate.name) as direct_reports,
                       COLLECT(DISTINCT friend.name) as friends
                ORDER BY e.name
            """)
            
            employees = []
            for record in result:
                employee_data = {
                    "name": record["name"],
                    "id": record["id"],
                    "email": record["email"],
                    "department": record["department"],
                    "position": record["position"],
                    "hire_date": record["hire_date"]
                }
                # Filter out None values
                employee_data = {k: v for k, v in employee_data.items() if v is not None}
                employee = Employee(**employee_data)
                
                # Filter out None/empty values from relationships
                direct_reports = [name for name in record["direct_reports"] if name]
                friends = [name for name in record["friends"] if name]
                
                emp_with_rel = EmployeeWithRelationships(
                    employee=employee,
                    boss=record["boss_name"],
                    direct_reports=direct_reports,
                    friends=friends
                )
                employees.append(emp_with_rel)
            
            return employees
    
    def get_relationships(self) -> List[Relationship]:
        """Get all relationships in the database"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (a:Employee)-[r]->(b:Employee)
                RETURN a.name as from_employee, 
                       b.name as to_employee, 
                       TYPE(r) as relationship_type
                ORDER BY a.name, b.name
            """)
            
            relationships = []
            for record in result:
                rel = Relationship(
                    from_employee=record["from_employee"],
                    to_employee=record["to_employee"],
                    relationship_type=record["relationship_type"]
                )
                relationships.append(rel)
            
            return relationships
    
    def load_csv_data(self):
        """Load employee data from CSV files"""
        # Clear existing data
        with self.driver.session(database=self.database) as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Cleared existing data")
        
        # Load employees from boss relationships CSV
        boss_file = "../dataset/employees-and-their-boss.csv"
        if os.path.exists(boss_file):
            self._load_boss_relationships(boss_file)
        else:
            print(f"Boss relationships file not found: {boss_file}")
        
        # Load friend relationships CSV
        friends_file = "../dataset/employees-and-their-friends.csv"
        if os.path.exists(friends_file):
            self._load_friend_relationships(friends_file)
        else:
            print(f"Friends relationships file not found: {friends_file}")
    
    def _load_boss_relationships(self, file_path: str):
        """Load boss-employee relationships from CSV"""
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            with self.driver.session(database=self.database) as session:
                for row in reader:
                    employee_name = row['employee name'].strip()
                    boss_name = row['has boss'].strip()
                    
                    # Create employee and boss nodes if they don't exist
                    session.run("""
                        MERGE (emp:Employee {name: $employee_name})
                        SET emp.id = $employee_name
                        MERGE (boss:Employee {name: $boss_name})
                        SET boss.id = $boss_name
                        MERGE (emp)-[:REPORTS_TO]->(boss)
                    """, employee_name=employee_name, boss_name=boss_name)
        
        print(f"Loaded boss relationships from {file_path}")
    
    def _load_friend_relationships(self, file_path: str):
        """Load friendship relationships from CSV"""
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            with self.driver.session(database=self.database) as session:
                for row in reader:
                    employee_name = row['employee name'].strip()
                    friend_name = row['is friends with'].strip()
                    
                    # Skip self-references (like "Millie,Millie")
                    if employee_name == friend_name:
                        continue
                    
                    # Create employee and friend nodes if they don't exist
                    session.run("""
                        MERGE (emp:Employee {name: $employee_name})
                        SET emp.id = $employee_name
                        MERGE (friend:Employee {name: $friend_name})
                        SET friend.id = $friend_name
                        MERGE (emp)-[:FRIENDS_WITH]->(friend)
                    """, employee_name=employee_name, friend_name=friend_name)
        
        print(f"Loaded friendship relationships from {file_path}")
    
    def seed_sample_data(self):
        """Load data from CSV files instead of hardcoded sample data"""
        print("Loading employee data from CSV files...")
        try:
            self.load_csv_data()
            
            # Get count of employees loaded
            with self.driver.session(database=self.database) as session:
                result = session.run("MATCH (e:Employee) RETURN COUNT(e) as count")
                count = result.single()["count"]
                print(f"Successfully loaded {count} employees from CSV data!")
                
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            # Fallback to sample data if CSV loading fails   


# Global instance
neo4j_client = Neo4jClient()

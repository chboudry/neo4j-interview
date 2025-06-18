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
        
        # Get the Neo4j URI and try different connection strategies
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")
        self.driver = None
        
        # Store fallback URIs for different scenarios
        self.fallback_uris = [
            self.uri,  # Original URI from environment
            "bolt://localhost:8888",  # Dev container port forwarding
            "bolt://host.docker.internal:8888",  # Docker Desktop
            "bolt://neo4j-gds:7687",  # Direct container name
        ]
        
    def connect(self):
        """Try to connect to Neo4j using different URI strategies"""
        last_error = None
        
        for uri in self.fallback_uris:
            try:
                print(f"Attempting to connect to Neo4j at {uri}")
                self.driver = GraphDatabase.driver(
                    uri, 
                    auth=(self.username, self.password)
                )
                # Test the connection
                with self.driver.session(database=self.database) as session:
                    session.run("RETURN 1")
                print(f"Successfully connected to Neo4j at {uri}")
                self.uri = uri  # Store the successful URI
                return
            except Exception as e:
                print(f"Failed to connect to {uri}: {e}")
                last_error = e
                if self.driver:
                    self.driver.close()
                    self.driver = None
        
        # If all attempts failed, raise the last error
        raise Exception(f"Could not connect to Neo4j after trying all URIs. Last error: {last_error}")
    
    def close(self):
        if self.driver:
            self.driver.close()
    
    def get_employees(self) -> List[Employee]:
        """Fetch all employees from Neo4j database"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (e:Employee)
                RETURN e.name as name, 
                       e.emp_id as emp_id, 
                       e.email as email,
                       e.department as department,
                       e.position as position
                ORDER BY e.name
            """)
            
            employees = []
            for record in result:
                employee_data = {
                    "name": record["name"],
                    "emp_id": record["emp_id"],
                    "email": record["email"],
                    "department": record["department"],
                    "position": record["position"]
                }
                # Filter out None values
                employee_data = {k: v for k, v in employee_data.items() if v is not None}
                employees.append(Employee(**employee_data))
            
            return employees
    
    def ensure_unique_constraints(self):
        """Set up database constraints for unique employee IDs"""
        with self.driver.session(database=self.database) as session:
            try:
                session.run("CREATE CONSTRAINT emp_id FOR (e:Employee) REQUIRE e.emp_id IS UNIQUE")
            except Exception as e:
                print(f"Constraints may already exist: {e}")


    def create_employee(self, employee: Employee):
        """Create a new employee node in the Neo4j database"""
        with self.driver.session(database=self.database) as session:
            session.run("""
                 CREATE (e:Employee {
                    emp_id: $emp_id,
                    name: $name,
                    email: $email,
                    department: $department,
                    position: $position
                })
            """, 
            name=employee.name, 
            emp_id=employee.emp_id, 
            email=employee.email, 
            department=employee.department, 
            position=employee.position)

    def get_employees_with_relationships(self) -> List[EmployeeWithRelationships]:
        """Fetch all employees with their relationships"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (e:Employee)
                OPTIONAL MATCH (e)-[:REPORTS_TO]->(boss:Employee)
                OPTIONAL MATCH (subordinate:Employee)-[:REPORTS_TO]->(e)
                OPTIONAL MATCH (e)-[:FRIENDS_WITH]-(friend:Employee)
                RETURN e.name as name,
                       e.emp_id as emp_id,
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
                    "emp_id": record["emp_id"],
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
        boss_file = "./dataset/employees-and-their-boss.csv"
        if os.path.exists(boss_file):
            self._load_boss_relationships(boss_file)
        else:
            print(f"Boss relationships file not found: {boss_file}")
        
        # Load friend relationships CSV
        friends_file = "./dataset/employees-and-their-friends.csv"
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
                        MERGE (boss:Employee {name: $boss_name})
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
                        //SET emp.id = $employee_name
                        MERGE (friend:Employee {name: $friend_name})
                        //SET friend.id = $friend_name
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
    def get_graph_data(self) -> dict:
        """Get graph data in NVL format with nodes and relationships"""
        with self.driver.session(database=self.database) as session:
            # Get nodes (employees)
            nodes_result = session.run("""
                MATCH (e:Employee)
                RETURN e.emp_id as id,
                       e.name as name,
                       e.department as department,
                       e.position as position,
                       e.email as email
                ORDER BY e.name
            """)
            
            nodes = []
            for record in nodes_result:
                node = {
                    "id": str(record["id"]) if record["id"] is not None else record["name"].replace(" ", "_"),
                    "name": record["name"],
                    "department": record["department"],
                    "position": record["position"],
                    "email": record["email"]
                }
                # Remove None values
                node = {k: v for k, v in node.items() if v is not None}
                nodes.append(node)
            
            # Get relationships
            rels_result = session.run("""
                MATCH (a:Employee)-[r]->(b:Employee)
                RETURN a.emp_id as from_id,
                       a.name as from_name,
                       b.emp_id as to_id,
                       b.name as to_name,
                       TYPE(r) as rel_type,
                       id(r) as rel_id
                ORDER BY a.name, b.name
            """)
            
            relationships = []
            for record in rels_result:
                from_id = str(record["from_id"]) if record["from_id"] is not None else record["from_name"].replace(" ", "_")
                to_id = str(record["to_id"]) if record["to_id"] is not None else record["to_name"].replace(" ", "_")
                
                rel = {
                    "id": str(record["rel_id"]),
                    "from": from_id,
                    "to": to_id,
                    "type": record["rel_type"]
                }
                relationships.append(rel)
            
            return {
                "nodes": nodes,
                "relationships": relationships
            }

# Create a global instance for use across the application
neo4j_client = Neo4jClient()

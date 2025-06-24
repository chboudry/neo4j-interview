from fastapi import APIRouter, HTTPException
from models import Employee, Relationship, BossRelationship, FriendshipRelationship, EmployeeResponse, RelationshipResponse, EmployeeNetworkResponse, GraphData
from database import neo4j_client


routes = APIRouter()

@routes.get("/")
def root():
    return {"message": "Welcome to Neo4j Interview API"}


@routes.get("/health")
def health():
    return {"status": "healthy"}


# Optionally seed sample data on startup
@routes.post("/seed")
def seed_data():
    """
    Seed the Neo4j database with sample data
    """
    try:
        neo4j_client.seed_sample_data()
        return {"message": "Sample data seeded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to seed sample data: {str(e)}")
    
@routes.get("/employees", response_model=EmployeeResponse)
def list_employees():
    """
    Get all employees from the Neo4j database
    """
    try:
        employees = neo4j_client.get_employees()
        return EmployeeResponse(employees=employees, total=len(employees))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch employees: {str(e)}")
    
@routes.get("/employees-with-relationship", response_model=EmployeeNetworkResponse)
def get_employee_network():
    """
    Get the complete employee network including all relationship data
    """
    try:
        employee_network = neo4j_client.get_employees_with_relationships()
        return EmployeeNetworkResponse(employees=employee_network, total=len(employee_network))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch employee network: {str(e)}")


@routes.get("/relationships", response_model=RelationshipResponse)
def list_relationships():
    """
    Get all relationships (boss and friendship) from the Neo4j database
    """
    try:
        relationships = neo4j_client.get_relationships()
        return RelationshipResponse(relationships=relationships, total=len(relationships))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch relationships: {str(e)}")
    
@routes.post("/employees", response_model=EmployeeResponse)
def create_employee(employee: Employee):
    """
    Create a new employee in the Neo4j database
    """
    try:
        neo4j_client.create_employee(employee)
        return EmployeeResponse(employees=[employee], total=1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create employee: {str(e)}")
    
@routes.get("/graph")
def get_graph_data():
    """
    Get graph data in NVL format for visualization
    """
    try:
        graph_data = neo4j_client.get_graph_data()
        return graph_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch graph data: {str(e)}")



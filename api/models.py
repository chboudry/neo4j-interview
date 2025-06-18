from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Employee(BaseModel):
    """Basic employee node"""
    name: str
    emp_id: Optional[int] = None  # Can be auto-generated from name
    email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None


class Relationship(BaseModel):
    """Generic relationship between two employees"""
    from_employee: str
    to_employee: str
    relationship_type: str  # "REPORTS_TO", "FRIENDS_WITH", etc.


class BossRelationship(BaseModel):
    """Employee reporting relationship"""
    employee_name: str
    boss_name: str


class FriendshipRelationship(BaseModel):
    """Friendship relationship between employees"""
    employee_name: str
    friend_name: str


class EmployeeWithRelationships(BaseModel):
    """Employee with their relationships"""
    employee: Employee
    boss: Optional[str] = None
    direct_reports: List[str] = []
    friends: List[str] = []


class EmployeeResponse(BaseModel):
    employees: List[Employee]
    total: int


class RelationshipResponse(BaseModel):
    relationships: List[Relationship]
    total: int


class EmployeeNetworkResponse(BaseModel):
    """Complete employee network with relationships"""
    employees: List[EmployeeWithRelationships]
    total: int


# NVL Graph Models
class NVLNode(BaseModel):
    """Node model for NVL visualization"""
    id: str
    name: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    email: Optional[str] = None


class NVLRelationship(BaseModel):
    """Relationship model for NVL visualization"""
    id: str
    from_node: str
    to: str
    type: Optional[str] = None


class GraphData(BaseModel):
    """Complete graph data for NVL visualization"""
    nodes: List[NVLNode]
    relationships: List[NVLRelationship]

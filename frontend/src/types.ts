export interface Employee {
  name: string;
  id?: string;
  email?: string;
  department?: string;
  position?: string;
  hire_date?: string;
}

export interface Relationship {
  from_employee: string;
  to_employee: string;
  relationship_type: string;
}

export interface BossRelationship {
  employee_name: string;
  boss_name: string;
}

export interface FriendshipRelationship {
  employee_name: string;
  friend_name: string;
}

export interface EmployeeWithRelationships {
  employee: Employee;
  boss?: string;
  direct_reports: string[];
  friends: string[];
}

export interface EmployeeResponse {
  employees: Employee[];
  total: number;
}

export interface RelationshipResponse {
  relationships: Relationship[];
  total: number;
}

export interface EmployeeNetworkResponse {
  employees: EmployeeWithRelationships[];
  total: number;
}

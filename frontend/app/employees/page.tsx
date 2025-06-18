'use client'

import { useState, useEffect } from 'react'

interface Employee {
  id: string
  name: string
  email: string
  department: string
  position: string
  hire_date: string
}

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<Employee[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/employees')
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`)
        }
        return res.json()
      })
      .then(data => {
        setEmployees(data.employees || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching employees:', err)
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading employees...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">
          <h2>Error loading employees</h2>
          <p>{error}</p>
          <p>Make sure the API server is running on port 8000</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1>Employee Directory</h1>
        <p>Total employees: {employees.length}</p>
      </div>
      
      <div className="employees-grid">
        {employees.map(employee => (
          <div key={employee.id} className="employee-card">
            <div className="employee-header">
              <h3>{employee.name}</h3>
              <span className="employee-id">ID: {employee.id}</span>
            </div>
            <div className="employee-details">
              <p><strong>Email:</strong> {employee.email}</p>
              <p><strong>Department:</strong> {employee.department}</p>
              <p><strong>Position:</strong> {employee.position}</p>
              {employee.hire_date && (
                <p><strong>Hire Date:</strong> {new Date(employee.hire_date).toLocaleDateString()}</p>
              )}
            </div>
          </div>
        ))}
      </div>

      {employees.length === 0 && (
        <div className="empty-state">
          <h3>No employees found</h3>
          <p>The employee database appears to be empty.</p>
        </div>
      )}
    </div>
  )
}

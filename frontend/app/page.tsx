'use client'

import { useState, useEffect } from 'react'

interface Employee {
  id: string
  name: string
  email: string
  department: string
  position: string
}

export default function Home() {
  const [employees, setEmployees] = useState<Employee[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/employees')
      .then(res => res.json())
      .then(data => {
        setEmployees(data.employees || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching employees:', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div className="container">Loading...</div>
  }

  return (
    <div className="container">
      <h1>Neo4j Interview Project</h1>
      <h2>Employees ({employees.length})</h2>
      
      <div className="employees-grid">
        {employees.map(employee => (
          <div key={employee.id} className="employee-card">
            <h3>{employee.name}</h3>
            <p><strong>Email:</strong> {employee.email}</p>
            <p><strong>Department:</strong> {employee.department}</p>
            <p><strong>Position:</strong> {employee.position}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

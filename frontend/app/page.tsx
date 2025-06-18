export default function Home() {
  return (
    <div className="container">
      <div className="hero">
        <h1>Hello! Welcome to Neo4j Interview Project</h1>
        <p>This is a full-stack application showcasing Neo4j graph database integration with a modern React frontend.</p>
        
        <div className="features">
          <div className="feature-card">
            <h3>📊 Employee Management</h3>
            <p>Browse and manage employee data stored in Neo4j</p>
          </div>
          
          <div className="feature-card">
            <h3>🕸️ Graph Visualization</h3>
            <p>Interactive graph visualization of relationships between employees</p>
          </div>
          
          <div className="feature-card">
            <h3>🔗 Relationship Analysis</h3>
            <p>Explore reporting structures and social connections</p>
          </div>
        </div>
      </div>
    </div>
  )
}

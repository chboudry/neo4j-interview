import Link from 'next/link'

export default function Header() {
  return (
    <header className="header">
      <div className="header-container">
        <div className="logo">
          <Link href="/">Neo4j Interview App</Link>
        </div>
        <nav className="nav">
          <Link href="/" className="nav-link">Home</Link>
          <Link href="/employees" className="nav-link">Employees</Link>
          <Link href="/graph" className="nav-link">Graph Visualization</Link>
        </nav>
      </div>
    </header>
  )
}

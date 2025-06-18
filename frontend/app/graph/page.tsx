'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import type { MouseEventCallbacks } from '@neo4j-nvl/react'
import type { HitTargets, Node, Relationship } from '@neo4j-nvl/base'

// Dynamically import the NVL component to prevent SSR issues
const InteractiveNvlWrapper = dynamic(
  () => import('@neo4j-nvl/react').then((mod) => ({ default: mod.InteractiveNvlWrapper })),
  { 
    ssr: false,
    loading: () => <div>Loading graph visualization...</div>
  }
)

// Define interfaces for our graph data
interface GraphNode {
  id: string
  name?: string
  department?: string
  position?: string
  email?: string
}

interface GraphRelationship {
  id: string
  from: string
  to: string
  type?: string
}

interface GraphData {
  nodes: GraphNode[]
  relationships: GraphRelationship[]
}

export default function GraphPage() {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], relationships: [] })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedElement, setSelectedElement] = useState<Node | Relationship | null>(null)

  // Mouse event callbacks for NVL interactions
  const mouseEventCallbacks: MouseEventCallbacks = {
    onHover: (element: Node | Relationship, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('onHover', element, hitTargets, evt)
    },
    onRelationshipRightClick: (rel: Relationship, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('onRelationshipRightClick', rel, hitTargets, evt)
      setSelectedElement(rel)
    },
    onNodeClick: (node: Node, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('onNodeClick', node, hitTargets, evt)
      setSelectedElement(node)
    },
    onNodeRightClick: (node: Node, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('onNodeRightClick', node, hitTargets, evt)
      setSelectedElement(node)
    },
    onNodeDoubleClick: (node: Node, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('onNodeDoubleClick', node, hitTargets, evt)
      // You could implement focus/zoom functionality here
    },
    onRelationshipClick: (rel: Relationship, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('onRelationshipClick', rel, hitTargets, evt)
      setSelectedElement(rel)
    },
    onRelationshipDoubleClick: (rel: Relationship, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('onRelationshipDoubleClick', rel, hitTargets, evt)
    },
    onCanvasClick: (evt: MouseEvent) => {
      console.log('onCanvasClick', evt)
      setSelectedElement(null) // Clear selection when clicking on canvas
    },
    onCanvasDoubleClick: (evt: MouseEvent) => {
      console.log('onCanvasDoubleClick', evt)
    },
    onCanvasRightClick: (evt: MouseEvent) => {
      console.log('onCanvasRightClick', evt)
    },
    onDrag: (nodes: Node[]) => {
      console.log('onDrag', nodes)
    },
    onPan: (panning: { x: number; y: number }, event: MouseEvent) => {
      console.log('onPan', panning, event)
    },
    onZoom: (zoomLevel: number) => {
      console.log('onZoom', zoomLevel)
    }
  }

  // Fetch graph data from API
  useEffect(() => {
    const fetchGraphData = async () => {
      try {
        setLoading(true)
        const response = await fetch('/api/graph')
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data: GraphData = await response.json()
        console.log('Fetched graph data:', data)
        setGraphData(data)
        setError(null)
      } catch (err) {
        console.error('Error fetching graph data:', err)
        setError(err instanceof Error ? err.message : 'Unknown error occurred')
      } finally {
        setLoading(false)
      }
    }

    fetchGraphData()
  }, [])

  // Helper function to get node color based on department
  const getNodeColor = (department?: string) => {
    const colorMap: { [key: string]: string } = {
      'Engineering': '#3182ce',
      'Marketing': '#38a169', 
      'Sales': '#e53e3e',
      'HR': '#d69e2e',
      'Finance': '#805ad5',
      'Operations': '#dd6b20'
    }
    return department ? colorMap[department] || '#718096' : '#718096'
  }

  // Helper function to get relationship color based on type
  const getRelationshipColor = (type?: string) => {
    const colorMap: { [key: string]: string } = {
      'REPORTS_TO': '#e53e3e',
      'FRIENDS_WITH': '#38a169',
      'COLLABORATES_WITH': '#3182ce'
    }
    return type ? colorMap[type] || '#718096' : '#718096'
  }

  // Render loading state
  if (loading) {
    return (
      <div className="container">
        <div className="page-header">
          <h1>Interactive Graph Visualization</h1>
          <p>Loading employee relationship data...</p>
        </div>
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Fetching graph data...</p>
        </div>
      </div>
    )
  }

  // Render error state
  if (error) {
    return (
      <div className="container">
        <div className="page-header">
          <h1>Interactive Graph Visualization</h1>
          <p>Explore employee relationships using Neo4j Visualization Library</p>
        </div>
        <div className="error">
          <h2>❌ Error Loading Graph Data</h2>
          <p>{error}</p>
          <p>Make sure the API server is running on port 8000 and the database contains data.</p>
          <button 
            onClick={() => window.location.reload()} 
            className="btn primary"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  // Render empty state
  if (graphData.nodes.length === 0) {
    return (
      <div className="container">
        <div className="page-header">
          <h1>Interactive Graph Visualization</h1>
          <p>Explore employee relationships using Neo4j Visualization Library</p>
        </div>
        <div className="empty-state">
          <h3>📊 No Graph Data Available</h3>
          <p>The database appears to be empty. Try seeding some sample data first.</p>
          <p>You can use the <code>/api/seed</code> endpoint to populate the database with sample data.</p>
        </div>
      </div>
    )
  }

  // Render the graph visualization
  return (
    <div className="container">
      <div className="page-header">
        <h1>Interactive Graph Visualization</h1>
        <p>Explore employee relationships using Neo4j Visualization Library</p>
      </div>

      <div className="graph-container">
        <div className="graph-wrapper">
          {/* NVL React Component */}
          <div 
            style={{
              margin: 10,
              borderRadius: 12,
              border: '2px solid #e2e8f0',
              height: 600,
              background: 'radial-gradient(circle, #FFF 0%, #F8FAFC 100%)',
              boxShadow: '0 4px 16px rgba(0,0,0,0.1)'
            }}
          >
            <InteractiveNvlWrapper
              nodes={graphData.nodes.map(node => ({
                id: node.id,
                caption: node.name || node.id,
                size: 25,
                color: getNodeColor(node.department),
                borderColor: '#333',
                borderWidth: 2,
                properties: {
                  name: node.name,
                  department: node.department,
                  position: node.position,
                  email: node.email
                }
              }))}
              rels={graphData.relationships.map(rel => ({
                id: rel.id,
                from: rel.from,
                to: rel.to,
                caption: rel.type || '',
                color: getRelationshipColor(rel.type),
                width: 2,
                properties: {
                  type: rel.type
                }
              }))}
              mouseEventCallbacks={mouseEventCallbacks}
              onClick={(evt) => console.log('custom click event', evt)}
              nvlOptions={{
                layout: 'd3Force',
                initialZoom: 0.8,
                disableTelemetry: true,
                allowDynamicMinZoom: true,
                maxZoom: 3,
                minZoom: 0.1
              }}
            />
          </div>
          
          {/* Element Details Panel */}
          {selectedElement && (
            <div className="element-details">
              <h3>
                {selectedElement.id.includes('rel') ? '🔗 Relationship Details' : '👤 Node Details'}
              </h3>
              <div className="details-content">
                <p><strong>ID:</strong> {selectedElement.id}</p>
                {selectedElement.caption && (
                  <p><strong>Caption:</strong> {selectedElement.caption}</p>
                )}
                {(selectedElement as any).properties && (
                  <div className="properties">
                    <strong>Properties:</strong>
                    <pre>{JSON.stringify((selectedElement as any).properties, null, 2)}</pre>
                  </div>
                )}
              </div>
              <button 
                onClick={() => setSelectedElement(null)}
                className="btn secondary"
              >
                Close
              </button>
            </div>
          )}
          
          {/* Graph Statistics */}
          <div className="graph-stats">
            <div className="stat-card">
              <h3>📊 Graph Statistics</h3>
              <div className="stats-grid">
                <div className="stat-item">
                  <span className="stat-number">{graphData.nodes.length}</span>
                  <span className="stat-label">Employees</span>
                </div>
                <div className="stat-item">
                  <span className="stat-number">{graphData.relationships.length}</span>
                  <span className="stat-label">Relationships</span>
                </div>
              </div>
            </div>
            
            {/* Legend */}
            <div className="graph-legend">
              <h3>🏷️ Legend</h3>

              <div className="legend-section">
                <h4>Relationship Types</h4>
                <div className="legend-items">
                  <div className="legend-item">
                    <span className="legend-line" style={{background: '#e53e3e'}}></span>
                    <span>Reports To</span>
                  </div>
                  <div className="legend-item">
                    <span className="legend-line" style={{background: '#38a169'}}></span>
                    <span>Friends With</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  )
}

import React, { useState, useEffect } from 'react'
import type { Node, Relationship, HitTargets } from '@neo4j-nvl/base'
import { InteractiveNvlWrapper } from '@neo4j-nvl/react'
import type { MouseEventCallbacks } from '@neo4j-nvl/react'

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

interface GraphVisualizationProps {
  graphData: GraphData
}

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

export default function GraphVisualization({ graphData }: GraphVisualizationProps) {
  const [nodes, setNodes] = useState<Node[]>([])
  const [relationships, setRelationships] = useState<Relationship[]>([])

  // Transform data to NVL format
  useEffect(() => {
    if (graphData.nodes.length > 0) {
      const transformedNodes: Node[] = graphData.nodes.map(node => ({
        id: node.id,
        size: 30,
        color: getNodeColor(node.department),
        borderColor: '#333',
        borderWidth: 2,
        caption: node.name || node.id,
        properties: {
          name: node.name,
          department: node.department,
          position: node.position,
          email: node.email
        }
      }))

      const transformedRelationships: Relationship[] = graphData.relationships.map(rel => ({
        id: rel.id,
        from: rel.from,
        to: rel.to,
        caption: rel.type || '',
        color: getRelationshipColor(rel.type),
        width: 3,
        properties: {
          type: rel.type
        }
      }))

      setNodes(transformedNodes)
      setRelationships(transformedRelationships)

      console.log('Graph data transformed:', {
        nodes: transformedNodes.length,
        relationships: transformedRelationships.length
      })
    }
  }, [graphData])

  // Mouse event callbacks for interactivity
  const mouseEventCallbacks: MouseEventCallbacks = {
    onHover: (element: Node | Relationship, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('Hover:', element.id)
    },
    
    onNodeClick: (node: Node, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('Node clicked:', node.caption || node.id)
      // You could show a modal with node details here
    },
    
    onNodeRightClick: (node: Node, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('Node right-clicked:', node.caption || node.id)
      evt.preventDefault()
    },
    
    onNodeDoubleClick: (node: Node, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('Node double-clicked:', node.caption || node.id)
      // You could focus on the node and its neighbors here
    },
    
    onRelationshipClick: (rel: Relationship, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('Relationship clicked:', rel.caption || rel.id)
    },
    
    onRelationshipRightClick: (rel: Relationship, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('Relationship right-clicked:', rel.caption || rel.id)
      evt.preventDefault()
    },
    
    onRelationshipDoubleClick: (rel: Relationship, hitTargets: HitTargets, evt: MouseEvent) => {
      console.log('Relationship double-clicked:', rel.caption || rel.id)
    },
    
    onCanvasClick: (evt: MouseEvent) => {
      console.log('Canvas clicked')
    },
    
    onCanvasDoubleClick: (evt: MouseEvent) => {
      console.log('Canvas double-clicked')
    },
    
    onCanvasRightClick: (evt: MouseEvent) => {
      console.log('Canvas right-clicked')
      evt.preventDefault()
    },
    
    onDrag: (nodes: Node[]) => {
      console.log('Nodes dragged:', nodes.length)
    },
    
    onPan: (panning: { x: number; y: number }, event: MouseEvent) => {
      // Pan events can be very frequent, so we'll skip logging
    },
    
    onZoom: (zoomLevel: number) => {
      console.log('Zoom level:', zoomLevel)
    }
  }

  if (nodes.length === 0) {
    return (
      <div style={{
        height: '600px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: '1px solid #e2e8f0',
        borderRadius: '8px',
        background: '#ffffff',
        color: '#666'
      }}>
        <p>No graph data to display</p>
      </div>
    )
  }

  return (
    <div
      style={{
        height: '600px',
        border: '1px solid #e2e8f0',
        borderRadius: '8px',
        background: '#ffffff',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}
    >
      <InteractiveNvlWrapper
        nodes={nodes}
        rels={relationships}
        mouseEventCallbacks={mouseEventCallbacks}
        onClick={(evt) => console.log('Custom click event:', evt)}
      />
    </div>
  )
}

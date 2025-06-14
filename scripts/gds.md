#  Communities

## Separate Community Analysis by Relationship Type

## 1. Formal Communities (REPORTS_TO only)
Create projected graph for formal organizational structure
```cypher
CALL gds.graph.project(
  'formal-network',
  'Employee', 
  'REPORTS_TO'
)
```

Run Louvain on formal relationships
```cypher
CALL gds.louvain.stream('formal-network')
YIELD nodeId, communityId
WITH communityId, collect(gds.util.asNode(nodeId).name) as employees
RETURN communityId as FormalCommunity,
       size(employees) as MemberCount,
       employees as Members
ORDER BY MemberCount DESC, FormalCommunity
```

## 2. Informal Communities (FRIENDS_WITH only)  
Create projected graph for informal social relationships
```cypher
CALL gds.graph.project(
  'informal-network',
  'Employee', 
  'FRIENDS_WITH'
)
```

Run Louvain on friendship relationships
```cypher
CALL gds.louvain.stream('informal-network')
YIELD nodeId, communityId
WITH communityId, collect(gds.util.asNode(nodeId).name) as employees
RETURN communityId as InformalCommunity,
       size(employees) as MemberCount,
       employees as Members
ORDER BY MemberCount DESC, InformalCommunity
```

## 3. Community Comparison and Overlap Analysis

Write community assignments to node properties for comparison

https://neo4j.com/docs/graph-data-science/current/algorithms/louvain/

```cypher
// Write formal communities
CALL gds.louvain.write('formal-network', {
  writeProperty: 'formalCommunity'
})

// Write informal communities  
CALL gds.louvain.write('informal-network', {
  writeProperty: 'informalCommunity'
})
```

Compare formal vs informal community assignments
```cypher
MATCH (e:Employee)
WHERE e.formalCommunity IS NOT NULL AND e.informalCommunity IS NOT NULL
WITH e.formalCommunity as formal, e.informalCommunity as informal, 
     collect(e.name) as employees
RETURN formal as FormalCommunity,
       informal as InformalCommunity, 
       size(employees) as OverlapSize,
       employees as OverlappingMembers
ORDER BY OverlapSize DESC
```

## 4. Employees Bridging Communities
Find employees who span different community types
```cypher
MATCH (e:Employee)
WHERE e.formalCommunity IS NOT NULL AND e.informalCommunity IS NOT NULL
WITH e.formalCommunity as formal, e.informalCommunity as informal, 
     collect(e.name) as employees
WHERE size(employees) = 1  // Employees who are unique in their formal/informal combination
RETURN formal as FormalCommunity,
       informal as InformalCommunity,
       employees[0] as BridgingEmployee
ORDER BY formal, informal
```
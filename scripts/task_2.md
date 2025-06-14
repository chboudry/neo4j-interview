# Return all nodes and relationship 
Careful, might want to use LIMIT 25

```cypher
MATCH p=()-[]->() RETURN p
```


# Show a hierarchy of all people working under “Darth Vader”

Warning : there is a diprecancy between the browser and neo4j desktop

Neo4j desktop does not display relationship unless you explicitely ask for them while the browser will display all relationship between displayed nodes

## Option 1 : display as graph directs employee
```cypher
MATCH path = (subordinate:Employee)-[:REPORTS_TO]->(vader:Employee {name: "Darth Vader"})
RETURN path
```

## Option 2 : displays direct and indirect employee with depth level

In Browser, make sure to deactivate "Connect result nodes" to skip other type of relationships
This is default in Neo4j desktop

```cypher
MATCH path = ()-[:REPORTS_TO*]->(:Employee {name: "Darth Vader"})
RETURN path
```

## Option 3 : displays direct and indirect employee with depth level, but in tables
```cypher
MATCH path = (subordinate:Employee)-[:REPORTS_TO*]->(vader:Employee {name: "Darth Vader"})
RETURN vader.name as Manager, 
       subordinate.name as Subordinate,
       length(path) as Level,
       [node in nodes(path) | node.name] as HierarchyPath
ORDER BY Level, subordinate.name
```

## Option 4 : Hierarchical layout in Explore in Desktop (but you need to save the query first as part of the perspective designer )

A bit impractical

https://neo4j.com/docs/apoc/current/overview/apoc.path/apoc.path.subgraphAll/
```cypher
MATCH (vader:Employee {name: "Darth Vader"})
CALL apoc.path.subgraphAll(vader, {
    relationshipFilter: "<REPORTS_TO",
    labelFilter: "Employee"
}) YIELD nodes, relationships
RETURN nodes, relationships
```

We can then apply color per level using rule based styling on Employees color node

For more personalization, bloom is advised

# Show all the people that work in the team of Jacob, but are not friends with Jacob.

## Find Jacob's team members who are not his friends



### Review the connections

For this one we might actually want to reenable "Connect result nodes to makes this more easy

This will allow us to see who are the friends reporting to jacob (on top of the reports to relationship)

```cypher
MATCH (jacob:Employee {name: "Jacob"})<-[r:REPORTS_TO*]-(teammate:Employee)
RETURN jacob, r, teammate
```

### Iteration 1
We make sure the friends have been removed.
```cypher
MATCH (jacob:Employee {name: "Jacob"})<-[r:REPORTS_TO*]-(teammate:Employee)
WHERE NOT (jacob)-[:FRIENDS_WITH]-(teammate)
RETURN jacob, r, teammate
```
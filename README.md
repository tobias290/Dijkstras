# Dijkstra's Algorithm

Dijkstra's algorithm implemented in Python 3.6.

Example use:

```
# Create the tree 
weighted_graph = Graph([
        Node("A", [
            WeightedEdge("A", "B", 3),
            WeightedEdge("A", "C", 8),
        ]),
        Node("B", [
            WeightedEdge("B", "D", 2),
        ]),
        Node("C", [
            WeightedEdge("C", "E", 3),
        ]),
        Node("D", [
            WeightedEdge("D", "E", 10),
        ]),
        Node("E", [
            WeightedEdge("E", "F", 3),
            WeightedEdge("E", "Z", 7),
        ]),
        Node("F", [
            WeightedEdge("F", "Z", 2),
        ]),
        Node("Z", []),
    ])

# Instantiate the class
dijkstra = Dijkstra(weighted_graph)

# Solve it
dijkstra.solve("A", "Z")

# Display output
print("Path:", dijkstra.shortest_path)
print("Distance:", dijkstra.final_weight)
```

Output:

```
Path: ['A', 'C', 'E', 'F', 'Z']
Distance: 16
```
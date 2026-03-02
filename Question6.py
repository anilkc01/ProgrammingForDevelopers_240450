import heapq
import math

def safest_path_dijkstra(graph, start_node):
    # Initialize distances as infinity
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    pq = [(0, start_node)]
    parent = {node: None for node in graph}

    while pq:
        curr_dist, u = heapq.heappop(pq)
        
        if curr_dist > distances[u]:
            continue
            
        for v, probability in graph[u].items():
            # Apply transformation: w = -log(p)
            weight = -math.log(probability)
            
            # RELAX Step
            if distances[v] > distances[u] + weight:
                distances[v] = distances[u] + weight
                parent[v] = u
                heapq.heappush(pq, (distances[v], v))
                
    return parent, distances


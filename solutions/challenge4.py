from numpy import array
from scipy.sparse.csgraph import NegativeCycleError#, bellman_ford,

def solution(times, times_limit):
    try:
        shortest_paths = bellman_ford(
            csgraph=array(times).T,
            indices=len(times) - 1
        )
    except NegativeCycleError:
        return all_bunnies_saved(
            locations=len(times)
        )
    shortest_path_too_long = shortest_paths[0] > times_limit
    if shortest_path_too_long:
        return []
    return save_bunnies(
        graph=times, 
        limit=times_limit, 
        paths=shortest_paths
    )
    
def save_bunnies(graph, limit, paths):
    bunnies = []
    start = (0,bunnies)
    return bfs(
        graph=graph,
        limit=limit,
        paths=paths,
        bunnies=bunnies,
        visited={str(start): 0},
        queue=[start]
    )

def bfs(graph, limit, paths, bunnies, visited, queue):
    if not any(queue):
        return [bunny - 1 for bunny in bunnies]
    
    current = queue.pop(0)
    current_node,current_bunnies = current
        
    for next_node in range(len(graph[current_node])):
        if next_node == current_node:
            continue

        path_cost = visited[str(current)] + graph[current_node][next_node]
        next_bunnies = update_bunnies(
            bunnies=current_bunnies, 
            next_id=next_node, 
            total=len(graph)
        )
        next = (next_node, next_bunnies)
        previous_cost = visited.get(str(next), float('inf'))
        more_expensive = previous_cost <= path_cost
        if more_expensive:
            continue 
        
        exceeds_limit = (paths[next_node] + path_cost) > limit
        if exceeds_limit:
            continue

        queue.append(next)
        visited[str(next)] = path_cost
        bunnies = save_most_bunnies(
            max_bunnies=bunnies, 
            bunnies=next_bunnies
        )
        
        if len(bunnies) == len(graph) - 2:
            return all_bunnies_saved(
                locations=len(graph)
            )
    
    return bfs(
        graph=graph,
        limit=limit,
        paths=paths,
        bunnies=bunnies,
        visited=visited,
        queue=queue
    )

def index(bunnies, bunny):
    i = -1
    try:
        i = bunnies.index(bunny)
    except:
        i = -1 
    return i

def update_bunnies(bunnies, next_id, total):
    bunny_on_bounds = next_id in (0,total-1)
    if bunny_on_bounds: 
        return bunnies 

    bunny_already_in_bunnies = index(bunnies=bunnies, bunny=next_id) != -1
    if bunny_already_in_bunnies:
        return bunnies
    
    return insert_bunny_by_size(
        bunnies=bunnies,
        new_bunny=next_id
    )
    
def insert_bunny_by_size(bunnies, new_bunny):
    i = new_bunny_position_by_size(
        bunnies=bunnies, 
        new_bunny=new_bunny
    )
    return bunnies[:i] + [new_bunny] + bunnies[i:]

def new_bunny_position_by_size(bunnies, new_bunny):
    new_bunny_position = 0
    for bunny in bunnies:
        if bunny < new_bunny:
            new_bunny_position += 1
            continue
        break 
    return new_bunny_position
    
def save_most_bunnies(max_bunnies, bunnies):
    return bunnies if len(bunnies) > len(max_bunnies) else max_bunnies

def all_bunnies_saved(locations):
    return list(range(locations-2))

def bellman_ford(csgraph, indices):
    def edge_relaxation(graph, paths, source, destination):
        if source==destination:
            return 
        
        path = graph[source][destination] + paths[source] if paths[source] < float('inf') else float('inf')
        paths[destination] = min(paths[destination],path)
        
    def is_negative_cycle(graph, paths, source, destination):
        if source==destination:
            return False 
        
        if paths[source]==float('inf'):
            return False 
            
        return (graph[source][destination] + paths[source]) < paths[destination]
    
    paths = [
        float('inf') for _ in range(len(csgraph))
    ]
    paths[indices] = 0
    
    for _ in range(len(csgraph)-1):
        for src in range(len(csgraph)):
            for dst in range(len(csgraph[src])):
                edge_relaxation(
                    graph=csgraph, 
                    paths=paths, 
                    source=src, 
                    destination=dst
                )
    
    for src in range(len(csgraph)):
        for dst in range(len(csgraph[src])):
            if is_negative_cycle(
                graph=csgraph, 
                paths=paths, 
                source=src, 
                destination=dst
            ):
                raise NegativeCycleError 
    
    return paths
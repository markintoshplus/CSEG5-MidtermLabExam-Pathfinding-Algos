from queue import PriorityQueue
from dataclasses import dataclass
from typing import List, Tuple, Set, Optional
import timeit


@dataclass
class PathNode:
    position: Tuple[int, int]
    distance_from_start: int = 0
    estimated_distance_to_goal: int = 0
    previous: Optional["PathNode"] = None

    @property
    def total_distance(self) -> int:
        return self.distance_from_start + self.estimated_distance_to_goal

    def __lt__(self, other):
        return self.total_distance < other.total_distance


def calculate_manhattan_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def find_walkable_neighbors(position: Tuple[int, int], maze: List[List[int]]) -> List[Tuple[int, int]]:
    maze_height, maze_width = len(maze), len(maze[0])
    neighbors = []
    possible_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

    for move_x, move_y in possible_moves:
        next_x, next_y = position[0] + move_x, position[1] + move_y
        is_within_bounds = 0 <= next_x < maze_height and 0 <= next_y < maze_width
        is_walkable = is_within_bounds and maze[next_x][next_y] == 0
        
        if is_walkable:
            neighbors.append((next_x, next_y))
    return neighbors


def build_path(end_node: PathNode) -> List[Tuple[int, int]]:
    path = []
    current = end_node
    while current:
        path.append(current.position)
        current = current.previous
    return path[::-1]


def greedy_best_first_search(
    grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]
) -> Optional[List[Tuple[int, int]]]:
    start_node = PathNode(start)
    start_node.estimated_distance_to_goal = calculate_manhattan_distance(start, goal)

    open_set = PriorityQueue()
    open_set.put((start_node.estimated_distance_to_goal, start_node))
    visited = {start}

    while not open_set.empty():
        _, current = open_set.get()

        if current.position == goal:
            return build_path(current)

        for neighbor_pos in find_walkable_neighbors(current.position, grid):
            if neighbor_pos not in visited:
                neighbor = PathNode(
                    position=neighbor_pos,
                    previous=current
                )
                neighbor.estimated_distance_to_goal = calculate_manhattan_distance(neighbor_pos, goal)
                open_set.put((neighbor.estimated_distance_to_goal, neighbor))
                visited.add(neighbor_pos)

    return None


def a_star_search(
    grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]
) -> Optional[List[Tuple[int, int]]]:
    start_node = PathNode(start)
    start_node.estimated_distance_to_goal = calculate_manhattan_distance(start, goal)

    open_set = PriorityQueue()
    open_set.put((start_node.total_distance, start_node))
    visited = {start}

    while not open_set.empty():
        _, current = open_set.get()

        if current.position == goal:
            return build_path(current)

        for neighbor_pos in find_walkable_neighbors(current.position, grid):
            if neighbor_pos not in visited:
                neighbor = PathNode(
                    position=neighbor_pos,
                    previous=current
                )
                neighbor.distance_from_start = current.distance_from_start + 1
                neighbor.estimated_distance_to_goal = calculate_manhattan_distance(neighbor_pos, goal)
                open_set.put((neighbor.total_distance, neighbor))
                visited.add(neighbor_pos)

    return None


def measure_execution_time(func, *args):
    start_time = timeit.default_timer()
    result = func(*args)
    execution_time = timeit.default_timer() - start_time
    return result, execution_time


# Test the implementation
if __name__ == "__main__":
    grid = [
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    start = (0, 0)
    goal = (4, 4)

    # Test Greedy Best-First Search
    path_greedy, time_greedy = measure_execution_time(greedy_best_first_search, grid, start, goal)

    # Test A* Search
    path_a_star, time_a_star = measure_execution_time(a_star_search, grid, start, goal)

    # Print results
    print("Greedy Best-First Search:")
    print(f"Path found: {path_greedy}")
    print(f"Time taken: {time_greedy:.10f} seconds")

    print("\nA* Search:")
    print(f"Path found: {path_a_star}")
    print(f"Time taken: {time_a_star:.10f} seconds")

    print("\nPath Quality Comparison:")
    print(f"Length of path found by Greedy: {len(path_greedy) if path_greedy else 'No path found'}")
    print(f"Length of path found by A*: {len(path_a_star) if path_a_star else 'No path found'}")

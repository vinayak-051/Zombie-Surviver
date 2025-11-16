import random
from typing import List, Tuple, Set,Deque
from collections import deque

Coord = Tuple[int, int]

class Grid:
    def __init__(self, width: int, height: int, obstacles: Set[Coord] = None, safe_zones: Set[Coord] = None):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles) if obstacles else set()
        self.safe_zones = set(safe_zones) if safe_zones else set()

    def in_bounds(self, pos: Coord) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, pos: Coord) -> bool:
        return pos not in self.obstacles

    def neighbors(self, pos: Coord) -> List[Coord]:
        x, y = pos
        results = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        results = filter(self.in_bounds, results)
        return [p for p in results if self.passable(p)]

    def random_empty(self) -> Coord:
        while True:
            p = (random.randrange(self.width), random.randrange(self.height))
            if self.passable(p) and p not in self.safe_zones:
                return p

    def is_safe(self, pos: Coord) -> bool:
        return pos in self.safe_zones

    def add_obstacle(self, pos: Coord):
        if self.in_bounds(pos):
            self.obstacles.add(pos)

    def add_safe_zone(self, pos: Coord):
        if self.in_bounds(pos):
            self.safe_zones.add(pos)
            
    def generate_random_obstacles(self, count: int, exclude_coords: Set[Coord]):
        """Generates a specified number of obstacles, excluding key locations."""
        generated_count = 0
        while generated_count < count:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            pos = (x, y)
            
            # Only add the obstacle if it's not a key location (safe zone, human start)
            if pos not in self.obstacles and pos not in self.safe_zones and pos not in exclude_coords:
                self.obstacles.add(pos)
                generated_count += 1

    def check_connectivity(self, start: Coord, goals: Set[Coord]) -> bool:
        """Checks if a path exists from start to any goal position using BFS."""
        if start in goals:
            return True
        
        queue: Deque[Coord] = deque([start])
        visited: Set[Coord] = {start}
        
        while queue:
            current = queue.popleft()
            
            for neighbor in self.neighbors(current):
                if neighbor in goals:
                    return True
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False
    
def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
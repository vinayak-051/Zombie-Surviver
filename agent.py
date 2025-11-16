import random
from environment import Grid, Coord, manhattan
from typing import List, Dict, Optional, Tuple, Set 
import heapq


class Human:
    def __init__(self, pos: Coord, grid: Grid):
        self.pos = pos
        self.grid = grid
        self.path: List[Coord] = [] # Stores the full calculated path for visualization

    def _a_star_path(self, goal: Coord, zombies: List["Zombie"]) -> Optional[List[Coord]]:
        """A* pathfinding from self.pos to goal, returning the full path, prioritizing paths away from zombies."""
        if not self.grid.safe_zones:
            return None
        
        # Ensure goal is the nearest safe zone
        nearest_safe = min(self.grid.safe_zones, key=lambda s: manhattan(s, self.pos))
        goal = nearest_safe
        
        if self.pos == goal:
            return []

        g_cost: Dict[Coord, int] = {self.pos: 0} # Actual distance cost (unpenalized)
        came_from: Dict[Coord, Optional[Coord]] = {self.pos: None}
        priority_queue: List[Tuple[int, Coord]] = [(manhattan(self.pos, goal), self.pos)]

        while priority_queue:
            _, current = heapq.heappop(priority_queue)

            if current == goal:
                path: List[Coord] = []
                while came_from[current] is not None:
                    path.append(current)
                    current = came_from[current]
                # Return the path in order from next step to goal (excluding current position)
                return path[::-1] 

            for neighbor in self.grid.neighbors(current):
                if not self.grid.passable(neighbor):
                    continue

                # 1. ACTUAL PATH COST (G-Cost): Cost from start (current g + 1)
                new_g = g_cost[current] + 1
                
                # 2. DANGER PENALTY (used for F-Cost priority only)
                # Adds a heavy penalty for neighboring a zombie (Manhattan distance <= 1)
                danger_penalty_magnitude = sum(1 for z in zombies if manhattan(neighbor, z.pos) <= 1)
                
                # 3. TOTAL PRIORITY COST (F-Cost) = G-Cost + Heuristic + Penalty
                f_score_priority = new_g + manhattan(neighbor, goal) + danger_penalty_magnitude * 1000

                # Check if this path is better (A* optimization)
                # IMPORTANT: Use UNPENALIZED new_g for comparison against g_cost
                if neighbor not in g_cost or new_g < g_cost[neighbor]:
                    # Update g_cost using the UNPENALIZED cost
                    g_cost[neighbor] = new_g
                    came_from[neighbor] = current
                    # Push to queue using the PENALIZED F-Cost for prioritization
                    heapq.heappush(priority_queue, (f_score_priority, neighbor))

        return None # No path found

    def move(self, direction: str, zombies: List["Zombie"] = []):
        x, y = self.pos
        
        if direction == "up":
            new_pos = (x, y - 1)
            self.path = [] # Clear path on manual move
        elif direction == "down":
            new_pos = (x, y + 1)
            self.path = [] # Clear path on manual move
        elif direction == "left":
            new_pos = (x - 1, y)
            self.path = [] # Clear path on manual move
        elif direction == "right":
            new_pos = (x + 1, y)
            self.path = [] # Clear path on manual move
        elif direction == "auto":
            # 1. Determine goal (nearest safe zone)
            nearest_safe = min(self.grid.safe_zones, key=lambda s: manhattan(s, self.pos)) if self.grid.safe_zones else self.pos
            
            # CRITICAL FIX: RECALCULATE PATH EVERY TURN. 
            # This ensures the human reacts to the latest zombie positions.
            self.path = self._a_star_path(nearest_safe, zombies)
            
            # 2. Execute move along the path
            if self.path:
                next_pos = self.path.pop(0) # Get the next step and remove it
                if self.grid.passable(next_pos):
                    self.pos = next_pos
                return
            
            # If no path is found or the goal is reached, stay put
            return
        else:
            new_pos = self.pos
            self.path = [] 

        if self.grid.in_bounds(new_pos) and self.grid.passable(new_pos):
            self.pos = new_pos


class Zombie:
    def __init__(self, pos: Coord, grid: Grid):
        self.pos = pos
        self.grid = grid

    # MODIFIED: Accepts occupied_cells to prevent collision
    def a_star_search(self, start: Coord, goal: Coord, occupied_cells: Set[Coord]) -> Optional[Coord]:
        """A* pathfinding towards the goal (human), avoiding occupied cells."""
        g_cost: Dict[Coord, int] = {start: 0}
        came_from: Dict[Coord, Optional[Coord]] = {start: None}
        priority_queue: List[Tuple[int, Coord]] = [(manhattan(start, goal), start)]
        

        while priority_queue:
            _, current = heapq.heappop(priority_queue)
            if current == goal:
                path: List[Coord] = []
                while came_from[current] is not None:
                    path.append(current)
                    current = came_from[current]
                return path[-1] if path else None

            for neighbor in self.grid.neighbors(current):
                if not self.grid.passable(neighbor):
                    continue
                
                # NEW CHECK: Prevent movement to a cell already claimed by a higher-priority zombie
                if neighbor in occupied_cells and neighbor != goal: 
                    continue

                new_g = g_cost[current] + 1
                if neighbor not in g_cost or new_g < g_cost[neighbor]:
                    g_cost[neighbor] = new_g
                    f_cost = new_g + manhattan(neighbor, goal)
                    came_from[neighbor] = current
                    heapq.heappush(priority_queue, (f_cost, neighbor))

        valid_moves = [n for n in self.grid.neighbors(start) if self.grid.passable(n)]
        # Filter random moves to avoid occupied cells
        valid_moves = [n for n in valid_moves if n not in occupied_cells] 
        return random.choice(valid_moves) if valid_moves else start

    # MODIFIED: Accepts occupied_cells set
    def chase(self, humans: List[Human], occupied_cells: Set[Coord]) -> Coord:
        """Chase nearest human, avoiding cells in occupied_cells."""
        if not humans:
            return self.pos
        nearest = min(humans, key=lambda h: manhattan(h.pos, self.pos))
        # Pass occupied_cells to A* search
        next_step = self.a_star_search(self.pos, nearest.pos, occupied_cells)
        return next_step if next_step else self.pos

    def move_to(self, pos: Coord):
        self.pos = pos
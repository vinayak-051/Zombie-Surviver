import random
from environment import Grid, manhattan, Coord
from agent import Human, Zombie
from game import Game
from visualization import Visualizer
from typing import Set, List, Tuple
import pygame
import time

# --- Configuration (Constants) ---
GRID_SIZE = 15
NUM_OBSTACLES = 30
NUM_ZOMBIES = 3

# Global Visualizer instance (or None if not initialized)
viz: Visualizer = None


def choose_max_distance_positions(grid_size: int) -> Tuple[Set[Coord], Coord]:
    """Chooses a Safe Zone and a Human Start position that are maximally distant."""
    all_possible_coords = [(x, y) for x in range(grid_size) for y in range(grid_size)]
    
    # 1. Pick a random point P1
    p1 = random.choice(all_possible_coords)

    # 2. Find the point P2 that is maximally distant from P1 (max distance is usually diagonal)
    p2 = max(
        all_possible_coords, 
        key=lambda pos: manhattan(pos, p1)
    )
    
    # Randomly assign p1 and p2 to Safe Zone and Human Start
    if random.choice([True, False]):
        SAFE_ZONE_POS: Set[Coord] = {p1}
        HUMAN_START_POS: Coord = p2
    else:
        SAFE_ZONE_POS: Set[Coord] = {p2}
        HUMAN_START_POS: Coord = p1
        
    return SAFE_ZONE_POS, HUMAN_START_POS


def setup_new_game() -> Game:
    """Sets up a new Grid, Humans, and Zombies, ensuring map connectivity."""
    
    # --- Randomize Safe Zone and Human Start ---
    SAFE_ZONE_POS, HUMAN_START_POS = choose_max_distance_positions(GRID_SIZE)
    EXCLUDED_POSITIONS = SAFE_ZONE_POS.union({HUMAN_START_POS})
    
    # Initialize the grid
    grid = Grid(GRID_SIZE, GRID_SIZE)

    # Add the randomized safe zone
    for pos in SAFE_ZONE_POS:
        grid.add_safe_zone(pos)

    # Loop to ensure map is solvable
    is_connected = False
    attempts = 0
    while not is_connected:
        attempts += 1
        # 1. Generate random obstacles (need to reset obstacles for each retry)
        grid.obstacles = set() 
        grid.generate_random_obstacles(NUM_OBSTACLES, EXCLUDED_POSITIONS)
        
        # 2. Check for connectivity from Human start to Safe Zones
        is_connected = grid.check_connectivity(HUMAN_START_POS, grid.safe_zones)
        
        if not is_connected:
            pass
        else:
            print(f"Map successfully generated and connected after {attempts} attempts.")
            break
        
        if attempts > 1000:
            raise RuntimeError("Failed to generate a connected map after 1000 attempts. Check configuration.")

    # --- Spawn agents ---
    humans = [Human(HUMAN_START_POS, grid)]
    zombies: List[Zombie] = []
    
    for _ in range(NUM_ZOMBIES):
        while True:
            # Zombie spawn is still in the general Top-Left area (0 to GRID_SIZE//2 + 1) to ensure a chase distance
            z_x = random.randrange(0, GRID_SIZE // 2 + 1)
            z_y = random.randrange(0, GRID_SIZE // 2 + 1)
            z_pos: Coord = (z_x, z_y)
            
            # Check for initial distance 
            if (grid.passable(z_pos) and 
                z_pos not in EXCLUDED_POSITIONS and 
                z_pos not in {z.pos for z in zombies} and
                manhattan(z_pos, HUMAN_START_POS) > (GRID_SIZE * 0.75)): # Ensure distance is still large
                zombies.append(Zombie(z_pos, grid))
                break

    print(f"Game Initialized: Grid {GRID_SIZE}x{GRID_SIZE}, {len(grid.obstacles)} Obstacles, {len(zombies)} Zombies.")
    print(f"Safe Zone: {SAFE_ZONE_POS}, Human Start: {HUMAN_START_POS}")
    
    return Game(grid, humans, zombies)

# --- Initialize game and visualization ---
game = setup_new_game()
viz = Visualizer(game.grid)


# --- Main loop ---
running = True
while running:
    
    # 1. Game in progress (Non-Game Over)
    if not game.game_over:
        new_game_requested = viz.draw(game) 
        
        if game.game_over:
            print("Game Over. Awaiting user input...")
            viz.draw(game) 
            
    # 2. Game is over (Awaiting New Game button press)
    else:
        new_game_requested = viz.draw(game) 
        
        if new_game_requested:
            print("Starting a new game...")
            # Setup a completely new game with new random positions/map
            new_game = setup_new_game()
            viz.grid = new_game.grid
            game = new_game
            
    
    # Check for quit events that might have been set by the visualizer
    if not pygame.get_init():
        running = False
        
print("Game loop finished.")
if pygame.get_init():
    pygame.quit()
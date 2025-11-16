from typing import List
from agent import Human, Zombie
from environment import Grid, Coord
from typing import Set, Dict


class Game:
    def __init__(self, grid: Grid, humans: List[Human], zombies: List[Zombie]):
        self.grid = grid
        self.humans = humans
        self.zombies = zombies
        self.turn = 0
        self.game_over = False

    def human_turn(self, direction: str):
        """Move all humans in the specified direction and check victory."""
        if self.game_over or not self.humans:
            return

        for h in self.humans:
            # Pass zombies list for Human's 'auto' logic to avoid them
            h.move(direction, self.zombies) 

        self.check_victory()

    # MODIFIED: Coordinated zombie movement
    def zombie_turn(self):
        """Move all zombies toward humans and handle catches, preventing collisions."""
        if self.game_over:
            return

        # Track positions that a zombie has already claimed as its destination this turn.
        claimed_positions: Set[Coord] = set()
        pending_moves: Dict[Zombie, Coord] = {}

        # 1. Calculate all moves in order, respecting claimed spots
        for z in self.zombies:
            # The zombie treats all claimed_positions as temporary obstacles
            next_pos = z.chase(self.humans, claimed_positions) 
            
            pending_moves[z] = next_pos
            claimed_positions.add(next_pos) # Claim the position for this zombie

        # 2. Execute all calculated moves
        for z, new_pos in pending_moves.items():
            z.move_to(new_pos)

        # 3. Check for caught humans
        new_zombies = []
        for z in self.zombies:
            for h in list(self.humans):
                if z.pos == h.pos:
                    print(f"Human at {h.pos} caught!")
                    self.humans.remove(h)
                    # The caught human becomes a new zombie
                    new_zombies.append(Zombie(h.pos, self.grid))

        self.zombies.extend(new_zombies)
        self.check_victory()

    def check_victory(self):
        """Check if humans reached safe zones or all were caught."""
        if self.humans and all(self.grid.is_safe(h.pos) for h in self.humans):
            self.game_over = True
            print("All humans reached safety! Humans win!")
        elif not self.humans:
            self.game_over = True
            print("All humans were caught! Zombies win!")

    def step(self, human_direction: str):
        """Perform one game step: human moves, then zombies move."""
        if self.game_over:
            return

        self.human_turn(human_direction)
        if not self.game_over:
            self.zombie_turn()

        self.turn += 1
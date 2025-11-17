import pygame
import time
from environment import Grid, Coord
from typing import Tuple, List

CELL = 32

# Updated color scheme for a cleaner look
UI_COLORS = {
    'BACKGROUND': (15, 15, 20),
    'GRID_LINE': (30, 30, 40),
    'INFO_BAR': (25, 25, 35),
    'TEXT': (200, 200, 220),
    # NEW COLORS for the game over screen
    'HUMAN_WIN': (40, 200, 40), # Green for Human Win
    'ZOMBIE_WIN': (200, 40, 40), # Red for Zombie Win
    'BUTTON_NORMAL': (80, 80, 90),
    'BUTTON_HOVER': (120, 120, 130),
    'BUTTON_TEXT': (255, 255, 255)
}

# Image file paths (User needs to provide these files)
IMAGE_FILES = {
    'obstacle': 'assets/brick.png',
    'safe_zone': 'assets/home.jpeg',
    'human': 'assets/human.png',
    'zombie': 'assets/zombie.jpeg'
}


class Visualizer:
    def __init__(self, grid: Grid):
        pygame.init()
        self.grid = grid
        self.screen = pygame.display.set_mode((grid.width * CELL, grid.height * CELL + 40))
        pygame.display.set_caption("🧟 Zombie Surviver")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20, bold=True)
        self.big_font = pygame.font.SysFont("consolas", 40, bold=True)
        self.images = self.load_images()
        
        # Button properties for New Game
        self.new_game_button_rect = pygame.Rect(0, 0, 0, 0)

    def load_images(self):
        loaded_images = {}
        for key, filename in IMAGE_FILES.items():
            try:
                img = pygame.image.load(filename).convert_alpha() 
                loaded_images[key] = pygame.transform.scale(img, (CELL, CELL))
            except pygame.error as e:
                print(f"Warning: Could not load image '{filename}'. Using fallback color. Error: {e}")
                
                fallback_color = (0, 0, 0)
                if key == 'obstacle': fallback_color = (100, 100, 100)
                elif key == 'safe_zone': fallback_color = (40, 160, 40)
                elif key == 'human': fallback_color = (80, 200, 255)
                elif key == 'zombie': fallback_color = (200, 60, 60)
                
                surface = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
                
                if key in ['obstacle', 'safe_zone']:
                     surface.fill(fallback_color)
                else:
                    pygame.draw.circle(surface, fallback_color, (CELL//2, CELL//2), CELL//2 - 2)
                
                loaded_images[key] = surface

        return loaded_images

    # NEW METHOD
    def get_center_coords(self, pos: Coord) -> Tuple[int, int]:
        """Converts grid (x, y) to screen center pixel coordinates."""
        x, y = pos
        center_x = x * CELL + CELL // 2
        center_y = y * CELL + CELL // 2
        return (center_x, center_y)

    # NEW METHOD
    def draw_path(self, screen, game):
        """Draws the human's calculated path as a black line."""
        
        if not game.humans:
            return

        human = game.humans[0]
        
        # The path includes the current position and the calculated future steps
        path_coords = [human.pos] + human.path
        
        if len(path_coords) < 2:
            return

        # Convert grid coords to pixel coords
        pixel_points = [self.get_center_coords(coord) for coord in path_coords]
        
        # Draw the main black line
        pygame.draw.lines(
            screen, 
            (0, 255, 0), # Black color
            False,     # Do not close the line (open polyline)
            pixel_points,
            4          # Line thickness
        )
            

    def draw_game_over_screen(self, game) -> bool:
        """Draws the game over screen, button, and handles click events.
           Returns True if the 'New Game' button was clicked."""
        
        mouse_pos = pygame.mouse.get_pos()
        clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_over = True
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.new_game_button_rect.collidepoint(mouse_pos):
                    clicked = True

        # --- Game Over Message (Color-coded) ---
        win_color = UI_COLORS['HUMAN_WIN'] if game.humans else UI_COLORS['ZOMBIE_WIN']
        result = " HUMANS WIN!" if game.humans else " ZOMBIES WIN!"
        label = self.big_font.render(result, True, win_color)
        
        text_x = self.grid.width * CELL // 2 - label.get_width() // 2
        text_y = self.grid.height * CELL // 2 - label.get_height() - 20
        self.screen.blit(label, (text_x, text_y))

        # --- New Game Button ---
        button_text = "New Game"
        button_label = self.font.render(button_text, True, UI_COLORS['BUTTON_TEXT'])
        
        btn_width = button_label.get_width() + 40
        btn_height = button_label.get_height() + 20
        btn_x = self.grid.width * CELL // 2 - btn_width // 2
        btn_y = self.grid.height * CELL // 2 + 10

        self.new_game_button_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
        
        # Draw the button and handle cursor
        button_color = UI_COLORS['BUTTON_NORMAL']
        if self.new_game_button_rect.collidepoint(mouse_pos):
            button_color = UI_COLORS['BUTTON_HOVER']
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) # Change cursor to pointer
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.draw.rect(self.screen, button_color, self.new_game_button_rect, border_radius=5)
        
        text_x = btn_x + (btn_width - button_label.get_width()) // 2
        text_y = btn_y + (btn_height - button_label.get_height()) // 2
        self.screen.blit(button_label, (text_x, text_y))

        pygame.display.flip()
        self.clock.tick(10)
        
        return clicked

    def draw(self, game):
        """Handles input, updates game state, and draws the current frame."""
        
        if game.game_over:
            # ... (Game over screen logic) ...
            overlay = pygame.Surface((self.grid.width * CELL, self.grid.height * CELL))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            info_rect = pygame.Rect(0, self.grid.height * CELL, self.grid.width * CELL, 40)
            pygame.draw.rect(self.screen, UI_COLORS['INFO_BAR'], info_rect)
            
            result = " HUMANS WIN!" if game.humans else " ZOMBIES WIN!"
            win_color = UI_COLORS['HUMAN_WIN'] if game.humans else UI_COLORS['ZOMBIE_WIN']
            label = self.font.render(result, True, win_color)
            text_x = self.grid.width*CELL//2 - label.get_width()//2
            self.screen.blit(label, (text_x, self.grid.height * CELL + 10))
            
            return self.draw_game_over_screen(game)
            
        
        # --- Input Handling for live game ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_over = True
                pygame.quit()
                return

        # ... (Movement logic remains the same) ...
        keys = pygame.key.get_pressed()
        moved = False
        
        # Player controlled movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            game.human_turn("up")
            moved = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            game.human_turn("down")
            moved = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game.human_turn("left")
            moved = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game.human_turn("right")
            moved = True
        elif keys[pygame.K_SPACE]:
            # Human AI mode (moves to safe zone avoiding zombies)
            game.human_turn("auto")
            moved = True

        # After human moves, zombies chase
        if moved and not game.game_over:
            time.sleep(0.1) # Slow down the game when a move is made
            game.zombie_turn()
            
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 

        # === DRAWING ===
        self.screen.fill(UI_COLORS['BACKGROUND'])

        # Draw grid cells (map features)
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
                
                # 1. Draw map features (Images/Fallbacks)
                if (x, y) in self.grid.safe_zones:
                    self.screen.blit(self.images['safe_zone'], rect)
                elif (x, y) in self.grid.obstacles:
                    self.screen.blit(self.images['obstacle'], rect)
                
                # 2. Draw grid lines (cleaner)
                pygame.draw.rect(self.screen, UI_COLORS['GRID_LINE'], rect, 1)

        # NEW: Draw the shortest path line AFTER the map but BEFORE agents
        if not game.game_over:
            self.draw_path(self.screen, game)

        # 3. Draw agents (Images/Fallbacks)
        for h in game.humans:
            pos = (h.pos[0] * CELL, h.pos[1] * CELL)
            self.screen.blit(self.images['human'], pos)

        for z in game.zombies:
            pos = (z.pos[0] * CELL, z.pos[1] * CELL)
            self.screen.blit(self.images['zombie'], pos)

        # 4. Bottom info bar
        info_rect = pygame.Rect(0, self.grid.height * CELL, self.grid.width * CELL, 40)
        pygame.draw.rect(self.screen, UI_COLORS['INFO_BAR'], info_rect)

        # Info text
        text = f"Humans: {len(game.humans)} | Zombies: {len(game.zombies)} | Turn: {game.turn}"
        label = self.font.render(text, True, UI_COLORS['TEXT'])
        self.screen.blit(label, (10, self.grid.height * CELL + 10))

        pygame.display.flip()
        self.clock.tick(10)

        return False

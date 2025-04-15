import pygame
import sys
from game.levels import Level
from home.menu import Menu
from constants import WIDTH, HEIGHT, FPS, BLACK

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Initialize game components
    level = Level()
    menu = Menu()

    # Game state: 'menu' or 'game'
    game_state = "menu"

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle state-specific events
            if game_state == "menu":
                menu.handle_event(event)
                if menu.start_game:  # Assuming Menu has a `start_game` flag
                    game_state = "game"
            elif game_state == "game":
                level.handle_event(event)
                if level.back_to_menu:  # Assuming Level has a `back_to_menu` flag
                    game_state = "menu"

        # Update game state
        if game_state == "menu":
            menu.update()
        elif game_state == "game":
            level.update()

        # Draw everything
        screen.fill(BLACK)
        if game_state == "menu":
            menu.draw(screen)
        elif game_state == "game":
            level.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
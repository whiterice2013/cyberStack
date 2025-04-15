class Menu:
    def __init__(self):
        self.options = ["Start Game", "Base Upgrades", "Exit"]
        self.selected_option = 0

    def display_menu(self, screen):
        screen.fill((0, 0, 0))  # Clear the screen with black
        font = pygame.font.Font(None, 74)
        for index, option in enumerate(self.options):
            if index == self.selected_option:
                text = font.render(option, True, (255, 255, 0))  # Highlight selected option
            else:
                text = font.render(option, True, (255, 255, 255))  # Regular option
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + index * 80))

    def navigate(self, direction):
        self.selected_option += direction
        if self.selected_option < 0:
            self.selected_option = len(self.options) - 1
        elif self.selected_option >= len(self.options):
            self.selected_option = 0

    def select_option(self):
        return self.options[self.selected_option]
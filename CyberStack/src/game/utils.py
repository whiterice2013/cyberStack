def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def random_choice(choices):
    return random.choice(choices)

def load_image(file_path):
    return pygame.image.load(file_path)

def draw_text(surface, text, pos, font, color):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))
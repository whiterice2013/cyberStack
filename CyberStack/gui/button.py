class Button:
    def __init__(
        self, rect, text, cost, level, effect, on_click, time, color, hover_color, font
    ):
        self.rect = rect
        self.text = text
        self.cost = cost
        self.level = level
        self.effect = effect
        self.on_click = on_click
        self.hovered = False
        self.time = time
        self.hover_color = hover_color
        self.color = color
        self.font = font

    def update(self, mouse_pos, mouse_click, coins):
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
            if mouse_click and coins >= self.cost:
                self.on_click()
        else:
            self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        surface.fill(color, self.rect)
        text = self.font.render(f"{self.text} Lv.{self.level}", True, (255, 255, 255))
        cost = self.font.render(f"Cost: {self.cost}", True, (255, 255, 0))
        effect = self.font.render(self.effect, True, (0, 255, 255))
        surface.blit(text, (self.rect.x + 5, self.rect.y + 5))
        surface.blit(cost, (self.rect.x + 5, self.rect.y + 35))
        surface.blit(effect, (self.rect.x + 5, self.rect.y + 65))

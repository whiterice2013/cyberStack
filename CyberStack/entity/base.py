class Base:
    def __init__(self, x, y, fade_color, draw_hexagon, BASE_COLOR):
        self.x = x
        self.y = y
        self.fade_color = fade_color
        self.draw_hexagon = draw_hexagon
        self.BASE_COLOR = BASE_COLOR

    def draw(self, surface):
        for glow in range(1, 25):
            glow_size = 30 + glow * glow / (glow / 2)
            color = self.fade_color(self.BASE_COLOR, glow * 50)
            self.draw_hexagon(surface, color, (self.x, self.y), glow_size, width=5)
        for glow in range(1, 25):
            glow_size = 30 - glow * glow / (glow / 2)
            color = self.fade_color(self.BASE_COLOR, glow * 50)
            self.draw_hexagon(surface, color, (self.x, self.y), glow_size, width=5)
        self.draw_hexagon(surface, self.BASE_COLOR, (self.x, self.y), 30, width=5)

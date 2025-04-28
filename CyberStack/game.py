class Game:
    def __init__(
        self,
        base,
        pause_button_rect,
        shop_button_rect,
        BUTTON_COLOR,
        BUTTON_HOVER_COLOR,
        ENEMY_COLOR,
        LASER_COLOR,
        WIDTH,
        HEIGHT,
        font,
        screen,
        fade_color,
        button,
        enemy,
        laser,
        random,
        pygame,
        time,
        math,
    ):
        self.base = base
        self.enemies = []
        self.lasers = []
        self.coins = 80
        self.laser_timer = 0
        self.laser_fire_rate = 50
        self.laser_speed = 50
        self.wave = 1
        self.pause_button_rect = pause_button_rect
        self.paused = False
        self.shop_visible = False

        self.BUTTON_COLOR = BUTTON_COLOR
        self.BUTTON_HOVER_COLOR = BUTTON_HOVER_COLOR
        self.ENEMY_COLOR = ENEMY_COLOR
        self.LASER_COLOR = LASER_COLOR
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = screen
        self.font = font
        self.fade_color = fade_color

        self.button = button
        self.enemy = enemy
        self.laser = laser
        self.random = random
        self.pygame = pygame
        self.time = time
        self.math = math

        # Button for Shop and Upgrade buttons
        self.shop_button_rect = shop_button_rect
        self.buttons = self.create_buttons(
            [
                {
                    "rect": (10, 60, 200, 100),
                    "label": "Laser Speed",
                    "cost": 2,
                    "level": 1,
                    "description": "+2 speed",
                    "action": self.upgrade_laser_speed,
                },
                {
                    "rect": (10, 180, 200, 100),
                    "label": "Shot Rate",
                    "cost": 3,
                    "level": 1,
                    "description": "-3 delay",
                    "action": self.upgrade_laser_rate,
                },
            ]
        )

    def toggle_shop(self):
        self.shop_visible = not self.shop_visible

    def create_buttons(self, button_data):
        buttons = []
        for data in button_data:
            buttons.append(
                self.button(
                    self.pygame.Rect(data["rect"]),
                    data["label"],
                    data["cost"],
                    data["level"],
                    data["description"],
                    data["action"],
                    self.time.time(),
                    self.BUTTON_COLOR,
                    self.BUTTON_HOVER_COLOR,
                    self.pygame.font.Font(None, 36),
                )
            )
        return buttons

    def upgrade_laser_speed(self):
        btn = self.buttons[0]
        if self.coins >= btn.cost:
            self.coins -= btn.cost
            self.laser_speed += 2
            btn.level += 1
            btn.cost = int(btn.cost * 1.8)

    def upgrade_laser_rate(self):
        btn = self.buttons[1]
        if self.coins >= btn.cost:
            self.coins -= btn.cost
            self.laser_fire_rate = max(10, self.laser_fire_rate - 3)
            btn.level += 1
            btn.cost = int(btn.cost * 1.5)

    def spawn_enemies(self):
        for _ in range(self.random.randint(1, self.wave + 1)):
            x = (
                self.random.choice([0, self.WIDTH])
                if self.random.choice([True, False])
                else self.random.uniform(0, self.WIDTH)
            )
            y = (
                self.random.choice([0, self.HEIGHT])
                if not self.random.choice([True, False])
                else self.random.uniform(0, self.HEIGHT)
            )
            if x == 0 and y == 0 or x == self.WIDTH and y == self.HEIGHT:
                self.enemies.append(
                    self.enemy(
                        x, y, self.fade_color, self.ENEMY_COLOR, self.pygame, self.math
                    )
                )

    def fire_laser(self):
        if self.enemies:
            target = min(
                self.enemies,
                key=lambda e: self.math.hypot(e.x - self.base.x, e.y - self.base.y),
            )
            dx, dy = target.x - self.base.x, target.y - self.base.y
            dist = self.math.hypot(dx, dy)
            dx, dy = (dx / dist, dy / dist) if dist else (0, 0)
            self.lasers.append(
                self.laser(
                    self.base.x,
                    self.base.y,
                    dx,
                    dy,
                    self.fade_color,
                    self.LASER_COLOR,
                    self.pygame,
                )
            )

    def update(self):
        if (
            self.pygame.time.get_ticks()
            % self.random.randint(1000, 3000)
            / (self.wave / 3)
            < 20
        ):
            self.spawn_enemies()
        if self.pygame.time.get_ticks() % 10000 < 20:
            self.wave += 1
        self.laser_timer += 1
        if self.laser_timer >= self.laser_fire_rate:
            self.laser_timer = 0
            self.fire_laser()
        for laser in self.lasers[:]:
            laser.move(self.laser_speed)
            for enemy in self.enemies[:]:
                if self.math.hypot(enemy.x - laser.x, enemy.y - laser.y) < 30:
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    if laser in self.lasers:
                        self.lasers.remove(laser)
                    self.coins += 1
                    break
            if laser in self.lasers and not (
                0 <= laser.x <= self.WIDTH and 0 <= laser.y <= self.HEIGHT
            ):
                self.lasers.remove(laser)
        for enemy in self.enemies:
            enemy.move_towards(self.base.x, self.base.y)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.base.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for laser in self.lasers:
            laser.draw(self.screen)
        text = self.font.render(f"Coins: {self.coins}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        # Draw Shop Button
        self.pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.shop_button_rect)
        label = "Shop" if not self.shop_visible else "Close"
        btn_text = self.font.render(label, True, (255, 255, 255))
        self.screen.blit(
            btn_text, (self.shop_button_rect.x + 10, self.shop_button_rect.y + 5)
        )

        # Draw Pause Button
        button_color = self.fade_color((100, 100, 100), 50 if self.paused else 0)
        self.pygame.draw.rect(self.screen, button_color, self.pause_button_rect)
        label = "Start" if self.paused else "Pause"
        btn_text = self.font.render(label, True, (255, 255, 255))
        self.screen.blit(
            btn_text, (self.pause_button_rect.x + 10, self.pause_button_rect.y + 5)
        )

        if self.paused:
            overlay = self.pygame.Surface(
                (self.WIDTH, self.HEIGHT), self.pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            pause_text = self.font.render("!Paused!", True, (255, 255, 0))
            self.screen.blit(pause_text, (self.WIDTH // 2 - 50, self.HEIGHT // 2 - 20))

        # Draw upgrade buttons only if shop is visible
        if self.shop_visible:
            for btn in self.buttons:
                btn.draw(self.screen)

        self.pygame.display.update()

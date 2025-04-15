class Enemy:
    def __init__(self, health, speed):
        self.health = health
        self.speed = speed
        self.position = [0, 0]

    def move(self):
        self.position[0] += self.speed

    def attack(self, target):
        target.health -= 1  # Example damage value, can be adjusted based on game design

    def is_alive(self):
        return self.health > 0
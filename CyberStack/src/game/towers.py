class Tower:
    def __init__(self, damage, range):
        self.damage = damage
        self.range = range

    def attack(self, enemy):
        if self.is_in_range(enemy):
            enemy.health -= self.damage

    def is_in_range(self, enemy):
        # Placeholder for range checking logic
        return True

    def upgrade(self, additional_damage, additional_range):
        self.damage += additional_damage
        self.range += additional_range
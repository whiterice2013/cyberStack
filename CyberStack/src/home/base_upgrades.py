class BaseUpgrade:
    def __init__(self, name, cost, effect):
        self.name = name
        self.cost = cost
        self.effect = effect

    def apply_upgrade(self, player):
        if player.gems >= self.cost:
            player.gems -= self.cost
            self.effect(player)
            return True
        return False

    def __str__(self):
        return f"{self.name} (Cost: {self.cost} gems)"
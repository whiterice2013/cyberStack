def collect_coins(coins, amount):
    """Collect coins and return the updated total."""
    return coins + amount

def apply_temporary_upgrade(tower, upgrade_type):
    """Apply a temporary upgrade to a tower."""
    if upgrade_type == "damage":
        tower.damage *= 1.5  # Increase damage by 50%
    elif upgrade_type == "range":
        tower.range *= 1.2  # Increase range by 20%
    elif upgrade_type == "speed":
        tower.attack_speed *= 0.8  # Decrease attack speed by 20%
    
    # Temporary effect duration can be implemented here
    # For now, we will just return the upgraded tower
    return tower

def reset_tower(tower):
    """Reset tower to its original state after temporary upgrades expire."""
    tower.damage = tower.original_damage
    tower.range = tower.original_range
    tower.attack_speed = tower.original_attack_speed
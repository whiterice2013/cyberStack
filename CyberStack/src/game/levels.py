class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.enemy_waves = []
        self.current_wave = 0
        self.is_wave_active = False

    def create_wave(self, enemy_count):
        wave = [{'type': 'enemy', 'count': enemy_count}]
        self.enemy_waves.append(wave)

    def start_wave(self):
        if self.current_wave < len(self.enemy_waves):
            self.is_wave_active = True
            # Logic to spawn enemies based on the current wave
            self.current_wave += 1

    def update(self):
        if self.is_wave_active:
            # Logic to update the state of the current wave
            pass

    def end_wave(self):
        self.is_wave_active = False
        # Logic to handle end of wave, such as collecting coins or preparing for the next wave

    def reset(self):
        self.current_wave = 0
        self.is_wave_active = False
        self.enemy_waves.clear()
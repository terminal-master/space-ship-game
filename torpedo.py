class Torpedo:
    def __init__(self, x, y, speed_x, speed_y, angle):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.angle = angle
        self.life = 200

    def radius(self):
        return 4

    def set_place(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
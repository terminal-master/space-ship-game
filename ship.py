class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.angle = 0.0
        self.life = 3
        self.missles = 10

    def set_place(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def set_angle(self, newAngle):
        self.angle = newAngle

    def set_speed(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y

    def radius(self):
        return 1


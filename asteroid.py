import math
class Asteroid:
    def __init__(self, x, y, speed_x, speed_y, size):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.size = size

    def has_intersection(self, obj):
        dist = math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)
        return dist <= self.radius() + obj.radius()

    def radius(self):
        return self.size*10 - 5

    def set_place(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
from screen import Screen
import sys
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import math
import random


DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.ship = Ship(random.randint(self.__screen_min_x, self.__screen_max_x), random.randint(self.__screen_min_y, self.__screen_max_y))
        self.all_asteroids = []
        self.all_torpedos = []
        self.score = 0
        self.title = "Game Ended"
        self.message = ""
        for i in range(asteroids_amount):
            rand_x = random.randint(self.__screen_min_x, self.__screen_max_x)
            rand_y = random.randint(self.__screen_min_y, self.__screen_max_y)
            dist = math.sqrt((rand_x - self.ship.x)**2 + (rand_y - self.ship.y)**2)
            while dist <= 26:
                rand_x = random.randint(self.__screen_min_x, self.__screen_max_x)
                rand_y = random.randint(self.__screen_min_y, self.__screen_max_y)
                dist = math.sqrt((rand_x - self.ship.x) ** 2 + (rand_y - self.ship.y) ** 2)
            speed_x = random.randint(-4,4)
            speed_y = random.randint(-4,4)
            while speed_y == 0 or speed_x == 0:
                speed_x = random.randint(-4, 4)
                speed_y = random.randint(-4, 4)
            self.all_asteroids.append(Asteroid(rand_x, rand_y, speed_x, speed_y, 3))
            self.__screen.register_asteroid(self.all_asteroids[i], 3)
            self.__screen.draw_asteroid(self.all_asteroids[i], rand_x, rand_y)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        self._game_loop()
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        if self.__screen.should_end():
            self.message = "you pressed 'q', the game will end."
            self.end()
        if len(self.all_asteroids) == 0:
            self.message = "Congrats, you have destroyed all the asteroid and won the game!!"
            self.end()
        self.mov_obj(self.ship)
        self.redirect_ship(self.ship)
        self.accelerate(self.ship)
        self.__screen.draw_ship(self.ship.x, self.ship.y, self.ship.angle)
        # ********************
        self.fire(self.ship)
        for ast in self.all_asteroids:
            self.__screen.draw_asteroid(ast, ast.x, ast.y)
            self.mov_obj(ast)
            if ast.has_intersection(self.ship):
                if self.ship.life == 0:
                    self.message = "you have no more lives, you have been defeated!"
                    self.end()
                else:
                    self.__screen.show_message("Watch Out!!!", "the ship  has collided with an asteroid!!!")
                    self.__screen.remove_life()
                    self.ship.life -= 1
                    self.__screen.unregister_asteroid(ast)
                    self.all_asteroids.remove(ast)
                    continue
            for tor in self.all_torpedos:
                if ast.has_intersection(tor):
                    self.update_ast(ast, tor)
                    self.ship.missles += 1
                    self.__screen.unregister_torpedo(tor)
                    self.all_torpedos.remove(tor)

        for tor in self.all_torpedos:
            if tor.life == 0:
                self.ship.missles += 1
                self.__screen.unregister_torpedo(tor)
                self.all_torpedos.remove(tor)
            else:
                tor.life -= 1
                self.mov_obj(tor)
                self.__screen.draw_torpedo(tor, tor.x, tor.y, tor.angle)

        pass

    def mov_obj(self, obj):
        delta_x = self.__screen_max_x - self.__screen_min_x
        delta_y = self.__screen_max_y - self.__screen_min_y
        newSpot_x = self.__screen_min_x + (obj.x + obj.speed_x - self.__screen_min_x)%delta_x
        newSpot_y = self.__screen_min_y + (obj.y + obj.speed_y - self.__screen_min_y)%delta_y
        obj.set_place(newSpot_x, newSpot_y)

    def redirect_ship(self, sh):
        if self.__screen.is_left_pressed():
            sh.set_angle(sh.angle + 7)
        elif self.__screen.is_right_pressed():
            sh.set_angle(sh.angle - 7)

    def accelerate(self, sh):
        if self.__screen.is_up_pressed():
            newSpeedx = sh.speed_x + math.cos(sh.angle*(math.pi/180))
            newSpeedy = sh.speed_y + math.sin(sh.angle*(math.pi/180))
            sh.set_speed(newSpeedx, newSpeedy)

    def update_ast(self, ast, tor):
        self.__screen.unregister_asteroid(ast)
        if ast.size == 1:
            self.all_asteroids.remove(ast)
            self.score += 100
        else:
            speed_xy = math.sqrt((ast.speed_x)**2 + (ast.speed_y)**2)
            ast1 = Asteroid(ast.x, ast.y, self.get_ast_speed(ast.speed_x, tor.speed_x)/speed_xy, self.get_ast_speed(ast.speed_y, tor.speed_y)/speed_xy, ast.size-1)
            ast2 = Asteroid(ast.x, ast.y, -1*self.get_ast_speed(ast.speed_x, tor.speed_x)/speed_xy, -1*self.get_ast_speed(ast.speed_y, tor.speed_y)/speed_xy, ast.size-1)
            self.__screen.register_asteroid(ast1, ast1.size)
            self.__screen.register_asteroid(ast2, ast2.size)
            self.all_asteroids.append(ast1)
            self.all_asteroids.append(ast2)
            self.all_asteroids.remove(ast)
            if ast.size == 2:
                self.score += 50
            else:
                self.score += 20

        self.__screen.set_score(self.score)

    def get_ast_speed(self, ast_speed, tor_speed):
        return ast_speed + tor_speed

    def fire(self, sh):
        if self.__screen.is_space_pressed():
            if sh.missles > 0:
                speed_x = sh.speed_x + 2*math.cos(sh.angle*(math.pi/180))
                speed_y = sh.speed_y + 2 * math.sin(sh.angle * (math.pi / 180))
                newTor = Torpedo(sh.x, sh.y, speed_x, speed_y, sh.angle)
                self.all_torpedos.append(newTor)
                self.__screen.register_torpedo(newTor)
                sh.missles -= 1

    def end(self):
        self.__screen.show_message(self.title, self.message)
        self.__screen.end_game()
        sys.exit()





def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)

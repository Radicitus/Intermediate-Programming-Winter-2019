# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage

# from PIL.ImageTk import PhotoImage
from prey import Prey
from random import random


class Floater(Prey):
    radius = 5

    def __init__(self, x, y):
        super().__init__(x, y, 10, 10, 0, 5)
        super().randomize_angle()
        self._color = "#FF0000"

    def update(self, model):
        if random() > .3:
            self.move()
        else:
            spd = self.get_speed() + (-.5 if random() < .5 else .5)
            if 7 > spd > 3:
                self.set_speed(spd)
            self.set_angle(self.get_angle() + (-.5 if random() < .5 else .5))
            self.move()

    def display(self, canvas):
        canvas.create_oval(self._x - Floater.radius, self._y - Floater.radius,
                           self._x + Floater.radius, self._y + Floater.radius,
                           fill=self._color)

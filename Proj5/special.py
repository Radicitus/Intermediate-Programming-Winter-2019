#This special is called "Teleport" and when a simulton comes within 25 pixels of it,
# the simulton has its angle randomized and its position chaged to a random (x, y)
# along the perimeter of a circle surrounding the Special, 25 pixels away from its center.


from mobilesimulton import Mobile_Simulton
from blackhole import Black_Hole
from random import randint


class Special(Black_Hole):
    radius = 10

    def __init__(self, x, y):
        Black_Hole.__init__(self, x, y)
        self._color = "#add8e6"

    def update(self, model):
        teleport = model.find(Mobile_Simulton)
        for sim in teleport:
            if self.contains(sim.get_location()):
                self.teleport(sim, model)


    def display(self, canvas):
        super().display(canvas)

    def contains(self, xy):
        if self.distance(xy) < 25:
            return True
        else:
            return False

    def teleport(self, sim, model):
        new_x = randint(self.get_location()[0] - 25, self.get_location()[0] + 25)
        new_y = randint(self.get_location()[1] - 25, self.get_location()[1] + 25)
        if new_x < 0:
            new_x = 0
        if new_x > model.world()[0]:
            new_x = model.world()[0]
        if new_y < 0:
            new_y = 0
        if new_y > model.world()[1]:
            new_y = model.world()[1]
        sim.set_location(new_x, new_y)
        sim.randomize_angle()

# Black_Hole is derived from only Simulton: each updates by finding and removing
#   any Prey whose center is contained within its radius
#  (returning a set of all eaten simultons), and
#   displays as a black circle with a radius of 10
#   (width/height 20).
# Calling get_dimension for the width/height (for
#   containment and displaying) will facilitate
#   inheritance in Pulsator and Hunter

from simulton import Simulton
from prey import Prey


class Black_Hole(Simulton):
    radius = 10

    def __init__(self, x, y):
        Simulton.__init__(self, x, y, 20, 20)
        self._color = "#000000"

    def update(self, model):
        prey = model.find(Prey)
        contained = set()
        for p in prey:
            if self.contains(p.get_location()):
                contained.add(p)
        return contained

    def display(self, canvas):
        canvas.create_oval(self._x - self.get_dimension()[0]/2, self._y - self.get_dimension()[1]/2,
                           self._x + self.get_dimension()[0]/2, self._y + self.get_dimension()[1]/2,
                           fill=self._color)

    def contains(self, xy):
        if self.distance(xy) < Black_Hole.radius:
            return True
        else:
            return False




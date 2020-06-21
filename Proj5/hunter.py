# Hunter is derived from both the Mobile_Simulton and Pulsator classes;
#   each updates like a Pulsator, but it also moves (either in a straight line
#   or in pursuit of Prey), and displays as a Pulsator.


from prey import Prey
from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from math import atan2


class Hunter(Pulsator, Mobile_Simulton):
    sight = 200

    def __init__(self, x, y):
        Pulsator.__init__(self, x, y)
        Mobile_Simulton.__init__(self, x, y, Pulsator.get_dimension(self)[0], Pulsator.get_dimension(self)[1], 0, 5)
        self.randomize_angle()

    def update(self, model):
        rem = model.find(Prey)
        targets = set()
        for sim in rem:
            if 0 <= self.distance(sim.get_location()) <= Hunter.sight:
                targets.add(sim)
        if len(targets) > 0:
            target = min(targets, key=lambda x: x.distance(self.get_location()))
            self.set_angle(atan2(target.get_location()[1] - self._y, target.get_location()[0] - self._x))
            self.move()
            return super().update(model)
        else:
            self.move()
            return super().update(model)

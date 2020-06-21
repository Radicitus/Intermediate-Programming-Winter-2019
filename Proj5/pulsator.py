# A Pulsator is a Black_Hole; it updates as a Black_Hole
#   does, but also by growing/shrinking depending on
#   whether or not it eats Prey (and removing itself from
#   the simulation if its dimension becomes 0), and displays
#   as a Black_Hole but with varying dimensions


from blackhole import Black_Hole


class Pulsator(Black_Hole):
    counter = 30

    def __init__(self, x, y):
        Black_Hole.__init__(self, x, y)
        self.counter = Pulsator.counter

    def update(self, model):
        rem = super().update(model)
        if len(rem) == 0:
            if self.counter == 0:
                if self.get_dimension()[0] == 1:
                    return {self}
                self.change_dimension(-1, -1)
                self.counter = Pulsator.counter
            self.counter -= 1
            return rem
        else:
            self.change_dimension(len(rem), len(rem))
            self.counter = Pulsator.counter
            return rem



from math import sqrt
class Location2D():

    def __init__(self, x, y):
        """2D Location defined by x and y coords"""
        self.x = x
        self.y = y

    def distance(self, other):
        """Calculates distance between my location and another"""
        if type(other) is not Location2D:
            # TODO throw exception; which exception?
            pass
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __repr__(self):
        return '(%02f:%02f)'%(self.x, self.y)

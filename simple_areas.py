class DiscArea():
    def __init__(self, radius):
        """ A circular area centred at 0,0 with given radius """
        self.radius = radius

    def get_bounds(self):
        return self.radius

class RectangleArea():
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_bounds(self):
        return width, height

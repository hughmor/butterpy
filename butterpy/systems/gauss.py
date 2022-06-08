from numpy import sqrt, exp, pi

class Gaussian:
    # TODO: implement this so its actually useful
    def __init__(self):
        self.center = (0,0)
        self.sig = 1.0

    def gaussian(self, state, t):
        x, y = state
        x0, y0 = self.center
        return exp(-((x-x0)**2 + (y-y0)**2)/(2*self.sig**2))/(self.sig*sqrt(2*pi))

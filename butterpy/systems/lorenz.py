from butterpy.util import random_coord
#rom butterpy.systems.simulation import SystemSimulation
import numpy as np
from numpy import sqrt


class Lorenz(butterpy.systems.simulation.SystemSimulation):
    """
    system of a lorenz attractor
    this object represents an instance of a lorenz system defined by its set of parameters, and initial state

    TODO: accept dictionary for parameters
    """
    dim = 3
    
    def __init__(self, init=(), pars=()):
        self._pars = [
            p for p in pars
        ] if len(pars)==self.dim else random_coord(self.dim)
        self._init_state = [
            p for p in init
        ] if len(init)==self.dim else random_coord(self.dim)
        self.sim = None
<<<<<<< Updated upstream
=======
        self._traj = None
        self._speeds = None

    def save(self, fn):
        if fn[-7:] != '.pickle':
            fn = fn.append('.pickle')
        with open(fn, 'wb') as handle:
            pickle.dump(self.__dict__, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    @classmethod
    def from_file(cls, fn):
        if fn[-7:] != '.pickle':
            fn = fn.append('.pickle')
        with open(fn, 'rb') as handle:
            d = pickle.load(handle)
        ret = cls()
        ret.__dict__ = d
        return ret
>>>>>>> Stashed changes

    @classmethod
    def random_system(cls, s0=None, parameters=None):
        import random
        random.seed()
        means = [10.0, 60.0, 4.20]
        stds = [2.0, 15.0, 1.0]
        parameters = [random.gauss(mu, si) for mu,si in zip(means,stds)] if parameters is None else parameters
        s0 = [random.uniform(1.0, parameters[1]*2) for i in range(3)] if s0 is None else s0
        return cls(init=s0, pars=parameters)
    
    def system(self, state, t):
        """
        Defines the 3d dynamical equation of the system:
            ds/dt=f(s,t)
        I'm using the definition of parameters and coordinates given here: https://en.wikipedia.org/wiki/Lorenz_system
        """
        x,y,z = state
        sigma,rho,beta = self.parameters
        return [
            sigma * (y - x),
            x * (rho - z) - y,
            x * y - beta * z
        ]
    
    def fixed_points(self):
        sigma,rho,beta = self.parameters
        if rho < 1:
            return [(0,0,0)]
        else:
            return [(sqrt(beta*(rho-1)), sqrt(beta*(rho-1)), rho-1),(-sqrt(beta*(rho-1)), -sqrt(beta*(rho-1)), rho-1)]
    
    def simulate(self, time_vect=None):
        time_vect = np.arange(0.0, 50.0, 0.1) if time_vect is None else time_vect
        simulation = SystemSimulation(self, time_vect)
        if simulation.run():
            self.sim = simulation

    @property
    def initial_state(self):
        return self._init_state

    @property
    def sigma(self):
        return self._pars[0]
    
    @property
    def rho(self):
        return self._pars[1]
    
    @property
    def beta(self):
        return self._pars[2]

    @property
    def parameters(self):
        return (self.sigma, self.rho, self.beta)
    
    @sigma.setter
    def sigma(self, val):
        self._pars[0] = val
    
    @rho.setter
    def rho(self, val):
        self._pars[1] = val
    
    @beta.setter
    def beta(self, val):
        self._pars[2] = val
        
    @parameters.setter
    def parameters(self, val): 
        assert len(val) == 3, "Must provide sigma, rho, and beta: parameters must be an iterable of length 3."
        self.sigma = val[0]
        self.rho = val[1]
        self.beta = val[2]

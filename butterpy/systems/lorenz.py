from butterpy.util import random_coord
from butterpy.util.solvers import odeint, rk45
from butterpy.systems.simulation import SystemSimulation
import numpy as np
from numpy import sqrt


class Lorenz:
    """
    system of a lorenz attractor
    this object represents an instance of a lorenz system defined by its set of parameters, and initial state

    TODO: accept dictionary for parameters
    """
    
    def __init__(self, init=(), pars=()):
        self._pars = [
            p for p in pars
        ] if len(pars)==3 else random_coord(3)
        self._init_state = [
            p for p in init
        ] if len(init)==3 else random_coord(3)
        self.sim = None
        self._traj = None
        self._speeds = None

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
            self._traj = self.sim._positions
            self._speeds = self._compute_speed()
            self._max_speed = max(self._speeds)

    def _compute_speed(self):
        self._derivs = np.zeros_like(self.sim._positions)
        for i,t in enumerate(self.sim._time):
            self._derivs[:,i] = self.system(self.trajectory[:,i], t)
        return np.linalg.norm(self._derivs, axis=0)

    @property
    def trajectory(self):
        if self.sim.simulated:
            return self._traj
        else:
            raise RuntimeError("System hasn't been simulated")

    @property
    def speeds(self):
        if self.sim.simulated:
            return self._speeds
        else:
            raise RuntimeError("System hasn't been simulated")

    @property
    def max_speed(self):
        if self.sim.simulated:
            return self._max_speed
        else:
            raise RuntimeError("System hasn't been simulated")

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

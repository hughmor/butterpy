from butterpy.util.solvers import odeint, rk45
import numpy as np

class SystemSimulation:

    def __init__(self, system, time_vect):
        self.simulated = False
        self._sys = system
        self._state = [p for p in system.initial_state]
        self._time = time_vect
        self._solver = odeint

    def run(self):        
        self._positions = self._solver(self._sys.system, self._state, self._time)
        self._positions = self._positions.T
        self.simulated = True

    @property
    def trajectory(self):
        if self.simulated:
            return self._positions
        else:
            raise RuntimeError("System hasn't been simulated")

    @property
    def speeds(self):
        derivs = np.zeros_like(self.trajectory)
        for i,t in enumerate(self._time):
            derivs[:,i] = self._sys.system(self.trajectory[:,i], t)
        return np.linalg.norm(derivs, axis=0)

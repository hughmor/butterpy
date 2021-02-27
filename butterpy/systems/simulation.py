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



    # @property
    # def x(self):
    #     return self._state[0]
    
    # @property
    # def y(self):
    #     return self._state[1]
    
    # @property
    # def z(self):
    #     return self._state[2]
    
    # @property
    # def position(self):
    #     return (self.x, self.y, self.z)

    # @x.setter
    # def x(self, val):
    #     self._state[0] = val
    
    # @y.setter
    # def y(self, val):
    #     self._state[1] = val
    
    # @z.setter
    # def z(self, val):
    #     self._state[2] = val
        
    # @position.setter
    # def position(self, val):
    #     assert len(val) == 3, "This is a 3d system: position must be an iterable of length 3."
    #     self.x = val[0]
    #     self.y = val[1]
    #     self.z = val[2]

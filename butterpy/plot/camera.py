from numpy import linspace, ndarray

class Camera:
    def __init__(self, num_frames, di=5.0, az=10.0, el=1.0):
        add_frame = 2
        distances = self._get_array(di, num_frames+add_frame)
        azimuths = self._get_array(az, num_frames+add_frame)
        elevations = self._get_array(el, num_frames+add_frame)

        def gen():
            for d,a,e in zip(distances, azimuths, elevations):
                yield d,a,e

        self._generator = gen()

    def _get_array(self, v, n):
        if type(v) == tuple:
            if len(v) == 2:
                return linspace(v[0], v[1], n)
            else:
                raise ValueError("Tuple provided with incorrect format. Currently Camera only supports static coordinates, (start,end) tuples, or numpy arrays.")
        elif type(v) == ndarray:
            if len(v) == 2:
                return linspace(v[0], v[1], n)
            elif len(v) == n:
                return v
            else:
                raise ValueError("Bad numpy array provided. Currently Camera only supports static coordinates, (start,end) tuples, or numpy arrays.")
        else:
            return linspace(v, v, n)


    def __next__(self):
        return next(self._generator)
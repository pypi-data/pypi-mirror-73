from . import _kt17

import numpy as np
import logging


class Kt17:
    def __init__(self, rhel, idx):
        """ Initializes KT17 setting the dynamic parameters of the model

            :param rhel (float): heliocentric distance in astronomical units
            :param idx (float): disturbance index as defined by Anderson et al. (2013)

        """
        self.rhel = rhel
        self.idx = idx

        if type(self.rhel) not in [float]:
            raise TypeError("Heliocentric distance is not a float number")
        if type(self.idx) not in [float]:
            raise TypeError("Disturbance index is not a float number")

        self.logger = logging.getLogger('kt17py.Kt17')
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d-%(name)s-%(levelname)s %(message)s',
                                          "%Y-%m-%dT%H:%M:%S"))
        self.logger.addHandler(ch)

        _kt17.kt17_initialize(self.rhel, self.idx)

    def bfield(self, xyz_msm):
        """ Returns the KT17 magnetic field components in Mercury-centric Solar Magnetospheric coordinates in nT units
            corresponding to the given input position

            :param xyz_msm: position in Mercury-centric Solar Magnetospheric coordinates in units of
                            the Mercury radius (2440 Km).
            :return the magnetic field components in Mercury-centric Solar Magnetospheric coordinates, in nT

        """
        self.logger.debug("KT17 Model: distance = {distance} UA, disturbance_index = {idx}"
                          .format(distance=self.rhel, idx=self.idx))

        if not isinstance(xyz_msm, np.ndarray) or xyz_msm.ndim != 2:
            raise TypeError("Input coordinates is not a valid 2d numpy array")

        m = np.shape(xyz_msm)[0]
        n = np.shape(xyz_msm)[1]

        if n != 3:
            raise TypeError("Input coordinates is not a valid ({m}, 3) numpy array".format(m=m))

        x_msm = np.reshape(xyz_msm[:, 0:1], (m,))
        y_msm = np.reshape(xyz_msm[:, 1:2], (m,))
        z_msm = np.reshape(xyz_msm[:, 2:], (m,))

        b_msm = _kt17.kt17_bfield(x_msm, y_msm, z_msm)

        return np.transpose(b_msm)

    def mpdist(self, xyz_msm):
        """ Returns the distance to the magnetopause in Mercury radius units for the given input position
            following Shue et al. (1997) magnetopause model

            :param xyz_msm: position in Mercury-centric Solar Magnetospheric coordinates in units of
                            the Mercury radius (2440 Km).
            :return the distance to the magnetopause in Mercury radius units, negative if the input position is inside
                    the magnetopause, positive if it is outside

        """

        self.logger.debug("KT17 Model: distance = {distance} UA, disturbance_index = {idx}"
                          .format(distance=self.rhel, idx=self.idx))
        if not isinstance(xyz_msm, np.ndarray) or xyz_msm.ndim != 1 or xyz_msm.size != 3:
            raise TypeError("Input coordinates is not a valid 1d numpy array with 3 elements")
        x_msm = xyz_msm[0]
        y_msm = xyz_msm[1]
        z_msm = xyz_msm[2]

        distance, inside, *_ = _kt17.kt17_mpdist(0, x_msm, y_msm, z_msm)

        if inside == 1:
            self.logger.debug("Position [{x},{y},{x}] inside the magnetopause"
                              .format(x=x_msm, y=y_msm, z=z_msm))
        else:
            self.logger.debug("Position [{x},{y},{x}] outside the magnetopause"
                              .format(x=x_msm, y=y_msm, z=z_msm))

        return distance

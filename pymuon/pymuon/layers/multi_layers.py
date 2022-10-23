""".. moduleauthor:: Sacha Medaer"""


import math
from typing import Union

import numpy as np
from scipy.constants import c

from pymuon.elements.element import Element
import pymuon.utils.utilities as util


class MultiLayers():
    """This class simulates multiple layers of given thicknesses of
    specifie media.
    """

    def __init__(self, layers) -> None:
        """
        Parameters
        ----------
        layers_and_thicknesses :
            A dict that contains the element/compound as key and the
            thickness of the layer as value. [cm]

        """
        self._layers = layers

        return None

    @property
    def layers(self):

        return self._layers

    @property
    def thicknesses(self):

        return [layer.thickness for layer in self._layers]

    @property
    def total_thickness(self):

        return sum(self.thicknesses)

    def calc_attenuation(self, particle_kin_energy: float,
                         particle_charge: float, particle_mass: float,
                         nbr_points: int = int(1e3), return_xs: bool = False,
                         log_xs: bool = True) -> np.ndarray:
        """Simulate the mean energy loss through the multiple layers.

        Parameters:
        -----------
        particle_charge :
            The charge of the incident particle.
        particle_mass :
            The mass of the incident particle.
        rel_velocity :
            The relativistic velocity of the incident particle.
            [MeV/c^2]

        """
        thicknesses = self.thicknesses
        total_thickness = self.total_thickness
        fractions = [thickness/total_thickness for thickness in thicknesses]
        points_per_layer = [int(nbr_points*fraction) for fraction in fractions]
        # Make sure that the total nbr are equal to the requested number
        while (sum(points_per_layer) != nbr_points):
            if (sum(points_per_layer) < nbr_points):
                points_per_layer[-1] += 1
            else:
                points_per_layer[-1] -= 1
        # Initiating the calculation of attenuation
        res = np.zeros([])
        xs = np.zeros([])
        for i, layer in enumerate(self._layers):
            if (i):
                crt_particle_kin_energy = res[-1]
            else:
                crt_particle_kin_energy = particle_kin_energy
            crt_res = layer.calc_attenuation(crt_particle_kin_energy,
                                             particle_charge, particle_mass,
                                             points_per_layer[i],
                                             return_xs, log_xs)
            # Stack new results to previous results
            if (i):
                if (return_xs):
                    res =  np.hstack((res, crt_res[0]))
                    xs = np.hstack((xs, xs[-1]+crt_res[1]))
                else:
                    res = np.hstack((res, crt_res))
            else:
                if (return_xs):
                    res = crt_res[0]
                    xs = crt_res[1]
                else:
                    res = crt_res
        # Return results
        if (return_xs):

            return res, xs
        else:

            return res

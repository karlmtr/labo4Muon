""".. moduleauthor:: Sacha Medaer"""


import math
from typing import Union

import numpy as np
from scipy.constants import c

from pymuon.equations.bethe_bloch_equation import BetheBlochEquation
from pymuon.elements.element import Element
import pymuon.utils.utilities as util


class SingleLayer():
    """This class simulates a layer of a given thickness of a specified
    medium.
    """

    def __init__(self, medium, thickness) -> None:
        """
        Parameters
        ----------
        medium :
            The medium.
        thickness :
            The thickness of a the medium. [cm]

        N.B.: TO DO: find database for particle as for element and take
        as input the particle symbol
        """
        self._medium_elem = medium
        self._thickness = thickness

        return None

    @property
    def thickness(self) -> float:

        return self._thickness

    def calc_attenuation(self, particle_kin_energy: float,
                         particle_charge: float, particle_mass: float,
                         nbr_points: int = int(1e3), return_xs: bool = False,
                         log_xs: bool = True) -> np.ndarray:
        """Simulate the mean energy loss through a single layer.

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
        # Initializing Bethe-Bloch
        bethe_bloch = BetheBlochEquation(particle_charge, particle_mass,
                                         self._medium_elem)
        # Initializing distance grid
        xs, step = np.linspace(0., self._thickness, nbr_points, False, True)
        xs += step
        res = np.zeros_like(xs)
        last_kin_energy = particle_kin_energy
        i = 0
        while ((last_kin_energy > 0) and (i < nbr_points)):
            # Calculate lorentz factor
            rel_velocity = util.kin_energy_to_rel_velocity(last_kin_energy,
                                                           particle_mass)
            # Calculate mean attenutaion at the current velocity
            mean_att = bethe_bloch(rel_velocity)
            # Calculate new eneregy at the given distance point
            crt_kin_energy = last_kin_energy - (mean_att * step)
            res[i] = crt_kin_energy if (crt_kin_energy > 0) else 0.
            # Update counter and var
            last_kin_energy = res[i]
            i += 1

        if (return_xs):

            return res, xs
        else:

            return res

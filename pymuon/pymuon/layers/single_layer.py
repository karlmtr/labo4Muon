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

    def __init__(self, medium_symbol, thickness) -> None:
        """
        Parameters
        ----------
        medium_symbol :
            The symbol of the considered medium.
        thickness :
            The thickness of a the material. [cm]

        N.B.: TO DO: find database for particle as for element and take
        as input the particle symbol
        """
        self._medium_symbol = medium_symbol
        self._medium_elem = Element(medium_symbol)
        self._thickness = thickness

        return None

    def calc_attenuation(self, particle_kin_energy: float,
                         particle_charge: float, particle_mass: float,
                         nbr_points: int = int(1e3), return_xs: bool = False,
                         log_xs: bool = True) -> np.ndarray:
        """Simulate the mean energy loss through a given thickness x
        of material.

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
        bethe_bloch = BetheBlochEquation(particle_charge,
                                         particle_mass,
                                         self._medium_elem.mass_number,
                                         self._medium_elem.atomic_number,
                                         self._medium_elem.density)
        # Initializing distance grid
        xs, step = np.linspace(0, self._thickness, nbr_points, True, True)
        res = np.zeros_like(xs)
        res[0] = particle_kin_energy
        i = 1
        while ((res[i-1] > 0) and (i < nbr_points)):
            # Calculate lorentz factor
            rel_velocity = util.kin_energy_to_rel_velocity(res[i-1],
                                                           particle_mass)
            # Calculate mean attenutaion at the current velocity
            mean_att = bethe_bloch(rel_velocity)
            # Calculate new eneregy at the given distance point
            crt_en = res[i-1] - (mean_att * step)
            res[i] = crt_en if (crt_en > 0) else 0.
            # Update counter
            i += 1

        if (return_xs):

            return res, xs
        else:

            return res

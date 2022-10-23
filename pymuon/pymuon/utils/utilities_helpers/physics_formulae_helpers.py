""".. moduleauthor:: Sacha Medaer"""

import math

import numpy as np


'''
# Non-relativistic

def kin_energy_to_rel_velocity(kin_energy, mass):
    """Convert the kinetic energy to the relativistic velocity."""

    if (isinstance(kin_energy, float) or isinstance(kin_energy, int)):

        return math.sqrt(2*kin_energy/mass)

    else:

        return np.sqrt(2*kin_energy/mass)

def rel_velocity_to_kin_energy(rel_velocity, mass):
    """Convert the relativistic velocity to the kinetic energy."""

    if (isinstance(rel_velocity, float) or isinstance(rel_velocity, int)):

        return mass*(rel_velocity**2)/2.0

    else:

        return mass*np.square(rel_velocity)/2.0
'''


def kin_energy_to_momemtum(kin_energy, mass):
    """Convert kinetic energy to momentum."""

    if (isinstance(kin_energy, float) or (isinstance(kin_energy, int))):

        return math.sqrt((kin_energy+mass)**2  - (mass**2))

    else:

        return np.sqrt(np.square(kin_energy+mass) - np.square(mass))


def momentum_to_kin_energy(momentum, mass):
    """Convert momentum to kinetic energy."""

    if (isinstance(momentum, float) or isinstance(momentum, int)):

        return math.sqrt((momentum**2) + (mass**2)) - mass

    else:

        return np.sqrt(np.square(momentum)+np.square(mass)) - mass


def kin_energy_to_rel_velocity(kin_energy, mass):
    """Convert the kinetic energy to the relativistic velocity."""

    if (isinstance(kin_energy, float) or isinstance(kin_energy, int)):

        return math.sqrt(1 - (1/((kin_energy/mass)+1)))

    else:

        return np.sqrt(1 - (1/((kin_energy/mass)+1)))


def rel_velocity_to_kin_energy(rel_velocity, mass):
    """Convert the relativistic velocity to the kinetic energy."""

    if (isinstance(rel_velocity, float) or isinstance(rel_velocity, int)):

        return mass * ((1/math.sqrt(1-(rel_velocity**2))) - 1)

    else:

        return mass * ((1/np.sqrt(1-np.square(rel_velocity))) - 1)

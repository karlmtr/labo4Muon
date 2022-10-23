""".. moduleauthor:: Sacha Medaer"""

import numpy as np
from scipy.constants import physical_constants, c
m_e = physical_constants['electron mass energy equivalent in MeV'][0]   # MeV

from pymuon.formulae.lorentz_factor_formula import LorentzFactorFormula
from pymuon.formulae.max_energy_collision_formula import \
    MaxEnergyCollisionFormula


# Define local methods
calc_lorentz_factor = LorentzFactorFormula.calc_lorentz_factor
calc_max_energy_collision = MaxEnergyCollisionFormula.calc_max_energy_collision

# Constants should be place in dedicated folder constants under utils
# Derive K from basic constant (see Particles et Noyaux)
CONSTANTE_K = 0.307 # MeV cm^2 / g


class BetheBlochEquation():
    """ This class is implementing the fundamental Bethe-Bloch
    equations. See 'Particle et Noyaux' for more details.
    """

    def __init__(self, elec_charge, particle_mass, medium,
                 charge_density_corr=None) -> None:
        """
        The equation is intended to be used for a given medium and
        incident particle. Thus the fixed parameters are given in the
        constructor where as the varying parameters such as the
        velocity of the incidint particle are given as parameters when
        calling the class.

        Parameters
        ----------
        elec_charge :
            The electric charge of the incident particle
        particle_mass :
            The mass of the incident particle
        medium :
            The target medium.
        charge_density_corr :
            The correction for the saturating effects of the charge
            density

        """
        self._elec_charge = elec_charge
        self._particle_mass = particle_mass
        self._medium = medium
        self._mass_number = medium.mass_number
        self._atomic_number = medium.atomic_number
        self._density = medium.density
        self._ionization_cst = medium.ionization_cst
        self._charge_density_corr = charge_density_corr

        return None

    def __call__(self, rel_velocity, medium_density=0):
        r"""
        Compute the Bethe-Bloch equations for the given input
        parameters.

        Parameters
        ----------
        rel_velocity :
            The relativistic velocity of the incident particle
        medium_density :
            The density of the medium

        Notes
        -----

        .. math:: -\langle -\frac{dE}{dx}\rangle = Kz^2 \frac{Z}{A}
                  \frac{1}{\beta^2}\Big(\frac{1}{2}
                  \ln\frac{2m_e c^2 \beta^2\gamma^2 T_{max}}{I^2}
                  - \beta^2 - \frac{\delta(\beta\gamma)}{2}\Big)

        """
        lorentz_factor = calc_lorentz_factor(rel_velocity)
        max_energy = calc_max_energy_collision(self._particle_mass,
                                               rel_velocity)

        first_term = ((CONSTANTE_K*self._atomic_number*(self._elec_charge**2))
                      / (self._mass_number*(rel_velocity**2)))

        ln_term = 0.5 * np.log((2*m_e*(rel_velocity**2)
                                *(lorentz_factor**2)*max_energy)
                               / (self._ionization_cst**2))

        density_corr = 0.
        if (self._charge_density_corr is not None):
            if (callable(self._charge_density_corr)):
                density_corr = self._charge_density_corr(rel_velocity
                                                         * lorentz_factor)
            else:
                density_corr = self._charge_density_corr

        second_term = (ln_term - (rel_velocity**2) - (density_corr/2.0))


        return self._density * first_term * second_term

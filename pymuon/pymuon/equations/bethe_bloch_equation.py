""".. moduleauthor:: Sacha Medaer"""

import numpy as np
from scipy.constants import physical_constants, c
m_e = physical_constants['electron mass energy equivalent in MeV'][0]   # MeV

from pymuon.formulae.lorentz_factor_formula import LorentzFactorFormula
from pymuon.formulae.ionization_constant_formula import \
    IonizationConstantFormula
from pymuon.formulae.max_energy_collision_formula import \
    MaxEnergyCollisionFormula


# Define local methods
calc_lorentz_factor = LorentzFactorFormula.calc_lorentz_factor
calc_ionization_constant = IonizationConstantFormula.calc_ionization_constant
calc_max_energy_collision = MaxEnergyCollisionFormula.calc_max_energy_collision

# Constants should be place in dedicated folder constants under utils
# Derive K from basic constant (see Particles et Noyaux)
CONSTANTE_K = 0.307 # MeV cm^2 / g


class BetheBlochEquation():
    """ This class is implementing the fundamental Bethe-Bloch
    equations. See 'Particle et Noyaux' for more details.
    """

    def __init__(self, elec_charge, particle_mass, mass_number, atomic_number,
                 density, charge_density_corr=None) -> None:
        """
        The equation is intended to be used for a given medium and
        incident particle. Thus the fixed parameters are given in the
        constructor where as the varying parameters such as the
        velocity of the incidint particle are given as parameters when
        calling the class.

        Parameters
        ----------
        mass_number :
            The mass number of the incident particle
        atomic_number :
            The atomic number of the incident particle
        elec_charge :
            The electric charge of the incident particle
        particle_mass :
            The mass of the incident particle
        charge_density_corr :
            The correction for the saturating effects of the charge
            density

        """
        self._elec_charge = elec_charge
        self._particle_mass = particle_mass
        self._mass_number = mass_number
        self._atomic_number = atomic_number
        self._density = density
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
        ionization_cst = calc_ionization_constant(self._atomic_number)
        ionization_cst *= 1e-6   # eV -> MeV
        max_energy = calc_max_energy_collision(self._particle_mass,
                                               rel_velocity)

        first_term = ((CONSTANTE_K*self._atomic_number*(self._elec_charge**2))
                      / (self._mass_number*(rel_velocity**2)))

        ln_term = 0.5 * np.log((2*m_e*(rel_velocity**2)
                                *(lorentz_factor**2)*max_energy)
                               / (ionization_cst**2))

        density_corr = 0.
        if (self._charge_density_corr is not None):
            if (callable(self._charge_density_corr)):
                density_corr = self._charge_density_corr(rel_velocity
                                                         * lorentz_factor)
            else:
                density_corr = self._charge_density_corr

        second_term = (ln_term - (rel_velocity**2) - (density_corr/2.0))


        return self._density * first_term * second_term


if __name__ == "__main__":
    """This code snippet shows the usage of the class.
    """

    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.constants import physical_constants, c

    from pymuon.formulae.lorentz_factor_formula import LorentzFactorFormula

    # For Fe -> our project
    Fe_A = 55.845
    Fe_Z = 26
    Fe_density = 7.874 # g/cm^3
    # For Cu -> often cited as example
    Cu_A = 63.546
    Cu_Z = 29
    Cu_density = 8.96 # g/cm^3
    # For muon
    e_muon = -1
    m_muon = physical_constants['muon mass energy equivalent in MeV'][0]   # MeV/c^2

    bb_eq = BetheBlochEquation(e_muon, m_muon, Cu_A, Cu_Z, Cu_density)

    betas = np.logspace(-1, 0, int(1e3), False)
    neg_atts = bb_eq(betas)

    gammas = LorentzFactorFormula.calc_lorentz_factor(betas)

    fig, ax1 = plt.subplots()

    ax1.plot(betas*gammas, neg_atts)
    plt.title("Mean Energy Loss as a function of the Relativistic Velocity",
              size=25)
    ax1.set_xlabel(r"Velocity $\beta\gamma$", size=20)
    ax1.set_ylabel(r"$-\langle \frac{dE}{dx}\rangle$ (MeV/cm)",
                   size=20)
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    plt.show()

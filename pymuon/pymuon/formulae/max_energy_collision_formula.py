""".. moduleauthor:: Sacha Medaer"""

from scipy.constants import physical_constants, c
m_e = physical_constants['electron mass energy equivalent in MeV'][0]   # MeV

from pymuon.formulae.lorentz_factor_formula import LorentzFactorFormula


# Define local method
calc_lorentz_factor = LorentzFactorFormula.calc_lorentz_factor


class MaxEnergyCollisionFormula():
    """This class compute the maximum energy transfer in a single
    collision depending on the kinetic energy of the incident particle.
    """

    def __init__(self) -> None:

        return None

    @staticmethod
    def calc_max_energy_collision(mass, rel_velocity):

        lorentz_factor = calc_lorentz_factor(rel_velocity)
        num = 2*m_e*(c**2)*(rel_velocity**2)*(lorentz_factor**2)
        den = 1  + (2*lorentz_factor*m_e/mass) + ((m_e/mass)**2)

        return num / den



if __name__ == "__main__":
    """This code snippet shows the usage of the class.
    """

    import matplotlib.pyplot as plt
    import numpy as np

    mass_muon = 105.6583755 # MeV/c^2
    betas = np.linspace(1e-3, 1, 1000, False)
    max_en = MaxEnergyCollisionFormula.calc_max_energy_collision(mass_muon,
                                                                 betas)


    fig, ax1 = plt.subplots()

    ax1.plot(betas, max_en)
    plt.title("Maximum Energy Transfer per Collision as a function of the "
              "relativistic velocity.")
    ax1.set_xlabel(r"Relativistic Velocity $\beta$")
    ax1.set_ylabel("Max. Energy Transfer per collision")

    plt.show()

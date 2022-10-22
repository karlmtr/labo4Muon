""".. moduleauthor:: Sacha Medaer"""

import math

import numpy as np


class LorentzFactorFormula():
    """This class compute  the Lorentz factor formula.
    """

    def __init__(self) -> None:

        return None

    @staticmethod
    def calc_lorentz_factor(rel_velocity):

        if (isinstance(rel_velocity, float) or  isinstance(rel_velocity, int)):

            return math.sqrt(1-rel_velocity**2)
        else:

            return 1.0 / np.sqrt(1-np.square(rel_velocity))


if __name__ == "__main__":
    """This code snippet shows the usage of the class.
    """

    import matplotlib.pyplot as plt
    import numpy as np

    betas = np.linspace(1e-3, 1, 1000, False)
    gammas = LorentzFactorFormula.calc_lorentz_factor(betas)

    fig, ax1 = plt.subplots()

    ax1.plot(betas, gammas)
    plt.title("Lorentz Factor as a function of the Relativistic Velocity")
    ax1.set_xlabel(r'Relativistic Velocity $\beta$')
    ax1.set_ylabel(r'Lorentz Factor $\gamma$')

    plt.show()

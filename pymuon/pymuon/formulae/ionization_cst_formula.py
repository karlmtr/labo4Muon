""".. moduleauthor:: Sacha Medaer"""

class IonizationCstFormula():
    """This class compute the ionization constant from a fitted formula
    depending on the atomic mass. See 'Particle et Noyaux' for more
    details.
    """

    def __init__(self) -> None:

        return None

    @staticmethod
    def calc_ionization_cst(atomic_number):
        if (atomic_number < 13):

            res = atomic_number * (12 + (7/atomic_number))
        else:

            res = atomic_number * (9.76 + (58.8 * atomic_number**(-1.19)))

        res *= 1e-6     # eV -> MeV

        return res


if __name__ == "__main__":
    """This code snippet shows the usage of the class.
    """

    import matplotlib.pyplot as plt
    import numpy as np

    Zs = np.arange(89) + 1
    Is = np.zeros_like(Zs)
    for i in range(len(Is)):
        Is[i] = IonizationCstFormula.calc_ionization_cst(Zs[i])

    fig, ax1 = plt.subplots()

    ax1.plot(Zs, Is)
    plt.title("Ionization Constant as a function of the Atomic Number")
    ax1.set_xlabel('Atomic Number Z')
    ax1.set_ylabel('Ionization Constant I (MeV)')

    plt.show()

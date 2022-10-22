""".. moduleauthor:: Sacha Medaer"""

class IonizationConstantFormula():
    """This class compute the ionization constant from a fitted formula
    depending on the atomic mass. See 'Particle et Noyaux' for more
    details.
    """

    def __init__(self) -> None:

        return None

    @staticmethod
    def calc_ionization_constant(atomic_number):
        if (atomic_number < 13):

            return atomic_number * (12 + (7/atomic_number))
        else:

            return atomic_number * (9.76 + (58.8 * atomic_number**(-1.19)))



if __name__ == "__main__":
    """This code snippet shows the usage of the class.
    """

    import matplotlib.pyplot as plt
    import numpy as np

    Zs = np.arange(89) + 1
    Is = np.zeros_like(Zs)
    for i in range(len(Is)):
        Is[i] = IonizationConstantFormula.calc_ionization_constant(Zs[i])

    fig, ax1 = plt.subplots()

    ax1.plot(Zs, Is)
    plt.title("Ionization Constant as a function of the Atomic Number")
    ax1.set_xlabel('Atomic Number Z')
    ax1.set_ylabel('Ionization Constant I')

    plt.show()

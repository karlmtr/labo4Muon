""".. moduleauthor:: Sacha Medaer"""


from pymuon.elements.abstract_element import AbstractElement


class CustomElement(AbstractElement):
    """This class represents a custom element from the Mendeleev table.
    """

    def __init__(self, atomic_number, mass_number, density, inonization_cst
                 ) -> None:
        """
        Parameters
        ----------
        atomic_number :
            The atomic number of the custom element.
        mass_number :
            The mass number of the custom element.
        density :
            The density of the custom element. [g/cm^3]

        """
        self._atomic_number = atomic_number
        self._mass_number = mass_number
        self._density = density
        self._ionization_cst = ionization_cst

        return None

    @property
    def atomic_number(self) -> float:

        return self._atomic_number

    @property
    def mass_number(self) -> float:

        return self._mass_number

    @property
    def density(self) -> float:

        return self._density

    @property
    def ionization_cst(self) -> float:

        return self._ionization_cst

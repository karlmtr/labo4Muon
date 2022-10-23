""".. moduleauthor:: Sacha Medaer"""


from abc import ABC, abstractmethod


class AbstractElement(ABC):
    """This class represents an element from the Medeleev table.
    """

    def __init__(self) -> None:

        return None

    @property
    @abstractmethod
    def atomic_number(self) -> float:
        pass

    @property
    @abstractmethod
    def mass_number(self) -> float:
        pass

    @property
    @abstractmethod
    def density(self) -> float:
        pass

    @property
    @abstractmethod
    def ionization_cst(self) -> float:
        pass

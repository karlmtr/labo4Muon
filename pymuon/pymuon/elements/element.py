""".. moduleauthor:: Sacha Medaer"""

from mendeleev import element


# Exceptions
class ElementInputError(Exception):
    pass


class Element():
    """This class contains the element properties. Currently, it acts
    as an custom API of the mendeleev python library.
    """

    def __init__(self, symbol: str) -> None:
        self._symbol: str = symbol
        if (Element.does_element_exist(symbol)):
            self._elem = element(symbol)
        else:

            raise ElementInputError('The specified symbol {} was not found.'
                                    .format(symbol))

        return None

    @staticmethod
    def does_element_exist(symbol: str):
        try:
            found = element(symbol)

            return True
        except:

            return False

    @property
    def atomic_number(self) -> int:

        return self._elem.atomic_number

    @property
    def mass_number(self) -> int:

        return self._elem.mass_number

    @property
    def density(self) -> int:

        return self._elem.density

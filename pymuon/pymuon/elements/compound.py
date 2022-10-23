""".. moduleauthor:: Sacha Medaer"""

import math
import warnings
from typing import Optional

import numpy as np
from mendeleev import element

from pymuon.elements.abstract_element import AbstractElement
from pymuon.elements.element import Element


# Exceptions
class CompoundInputError(Exception):
    pass

# Warnings
class CompoundWarning(UserWarning):
    pass


class Compound(AbstractElement):
    """This class represents a compound composed of several elements.
    The Bragg's rule is used, which assumes the additivity of stopping
    effects of the constituent elements of the compounds.
    In order to accurately compute the ionization constant, the
    fraction of total atomic electron population of the compound must
    be known. If this latter is not provided, the fraction of the
    constiuent will be used for the computation of the ionization
    constant.
    """

    def __init__(self, symbols_and_fractions: dict,
                 symbols_and_electron_fractions: Optional[dict] = None
                 ) -> None:
        self._symbols = symbols_and_fractions.keys()
        self._elements = [Element(symbol) for symbol in self._symbols]
        self._fractions = [symbols_and_fractions[symbol]
                           for symbol in self._symbols]
        if (np.sum(self._fractions) != 1.0):
            warning_message: str = ("The sum of the provided fractions of the "
                                    "constiuent elements of the compound is "
                                    "not equal to 1.")
            warnings.warn(warning_message, CompoundWarning)

        self._electron_fractions = []
        if (symbols_and_electron_fractions is not None):
            if (set(symbols_and_electron_fractions.keys())
                    != set(self._symbols)):
                error_msg: str = ("The symbols provided for the compound "
                                  "fraction are different than the symbols "
                                  "provided for the electronic fraction.")

                raise CompoundInputError(error_msg)
            else:
                for symbol in self._symbols:
                    fraction_ = symbols_and_electron_fractions[symbol]
                    self._electron_fractions.append(fraction_)

        return None

    @property
    def atomic_number(self) -> float:
        atomic_number = 0.
        for i in range(len(self._elements)):
            atomic_number += (self._elements[i].atomic_number
                              * self._fractions[i])

        return atomic_number

    @property
    def mass_number(self) -> float:
        mass_number = 0.
        for i in range(len(self._elements)):
            mass_number += (self._elements[i].mass_number * self._fractions[i])

        return mass_number

    @property
    def density(self) -> float:

        density = 0.
        for i in range(len(self._elements)):
            density += (self._elements[i].density * self._fractions[i])

        return density

    @property
    def ionization_cst(self) -> float:
        fractions_ = self._electron_fractions
        if (not fractions_):
            fractions_ = self._fractions

        ionization_cst = 0.
        for i in range(len(self._elements)):
            ionization_cst += (math.log(self._elements[i].ionization_cst)
                               * fractions_[i])

        return math.e**(ionization_cst)

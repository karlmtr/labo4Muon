__name__ = "pymuon"

available_formulae = []

from pymuon.formulae.ionization_cst_formula import IonizationCstFormula
calc_ionization_cst = IonizationCstFormula.calc_ionization_cst
available_formulae.append(calc_ionization_cst)
from pymuon.formulae.lorentz_factor_formula import LorentzFactorFormula
calc_lorentz_factor = LorentzFactorFormula.calc_lorentz_factor
available_formulae.append(calc_lorentz_factor)
from pymuon.formulae.max_energy_collision_formula import MaxEnergyCollisionFormula
calc_max_energy_collision = MaxEnergyCollisionFormula.calc_max_energy_collision
available_formulae.append(calc_max_energy_collision)

available_equations = []
from pymuon.equations.bethe_bloch_equation import BetheBlochEquation
available_equations.append(BetheBlochEquation)

available_elements = []
from pymuon.elements.element import Element
available_elements.append(Element)
from pymuon.elements.custom_element import CustomElement
available_elements.append(CustomElement)
from pymuon.elements.compound import Compound
available_elements.append(Compound)

available_simulations = []

from pymuon.layers.single_layer import SingleLayer


__all__ = (available_formulae + available_equations + available_elements
           + available_simulations)

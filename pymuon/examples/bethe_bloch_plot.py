""".. moduleauthor:: Sacha Medaer"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import physical_constants, c

from pymuon import calc_lorentz_factor, BetheBlochEquation, Element


symbols = ['Pb', 'Cu', 'Fe', 'He', 'H']
# For muon
e_muon = -1
m_muon = physical_constants['muon mass energy equivalent in MeV'][0]   # MeV/c^2

fig, ax1 = plt.subplots()
betas = np.logspace(-1, 0, int(1e3), False)

for symbol in symbols:
    elem = Element(symbol)
    A = elem.mass_number
    Z = elem.atomic_number
    rho = elem.density
    bb_eq = BetheBlochEquation(e_muon, m_muon, A, Z, rho)
    neg_atts = bb_eq(betas)

    gammas = calc_lorentz_factor(betas)


    ax1.plot(betas*gammas, neg_atts/rho, label=symbol)

ax1.legend(fontsize=20)
plt.title("Mean Energy Loss as a function of the Relativistic Velocity",
          size=25)
ax1.set_xlabel(r"Velocity $\beta\gamma$", size=20)
ax1.set_ylabel(r"$-\frac{1}{\rho}\langle \frac{dE}{dx}\rangle$ ($MeV\,cm^2\/g$)",
               size=20)
ax1.tick_params(axis='both', labelsize=20)
ax1.set_xscale('log')
ax1.set_yscale('log')

plt.show()

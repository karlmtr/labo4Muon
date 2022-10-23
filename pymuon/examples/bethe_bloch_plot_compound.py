""".. moduleauthor:: Sacha Medaer"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import physical_constants, c

from pymuon import calc_lorentz_factor, BetheBlochEquation, Compound


# Example of Bethe Block formula with coumpound
# Compound example is Polyvinyl toluene (type of scintillator) and air
compounds = ['Polyvinyl toluene', 'air']
symbols_and_fractions = [{'C': 0.476, 'H': 0.524}, {'N': 0.78, 'O': 0.22}]
# For muon
e_muon = -1
m_muon = physical_constants['muon mass energy equivalent in MeV'][0]   # MeV/c^2

fig, ax1 = plt.subplots()
betas = np.logspace(-1, 0, int(1e3), False)

for i in range(len(compounds)):
    elem = Compound(symbols_and_fractions[i])
    bb_eq = BetheBlochEquation(e_muon, m_muon, elem)
    neg_atts = bb_eq(betas)

    gammas = calc_lorentz_factor(betas)

    min_ind = np.argmin(neg_atts)
    print('Min : ', betas[min_ind]*gammas[min_ind])
    print(elem.density)
    ax1.plot(betas*gammas, neg_atts/elem.density, label=compounds[i])

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

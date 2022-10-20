import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import physical_constants, c

from pymuon import calc_lorentz_factor, BetheBlochEquation

# media_dic = {'Medium': [mass_number, atomic_number, density]}
media_dic = {}
# Pb
media_dic['Pb'] = [207.2, 82, 11.34]
# Cu
media_dic['Cu'] = [63.546, 29, 8.96]
# Fe
media_dic['Fe'] = [55.845, 26, 7.874]
# He
media_dic['He'] = [4.0026, 2, 0.145]
# H2
media_dic['H2'] = [1.007, 1, 0.0763]
# For muon
e_muon = -1
m_muon = physical_constants['muon mass energy equivalent in MeV'][0]   # MeV/c^2

fig, ax1 = plt.subplots()
betas = np.logspace(-1, 0, int(1e3), False)

for key in media_dic.keys():
    bb_eq = BetheBlochEquation(e_muon, m_muon, media_dic[key][0],
                               media_dic[key][1], media_dic[key][2])
    neg_atts = bb_eq(betas)

    gammas = calc_lorentz_factor(betas)


    ax1.plot(betas*gammas, neg_atts/media_dic[key][2], label=key)

ax1.legend(fontsize=20)
plt.title("Mean Energy Loss as a function of the Relativistic Velocity",
          size=25)
ax1.set_xlabel(r"Velocity $\beta\gamma$", size=20)
ax1.set_ylabel(r"$-\frac{1}{\rho}\langle \frac{dE}{dx}\rangle$ ($MeV\,cm^2\/g$)",
               size=20)
ax1.set_xscale('log')
ax1.set_yscale('log')

plt.show()

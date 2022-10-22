""".. moduleauthor:: Sacha Medaer"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import physical_constants, c

from pymuon import SingleLayer
import pymuon.utils.utilities as util


symbols = ['Pb', 'Cu', 'Fe', 'He']
# For muon
e_muon = -1
m_muon = physical_constants['muon mass energy equivalent in MeV'][0]   # MeV/c^2

fig, ax1 = plt.subplots()
x = 3e-0    # cm
p_muon  = 100.  # MeV
particle_kin_energy = util.momentum_to_kin_energy(p_muon, m_muon)
print('Particle Initial Kinetic Energy: ', particle_kin_energy, ' MeV')
nbr_points = 1000

for symbol in symbols:
    layer = SingleLayer(symbol, x)

    atts, xs = layer.calc_attenuation(particle_kin_energy, e_muon, m_muon,
                                      nbr_points, True)

    ax1.plot(xs, atts, label=symbol)

ax1.legend(fontsize=20)
plt.title("Mean Energy Loss as a function of the Relativistic Velocity",
          size=25)
ax1.set_xlabel(r"Distance (cm)", size=20)
ax1.set_ylabel(r"Kinetic Energy T (MeV)", size=20)
ax1.tick_params(axis='both', labelsize=20)

plt.show()

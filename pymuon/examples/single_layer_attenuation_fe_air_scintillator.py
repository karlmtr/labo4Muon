""".. moduleauthor:: Sacha Medaer"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import physical_constants, c

from pymuon import SingleLayer, Element, Compound
import pymuon.utils.utilities as util


media = {}
# Media 1 : Fe
media['Fe'] = Element('Fe')
# Media 2 : Air
media['Air'] = Compound({'N': 0.78, 'O': 0.22})
# Media 3 : Scintillator (e.g. Polyvinyl toluene)
media['Scintillator'] = Compound({'C': 0.476, 'H': 0.524})

symbols = media.keys()

# For muon
e_muon = -1
m_muon = physical_constants['muon mass energy equivalent in MeV'][0]   # MeV/c^2


fig, ax1 = plt.subplots()
x = 25    # cm
particle_kin_energy = 100.
nbr_points = 1000

for symbol in symbols:
    elem = media[symbol]
    layer = SingleLayer(elem, x)

    atts, xs = layer.calc_attenuation(particle_kin_energy, e_muon, m_muon,
                                      nbr_points, True)

    xs = np.hstack((np.zeros(1), xs))
    atts = np.hstack((np.array([particle_kin_energy]), atts))
    ax1.plot(xs, atts, label=symbol)

ax1.legend(fontsize=20)
plt.title("Kinetic Energy as a function of the Medium Depth with "
          "{} MeV initial Kinetic Energy".format(int(particle_kin_energy)),
          size=25)
ax1.set_xlabel(r"Depth (cm)", size=20)
ax1.set_ylabel(r"Kinetic Energy T (MeV)", size=20)
ax1.tick_params(axis='both', labelsize=20)

plt.show()

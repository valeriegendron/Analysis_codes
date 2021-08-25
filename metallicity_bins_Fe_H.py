#####
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import decimal
from decimal import Decimal

# Parameters
galaxy_name = 'Af_v1'
time = 3.0  # in Gyr
dlim = 5  # z limit of disc in kpc. +/- lim.
rlim = 20  # limit of disc radius in kpc
width = 0.02  # width of bins for [O/Fe]_mean to [Fe/H] graph
content = 's'  # g (gas) or s (stars)
xlabel = 'Distance from center of mass [kpc]'
ylabel = 'Metallicity'

# Sun
XSH, XSO, XSFe = 0.706, 9.59E-3, 1.17E-3  # masses of H, O and Fe in solar masses

if content == 'g':
    fileName = str(galaxy_name) + "/g000564r"
    columns = (0, 1, 2, 6, 9, 12, 16, 17)  # x, y, z, m_particule, m_He, m_O, m_Fe, m_Z
    title = str(galaxy_name) + " gas metallicity at " + str(time) + " Gyr"
elif content == 's':
    fileName = str(galaxy_name) + "/s000564r"
    columns = (0, 1, 2, 6, 8, 11, 15, 16)  # x, y, z, m_particule, m_He, m_O, m_Fe, m_Z
    title = str(galaxy_name) + " star metallicity at " + str(time) + " Gyr"

# Read files
rx, ry, rz, rm_part, rm_He, rm_O, rm_Fe, rm_Z = np.loadtxt(fileName, usecols=columns, unpack=True)

# Exclude particles in halo
x, y, z, m_H, m_O, m_Fe = [], [], [], [], [], []
for i in range(0, len(rx)):
    if -dlim <= rz[i] <= dlim:
        x.append(rx[i]), y.append(ry[i]), z.append(rz[i]), m_O.append(rm_O[i]), m_Fe.append(rm_Fe[i])
        m_H.append(rm_part[i] - rm_He[i] - rm_Z[i])  # Hydrogen mass
    else:
        continue

# Compute [O/H], [Fe/H] and [O/Fe]
O_H, Fe_H, O_Fe = [], [], []  # will respectively contain [O/H], [Fe/H] and [O/Fe] for each particle
for i in range(0, len(m_H)):
    part_O_H = np.log10(m_O[i] / m_H[i]) - np.log10(XSO / XSH)  # [O/H] of particle
    part_Fe_H = np.log10(m_Fe[i] / m_H[i]) - np.log10(XSO / XSH)  # [Fe/H] of particle

    O_H.append(part_O_H)
    Fe_H.append(part_Fe_H)
    O_Fe.append(part_O_H - part_Fe_H)


# mean [O/Fe] selon bins de [Fe/H]
# Get the [Fe/H] bins
Fe_H_min, Fe_H_max = min(Fe_H), max(Fe_H)

decimal.getcontext().rounding = decimal.ROUND_FLOOR
Fe_H_min = float(Decimal(str(Fe_H_min)).quantize(Decimal("1.00")))
decimal.getcontext().rounding = decimal.ROUND_CEILING
Fe_H_max = float(Decimal(str(Fe_H_max)).quantize(Decimal("1.00")))
bin_number = int(round((Fe_H_max - Fe_H_min)/width))

Fe_H_edges = np.linspace(Fe_H_min, Fe_H_max, num=bin_number, endpoint=False)

# Compute the mean [O/Fe] for each [Fe/H] bin
O_Fe_mean = []  # will contain the mean [O/Fe] in each [Fe/H] bin
for i in range(0, len(Fe_H_edges)):
    O_Fe_bin = []  # will contain the [O/Fe] of each particle in the bin
    for j in range(0, len(Fe_H)):
        if i == (len(Fe_H_edges)-1):
            if Fe_H_edges[i] <= Fe_H[j] <= (Fe_H_edges[i]+0.02):
                O_Fe_bin.append(O_Fe[j])
        elif Fe_H_edges[i] <= Fe_H[j] < Fe_H_edges[i+1]:
            O_Fe_bin.append(O_Fe[j])
    if len(O_Fe_bin) == 0:  # empty list
        # O_Fe_mean.append(np.nan)
        O_Fe_mean.append(np.nan)
    else:
        # Compute mean and add to list
        O_Fe_mean.append(np.mean(O_Fe_bin))

Fe_H_x = []  # will contain the central value of each bin (for the plot)
for i in range(0, len(Fe_H_edges)):
    if i == (len(Fe_H_edges)-1):
        x = Fe_H_edges[i] + width/2
        Fe_H_x.append(x)
    else:
        x = Fe_H_edges[i] + (Fe_H_edges[i+1] - Fe_H_edges[i])/2
        Fe_H_x.append(x)


# Plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title(title)
ax.set_xlabel("[Fe/H]")
ax.set_ylabel("[O/Fe]$_{mean}$")
ax.scatter(Fe_H_x, O_Fe_mean)
ax.grid()
fig.tight_layout()

# Saving
fig.savefig(str(galaxy_name) + "-" + content + "_bins_Fe_H-" + str(time) + "_Gyr.png", dpi=500)
# plt.show()

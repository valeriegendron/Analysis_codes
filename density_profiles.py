#####
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# Parameters
galaxy_name = 'Af_v1'
time = 3.0  # in Gyr
dlim = 5  # z limit of disc in kpc. +/- lim.
rlim = 20  # limit of disc radius in kpc
content = 'g'  # g (gas) or s (stars)
xlabel = 'Distance from center of mass [kpc]'
ylabel = 'Density [M$_\odot$/kpc$^2$]'

if content == 'g':
    fileName = str(galaxy_name) + "/g000564r"
    columns = (0, 1, 2, 6)  # x, y, z, m_particule
    title = str(galaxy_name) + " gas density at " + str(time) + " Gyr"
elif content == 's':
    fileName = str(galaxy_name) + "/s000564r"
    columns = (0, 1, 2, 6)  # x, y, z, m_particule
    title = str(galaxy_name) + " star density at " + str(time) + " Gyr"

# Read files
rx, ry, rz, rm_part = np.loadtxt(fileName, usecols=columns, unpack=True)

# Exclude particles in halo
x, y, z, m_part = [], [], [], []
for i in range(0, len(rx)):
    if -dlim <= rz[i] <= dlim:
        x.append(rx[i]), y.append(ry[i]), z.append(rz[i]), m_part.append(rm_part[i])
    else:
        continue

# Separate data in rings
rings = np.arange(0.0, (rlim + 0.5), 0.5).tolist()  # liste de 0.25 à 19.75 kpc, intervalles de 0.5 kpc
density = []  # liste qui contiendra la densite de gas ou d'etoiles dans chaque anneau
for ring in range(0, len(rings)):
    mass_total = 0  # initialisation: masse totale de gas ou d'etoiles pour chaque anneau (change a chaque iteration)
    if ring == 0:
        continue
    else:
        for i in range(0, len(x)):
            radius = np.sqrt((x[i])**2 + (y[i])**2)
            if rings[ring-1] < radius <= rings[ring]:
                mass_total += m_part[i]
            else:
                continue

        density_ring = mass_total/(np.pi*((rings[ring])**2-(rings[ring-1])**2))  # unites de M_sun/kpc^2

        # Add to lists
        density.append(density_ring)

# Plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(rings[1:], density, color='k')
ax.set_title(title)
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
fig.tight_layout()

plt.savefig(str(galaxy_name) + "-" + content + "_density_" + str(time) + "_Gyr.png", dpi=500)
# plt.show()

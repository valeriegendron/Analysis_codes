#####
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# Parameters
content = 'g'  # g (gas) or s (stars)
time = 0.3  # in Gyr
xlabel = 'Distance from center of mass [kpc]'
ylabel = 'Density [M$_\odot$/kpc$^2$]'


def density_profile(galaxy_name, content, time):
    columns = (0, 1, 2, 6)  # x, y, z, m_particule
    dlim = 5  # z limit of disc in kpc. +/- lim.
    rlim = 20  # limit of disc radius in kpc

    dumps, times = np.loadtxt("/home/humar50/RING/RUNS/" + str(galaxy_name) + "/DUMPS/" + str(galaxy_name) + "/tzstep.dat", skiprows=1, usecols=(0, 1), unpack=True)
    index = times.tolist().index(time)
    dump = str(int(dumps[index]))
    while len(dump) != 3:
        dump = '0' + dump  # dump must be of format 000.

    filePath = "/home/humar50/RING/RUNS/" + str(galaxy_name) + "/DUMPS/" + str(galaxy_name)
    if (galaxy_name == 'I') or (galaxy_name == 'I_h') or (galaxy_name == 'I_hh') or (galaxy_name == 'i') or (galaxy_name == 'i_h') or (galaxy_name == 'i_hh'):
        if content == 'g':
            fileName = filePath + "/g000" + dump + "r"
            title = "Gas density at " + str(time) + " Gyr"
        elif content == 's':
            fileName = filePath + "/s000" + dump + "r"
            title = "Star density at " + str(time) + " Gyr"
    else:
        if content == 'g':
            fileName = filePath + "/g000" + dump + "targetr"
            title = "Gas density at " + str(time) + " Gyr"
        elif content == 's':
            fileName = filePath + "/s000" + dump + "targetr"
            title = "Star density at " + str(time) + " Gyr"

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
                radius = np.sqrt((x[i]) ** 2 + (y[i]) ** 2)
                if rings[ring - 1] < radius <= rings[ring]:
                    mass_total += m_part[i]
                else:
                    continue

            density_ring = mass_total / (np.pi * ((rings[ring]) ** 2 - (rings[ring - 1]) ** 2))  # unites de M_sun/kpc^2

            # Add to lists
            density.append(density_ring)

    return rings, density, title


# Plot
galaxy_names = ['I', 'Af_v1']
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
picName = ""
for name in galaxy_names:
    rings, density, title = density_profile(name, content, time)
    ax.plot(rings[1:], density, label='Run ' + name)
    picName += (name + "-")

ax.set_title(title)
plt.legend()
fig.tight_layout()

# Save figure
plt.savefig(picName + content + "_density_" + str(time) + "_Gyr.png", dpi=500)
# plt.show()

#####
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# Parameters
content = 'g'  # g (gas) or s (stars)
time = 0.48  # in Gyr
xlabel = 'Distance from center of mass [kpc]'


def metallicity_profile(galaxy_name, content, time):
    dlim = 5  # z limit of disc in kpc. +/- lim.
    rlim = 20  # limit of disc radius in kpc

    # Sun
    XSH, XSO, XSFe = 0.706, 9.59E-3, 1.17E-3  # masses of H, O and Fe in solar masses

    dumps, times = np.loadtxt("/home/humar50/RING/RUNS/" + str(galaxy_name) + "/DUMPS/" + str(galaxy_name) + "/tzstep.dat", skiprows=1, usecols=(0, 1), unpack=True)
    index = times.tolist().index(time)
    dump = str(int(dumps[index]))
    while len(dump) != 3:
        dump = '0' + dump  # dump must be of format 000.

    filePath = "/home/humar50/RING/RUNS/" + str(galaxy_name) + "/DUMPS/" + str(galaxy_name)
    if (galaxy_name == 'I') or (galaxy_name == 'I_h') or (galaxy_name == 'I_hh') or (galaxy_name == 'i') or (galaxy_name == 'i_h') or (galaxy_name == 'i_hh'):
        if content == 'g':
            fileName = filePath + "/g000" + dump + "r"
            columns = (0, 1, 2, 6, 9, 12, 16, 17)  # x, y, z, m_particule, m_He, m_O, m_Fe, m_Z
            title = "Gas metallicity at " + str(time) + " Gyr"
        elif content == 's':
            fileName = filePath + "/s000" + dump + "r"
            columns = (0, 1, 2, 6, 8, 11, 15, 16)  # x, y, z, m_particule, m_He, m_O, m_Fe, m_Z
            title = "Star metallicity at " + str(time) + " Gyr"
    else:
        if content == 'g':
            fileName = filePath + "/g000" + dump + "targetr"
            columns = (0, 1, 2, 6, 9, 12, 16, 17)  # x, y, z, m_particule, m_He, m_O, m_Fe, m_Z
            title = "Gas metallicity at " + str(time) + " Gyr"
        elif content == 's':
            fileName = filePath + "/s000" + dump + "targetr"
            columns = (0, 1, 2, 6, 8, 11, 15, 16)  # x, y, z, m_particule, m_He, m_O, m_Fe, m_Z
            title = "Star metallicity at " + str(time) + " Gyr"

    # Read files
    rx, ry, rz, rm_part, rm_He, rm_O, rm_Fe, rm_Z = np.loadtxt(fileName, usecols=columns, unpack=True)

    # Exclude particles in halo
    x, y, z, m_H, m_O, m_Fe = [], [], [], [], [], []
    for j in range(0, len(rx)):
        if -dlim <= rz[j] <= dlim:
            x.append(rx[j]), y.append(ry[j]), z.append(rz[j]), m_O.append(rm_O[j]), m_Fe.append(rm_Fe[j])
            m_H.append(rm_part[j] - rm_He[j] - rm_Z[j])  # Hydrogen mass
        else:
            continue

    # Separate data in rings
    rings = np.arange(0.0, (rlim + 0.5), 0.5).tolist()  # liste de 0.0 à rlim kpc, intervalles de 0.5 kpc
    O_H, Fe_H, O_Fe = [], [], []  # listes qui contiendront la metallicite dans chaque anneau
    for ring in range(0, len(rings)):
        ring_O, ring_Fe, ring_H = 0, 0, 0  # initialisation: masses totales de O, Fe, H dans chaque anneau
        if ring == 0:
            continue
        else:
            for k in range(0, len(x)):
                radius = np.sqrt((x[k]) ** 2 + (y[k]) ** 2)
                if rings[ring - 1] < radius <= rings[ring]:
                    ring_H += m_H[k]
                    ring_O += m_O[k]
                    ring_Fe += m_Fe[k]
                else:
                    continue

            O_H_ring = np.log10(ring_O / ring_H) - np.log10(XSO / XSH)
            Fe_H_ring = np.log10(ring_Fe / ring_H) - np.log10(XSFe / XSH)
            O_Fe_ring = O_H_ring - Fe_H_ring

            # Add to lists
            O_H.append(O_H_ring), Fe_H.append(Fe_H_ring), O_Fe.append(O_Fe_ring)

    return rings, O_H, Fe_H, O_Fe, title


# Plot
galaxy_names = ['I', 'Af_v1', 'Af_v2']

# [O/H] #
print("Plotting [O/H]")
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel(xlabel)
ax.set_ylabel('[O/H]')
picName = ""
for name in galaxy_names:
    rings, O_H, Fe_H, O_Fe, title = metallicity_profile(name, content, time)
    ax.plot(rings[1:], O_H, label='Run ' + name)
    picName += (name + "-")

ax.set_title(title)
ax.legend()
fig.tight_layout()

# Save figure
fig.savefig(picName + content + "_O_H_" + str(time) + "_Gyr.png", dpi=500)
# plt.show()


# [Fe/H] #
print("Plotting [Fe/H]")
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.set_xlabel(xlabel)
ax2.set_ylabel('[Fe/H]')
picName = ""
for name in galaxy_names:
    rings, O_H, Fe_H, O_Fe, title = metallicity_profile(name, content, time)
    ax2.plot(rings[1:], Fe_H, label='Run ' + name)
    picName += (name + "-")

ax2.set_title(title)
ax2.legend()
fig2.tight_layout()

# Save figure
fig2.savefig(picName + content + "_Fe_H_" + str(time) + "_Gyr.png", dpi=500)
# plt.show()


# [O/Fe] #
print("Plotting [O/Fe]")
fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.set_xlabel(xlabel)
ax3.set_ylabel('[O/Fe]')
picName = ""
for name in galaxy_names:
    rings, O_H, Fe_H, O_Fe, title = metallicity_profile(name, content, time)
    ax3.plot(rings[1:], O_Fe, label='Run ' + name)
    picName += (name + "-")

ax3.set_title(title)
ax3.legend()
fig3.tight_layout()

# Save figure
fig3.savefig(picName + content + "_O_Fe_" + str(time) + "_Gyr.png", dpi=500)
# plt.show()

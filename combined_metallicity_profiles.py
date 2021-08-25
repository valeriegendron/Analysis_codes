#####
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import os

# Parameters
galaxy_name = 'Af_v1'
time_list = [0.3, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]  # in Gyr
dlim = 5  # z limit of disc in kpc. +/- lim.
rlim = 20  # limit of disc radius in kpc
content = 'g'  # g (gas) or s (stars)
metallicity = 'O_H'  # 'O_H', 'Fe_H' ou 'O_Fe'
xlabel = 'Distance from center of mass [kpc]'

# Sun
XSH, XSO, XSFe = 0.706, 9.59E-3, 1.17E-3  # masses of H, O and Fe in solar masses

# Figure set up
fig = plt.figure()
ax = fig.add_subplot(111)

# Dumps and times corresponding
dumps, times = np.loadtxt(str(galaxy_name) + "/tzstep.dat", skiprows=1, usecols=(0, 1), unpack=True)
index = []
for time in time_list:
    index.append((times.tolist()).index(time))

dumps_list = []
for i in index:
    dumps_list.append(int(dumps[i]))

ends = []
for i in range(0, len(dumps_list)):
    ends.append("00" + str(dumps_list[i]) + "r")

if content == 'g':
    start = 'g00'
    columns = (0, 1, 2, 6, 9, 12, 16, 17)  # x, y, z, m_particule, m_He, m_O, m_Fe, m_Z
    title = str(galaxy_name) + " gas metallicity"
elif content == 's':
    start = 's00'
    columns = (0, 1, 2, 6, 8, 11, 15, 16)  # x, y, z, m_particule, m_He, m_O, m_Fe, m_Z
    title = str(galaxy_name) + " star metallicity"


for i in range(0, len(time_list)):
    for fileName in os.listdir(str(galaxy_name)):
        if fileName.startswith(start):
            if fileName.endswith(ends[i]):
                print(ends[i])
                # Read files
                rx, ry, rz, rm_part, rm_He, rm_O, rm_Fe, rm_Z = np.loadtxt(str(galaxy_name) + "/" + fileName,
                                                                           usecols=columns, unpack=True)

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
                            radius = np.sqrt((x[k])**2 + (y[k])**2)
                            if rings[ring-1] < radius <= rings[ring]:
                                ring_H += m_H[k]
                                ring_O += m_O[k]
                                ring_Fe += m_Fe[k]
                            else:
                                continue

                        O_H_ring = np.log10(ring_O/ring_H) - np.log10(XSO/XSH)
                        Fe_H_ring = np.log10(ring_Fe/ring_H) - np.log10(XSFe/XSH)
                        O_Fe_ring = O_H_ring - Fe_H_ring

                        # Add to lists
                        O_H.append(O_H_ring), Fe_H.append(Fe_H_ring), O_Fe.append(O_Fe_ring)
                # Plot
                if metallicity == 'O_H':
                    ylabel = '[O/H]'
                    ax.plot(rings[1:], O_H, label=str(time_list[i]) + " Gyr")
                    continue
                elif metallicity == 'Fe_H':
                    ylabel = '[Fe/H]'
                    ax.plot(rings[1:], Fe_H, label=str(time_list[i]) + " Gyr")
                    continue
                elif metallicity == 'O_Fe':
                    ylabel = '[O/Fe]'
                    ax.plot(rings[1:], O_Fe, label=str(time_list[i]) + " Gyr")
                    continue


ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.set_title(title)
ax.legend()
fig.tight_layout()

# Save figure
plt.savefig(str(galaxy_name) + "-" + content + "_" + metallicity + ".png", dpi=500)
# plt.show()



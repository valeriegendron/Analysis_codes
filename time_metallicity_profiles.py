####
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os

galaxy_name = 'Af_v1'
content = 'g'  # 'g' or 's'
dlim = 5  # z limit of disc in kpc +/- lim
rlim = 20  # limit of disc radius in kpc
xlabel = 'Time [Gyr]'
ylabel = 'Metallicity'

# Sun
XSH, XSO, XSFe = 0.706, 9.59E-3, 1.17E-3  # masses of H, O and Fe in solar masses

# Time
time = np.loadtxt("/home/humar50/RING/RUNS/" + str(galaxy_name) + "/DUMPS/" + str(galaxy_name) + "/tzstep.dat",
                  skiprows=1, usecols=1, unpack=True)

if content == 'g':
    start = "g00"
    columns = (0, 1, 2, 6, 9, 12, 16, 17)  # x, y, z, m_particule, m_He, m_O, m_Fe, m_Z
    title = str(galaxy_name) + " gas metallicity"
elif content == 's':
    start = "s00"
    columns = (0, 1, 2, 6, 8, 11, 15, 16)  # x, y, z, m_particule, m_He, m_O, m_Fe, m_Z
    title = str(galaxy_name) + " star metallicity"


O_H_1, Fe_H_1, O_Fe_1 = [], [], []  # listes qui contiendront les metallicites selon le temps a 1 kpc
O_H_10, Fe_H_10, O_Fe_10 = [], [], []  # listes qui contiendront les metallicites selon le temps a 10 kpc

O_H_names = ['O_H_1', 'O_H_10']
Fe_H_names = ['Fe_H_1', 'Fe_H_10']
O_Fe_names = ['O_Fe_1', 'O_Fe_10']

for fileName in os.listdir(str(galaxy_name)):
    if fileName.startswith(start):
        if fileName.endswith("r"):
            # Read files
            rx, ry, rz, rm_part, rm_He, rm_O, rm_Fe, rm_Z = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=columns, unpack=True)

            # Exclude particles in halo
            x, y, z, m_H, m_O, m_Fe = [], [], [], [], [], []
            for i in range(0, len(rx)):
                if -dlim <= rz[i] <= dlim:
                    x.append(rx[i]), y.append(ry[i]), z.append(rz[i]), m_O.append(rm_O[i]), m_Fe.append(rm_Fe[i])
                    m_H.append(rm_part[i] - rm_He[i] - rm_Z[i])  # Hydrogen mass
                else:
                    continue

            # Separate data in rings
            rings = [1.0, 10.0]  # contient deux anneaux: un qui finit à 1 kpc et l'autre à 10 kpc
            for ring in range(0, len(rings)):
                ring_O, ring_Fe, ring_H = 0, 0, 0  # initialisation: masses totales de O, Fe, H dans chaque anneau
                for i in range(0, len(x)):
                    radius = np.sqrt((x[i]) ** 2 + (y[i]) ** 2)
                    if rings[ring] - 0.5 < radius <= rings[ring]:  # anneaux de 0.5 kpc d'epaisseur
                        ring_H += m_H[i]
                        ring_O += m_O[i]
                        ring_Fe += m_Fe[i]
                    else:
                        continue

                O_H_ring = np.log10(ring_O / ring_H) - np.log10(XSO / XSH)
                Fe_H_ring = np.log10(ring_Fe / ring_H) - np.log10(XSFe / XSH)
                O_Fe_ring = O_H_ring - Fe_H_ring

                # Add to lists
                globals()[O_H_names[ring]].append(O_H_ring)
                globals()[Fe_H_names[ring]].append(Fe_H_ring)
                globals()[O_Fe_names[ring]].append(O_Fe_ring)


# Get the corresponding time list
time_list = time[(-len(O_H_1)-1):-1]  # on coupe par la fin puisqu'on choisit un temps apres la collision et on se rend a la fin

# Plot
# [O/H], [Fe/H] et [O/Fe] selon le temps a 1 kpc
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(time_list, O_H_1, color='mediumblue', label='[O/H]')
ax.plot(time_list, Fe_H_1, color='orangered', label='[Fe/H]')
ax.plot(time_list, O_Fe_1, color='darkmagenta', label='[O/Fe]')
ax.set_title(title + " in ring at 1 kpc from center")
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.legend()
fig.tight_layout()

plt.savefig(str(galaxy_name) + "-" + content + "_metallicity_1kpc.png", dpi=500)
# plt.show()

# [O/H], [Fe/H] et [O/Fe] selon le temps, a 10 kpc
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot(time_list, O_H_10, color='mediumblue', label='[O/H]')
ax2.plot(time_list, Fe_H_10, color='orangered', label='[Fe/H]')
ax2.plot(time_list, O_Fe_10, color='darkmagenta', label='[O/Fe]')
ax2.set_title(title + " in ring at 10 kpc from center")
ax2.set_xlabel(xlabel)
ax2.set_ylabel(ylabel)
ax2.legend()
fig2.tight_layout()

plt.savefig(str(galaxy_name) + "-" + content + "_metallicity_10kpc.png", dpi=500)
# plt.show()

# [O/Fe] selon [Fe/H], a 1 et 10 kpc
fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.plot(Fe_H_1, O_Fe_1, label='ring at 1 kpc')
ax3.plot(Fe_H_10, O_Fe_10, label='ring at 10 kpc')
ax3.set_title(title)
ax3.set_xlabel('[Fe/H]')
ax3.set_ylabel('[O/Fe]')
fig3.tight_layout()

plt.savefig(str(galaxy_name) + "-" + content + "_metallicity2_1-10kpc.png", dpi=500)
# plt.show()

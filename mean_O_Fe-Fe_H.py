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

# Separate data in rings
rings = np.arange(0.0, (rlim + 0.5), 0.5).tolist()  # liste de 0.0 à rlim kpc, intervalles de 0.5 kpc
O_H, Fe_H, O_Fe = [], [], []  # listes qui contiendront la metallicite dans chaque anneau
mean_O_H, mean_Fe_H, mean_O_Fe = [], [], []  # listes qui contiendront la moyenne de la metallicite des particules dans chaque anneau

for ring in range(0, len(rings)):
    ring_O, ring_Fe, ring_H = 0, 0, 0  # initialisation: masses totales de O, Fe, H pour un anneau
    ring_O_H, ring_Fe_H, ring_O_Fe = [], [], []  # listes qui contiendront la metallicite de chaque particule dans un anneau
    if ring == 0:
        continue
    else:
        for i in range(0, len(x)):
            radius = np.sqrt((x[i])**2 + (y[i])**2)
            if rings[ring-1] < radius <= rings[ring]:
                part_O_H = np.log10(m_O[i]/m_H[i]) - np.log10(XSO/XSH)  # [O/H] d'une particule
                part_Fe_H = np.log10(m_Fe[i]/m_H[i]) - np.log10(XSO/XSH)  # [Fe/H] d'une particule

                ring_O_H.append(part_O_H)
                ring_Fe_H.append(part_Fe_H)
                ring_O_Fe.append(part_O_H - part_Fe_H)

                ring_H += m_H[i]
                ring_O += m_O[i]
                ring_Fe += m_Fe[i]
            else:
                continue

        O_H_ring = np.log10(ring_O/ring_H) - np.log10(XSO/XSH)
        Fe_H_ring = np.log10(ring_Fe/ring_H) - np.log10(XSFe/XSH)
        O_Fe_ring = O_H_ring - Fe_H_ring

        # Add to lists
        mean_O_H.append(np.mean(ring_O_H)), mean_Fe_H.append(np.mean(ring_Fe_H)), mean_O_Fe.append(np.mean(ring_O_Fe))
        O_H.append(O_H_ring), Fe_H.append(Fe_H_ring), O_Fe.append(O_Fe_ring)

# Plot
# [O/H], [Fe/H] et [O/Fe] selon la distance au centre de masse
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(rings[1:], O_H, color='mediumblue', label='[O/H]')
ax.plot(rings[1:], Fe_H, color='orangered', label='[Fe/H]')
ax.plot(rings[1:], O_Fe, color='darkmagenta', label='[O/Fe]')
ax.set_title(title)
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.legend()
fig.tight_layout()

plt.savefig(str(galaxy_name) + "-" + content + "_metallicity_" + str(time) + "_Gyr.png", dpi=500)
# plt.show()


# [O/Fe] selon [Fe/H]
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.scatter(Fe_H, O_Fe, c=rings[1:])
ax2.set_title(title)
ax2.set_xlabel('[Fe/H]')
ax2.set_ylabel('[O/Fe]')
fig2.tight_layout()

plt.savefig(str(galaxy_name) + "-" + content + "_metallicity2_" + str(time) + "_Gyr.png", dpi=500)
# plt.show()


# mean [O/Fe] selon [Fe/H]
fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.scatter(Fe_H, mean_O_Fe, c=rings[1:])
ax3.set_title(title)
ax3.set_xlabel('[Fe/H]')
ax3.set_ylabel('[O/Fe]$_{mean}$')
fig3.tight_layout()

plt.savefig(str(galaxy_name) + "-" + content + "_mean-O_Fe-Fe_H_" + str(time) + "_Gyr.png", dpi=500)
# plt.show()


# mean [O/Fe] selon mean [Fe/H]
fig4 = plt.figure()
ax4 = fig4.add_subplot(111)
ax4.scatter(mean_Fe_H, mean_O_Fe, c=rings[1:])
ax4.set_title(title)
ax4.set_xlabel('[Fe/H]$_{mean}$')
ax4.set_ylabel('[O/Fe]$_{mean}$')
fig4.tight_layout()

plt.savefig(str(galaxy_name) + "-" + content + "_mean-O_Fe-mean-Fe_H_" + str(time) + "_Gyr.png", dpi=500)
# plt.show()

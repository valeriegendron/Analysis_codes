import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os

galaxy_name = 'Af_v1'
columns = (0, 1, 2, 6)  # x, y, z et masse de la particule

# Initialisation
# Target galaxy
tx_cm_gas, tx_cm_stars = [], []
ty_cm_gas, ty_cm_stars = [], []
tz_cm_gas, tz_cm_stars = [], []

# Impactor galaxy
ix_cm_gas, ix_cm_stars = [], []
iy_cm_gas, iy_cm_stars = [], []
iz_cm_gas, iz_cm_stars = [], []

tgmass, tsmass = [], []  # contiendra les masses totales de particules de gas, d'etoiles et de matiere sombre
                                     # a chaque temps
igmass, ismass = [], []

for fileName in os.listdir(str(galaxy_name)):
    if fileName.endswith("_1"):  # Target galaxy
        if fileName.startswith("g00"):
            # Lecture des donnees
            x, y, z, mass = np.loadtxt(str(galaxy_name) + "/" + str(fileName), usecols=columns, unpack=True)

            # Calcul du centre de masse
            mx, my, mz, m_tot = 0, 0, 0, 0
            for i in range(0, len(x)):
                mx += mass[i]*x[i]
                my += mass[i]*y[i]
                mz += mass[i]*z[i]
                m_tot += mass[i]

            x_cm, y_cm, z_cm = mx/m_tot, my/m_tot, mz/m_tot

            tx_cm_gas.append(x_cm*100)  # pour etre en kpc
            ty_cm_gas.append(y_cm*100)
            tz_cm_gas.append(z_cm*100)

            tgmass.append(m_tot)  # en unites de 10^12 M_sun.

        elif fileName.startswith("s00"):
            # Lecture des données
            x, y, z, mass = np.loadtxt(str(galaxy_name) + "/" + str(fileName), usecols=columns, unpack=True)

            # Calcul du centre de masse
            mx, my, mz, m_tot = 0, 0, 0, 0
            for i in range(0, len(x)):
                mx += mass[i] * x[i]
                my += mass[i] * y[i]
                mz += mass[i] * z[i]
                m_tot += mass[i]

            x_cm, y_cm, z_cm = mx / m_tot, my / m_tot, mz / m_tot

            tx_cm_stars.append(x_cm*100)  # pour etre en kpc
            ty_cm_stars.append(y_cm*100)
            tz_cm_stars.append(z_cm*100)

            tsmass.append(m_tot)  # en unites de 10^12 M_sun.

    elif fileName.endswith("_2"):  # Impactor galaxy
        if fileName.startswith("g00"):
            # Lecture des données
            x, y, z, mass = np.loadtxt(str(galaxy_name) + "/" + str(fileName), usecols=columns, unpack=True)

            # Calcul du centre de masse
            mx, my, mz, m_tot = 0, 0, 0, 0
            for i in range(0, len(x)):
                mx += mass[i]*x[i]
                my += mass[i]*y[i]
                mz += mass[i]*z[i]
                m_tot += mass[i]

            x_cm, y_cm, z_cm = mx/m_tot, my/m_tot, mz/m_tot

            ix_cm_gas.append(x_cm*100)  # pour etre en kpc
            iy_cm_gas.append(y_cm*100)
            iz_cm_gas.append(z_cm*100)

            igmass.append(m_tot)  # en unites de 10^12 M_sun.

        elif fileName.startswith("s00"):
            # Lecture des données
            x, y, z, mass = np.loadtxt(str(galaxy_name) + "/" + str(fileName), usecols=columns, unpack=True)

            # Calcul du centre de masse
            mx, my, mz, m_tot = 0, 0, 0, 0
            for i in range(0, len(x)):
                mx += mass[i] * x[i]
                my += mass[i] * y[i]
                mz += mass[i] * z[i]
                m_tot += mass[i]

            x_cm, y_cm, z_cm = mx / m_tot, my / m_tot, mz / m_tot

            ix_cm_stars.append(x_cm*100)  # pour etre en kpc
            iy_cm_stars.append(y_cm*100)
            iz_cm_stars.append(z_cm*100)

            ismass.append(m_tot)  # en unites de 10^12 M_sun.

    else:
        continue

# Calcul de la position du centre de masse total (gas+stars+dm)
tx_cm_tot, ty_cm_tot, tz_cm_tot = [], [], []
ix_cm_tot, iy_cm_tot, iz_cm_tot = [], [], []

for t in range(0, len(tgmass)):
    # Position
    xcm = (tgmass[t]*tx_cm_gas[t]+tsmass[t]*tx_cm_stars[t])/(tgmass[t]+tsmass[t])
    ycm = (tgmass[t]*ty_cm_gas[t]+tsmass[t]*ty_cm_stars[t])/(tgmass[t]+tsmass[t])
    zcm = (tgmass[t]*tz_cm_gas[t]+tsmass[t]*tz_cm_stars[t])/(tgmass[t]+tsmass[t])
    tx_cm_tot.append(xcm)
    ty_cm_tot.append(ycm)
    tz_cm_tot.append(zcm)

for t in range(0, len(igmass)):
    # Position
    xcm = (igmass[t]*ix_cm_gas[t]+ismass[t]*ix_cm_stars[t])/(igmass[t]+ismass[t])
    ycm = (igmass[t]*iy_cm_gas[t]+ismass[t]*iy_cm_stars[t])/(igmass[t]+ismass[t])
    zcm = (igmass[t]*iz_cm_gas[t]+ismass[t]*iz_cm_stars[t])/(igmass[t]+ismass[t])
    ix_cm_tot.append(xcm)
    iy_cm_tot.append(ycm)
    iz_cm_tot.append(zcm)


# Difference de distance entre centres de masses
x_cm_diff, y_cm_diff, z_cm_diff = [], [], []
for t in range(0, len(tgmass)):
    x_cm_diff.append(abs(tx_cm_tot[t] - ix_cm_tot[t]))
    y_cm_diff.append(abs(ty_cm_tot[t] - iy_cm_tot[t]))
    z_cm_diff.append(abs(tz_cm_tot[t] - iz_cm_tot[t]))

# Graphique
time = np.loadtxt(str(galaxy_name) + "/tzstep.dat", skiprows=1, usecols=1, unpack=True)
fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(time, x_cm_diff, color='c', label='x axis')
ax.plot(time, y_cm_diff, color='m', label='y axis')
ax.plot(time, z_cm_diff, color='gold', label='z axis')

ax.set_xlabel('Time [Gyr]')
ax.set_ylabel('Distance [kpc]')
ax.set_title('Distance between centers of mass of target and impactor galaxies, run ' + str(galaxy_name))
ax.legend()

fig.tight_layout()
plt.savefig(str(galaxy_name) + "_distances_cms_g-s.png", dpi=500)
# Ajouter lignes pointillees representant les passages de l'impactor dans la galaxie cible

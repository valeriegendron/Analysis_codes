import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os

galaxy_name = 'Af_v1'
columns = (0, 1, 2, 3, 4, 5, 6)  # x, y, z, v_x, v_y, v_z et masse de la particule

# Initialisation
x_cm_gas, x_cm_stars, x_cm_dm = [], [], []
x_v_gas, x_v_stars, x_v_dm = [], [], []

y_cm_gas, y_cm_stars, y_cm_dm = [], [], []
y_v_gas, y_v_stars, y_v_dm = [], [], []

z_cm_gas, z_cm_stars, z_cm_dm = [], [], []
z_v_gas, z_v_stars, z_v_dm = [], [], []

gmass, smass, dmass = [], [], []  # contiendra les masses totales de particules de gas, d'etoiles et de matiere sombre
                                  # a chaque temps

for fileName in os.listdir(str(galaxy_name)):
    if fileName.startswith("d00"):
        # Lecture des données
        x, y, z, v_x, v_y, v_z, mass = np.loadtxt(str(galaxy_name) + "/" + str(fileName), usecols=columns, unpack=True)

        # Calcul du centre de masse
        mx, my, mz, mv_x, mv_y, mv_z, m_tot = 0, 0, 0, 0, 0, 0, 0
        for i in range(0, len(x)):
            mx += mass[i] * x[i]
            my += mass[i] * y[i]
            mz += mass[i] * z[i]
            mv_x += mass[i] * v_x[i]
            mv_y += mass[i] * v_y[i]
            mv_z += mass[i] * v_z[i]
            m_tot += mass[i]

        x_cm, y_cm, z_cm = mx / m_tot, my / m_tot, mz / m_tot
        v_x_cm, v_y_cm, v_z_cm = mv_x / m_tot, mv_y / m_tot, mv_z / m_tot

        x_cm_dm.append(x_cm*100)  # pour etre en kpc
        y_cm_dm.append(y_cm*100)
        z_cm_dm.append(z_cm*100)
        x_v_dm.append(v_x_cm*207.4)  # pour etre en km/s
        y_v_dm.append(v_y_cm*207.4)
        z_v_dm.append(v_z_cm*207.4)

        dmass.append(m_tot)  # en unites de 10^12 M_sun.

    elif fileName.startswith("g00"):
        # Lecture des données
        x, y, z, v_x, v_y, v_z, mass = np.loadtxt(str(galaxy_name)+"/"+str(fileName), usecols=columns, unpack=True)

        # Calcul du centre de masse
        mx, my, mz, mv_x, mv_y, mv_z, m_tot = 0, 0, 0, 0, 0, 0, 0
        for i in range(0, len(x)):
            mx += mass[i]*x[i]
            my += mass[i]*y[i]
            mz += mass[i]*z[i]
            mv_x += mass[i]*v_x[i]
            mv_y += mass[i]*v_y[i]
            mv_z += mass[i]*v_z[i]
            m_tot += mass[i]

        x_cm, y_cm, z_cm = mx/m_tot, my/m_tot, mz/m_tot
        v_x_cm, v_y_cm, v_z_cm = mv_x/m_tot, mv_y/m_tot, mv_z/m_tot

        x_cm_gas.append(x_cm*100)  # pour etre en kpc
        y_cm_gas.append(y_cm*100)
        z_cm_gas.append(z_cm*100)
        x_v_gas.append(v_x_cm*207.4)  # pour etre en km/s
        y_v_gas.append(v_y_cm*207.4)
        z_v_gas.append(v_z_cm*207.4)

        gmass.append(m_tot)  # en unites de 10^12 M_sun.

    elif fileName.startswith("s00"):
        # Lecture des données
        x, y, z, v_x, v_y, v_z, mass = np.loadtxt(str(galaxy_name) + "/" + str(fileName), usecols=columns, unpack=True)

        # Calcul du centre de masse
        mx, my, mz, mv_x, mv_y, mv_z, m_tot = 0, 0, 0, 0, 0, 0, 0
        for i in range(0, len(x)):
            mx += mass[i] * x[i]
            my += mass[i] * y[i]
            mz += mass[i] * z[i]
            mv_x += mass[i] * v_x[i]
            mv_y += mass[i] * v_y[i]
            mv_z += mass[i] * v_z[i]
            m_tot += mass[i]

        x_cm, y_cm, z_cm = mx / m_tot, my / m_tot, mz / m_tot
        v_x_cm, v_y_cm, v_z_cm = mv_x / m_tot, mv_y / m_tot, mv_z / m_tot

        x_cm_stars.append(x_cm*100)  # pour etre en kpc
        y_cm_stars.append(y_cm*100)
        z_cm_stars.append(z_cm*100)
        x_v_stars.append(v_x_cm*207.4)  # pour etre en km/s
        y_v_stars.append(v_y_cm*207.4)
        z_v_stars.append(v_z_cm*207.4)

        smass.append(m_tot)  # en unites de 10^12 M_sun.

# Calcul de la position et de la vitesse du centre de masse total (gas+stars+dm)
x_cm_tot, y_cm_tot, z_cm_tot = [], [], []
x_v_tot, y_v_tot, z_v_tot = [], [], []

for t in range(0, len(gmass)):
    # Position
    xcm = (gmass[t]*x_cm_gas[t]+smass[t]*x_cm_stars[t]+dmass[t]*x_cm_dm[t])/(gmass[t]+smass[t]+dmass[t])
    ycm = (gmass[t]*y_cm_gas[t]+smass[t]*y_cm_stars[t]+dmass[t]*y_cm_dm[t])/(gmass[t]+smass[t]+dmass[t])
    zcm = (gmass[t]*z_cm_gas[t]+smass[t]*z_cm_stars[t]+dmass[t]*z_cm_dm[t])/(gmass[t]+smass[t]+dmass[t])
    x_cm_tot.append(xcm)
    y_cm_tot.append(ycm)
    z_cm_tot.append(zcm)

    # Vitesse
    xv = (gmass[t]*x_v_gas[t]+smass[t]*x_v_stars[t]+dmass[t]*x_v_dm[t])/(gmass[t]+smass[t]+dmass[t])
    yv = (gmass[t]*y_v_gas[t]+smass[t]*y_v_stars[t]+dmass[t]*y_v_dm[t])/(gmass[t]+smass[t]+dmass[t])
    zv = (gmass[t]*z_v_gas[t]+smass[t]*z_v_stars[t]+dmass[t]*z_v_dm[t])/(gmass[t]+smass[t]+dmass[t])
    x_v_tot.append(xv)
    y_v_tot.append(yv)
    z_v_tot.append(zv)


# Plotting
time = np.loadtxt(str(galaxy_name) + "/tzstep.dat", skiprows=1, usecols=1, unpack=True)

# Position du centre de masse
fig1, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex='all')

ax1.plot(time, x_cm_gas, label="Gas", color='tab:red')
ax1.plot(time, x_cm_stars, label="Stars", color=(1, 0.9, 0))
ax1.plot(time, x_cm_dm, label="Dark matter", color='k')
ax1.plot(time, x_cm_tot, label='All particles', color=(0.5, 0, 1))
ax1.set_ylabel("x position [kpc]")
ax1.set_title("CM position")

ax2.plot(time, y_cm_gas, color='tab:red')
ax2.plot(time, y_cm_stars, color=(1, 0.9, 0))
ax2.plot(time, y_cm_dm, color='k')
ax2.plot(time, y_cm_tot, color=(0.5, 0, 1))
ax2.set_ylabel("y position [kpc]")

ax3.plot(time, z_cm_gas, color='tab:red')
ax3.plot(time, z_cm_stars, color=(1, 0.9, 0))
ax3.plot(time, z_cm_dm, color='k')
ax3.plot(time, z_cm_tot, color=(0.5, 0, 1))
ax3.set_ylabel("z position [kpc]")
ax3.set_xlabel("Time [Gyr]")


# ax1.legend(fontsize=8, frameon=True, loc=(1.05, 0.20))
ax1.legend()

fig1.tight_layout()
plt.savefig(str(galaxy_name)+"_cm-position.png", dpi=500)

# Vitesse du centre de masse
fig2, (ax4, ax5, ax6) = plt.subplots(3, 1, sharex='all')

ax4.plot(time, x_v_gas, label='Gas', color='tab:red')
ax4.plot(time, x_v_stars, label='Stars', color=(1, 0.9, 0))
ax4.plot(time, x_v_dm, label='Dark matter', color='k')
ax4.plot(time, x_v_tot, label='All particles', color=(0.5, 0, 1))
ax4.set_ylabel("x velocity [km/s]")
ax4.set_title("CM velocity")

ax5.plot(time, y_v_gas, color='tab:red')
ax5.plot(time, y_v_stars, color=(1, 0.9, 0))
ax5.plot(time, y_v_dm, color='k')
ax5.plot(time, y_v_tot, color=(0.5, 0, 1))
ax5.set_ylabel("y velocity [km/s]")

ax6.plot(time, z_v_gas, color='tab:red')
ax6.plot(time, z_v_stars, color=(1, 0.9, 0))
ax6.plot(time, z_v_dm, color='k')
ax6.plot(time, z_v_tot, color=(0.5, 0, 1))
ax6.set_ylabel("z velocity [km/s]")
ax6.set_xlabel("Time [Gyr]")

# ax4.legend(fontsize=8, frameon=True, loc=(1.05, 0.20))
ax4.legend()

fig2.tight_layout()
plt.savefig(str(galaxy_name)+"_cm-velocity.png", dpi=500)

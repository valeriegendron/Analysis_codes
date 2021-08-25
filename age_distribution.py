import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

fileName = 's000062_2'
galaxy_name = 'Af_v1'
lim = 10  # limit of center of system in kpc
bins_center = 10
bins_impactor = 20
w = 0.01  # width of bars in bar plot
label_center = "Under " + str(lim) + " kpc of center"
label_impactor = "Over " + str(lim) + " kpc of center"
time = 0.3  # in Gyr

# ------------------------------------------------------------------------------
# Center of mass of system
columns = (0, 1, 2, 6)  # x, y, z positions and particle mass
fileNames = ["d000062", "g000062", "s000062"]

for file in range(0, len(fileNames)):
    if fileNames[file].startswith("d00"):
        # Lecture des données
        x, y, z, mass = np.loadtxt(fileNames[file], usecols=columns, unpack=True)

        # Calcul du centre de masse
        mx, my, mz, m_tot = 0, 0, 0, 0
        for i in range(0, len(x)):
            mx += mass[i] * x[i]
            my += mass[i] * y[i]
            mz += mass[i] * z[i]
            m_tot += mass[i]

        x_cm, y_cm, z_cm = mx / m_tot, my / m_tot, mz / m_tot

        x_cm_dm = x_cm*100  # pour etre en kpc
        y_cm_dm = y_cm*100
        z_cm_dm = z_cm*100

        dmass = m_tot  # en unites de 10^12 M_sun.

    elif fileNames[file].startswith("g00"):
        # Lecture des données
        x, y, z, mass = np.loadtxt(fileNames[file], usecols=columns, unpack=True)

        # Calcul du centre de masse
        mx, my, mz, m_tot = 0, 0, 0, 0
        for i in range(0, len(x)):
            mx += mass[i]*x[i]
            my += mass[i]*y[i]
            mz += mass[i]*z[i]
            m_tot += mass[i]

        x_cm, y_cm, z_cm = mx/m_tot, my/m_tot, mz/m_tot

        x_cm_gas = x_cm*100  # pour etre en kpc
        y_cm_gas = y_cm*100
        z_cm_gas = z_cm*100

        gmass = m_tot  # en unites de 10^12 M_sun.

    elif fileNames[file].startswith("s00"):
        # Lecture des données
        x, y, z, mass = np.loadtxt(fileNames[file], usecols=columns, unpack=True)

        # Calcul du centre de masse
        mx, my, mz, m_tot = 0, 0, 0, 0
        for i in range(0, len(x)):
            mx += mass[i] * x[i]
            my += mass[i] * y[i]
            mz += mass[i] * z[i]
            m_tot += mass[i]

        x_cm, y_cm, z_cm = mx / m_tot, my / m_tot, mz / m_tot

        x_cm_stars = x_cm*100  # pour etre en kpc
        y_cm_stars = y_cm*100
        z_cm_stars = z_cm*100

        smass = m_tot  # en unites de 10^12 M_sun.

# Coordinates of center of mass
xcm = (gmass*x_cm_gas+smass*x_cm_stars+dmass*x_cm_dm)/(gmass+smass+dmass)
ycm = (gmass*y_cm_gas+smass*y_cm_stars+dmass*y_cm_dm)/(gmass+smass+dmass)
zcm = (gmass*z_cm_gas+smass*z_cm_stars+dmass*z_cm_dm)/(gmass+smass+dmass)
# ------------------------------------------------------------------------------

# Read file
x, smass, age = np.loadtxt(fileName, usecols=(0, 6, 21), unpack=True)

# Set to real unit
for i in range(0, len(x)):
    x[i] = x[i]*100  # in kpc
    # age[i] = age[i]*0.471  # in Gyr
    smass[i] = smass[i]*10**(12)  # in M_sun

# Data separation
x_center, age_center = [], []
x_impactor, age_impactor = [], []
for i in range(0, len(x)):
    if (xcm-lim) <= x[i] <= (xcm+lim):
        x_center.append(x[i])
        age_center.append(age[i])
    else:
        x_impactor.append(x[i])
        age_impactor.append(age[i])

# Age distribution (2 subplots)
# fig, (ax1, ax2) = plt.subplots(2, 1, sharex='col', sharey='row')
# ax1.hist(age_center, color='tab:red', label='Under 10 kpc of center')
# ax1.grid()
# ax1.set_ylabel('Number of stars')
# ax1.set_title('Age distribution of star particles of run ' + str(galaxy_name) + ' at 3.0 Gyr')
#
# ax2.hist(age_impactor, color='blue', label='Over 10 kpc of center')
# ax2.grid()
# ax2.set_ylabel('Number of stars')
# ax2.set_xlabel('Age [Gyr]')
# fig.tight_layout()
# plt.show()

# Age distribution (1 frame)
hist_center, cbins_edges = np.histogram(age_center, bins=bins_center)
hist_impactor, ibins_edges = np.histogram(age_impactor, bins=bins_impactor)
for i in range(0, len(hist_center)):
    hist_center[i] = hist_center[i]*smass[0]  # all of smass' elements are the same
for i in range(0, len(hist_impactor)):
    hist_impactor[i] = hist_impactor[i]*smass[0]  # all of smass' elements are the same

fig2 = plt.figure()
ax = fig2.add_subplot(111)
ax.set_xlim(left=0.00, right=time)
ax.bar(cbins_edges[:-1], hist_center, color='blue', alpha=0.6, width=w, label=label_center)
ax.bar(ibins_edges[:-1], hist_impactor, color='tab:red', alpha=0.7, width=w, label=label_impactor)
ax.set_ylabel('Mass of stars [M$_\odot$]')
ax.set_xlabel('Age [Gyr]')
ax.set_title('Age distribution of star particles of run ' + str(galaxy_name) + ' at ' + str(time) + ' Gyr')
ax.grid()
ax.legend()
fig2.tight_layout()
# plt.show()
plt.savefig(str(galaxy_name)+"-age_distribution_" + str(lim) + "_kpc-" + str(time) + "_gyr.png")

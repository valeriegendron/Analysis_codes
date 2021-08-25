import numpy as np
import matplotlib.pyplot as plt
columns = (0, 1)
galaxy_name = 'Af_v3'
time = 1.28
lim = 300  # max extent of x and y axi in kpc
pic_name = str(galaxy_name) + '-galaxy_map_xy'

dt1x_1, dt1y_1 = np.loadtxt('d000164_1', usecols=columns, unpack=True)
dt1x_2, dt1y_2 = np.loadtxt('d000164_2', usecols=columns, unpack=True)

gt1x_1, gt1y_1 = np.loadtxt('g000164_1', usecols=columns, unpack=True)
gt1x_2, gt1y_2 = np.loadtxt('g000164_2', usecols=columns, unpack=True)

st1x_1, st1y_1 = np.loadtxt('s000164_1', usecols=columns, unpack=True)
st1x_2, st1y_2 = np.loadtxt('s000164_2', usecols=columns, unpack=True)

liste_xdata = ['dt1x_1', 'dt1x_2', 'gt1x_1', 'gt1x_2', 'st1x_1', 'st1x_2']
liste_ydata = ['dt1y_1', 'dt1y_2', 'gt1y_1', 'gt1y_2', 'st1y_1', 'st1y_2']

# Set to real unit
for i in range(0, len(liste_xdata)):  # pour parcourir tous les sets de donnees
    for j in range(0, len(globals()[liste_xdata[i]])):  # pour parcourir toutes les donnees d'un fichier
        globals()[liste_xdata[i]][j] = globals()[liste_xdata[i]][j]*100  # conversion en kpc
    for k in range(0, len(globals()[liste_ydata[i]])):
        globals()[liste_ydata[i]][k] = globals()[liste_ydata[i]][k]*100  # conversion en kpc

colors1 = ['k', 'tab:red', (1, 0.9, 0)]
colors2 = ['grey', 'tab:cyan', 'blue']

labels1 = ['Target dark matter', 'Target gas', 'Target stars']
labels2 = ['Impactor dark matter', 'Impactor gas', 'Impactor gas']

marker_size = 0.2
t = 0.2  # transparency

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(dt1x_1, dt1y_1, color=colors1[0], label=labels1[0], s=marker_size, alpha=t)
ax.scatter(gt1x_1, gt1y_1, color=colors1[1], label=labels1[1], s=marker_size, alpha=t)
ax.scatter(st1x_1, st1y_1, color=colors1[2], label=labels1[2], s=marker_size, alpha=t)
ax.scatter(dt1x_2, dt1y_2, color=colors2[0], label=labels2[0], s=marker_size, alpha=t)
ax.scatter(gt1x_2, gt1y_2, color=colors2[1], label=labels2[1], s=marker_size, alpha=t)
ax.scatter(st1x_2, st1y_2, color=colors2[2], label=labels2[2], s=marker_size, alpha=t)
ax.set_ylim(-lim, lim)
ax.set_xlim(-lim, lim)
ax.set_aspect(1)

ax.set_ylabel('y [kpc]')
ax.set_xlabel('x [kpc]')

ax.set_title('Af_v1 evolution'+', '+str(time)+' Gyr')

# Plot legend.
lgnd = ax.legend(fontsize=8, frameon=True, loc=(1.05, 0.20))
for i in range(0, len(liste_xdata)):
    lgnd.legendHandles[i]._sizes = [30]

fig.tight_layout()
plt.show()

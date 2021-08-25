import numpy as np
import matplotlib.pyplot as plt
columns = (0, 1)
galaxy_name = 'Af_v1'
time = [0.02, 0.5, 1.0, 1.5, 2.0, 3.0]
lim = 400  # max extent of x and y axi in kpc
pic_name = str(galaxy_name) + '-galaxy_map_xy'

dt1x_1, dt1y_1 = np.loadtxt('d000005_1', usecols=columns, unpack=True)
dt1x_2, dt1y_2 = np.loadtxt('d000005_2', usecols=columns, unpack=True)
dt2x_1, dt2y_1 = np.loadtxt('d000107_1', usecols=columns, unpack=True)
dt2x_2, dt2y_2 = np.loadtxt('d000107_2', usecols=columns, unpack=True)
dt3x_1, dt3y_1 = np.loadtxt('d000216_1', usecols=columns, unpack=True)
dt3x_2, dt3y_2 = np.loadtxt('d000216_2', usecols=columns, unpack=True)
dt4x_1, dt4y_1 = np.loadtxt('d000317_1', usecols=columns, unpack=True)
dt4x_2, dt4y_2 = np.loadtxt('d000317_2', usecols=columns, unpack=True)
dt5x_1, dt5y_1 = np.loadtxt('d000400_1', usecols=columns, unpack=True)
dt5x_2, dt5y_2 = np.loadtxt('d000400_2', usecols=columns, unpack=True)
dt6x_1, dt6y_1 = np.loadtxt('d000564_1', usecols=columns, unpack=True)
dt6x_2, dt6y_2 = np.loadtxt('d000564_2', usecols=columns, unpack=True)

gt1x_1, gt1y_1 = np.loadtxt('g000005_1', usecols=columns, unpack=True)
gt1x_2, gt1y_2 = np.loadtxt('g000005_2', usecols=columns, unpack=True)
gt2x_1, gt2y_1 = np.loadtxt('g000107_1', usecols=columns, unpack=True)
gt2x_2, gt2y_2 = np.loadtxt('g000107_2', usecols=columns, unpack=True)
gt3x_1, gt3y_1 = np.loadtxt('g000216_1', usecols=columns, unpack=True)
gt3x_2, gt3y_2 = np.loadtxt('g000216_2', usecols=columns, unpack=True)
gt4x_1, gt4y_1 = np.loadtxt('g000317_1', usecols=columns, unpack=True)
gt4x_2, gt4y_2 = np.loadtxt('g000317_2', usecols=columns, unpack=True)
gt5x_1, gt5y_1 = np.loadtxt('g000400_1', usecols=columns, unpack=True)
gt5x_2, gt5y_2 = np.loadtxt('g000400_2', usecols=columns, unpack=True)
gt6x_1, gt6y_1 = np.loadtxt('g000564_1', usecols=columns, unpack=True)
gt6x_2, gt6y_2 = np.loadtxt('g000564_2', usecols=columns, unpack=True)

st1x_1, st1y_1 = np.loadtxt('s000005_1', usecols=columns, unpack=True)
st1x_2, st1y_2 = np.loadtxt('s000005_2', usecols=columns, unpack=True)
st2x_1, st2y_1 = np.loadtxt('s000107_1', usecols=columns, unpack=True)
st2x_2, st2y_2 = np.loadtxt('s000107_2', usecols=columns, unpack=True)
st3x_1, st3y_1 = np.loadtxt('s000216_1', usecols=columns, unpack=True)
st3x_2, st3y_2 = np.loadtxt('s000216_2', usecols=columns, unpack=True)
st4x_1, st4y_1 = np.loadtxt('s000317_1', usecols=columns, unpack=True)
st4x_2, st4y_2 = np.loadtxt('s000317_2', usecols=columns, unpack=True)
st5x_1, st5y_1 = np.loadtxt('s000400_1', usecols=columns, unpack=True)
st5x_2, st5y_2 = np.loadtxt('s000400_2', usecols=columns, unpack=True)
st6x_1, st6y_1 = np.loadtxt('s000564_1', usecols=columns, unpack=True)
st6x_2, st6y_2 = np.loadtxt('s000564_2', usecols=columns, unpack=True)

liste_xdata = ['dt1x_1', 'dt1x_2', 'dt2x_1', 'dt2x_2', 'dt3x_1', 'dt3x_2', 'dt4x_1', 'dt4x_2', 'dt5x_1', 'dt5x_2', 'dt6x_1', 'dt6x_2',
               'gt1x_1', 'gt1x_2', 'gt2x_1', 'gt2x_2', 'gt3x_1', 'gt3x_2', 'gt4x_1', 'gt4x_2', 'gt5x_1', 'gt5x_2', 'gt6x_1', 'gt6x_2',
               'st1x_1', 'st1x_2', 'st2x_1', 'st2x_2', 'st3x_1', 'st3x_2', 'st4x_1', 'st4x_2', 'st5x_1', 'st5x_2', 'st6x_1', 'st6x_2']
liste_ydata = ['dt1y_1', 'dt1y_2', 'dt2y_1', 'dt2y_2', 'dt3y_1', 'dt3y_2', 'dt4y_1', 'dt4y_2', 'dt5y_1', 'dt5y_2', 'dt6y_1', 'dt6y_2',
               'gt1y_1', 'gt1y_2', 'gt2y_1', 'gt2y_2', 'gt3y_1', 'gt3y_2', 'gt4y_1', 'gt4y_2', 'gt5y_1', 'gt5y_2', 'gt6y_1', 'gt6y_2',
               'st1y_1', 'st1y_2', 'st2y_1', 'st2y_2', 'st3y_1', 'st3y_2', 'st4y_1', 'st4y_2', 'st5y_1', 'st5y_2', 'st6y_1', 'st6y_2']

# Set to real unit
for i in range(0, len(liste_xdata)):  # pour parcourir tous les sets de donnees
    for j in range(0, len(globals()[liste_xdata[i]])):  # pour parcourir toutes les donnees d'un fichier
        globals()[liste_xdata[i]][j] = globals()[liste_xdata[i]][j]*100  # conversion en kpc
    for k in range(0, len(globals()[liste_ydata[i]])):
        globals()[liste_ydata[i]][k] = globals()[liste_ydata[i]][k]*100  # conversion en kpc

fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex='col', sharey='row', figsize=(6, 8))

colors1 = ['k', 'tab:red', (1, 0.9, 0)]
colors2 = ['grey', 'tab:cyan', 'blue']

labels1 = ['Target dark matter', 'Target gas', 'Target stars']
labels2 = ['Impactor dark matter', 'Impactor gas', 'Impactor gas']

marker_size = 0.2
t = 0.2  # transparency

ax1.scatter(dt1x_1, dt1y_1, color=colors1[0], label=labels1[0], s=marker_size, alpha=t)
ax1.scatter(gt1x_1, gt1y_1, color=colors1[1], label=labels1[1], s=marker_size, alpha=t)
ax1.scatter(st1x_1, st1y_1, color=colors1[2], label=labels1[2], s=marker_size, alpha=t)
ax1.scatter(dt1x_2, dt1y_2, color=colors2[0], label=labels2[0], s=marker_size, alpha=t)
ax1.scatter(gt1x_2, gt1y_2, color=colors2[1], label=labels2[1], s=marker_size, alpha=t)
ax1.scatter(st1x_2, st1y_2, color=colors2[2], label=labels2[2], s=marker_size, alpha=t)
ax1.set_ylim(-lim, lim)
ax1.set_xlim(-lim, lim)
ax1.set_aspect(1)

ax2.scatter(dt2x_1, dt2y_1, color=colors1[0], label=labels1[0], s=marker_size, alpha=t)
ax2.scatter(gt2x_1, gt2y_1, color=colors1[1], label=labels1[1], s=marker_size, alpha=t)
ax2.scatter(st2x_1, st2y_1, color=colors1[2], label=labels1[2], s=marker_size, alpha=t)
ax2.scatter(dt2x_2, dt2y_2, color=colors2[0], label=labels2[0], s=marker_size, alpha=t)
ax2.scatter(gt2x_2, gt2y_2, color=colors2[1], label=labels2[1], s=marker_size, alpha=t)
ax2.scatter(st2x_2, st2y_2, color=colors2[2], label=labels2[2], s=marker_size, alpha=t)
ax2.set_ylim(-lim, lim)
ax2.set_xlim(-lim, lim)
ax2.set_aspect(1)

ax3.scatter(dt3x_1, dt3y_1, color=colors1[0], label=labels1[0], s=marker_size, alpha=t)
ax3.scatter(gt3x_1, gt3y_1, color=colors1[1], label=labels1[1], s=marker_size, alpha=t)
ax3.scatter(st3x_1, st3y_1, color=colors1[2], label=labels1[2], s=marker_size, alpha=t)
ax3.scatter(dt3x_2, dt3y_2, color=colors2[0], label=labels2[0], s=marker_size, alpha=t)
ax3.scatter(gt3x_2, gt3y_2, color=colors2[1], label=labels2[1], s=marker_size, alpha=t)
ax3.scatter(st3x_2, st3y_2, color=colors2[2], label=labels2[2], s=marker_size, alpha=t)
ax3.set_ylim(-lim, lim)
ax3.set_xlim(-lim, lim)
ax3.set_aspect(1)

ax4.scatter(dt4x_1, dt4y_1, color=colors1[0], label=labels1[0], s=marker_size, alpha=t)
ax4.scatter(gt4x_1, gt4y_1, color=colors1[1], label=labels1[1], s=marker_size, alpha=t)
ax4.scatter(st4x_1, st4y_1, color=colors1[2], label=labels1[2], s=marker_size, alpha=t)
ax4.scatter(dt4x_2, dt4y_2, color=colors2[0], label=labels2[0], s=marker_size, alpha=t)
ax4.scatter(gt4x_2, gt4y_2, color=colors2[1], label=labels2[1], s=marker_size, alpha=t)
ax4.scatter(st4x_2, st4y_2, color=colors2[2], label=labels2[2], s=marker_size, alpha=t)
ax4.set_ylim(-lim, lim)
ax4.set_xlim(-lim, lim)
ax4.set_aspect(1)

ax5.scatter(dt5x_1, dt5y_1, color=colors1[0], label=labels1[0], s=marker_size, alpha=t)
ax5.scatter(gt5x_1, gt5y_1, color=colors1[1], label=labels1[1], s=marker_size, alpha=t)
ax5.scatter(st5x_1, st5y_1, color=colors1[2], label=labels1[2], s=marker_size, alpha=t)
ax5.scatter(dt5x_2, dt5y_2, color=colors2[0], label=labels2[0], s=marker_size, alpha=t)
ax5.scatter(gt5x_2, gt5y_2, color=colors2[1], label=labels2[1], s=marker_size, alpha=t)
ax5.scatter(st5x_2, st5y_2, color=colors2[2], label=labels2[2], s=marker_size, alpha=t)
ax5.set_ylim(-lim, lim)
ax5.set_xlim(-lim, lim)
ax5.set_aspect(1)

ax6.scatter(dt6x_1, dt6y_1, color=colors1[0], label=labels1[0], s=marker_size, alpha=t)
ax6.scatter(gt6x_1, gt6y_1, color=colors1[1], label=labels1[1], s=marker_size, alpha=t)
ax6.scatter(st6x_1, st6y_1, color=colors1[2], label=labels1[2], s=marker_size, alpha=t)
ax6.scatter(dt6x_2, dt6y_2, color=colors2[0], label=labels2[0], s=marker_size, alpha=t)
ax6.scatter(gt6x_2, gt6y_2, color=colors2[1], label=labels2[1], s=marker_size, alpha=t)
ax6.scatter(st6x_2, st6y_2, color=colors2[2], label=labels2[2], s=marker_size, alpha=t)
ax6.set_ylim(-lim, lim)
ax6.set_xlim(-lim, lim)
ax6.set_aspect(1)

ax1.set_ylabel('y [kpc]')
ax3.set_ylabel('y [kpc]')
ax5.set_ylabel('y [kpc]')
ax5.set_xlabel('x [kpc]')
ax6.set_xlabel('x [kpc]')

ax1.set_title('Af_v1 evolution'+', '+str(time[0])+' Gyr')
ax2.set_title(str(time[1])+' Gyr')
ax3.set_title(str(time[2])+' Gyr')
ax4.set_title(str(time[3])+' Gyr')
ax5.set_title(str(time[4])+' Gyr')
ax6.set_title(str(time[5])+' Gyr')

# Plot legend
#ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
lgnd = ax2.legend(fontsize=8, frameon=True, loc=(1.05, 0.20))
for i in range(0, len(liste_xdata)):
    lgnd.legendHandles[i]._sizes = [30]

fig.tight_layout()
plt.show()

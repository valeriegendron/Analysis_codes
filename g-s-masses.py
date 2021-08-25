###
# Trace la masse d'étoiles et de gaz en fonction du rayon pour différents temps
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Parameters
galaxy_name = 'I_hh'
columns = (0, 1, 3, 4)
fileName = galaxy_name + "/sfr_profile.out"
picName = galaxy_name + "-g_s_masses.png"

# Lecture des donnees
time, dist, gmass, smass = np.loadtxt(fileName, usecols=columns, unpack=True)

# Division des donnees selon le rayon
list_dist = []  # liste contenant les distances (chacune est unique)
for i in range(0, len(dist)):
    if dist[i] in list_dist:
        break
    else:
        list_dist.append(dist[i])

# arrays contenant les gmass et smass.
# La ligne 'i' contient les masses selon le temps a la distance a la position 'i' de 'list_dist'
array_gmass = np.zeros((len(list_dist), int(len(gmass)/len(list_dist))))  # initialisation
array_smass = np.zeros((len(list_dist), int(len(smass)/len(list_dist))))  # initialisation
list_time = []  # liste contenant le temps (chacun est unique)
i = 0
j = 0
for k in range(0, len(gmass)):
    if k == 0:
        array_gmass[i, j] = gmass[k]
        array_smass[i, j] = smass[k]
        list_time.append(time[k])
        i += 1
    elif time[k] == time[k-1]:  # meme bloc de temps: chg de ligne
        array_gmass[i, j] = gmass[k]
        array_smass[i, j] = smass[k]
        i += 1
    else:  # bloc de temps different: chg de colonne
        j += 1
        i = 0
        array_gmass[i, j] = gmass[k]
        array_smass[i, j] = smass[k]
        list_time.append(time[k])

# Graphique
fig, (ax1, ax2) = plt.subplots(2, 1, sharex='col', sharey='row')

# Aux temps 0.0, 0.5, 1.0, 1.5, 2.0 et 3.0 Ga.
t0, t0_5, t1, t1_5, t2, t3 = list_time.index(0.02), list_time.index(0.5), list_time.index(1.0),\
                              list_time.index(1.5), list_time.index(2.0), list_time.index(3.0)
index_time_graph = [t0, t0_5, t1, t1_5, t2, t3]
colors = [(1, 0.9, 0), (0.5, 1, 0), (0.3, 0.9, 0.7), (0, 0, 0.6), (0.5, 0, 1), (0.4, 0, 0.2)]

for i in range(0, len(index_time_graph)):
    j = index_time_graph[i]
    legend_gas = str(list_time[j]) + ' Gyr'
    legend_stars = str(list_time[j]) + ' Gyr'
    ax1.plot(list_dist, array_gmass[:, j], label=legend_gas, color=colors[i])
    ax2.plot(list_dist, array_smass[:, j], label=legend_stars, color=colors[i])

ax1.set_ylabel("Mass of gas in ring [M$_\odot$]")
ax2.set_ylabel("Mass of stars in ring [M$_\odot$]")
ax2.set_xlabel("Central radius of ring [kpc]")
ax2.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
ax1.legend()
ax2.legend()
ax1.set_title('Run ' + galaxy_name)
plt.tight_layout()

# save the figure to a png file
plt.savefig(picName, dpi=500)  # dpi sets the size of the image. higher dpi = bigger image
plt.show()

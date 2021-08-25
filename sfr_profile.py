###
# Trace le SRF selon le temps pour differents rayons
print("Importing")
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Parameters
galaxy_name = 'I_hh'  # A changer au besoin
galaxy_type = 'target'  # 'impactor' ou 'target'
columns = (0, 1, 5)  # time, dist, sfr
picName = galaxy_name + "-sfr_profile.png"
fileName = galaxy_name + "/sfr_profile.out"

# Lecture des donnees
print("Reading")
time, dist, sfr = np.loadtxt(fileName, usecols=columns, unpack=True)

# Division des donnees selon le rayon
list_dist = []  # liste contenant les distances (chacune est unique)
for i in range(0, len(dist)):
    if dist[i] in list_dist:
        break
    else:
        list_dist.append(dist[i])

# array contenant les SFR. La ligne 'i' contient les SFR selon le temps a la distance a la position 'i' de 'list_dist'
array_sfr = np.zeros((len(list_dist), int(len(sfr)/len(list_dist))))  # initialisation
list_time = []  # liste contenant le temps (chacun est unique)
i = 0
j = 0
for k in range(0, len(sfr)):
    if k == 0:
        array_sfr[i, j] = sfr[k]
        list_time.append(time[k])
        i += 1
    elif time[k] == time[k-1]:  # meme bloc de temps: chg de ligne
        array_sfr[i, j] = sfr[k]
        i += 1
    else:  # bloc de temps different: chg de colonne
        j += 1
        i = 0
        array_sfr[i, j] = sfr[k]
        list_time.append(time[k])


print("Plotting")
# # Legende
# for i in range(0, len(list_dist)):
#     legend = str(list_dist[i]) + " kpc"
#     plt.plot(list_time, array_sfr[i, :], label=legend)

# Aux distances 1, 2, 5, 10 et 20 kpc. À MODIFIER AU BESOIN
# Galaxie cible
if galaxy_type == 'target':
    d1, d2, d5, d10, d19 = list_dist.index(1.250000), list_dist.index(2.250000), list_dist.index(5.250000),\
                          list_dist.index(10.25000), list_dist.index(19.75000)
# Galaxie impactor
elif galaxy_type == 'impactor':
    d1, d2, d5, d10, d19 = list_dist.index(0.2500000), list_dist.index(1.250000), list_dist.index(2.250000),\
                          list_dist.index(3.25000), list_dist.index(4.25000)

index_dist_graph = [d1, d2, d5, d10, d19]

colors = [(1, 0.9, 0), (0.5, 1, 0), (0.3, 0.9, 0.7), (0, 0, 0.6), (0.5, 0, 1)]

for i in range(0, len(index_dist_graph)):
    j = index_dist_graph[i]
    legend = str(list_dist[j]) + ' kpc'
    plt.plot(list_time, array_sfr[j, :], label=legend, color=colors[i])

plt.xlabel("Time [Gyr]")
plt.ylabel("SFR [M$_\odot$/yr]")
plt.title("Run " + galaxy_name)
plt.legend()
plt.tight_layout()

# save the figure to a png file
plt.savefig(picName, dpi=500)  # dpi sets the size of the image. higher dpi = bigger image
# plt.show()

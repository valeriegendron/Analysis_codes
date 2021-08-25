import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

# Parameters
content = 'g'  # g (gas) or s (stars)
time = 3.0  # in Gyr
xlabel = "Distance from center of mass [kpc]"
ylabel = "Mean tangential velocity [km/s]"


def rotation_curve(galaxy_name, content, time):
    columns = (0, 1, 2, 3, 4)  # x, y, z, vx, vy
    zlim = 5  # +/- lim in z in kpc
    rlim = 10  # lim of radius of disc in kpc

    dumps, times = np.loadtxt("/home/humar50/RING/RUNS/" + str(galaxy_name) + "/DUMPS/" + str(galaxy_name)
                              + "/tzstep.dat", skiprows=1, usecols=(0, 1), unpack=True)
    index = times.tolist().index(time)
    dump = str(int(dumps[index]))
    while len(dump) != 3:
        dump = '0' + dump  # dump must be of format 000.

    filePath = "/home/humar50/RING/RUNS/" + str(galaxy_name) + "/DUMPS/" + str(galaxy_name)

    if content == 'g':
        fileName = filePath + "/g000" + dump + "r"
        title = "Gas particles at " + str(time) + " Gyr"
    elif content == 's':
        fileName = filePath + "/s000" + dump + "r"
        title = "Star particles at " + str(time) + " Gyr"

    # Read files
    rx, ry, rz, rvx, rvy = np.loadtxt(fileName, usecols=columns, unpack=True)

    # Exclude particles in halo
    x, y, z, vx, vy = [], [], [], [], []
    for i in range(0, len(rx)):
        if -zlim <= rz[i] <= zlim:
            x.append(rx[i]), y.append(ry[i]), z.append(rz[i]), vx.append(rvx[i]), vy.append(rvy[i])
        else:
            continue

    # Create bins
    dist_bins = np.linspace(0, rlim, num=50, endpoint=False)
    dist_bins = dist_bins.tolist()  # convert to list
    for i in range(0, len(dist_bins)):
        dist_bins[i] = round(dist_bins[i], 1)
    dist_bins.append(10.0)

    # Compute mean velocity of particles in each bin
    mean_vt = []  # list that will contain the mean tangential velocity in each bin
    for bin_no in range(0, len(dist_bins)):
        vt_list = []  # list containing the tangential velocity of each particle in the bin
        if bin_no == 0:
            continue
        else:
            for i in range(0, len(x)):
                radius = np.sqrt((x[i]) ** 2 + (y[i]) ** 2)
                if dist_bins[bin_no - 1] <= radius < dist_bins[bin_no]:
                    vt = (x[i]*vy[i] - y[i]*vx[i])/radius
                    vt_list.append(vt)
                else:
                    continue

        mean_vt.append(np.mean(vt_list))

    dist_bins_x = []  # will contain the central value of each bin (for the plot)
    for i in range(0, len(dist_bins)-1):
        x = dist_bins[i] + (dist_bins[i+1] - dist_bins[i])/2
        dist_bins_x.append(x)

    return dist_bins_x, mean_vt, title


# Plot
galaxy_names = ['I', 'Af_v1', 'Ar_v1', 'As_v1']
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
picName = ""
for name in galaxy_names:
    dist, vt, title = rotation_curve(name, content, time)
    ax.plot(dist, vt, label='Run ' + name)
    picName += (name + "-")

ax.set_title(title)
plt.legend()
fig.tight_layout()

# Save figure
plt.savefig(picName + content + "_rotation_curves_" + str(time) + "_Gyr.png", dpi=500)
# plt.show()

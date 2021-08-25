import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import math

# Parameters
content = 'g'  # g (gas) or s (stars)
velocity = 't'  # t (tangential) or r (radial)
time = 3.0  # in Gyr
width = 10  # width of velocity bins in km/s


def velocity_distribution(galaxy_name, content, velocity, time):
    columns = (0, 1, 2, 3, 4, 5, 6)  # x, y, z, vx, vy, vz, m
    zlim = 5  # +/- lim in z in kpc
    rlim = 20  # lim of radius of disc in kpc

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
        ylabel = "Gas mass fraction [-]"
        if velocity == 't':
            xlabel = "Tangential velocity [km/s]"
        elif velocity == 'r':
            xlabel = "Radial velocity [km/s]"
    elif content == 's':
        fileName = filePath + "/s000" + dump + "r"
        title = "Star particles at " + str(time) + " Gyr"
        ylabel = "Stellar mass fraction [-]"
        if velocity == 't':
            xlabel = "Tangential velocity [km/s]"
        elif velocity == 'r':
            xlabel = "Radial velocity [km/s]"

    # Read files
    rx, ry, rz, rvx, rvy, rvz, rm = np.loadtxt(fileName, usecols=columns, unpack=True)

    # Exclude particles in halo and outside of a 20 kpc radius
    x, y, z, vx, vy, vz, m = [], [], [], [], [], [], []
    for i in range(0, len(rx)):
        radius = np.sqrt((rx[i])**2 + (ry[i])**2)
        if (-zlim <= rz[i] <= zlim) and (radius < rlim):
            x.append(rx[i]), y.append(ry[i]), z.append(rz[i]), vx.append(rvx[i]), vy.append(rvy[i]),
            vz.append(rvz[i]), m.append(rm[i])
        else:
            continue

    # Compute tangential and radial velocities
    v_list = []  # list that will contain the tangential or radial velocity of all particles
    if velocity == 't':
        for i in range(0, len(m)):
            d = np.sqrt((x[i])**2 + (y[i])**2)
            vt = (x[i]*vy[i] - y[i]*vx[i])/d
            v_list.append(vt)
    elif velocity == 'r':
        for i in range(0, len(m)):
            d = np.sqrt((x[i])**2 + (y[i])**2)
            vr = (x[i]*vx[i] + y[i]*vy[i])/d
            v_list.append(vr)

    # Get the velocity bins
    v_min, v_max = min(v_list), max(v_list)
    v_min, v_max = math.floor(v_min), math.ceil(v_max)
    bin_number = int(round((v_max - v_min) / width))
    v_bins = np.linspace(v_min, v_max, num=bin_number+1, endpoint=False)

    # Compute total particle mass in each velocity bin
    total_mass = []
    for bin_no in range(0, len(v_bins)):
        bin_mass = 0  # initialization of mass of particles in bin
        if bin_no == 0:
            continue
        else:
            for i in range(0, len(m)):
                if v_bins[bin_no-1] <= v_list[i] < v_bins[bin_no]:
                   bin_mass += m[i]
                else:
                    continue

        total_mass.append(bin_mass)

    # Compute mass fraction in each velocity bin
    mass_fraction = []
    mass_galaxy = 0
    for i in range(0, len(m)):
        mass_galaxy += m[i]

    for i in range(0, len(total_mass)):
        mass_fraction.append(total_mass[i]/mass_galaxy)

    return v_bins[0:-1], mass_fraction, title, xlabel, ylabel


# Plot
galaxy_names = ['I', 'Af_v1', 'Ar_v1', 'As_v1']
fig = plt.figure()
ax = fig.add_subplot(111)
picName = ""
for name in galaxy_names:
    v, mass, title, xlabel, ylabel = velocity_distribution(name, content, velocity, time)
    ax.step(v, mass, label='Run ' + name)
    picName += (name + "-")

ax.set_title(title)
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
plt.legend()
fig.tight_layout()

# Save figure
plt.savefig(picName + content + "_" + velocity + "_velocity_distribution_" + str(time) + "_Gyr.png", dpi=500)
# plt.show()

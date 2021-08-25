import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# Parameters
galaxy_names = ['I', 'Af_v1', 'Af_v2']
time_list = [0.48, 1.0, 2.0, 3.0]  # in Gyr
marker_styles = ["o", "X", "d"]
content = 's'  # 'g' for gas particles and 's' for star particles
xlabel = 'Distance from center of mass [kpc]'
ylabel = 'Velocity dispersion [km/s]'


def velocity_dispersion(galaxy_names, content, time, xlabel, ylabel):
    """Computes the velocity dispersion (sigma_r, sigma_t and sigma_z) at a given time"""
    # Setting figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    picName = ""

    for galaxy_name in galaxy_names:
        # Read file
        fileName = '/home/humar50/RING/RUNS/' + galaxy_name + '/DUMPS/' + galaxy_name + '/data_sigma/sigma_v' + content + '.out'
        # times, distance from center, velocity dispersion in x, y and z
        rtimes, rdist, rsr, rst, rsz = np.loadtxt(fileName, usecols=(0, 1, 5, 6, 7), unpack=True)

        dist, sr, st, sz = [], [], [], []  # lists that will contain only the data at the time specified
        for i in range(0, len(rtimes)):
            if rtimes[i] == time:
                dist.append(rdist.tolist()[i]), sr.append(rsr.tolist()[i]), st.append(rst.tolist()[i]), sz.append(rsz.tolist()[i])

        # Plot
        if content == 'g':
            title = 'Gas particles at ' + str(time) + ' Gyr'
        elif content == 's':
            title = 'Star particles at ' + str(time) + ' Gyr'

        marker = marker_styles[galaxy_names.index(galaxy_name)]
        ax.scatter(dist, sr, color='tab:red', marker=marker, alpha=0.7, label=galaxy_name + ', $\sigma_r$')
        ax.scatter(dist, st, color='g', alpha=0.7, marker=marker, label=galaxy_name + ', $\sigma_t$')
        ax.scatter(dist, sz, color='mediumblue', alpha=0.7, marker=marker, label=galaxy_name + ', $\sigma_z$')
        picName += (galaxy_name + '-')

    ax.set_title(title)
    plt.legend()
    fig.tight_layout()

    # Save figure
    fig.savefig(picName + content + "_velocity-distribution_" + str(time) + "_Gyr.png", dpi=500)
    # plt.show()
    plt.cla()
    plt.close()


for time in time_list:
    velocity_dispersion(galaxy_names, content, time, xlabel, ylabel)
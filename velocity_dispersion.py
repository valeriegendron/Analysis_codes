import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# Parameters
galaxy_name = 'Af_v1'
time_list = [0.3, 0.48, 1.0, 2.0, 3.0]  # in Gyr
content = 'g'  # 'g' for gas particles and 's' for star particles
fileName = galaxy_name + '/data_sigma/sigma_v' + content + 'c.out'
xlabel = 'Distance from center of mass [kpc]'
ylabel = 'Velocity dispersion [km/s]'


def velocity_dispersion(galaxy_name, content, time, xlabel, ylabel):
    """Computes the velocity dispersion (sigma_r, sigma_t and sigma_z) at a given time"""
    # Read file
    # times, distance from center, velocity dispersion in x, y and z
    rtimes, rdist, rsr, rst, rsz = np.loadtxt(fileName, usecols=(0, 1, 5, 6, 7), unpack=True)

    dist, sr, st, sz = [], [], [], []  # lists that will contain only the data at the time specified
    for i in range(0, len(rtimes)):
        if rtimes[i] == time:
            dist.append(rdist.tolist()[i]), sr.append(rsr.tolist()[i]), st.append(rst.tolist()[i]), sz.append(rsz.tolist()[i])

    # Plot
    if content == 'g':
        title = 'Run ' + galaxy_name + ' at ' + str(time) + ' Gyr, gas particles'
    elif content == 's':
        title = 'Run ' + galaxy_name + ' at ' + str(time) + ' Gyr, star particles'

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.scatter(dist, sr, color='tab:red', alpha=0.7, label='$\sigma_r$')
    ax.scatter(dist, st, color='g', alpha=0.7, label='$\sigma_t$')
    ax.scatter(dist, sz, color='mediumblue', alpha=0.7, label='$\sigma_z$')
    ax.set_title(title)
    plt.legend()
    fig.tight_layout()

    # Save figure
    fig.savefig(str(galaxy_name) + "-" + content + "_velocity-dispersion_" + str(time) + "_Gyr.png", dpi=500)
    # plt.show()
    plt.cla()
    plt.close()


def velocity_dispersion_time(content, xlabel):
    """Computes the velocity dispersion (sigma_r, sigma_t OR sigma_z) for multiple times"""
    # Read file
    # times, distance from center, number of bin, velocity dispersion in x, y and z
    rtimes, rdist, rbin, rsr, rst, rsz = np.loadtxt(fileName, usecols=(0, 1, 3, 5, 6, 7), unpack=True)

    # Initializing figures
    fig, fig2, fig3 = plt.figure(), plt.figure(), plt.figure()
    ax, ax2, ax3 = fig.add_subplot(111), fig2.add_subplot(111), fig3.add_subplot(111)
    if content == 'g':
        title = 'Run ' + galaxy_name + ', gas particles'
    elif content == 's':
        title = 'Run ' + galaxy_name + ', star particles'

    for time in time_list:
        dist, sr, st, sz = [], [], [], []  # lists that will contain only the data at the time specified
        for j in range(0, len(rtimes)):
            if rtimes[j] == time:
                dist.append(rdist.tolist()[j]), sr.append(rsr.tolist()[j]), st.append(rst.tolist()[j]), sz.append(
                    rsz.tolist()[j])

        # Plot sx
        ax.scatter(dist, sr, alpha=0.7, label=str(time) + ' Gyr')

        # Plot sy
        ax2.scatter(dist, st, alpha=0.7, label=str(time) + ' Gyr')

        # Plot sz
        ax3.scatter(dist, sz, alpha=0.7, label=str(time) + ' Gyr')

    # Titles and legends
    ax.set_xlabel(xlabel), ax2.set_xlabel(xlabel), ax3.set_xlabel(xlabel)
    ax.set_ylabel("$\sigma_r$ [km/s]"), ax2.set_ylabel("$\sigma_t$ [km/s]"), ax3.set_ylabel("$\sigma_z$ [km/s]")
    ax.set_title(title), ax2.set_title(title), ax3.set_title(title)
    ax.legend(), ax2.legend(), ax3.legend()
    fig.tight_layout(), fig2.tight_layout(), fig3.tight_layout()

    # Save figures
    fig.savefig(str(galaxy_name) + "-" + content + "_velocity-dispersion_r.png", dpi=500)
    fig2.savefig(str(galaxy_name) + "-" + content + "_velocity-dispersion_t.png", dpi=500)
    fig3.savefig(str(galaxy_name) + "-" + content + "_velocity-dispersion_z.png", dpi=500)


for time in time_list:
    velocity_dispersion(galaxy_name, content, time, xlabel, ylabel)

for time in time_list:
    velocity_dispersion_time(content, xlabel)



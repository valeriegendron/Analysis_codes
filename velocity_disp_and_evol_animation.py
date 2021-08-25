print('Importing')
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
mpl.rcParams['animation.ffmpeg_path'] = r'/home/vagen16/ffmpeg/ffmpeg'
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import ffmpeg

# Parameters
galaxy_name = 'Af_v1'


def velocity_dispersion(galaxy_name, content, time):
    """Computes the velocity dispersion (sigma_r, sigma_t and sigma_z) at a given time"""
    # Read file
    fileName = galaxy_name + '/data_sigma/sigma_v' + content + 'c.out'
    # times, distance from center, velocity dispersion in x, y and z
    rtimes, rdist, rsr, rst, rsz = np.loadtxt(fileName, usecols=(0, 1, 5, 6, 7), unpack=True)

    dist, sr, st, sz = [], [], [], []  # lists that will contain only the data at the time specified
    for i in range(0, len(rtimes)):
        if rtimes[i] == time:
            dist.append(rdist.tolist()[i]), sr.append(rsr.tolist()[i]), st.append(rst.tolist()[i]), sz.append(rsz.tolist()[i])

    if content == 'g':
        title = 'Run ' + galaxy_name + ', gas particles'
    elif content == 's':
        title = 'Star particles'

    # Combining data to put into frame for animation
    data_y = sr + st + sz
    data_x = dist*3
    colors = np.array(['tab:red', 'g', 'mediumblue'])
    labels = np.array(['$\sigma_r$', '$\sigma_t$', '$\sigma_z$'])
    sr_cat, st_cat, sz_cat = [0]*len(sr), [1]*len(st), [2]*len(sz)
    categories = np.array(sr_cat + st_cat + sz_cat)
    if content == 'g':
        frame = ax1.scatter(data_x, data_y, c=colors[categories], alpha=0.7, s=1, label=labels[categories])
        ax1.set_title(title)
    if content == 's':
        frame = ax3.scatter(data_x, data_y, c=colors[categories], alpha=0.7, s=1, label=labels[categories])
        ax3.set_title(title)

    time_label = ax2.text(x=0.90, y=0.97, ha='center', va='center', transform=ax2.transAxes,
                          s=str(time) + " [Gyr]", bbox=dict(facecolor='w', edgecolor='k'))

    return frame, time_label


def run_evolution(galaxy_name, time, plan):
    # 0->x, 1->y, 2->z.
    if plan == 'xy':
        columns = (0, 1)
    elif plan == 'xz':
        columns = (0, 2)
    elif plan == 'yz':
        columns = (1, 2)

    dumps, times = np.loadtxt(str(galaxy_name) + "/tzstep.dat", skiprows=1, usecols=(0, 1), unpack=True)
    dumps, times = dumps.tolist(), times.tolist()

    dump = str(int(dumps[times.index(time)]))  # dump corresponding to time entered
    while len(dump) != 3:
        dump = "0" + dump

    # Initialization for data reading
    liste_xdata = ['gx_1', 'gx_2', 'sx_1', 'sx_2']
    liste_ydata = ['gy_1', 'gy_2', 'sy_1', 'sy_2']

    print("Reading and animating dump " + dump + " ...")
    for fileName in os.listdir(str(galaxy_name)):
        # Gas
        if fileName.startswith("g00"):
            # Galaxy 1
            if fileName.endswith(dump + "_1"):
                gx_1, gy_1 = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=columns, unpack=True)
            # Galaxy 2
            elif fileName.endswith(dump + "_2"):
                gx_2, gy_2 = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=columns, unpack=True)
            else:
                continue

        # Stars
        elif fileName.startswith("s00"):
            if dump == "000":
                # No stars at t=0
                sx_1, sy_1, sx_2, sy_2 = [0], [0], [0], [0]
            else:
                # Galaxy 1
                if fileName.endswith(dump + "_1"):
                    sx_1, sy_1 = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=columns, unpack=True)
                # Galaxy 2
                elif fileName.endswith(dump + "_2"):
                    sx_2, sy_2 = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=columns, unpack=True)
                else:
                    continue

    # Set to real unit
    for i in range(0, len(liste_xdata)):  # pour parcourir tous les sets de donnees
        for j in range(0, len(locals()[liste_xdata[i]])):  # pour parcourir toutes les donnees d'un fichier
            locals()[liste_xdata[i]][j] = locals()[liste_xdata[i]][j] * 100  # conversion en kpc
        for k in range(0, len(locals()[liste_ydata[i]])):
            locals()[liste_ydata[i]][k] = locals()[liste_ydata[i]][k] * 100  # conversion en kpc

    # Animation
    if plan == 'xy':
        if dump == "000":
            # No stars at t=0
            data_x = gx_1.tolist() + gx_2.tolist()
            data_y = gy_1.tolist() + gy_2.tolist()
            colors = np.array(['tab:red', 'tab:cyan'])
            g_1_cat, g_2_cat = [0] * len(gx_1), [1] * len(gx_2)
            categories = np.array(g_1_cat + g_2_cat)
            frame = ax4.scatter(data_x, data_y, c=colors[categories], alpha=0.2, s=0.05)
        else:
            data_x = gx_1.tolist() + sx_1.tolist() + gx_2.tolist() + sx_2.tolist()
            data_y = gy_1.tolist() + sy_1.tolist() + gy_2.tolist() + sy_2.tolist()
            colors = np.array(['tab:red', 'y', 'tab:cyan', 'blue'])
            g_1_cat, s_1_cat, g_2_cat, s_2_cat = [0] * len(gx_1), [1] * len(sx_1), [2] * len(gx_2), [3] * len(sx_2)
            categories = np.array(g_1_cat + s_1_cat + g_2_cat + s_2_cat)
            frame = ax4.scatter(data_x, data_y, c=colors[categories], alpha=0.2, s=0.05)

    elif plan == 'xz':
        if dump == "000":
            # No stars at t=0
            data_x = gx_1.tolist() + gx_2.tolist()
            data_y = gy_1.tolist() + gy_2.tolist()
            colors = np.array(['tab:red', 'tab:cyan'])
            g_1_cat, g_2_cat = [0] * len(gx_1), [1] * len(gx_2)
            categories = np.array(g_1_cat + g_2_cat)
            frame = ax2.scatter(data_x, data_y, c=colors[categories], alpha=0.2, s=0.05)
        else:
            data_x = gx_1.tolist() + sx_1.tolist() + gx_2.tolist() + sx_2.tolist()
            data_y = gy_1.tolist() + sy_1.tolist() + gy_2.tolist() + sy_2.tolist()
            colors = np.array(['tab:red', 'y', 'tab:cyan', 'blue'])
            g_1_cat, s_1_cat, g_2_cat, s_2_cat = [0] * len(gx_1), [1] * len(sx_1), [2] * len(gx_2), [3] * len(sx_2)
            categories = np.array(g_1_cat + s_1_cat + g_2_cat + s_2_cat)
            frame = ax2.scatter(data_x, data_y, c=colors[categories], alpha=0.2, s=0.05)

    return frame


# Figure setup
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
ax1.set_ylabel("Velocity dispersion [km/s]")
ax3.set_xlabel("Distance from center of mass [kpc]")
ax3.set_ylabel("Velocity dispersion [km/s]")
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
ax2.set_ylabel("y [kpc]")
ax4.yaxis.tick_right()
ax4.yaxis.set_label_position("right")
ax4.set_xlabel("x [kpc]")
ax4.set_ylabel("z [kpc]")
ax2.set_xlim(-150, 150)
ax2.set_ylim(-150, 150)
ax4.set_xlim(-150, 150)
ax4.set_ylim(-150, 150)
ax2.set_aspect(1)
ax4.set_aspect(1)

# ANIMATION
frames = []  # Initialization
time_list = np.loadtxt(galaxy_name + "/data_sigma/tzstep.dat", skiprows=1, usecols=1, unpack=True)

for time in time_list:
    print("Animating for time t=" + str(time) + " Gyr...")
    frame1 = velocity_dispersion(galaxy_name, 'g', time)[0]
    frame2, time_label = velocity_dispersion(galaxy_name, 's', time)
    frame3 = run_evolution(galaxy_name, time, 'xz')
    frame4 = run_evolution(galaxy_name, time, 'xy')
    frames.append([frame1, frame2, frame3, frame4, time_label])


# Save animation
print("Saving...")
ani = animation.ArtistAnimation(fig, frames, interval=500, blit=True, repeat=False)
writervideo = animation.FFMpegWriter(fps=5)
ani.save(galaxy_name + "_all_velocity-dispersion_anim.mp4", writer=writervideo)


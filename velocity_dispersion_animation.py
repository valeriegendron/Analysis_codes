print('Importing')
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
mpl.rcParams['animation.ffmpeg_path'] = r'/home/vagen16/ffmpeg/ffmpeg'
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ffmpeg

# Parameters
galaxy_name = 'Af_v1'
content = 'g'  # 'g' for gas particles and 's' for star particles
fileName = galaxy_name + '/data_target/sigma_v' + content + 'c.out'
xlabel = 'Distance from center of mass [kpc]'
ylabel = 'Velocity dispersion [km/s]'
ylim = 200


def velocity_dispersion(galaxy_name, content, time):
    """Computes the velocity dispersion (sigma_r, sigma_t and sigma_z) at a given time"""
    # Read file
    # times, distance from center, velocity dispersion in x, y and z
    rtimes, rdist, rsr, rst, rsz = np.loadtxt(fileName, usecols=(0, 1, 5, 6, 7), unpack=True)

    dist, sr, st, sz = [], [], [], []  # lists that will contain only the data at the time specified
    for i in range(0, len(rtimes)):
        if rtimes[i] == time:
            dist.append(rdist.tolist()[i]), sr.append(rsr.tolist()[i]), st.append(rst.tolist()[i]), sz.append(rsz.tolist()[i])

    if content == 'g':
        title = 'Gas particles of run ' + galaxy_name
    elif content == 's':
        title = 'Star particles of run ' + galaxy_name

    # Combining data to put into frame for animation
    data_y = sr + st + sz
    data_x = dist*3
    colors = np.array(['tab:red', 'g', 'mediumblue'])
    labels = np.array(['$\sigma_r$', '$\sigma_t$', '$\sigma_z$'])
    sr_cat, st_cat, sz_cat = [0]*len(sr), [1]*len(st), [2]*len(sz)
    categories = np.array(sr_cat + st_cat + sz_cat)
    frame = plt.scatter(data_x, data_y, c=colors[categories], alpha=0.7, label=labels[categories])
    time_label = plt.text(x=0.90, y=0.97, ha='center', va='center', transform=ax.transAxes,
                          s=str(time) + " [Gyr]", bbox=dict(facecolor='w', edgecolor='k'))

    return frame, time_label, title


# Figure setting
fig = plt.figure()
ax = fig.add_subplot(111)
# ax.set_ylim(0, ylim)
plt.xlabel(xlabel)
plt.ylabel(ylabel)

# ANIMATION
frames = []  # Initialization
time_list = np.loadtxt(galaxy_name + "/data_target/tzstep.dat", skiprows=1, usecols=1, unpack=True)

for time in time_list:
    print("Animating for time t=" + str(time) + " Gyr...")
    frame, time_label, title = velocity_dispersion(galaxy_name, content, time)
    frames.append([frame, time_label])
plt.title(title)

# Save animation
print("Saving...")
ani = animation.ArtistAnimation(fig, frames, interval=500, blit=True, repeat=False)
writervideo = animation.FFMpegWriter(fps=5)
ani.save(galaxy_name + "-" + content + "_velocity-dispersion_anim.mp4", writer=writervideo)

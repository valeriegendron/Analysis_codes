print('Importing')
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
mpl.rcParams['animation.ffmpeg_path'] = r'/home/vagen16/ffmpeg/ffmpeg'
mpl.rcParams['lines.markersize'] = 0.2  # size of scatter markers
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ffmpeg
import os

# Parameters
galaxy_name = 'Af_v1'
plan = 'xz'  # xy, xz or yz
pic_name = str(galaxy_name) + "-all_" + plan + "_anim.mp4"
lim = 400  # max extent of axi in kpc

# 0->x, 1->y, 2->z.
if plan == 'xy':
    columns = (0, 1)
elif plan == 'xz':
    columns = (0, 2)
elif plan == 'yz':
    columns = (1, 2)

# Figure setting
fig = plt.figure()
ax = fig.add_subplot(111)
plt.gca().set_aspect(1)
plt.title("Run " + str(galaxy_name) + " evolution")
plt.xlabel('Radius [kpc]')
plt.ylabel('Radius [kpc]')
plt.xlim(-lim, lim)
plt.ylim(-lim, lim)
t = 0.2  # transparency

print("Reading")
# Lists containing dump number and corresponding time
dumps, time = np.loadtxt(str(galaxy_name)+"/tzstep.dat", skiprows=1, usecols=(0, 1), unpack=True)
str_dumps = []  # list containing dumps number in string format
for i in range(0, len(dumps)):
    str_dumps.append("00"+str(int(dumps[i])))

# Initialization for data reading
liste_xdata = ['dx_1', 'dx_2', 'gx_1', 'gx_2', 'sx_1', 'sx_2']
liste_ydata = ['dy_1', 'dy_2', 'gy_1', 'gy_2', 'sy_1', 'sy_2']
frames = []
for index in range(0, len(dumps)):
    print("Reading and animating dump " + str(int(dumps[index])) + " ...")
    for fileName in os.listdir(str(galaxy_name)):
        # Dark matter
        if fileName.startswith("d00"):
            # Galaxy 1
            if fileName.endswith(str_dumps[index]+"_1"):
                dx_1, dy_1 = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=columns, unpack=True)
            # Galaxy 2
            elif fileName.endswith(str_dumps[index]+"_2"):
                dx_2, dy_2 = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=columns, unpack=True)
            else:
                continue

        # Gas
        if fileName.startswith("g00"):
            # Galaxy 1
            if fileName.endswith(str_dumps[index]+"_1"):
                gx_1, gy_1 = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=columns, unpack=True)
            # Galaxy 2
            elif fileName.endswith(str_dumps[index]+"_2"):
                gx_2, gy_2 = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=columns, unpack=True)
            else:
                continue

        # Stars
        elif fileName.startswith("s00"):
            if dumps[index] == 0:
                # No stars at t=0
                sx_1, sy_1, sx_2, sy_2 = [0], [0], [0], [0]
            else:
                # Galaxy 1
                if fileName.endswith(str_dumps[index]+"_1"):
                    sx_1, sy_1 = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=columns, unpack=True)
                # Galaxy 2
                elif fileName.endswith(str_dumps[index]+"_2"):
                    sx_2, sy_2 = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=columns, unpack=True)
                else:
                    continue

    # Set to real unit
    for i in range(0, len(liste_xdata)):  # pour parcourir tous les sets de donnees
        for j in range(0, len(globals()[liste_xdata[i]])):  # pour parcourir toutes les donnees d'un fichier
            globals()[liste_xdata[i]][j] = globals()[liste_xdata[i]][j]*100  # conversion en kpc
        for k in range(0, len(globals()[liste_ydata[i]])):
            globals()[liste_ydata[i]][k] = globals()[liste_ydata[i]][k]*100  # conversion en kpc

    # Animation
    if int(dumps[index]) == 0:
        # No stars at t=0
        data_x = dx_1.tolist() + gx_1.tolist() + dx_2.tolist() + gx_2.tolist()
        data_y = dy_1.tolist() + gy_1.tolist() + dy_2.tolist() + gy_2.tolist()
        colors = np.array(['k', 'tab:red', 'grey', 'tab:cyan'])
        d_1_cat, g_1_cat, d_2_cat, g_2_cat = [0]*len(dx_1), [1]*len(gx_1), [2]*len(dx_2), [3]*len(gx_2)
        categories = np.array(d_1_cat + g_1_cat + d_2_cat + g_2_cat)
        frame = plt.scatter(data_x, data_y, c=colors[categories], alpha=t)

    else:
        data_x = dx_1.tolist() + gx_1.tolist() + sx_1.tolist() + dx_2.tolist() + gx_2.tolist() + sx_2.tolist()
        data_y = dy_1.tolist() + gy_1.tolist() + sy_1.tolist() + dy_2.tolist() + gy_2.tolist() + sy_2.tolist()
        colors = np.array(['k', 'tab:red', 'y', 'grey', 'tab:cyan', 'blue'])
        d_1_cat, g_1_cat, s_1_cat, d_2_cat, g_2_cat, s_2_cat = [0]*len(dx_1), [1]*len(gx_1), [2]*len(sx_1), [3]*len(dx_2), [4]*len(gx_2), [5]*len(sx_2)
        categories = np.array(d_1_cat + g_1_cat + s_1_cat + d_2_cat + g_2_cat + s_2_cat)
        frame = plt.scatter(data_x, data_y, c=colors[categories], alpha=t)

    time_label = plt.text(x=0.90, y=0.97, ha='center', va='center', transform=ax.transAxes,
                          s=str(time[index])+" [Gyr]", bbox=dict(facecolor='w', edgecolor='k'))
    frames.append([frame, time_label])

# Save animation
print("Saving...")
ani = animation.ArtistAnimation(fig, frames, interval=500, blit=True, repeat=False)
writervideo = animation.FFMpegWriter(fps=5)
ani.save(pic_name, writer=writervideo)

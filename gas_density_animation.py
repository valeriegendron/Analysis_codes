# This script creates a 2D animation of the evolution of a galaxy for given time steps.
# I discovered during the semester that Funcanimation is more efficient than Artistanimation
# for a large amount of data frames so feel free to modify this script as it pleases you.
# Author: Jérémi Lesage (winter 2021)
# Modified by Valérie Gendron (summer 2021)

import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ffmpeg

name = 'I_h'
if name == 'I':
    file1 = "I/g000000"
    file2 = "I/g000061"
    file3 = "I/g000129"
    file4 = "I/g000178"
    file5 = "I/g000203"
    file6 = "I/g000256"
    v_min, v_max = 1E5, 2E6
elif name == 'I_h':
    file1 = "I_h/data_centered/g000000"
    file2 = "I_h/data_centered/g000058"
    file3 = "I_h/data_centered/g000112"
    file4 = "I_h/data_centered/g000164"
    file5 = "I_h/data_centered/g000222"
    file6 = "I_h/data_centered/g000297"
    v_min, v_max = 1E5, 4E6
elif name == 'I_hh':
    file1 = "I_hh/g000000"
    file2 = "I_hh/g000141"
    file3 = "I_hh/g000222"
    file4 = "I_hh/g000283"
    file5 = "I_hh/g000338"
    file6 = "I_hh/g000437"
    v_min, v_max = 1E5, 8E6
columns = [0, 1]  # columns to plot
nbins = [150, 150]  # number of bins in each direciton
xcut = 0.05  # max extent for axis in 100s of kpc
ycut = 0.05
zcut = 0.05


x1_in, y1_in = np.loadtxt(file1, usecols=columns, unpack=True)
x2_in, y2_in = np.loadtxt(file2, usecols=columns, unpack=True)
x3_in, y3_in = np.loadtxt(file3, usecols=columns, unpack=True)
x4_in, y4_in = np.loadtxt(file4, usecols=columns, unpack=True)
x5_in, y5_in = np.loadtxt(file5, usecols=columns, unpack=True)
x6_in, y6_in = np.loadtxt(file6, usecols=columns, unpack=True)


data_ok = (x1_in < xcut + 0.05) & (x1_in > -xcut - 0.05) & (y1_in < ycut + 0.05) & (y1_in > -ycut - 0.05)
x1_in = x1_in[data_ok] * 100
y1_in = y1_in[data_ok] * 100

data_ok = (x2_in < xcut + 0.05) & (x2_in > -xcut - 0.05) & (y2_in < ycut + 0.05) & (y2_in > -ycut - 0.05)
x2_in = x2_in[data_ok] * 100
y2_in = y2_in[data_ok] * 100

data_ok = (x3_in < xcut + 0.05) & (x3_in > -xcut - 0.05) & (y3_in < ycut + 0.05) & (y3_in > -ycut - 0.05)
x3_in = x3_in[data_ok] * 100
y3_in = y3_in[data_ok] * 100

data_ok = (x4_in < xcut + 0.05) & (x4_in > -xcut - 0.05) & (y4_in < ycut + 0.05) & (y4_in > -ycut - 0.05)
x4_in = x4_in[data_ok] * 100
y4_in = y4_in[data_ok] * 100

data_ok = (x5_in < xcut + 0.05) & (x5_in > -xcut - 0.05) & (y5_in < ycut + 0.05) & (y5_in > -ycut - 0.05)
x5_in = x5_in[data_ok] * 100
y5_in = y5_in[data_ok] * 100

data_ok = (x6_in < xcut + 0.05) & (x6_in > -xcut - 0.05) & (y6_in < ycut + 0.05) & (y6_in > -ycut - 0.05)
x6_in = x6_in[data_ok] * 100
y6_in = y6_in[data_ok] * 100


heatmap1, yedges1, xedges1 = np.histogram2d(y=x1_in, x=y1_in, bins=nbins)
heatmap2, yedges2, xedges2 = np.histogram2d(y=x2_in, x=y2_in, bins=nbins)
heatmap3, yedges3, xedges3 = np.histogram2d(y=x3_in, x=y3_in, bins=nbins)
heatmap4, yedges4, xedges4 = np.histogram2d(y=x4_in, x=y4_in, bins=nbins)
heatmap5, yedges5, xedges5 = np.histogram2d(y=x5_in, x=y5_in, bins=nbins)
heatmap6, yedges6, xedges6 = np.histogram2d(y=x6_in, x=y6_in, bins=nbins)


heatmaps = [heatmap1, heatmap2, heatmap3, heatmap4, heatmap5, heatmap6]
xedges = [xedges1, xedges2, xedges3, xedges4, xedges5, xedges6]
yedges = [yedges1, yedges2, yedges3, yedges4, yedges5, yedges6]
tsteps = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
frames = []
fig = plt.figure()
ax = fig.add_subplot(111)
plt.gca().set_aspect(1)
plt.title(f'Galaxy {name} gas density animation')
plt.xlabel('Radius [kpc]')
plt.ylabel('Radius [kpc]')
plt.xlim(-10, 10)
plt.ylim(-10, 10)
for i in range(0, len(tsteps)):
    frame = plt.pcolormesh(xedges[i], yedges[i], heatmaps[i]*112674, vmin=v_min, vmax=v_max, norm=mpl.colors.LogNorm())
    print(frame)
    time_label = plt.text(x=0.90, y=0.97, ha='center', va='center', transform=ax.transAxes,
                          s=f'{tsteps[i]} [Gyr]', bbox=dict(facecolor='w', edgecolor='k'))
    frames.append([frame, time_label])
cbar = plt.colorbar(orientation='vertical', label='Density [$M_\odot / pc^2$]')
ani = animation.ArtistAnimation(fig, frames, interval=500, blit=True, repeat=True)
writervideo = animation.FFMpegWriter()
#ani.save(f'{name}-anim.mp4', writer=writervideo)
plt.show()

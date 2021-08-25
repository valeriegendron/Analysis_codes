#####
# Parameters
plan = 'xy'  # Modify if needed
dim = 20  # Dimension of map in kpc. Modify if needed
time = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
fileName = "s000000"  # the file to read in
fileName2 = "s000061"  # the file to read in
fileName3 = "s000129"  # the file to read in
fileName4 = "s000178"  # the file to read in
fileName5 = "s000203"  # the file to read in
fileName6 = "s000256"  # the file to read in

v_min = 1E5
if plan == 'xy' and dim == 20:
    columns = (0, 1)  # List of the columns to plot. 0=1st column, 1=2nd column, etc
    pic_name = "I_smap-20kpc.png"  # set the name of the file to whatever you want
    xcut, ycut = 0.2, 0.2  # max extent for x and y axi in 100s of kpc
    lim = 20  # limit of figure axi in kpc
    v_max = 5E6
elif plan == 'xy' and dim == 5:
    columns = (0, 1)
    pic_name = "I_smap.png"
    xcut, ycut = 0.05, 0.05
    lim = 5
    v_max = 2E6
elif plan == 'xz' and dim == 5:
    columns = (0, 2)
    pic_name = "I_smap_xz.png"
    xcut, ycut = 0.05, 0.05
    lim = 5
    v_max = 2E7
elif plan == 'yz' and dim == 5:
    columns = (1, 2)
    pic_name = "I_smap_yz.png"
    xcut, ycut = 0.05, 0.05
    lim = 5
    v_max = 2E7

nbins = [150, 150]  # number of "bins" in each direciton
xlabel = "rayon [kpc]"  # labels for axes
ylabel = "rayon [kpc]"
cbarlabel = "density [M$_\odot / pc^2$]"
title = "Galaxy I star density"  # title of graph
logColour = True  # True or False - should I log the colour-scale?
######

print("Importing")

# Import libraries to do our magic
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


# Read in the data - because Python is magical, this is all done in one line
print("Reading")
x_in, y_in = np.loadtxt(fileName, usecols=columns, unpack=True)
x2_in, y2_in = np.loadtxt(fileName2, usecols=columns, unpack=True)
x3_in, y3_in = np.loadtxt(fileName3, usecols=columns, unpack=True)
x4_in, y4_in = np.loadtxt(fileName4, usecols=columns, unpack=True)
x5_in, y5_in = np.loadtxt(fileName5, usecols=columns, unpack=True)
x6_in, y6_in = np.loadtxt(fileName6, usecols=columns, unpack=True)


# Set to real unit

data_ok = (x_in<xcut+0.05) & (x_in>-xcut-0.05) & (y_in<ycut+0.05) & (y_in>-ycut-0.05)
x_in = x_in[data_ok]*100
y_in = y_in[data_ok]*100

data_ok = (x2_in<xcut+0.05) & (x2_in>-xcut-0.05) & (y2_in<ycut+0.05) & (y2_in>-ycut-0.05)
x2_in = x2_in[data_ok]*100
y2_in = y2_in[data_ok]*100

data_ok = (x3_in<xcut+0.05) & (x3_in>-xcut-0.05) & (y3_in<ycut+0.05) & (y3_in>-ycut-0.05)
x3_in = x3_in[data_ok]*100
y3_in = y3_in[data_ok]*100

data_ok = (x4_in<xcut+0.05) & (x4_in>-xcut-0.05) & (y4_in<ycut+0.05) & (y4_in>-ycut-0.05)
x4_in = x4_in[data_ok]*100
y4_in = y4_in[data_ok]*100

data_ok = (x5_in<xcut+0.05) & (x5_in>-xcut-0.05) & (y5_in<ycut+0.05) & (y5_in>-ycut-0.05)
x5_in = x5_in[data_ok]*100
y5_in = y5_in[data_ok]*100

data_ok = (x6_in<xcut+0.05) & (x6_in>-xcut-0.05) & (y6_in<ycut+0.05) & (y6_in>-ycut-0.05)
x6_in = x6_in[data_ok]*100
y6_in = y6_in[data_ok]*100


# Bin the data - because Python is magical, this is all done in one line
print("Binning")
heatmap, yedges, xedges = np.histogram2d(y=x_in, x=y_in,bins=nbins)
heatmap2, yedges2, xedges2 = np.histogram2d(y=x2_in, x=y2_in,bins=nbins)
heatmap3, yedges3, xedges3 = np.histogram2d(y=x3_in, x=y3_in,bins=nbins)
heatmap4, yedges4, xedges4 = np.histogram2d(y=x4_in, x=y4_in,bins=nbins)
heatmap5, yedges5, xedges5 = np.histogram2d(y=x5_in, x=y5_in,bins=nbins)
heatmap6, yedges6, xedges6 = np.histogram2d(y=x6_in, x=y6_in,bins=nbins)

# Plot the data! Okay, this takes a few lines, but only because we're setting up the axes etc
print("Plotting")
plt.clf()  # clear the frame


mpl.rcParams.update({'font.size': 8})


fig = plt.figure(figsize=(8, 11), dpi=500)


fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex='col', sharey='row', figsize=(6,8))


im=ax1.pcolormesh(xedges,yedges, heatmap*112674, vmin=v_min, vmax=v_max, norm=mpl.colors.LogNorm(), cmap=plt.cm.get_cmap('viridis'))
ax1.set_ylim(-lim, lim)
ax1.set_xlim(-lim, lim)
ax1.set_aspect(1)
#ax1.text(15, 1.4, 't=0')


ax2.pcolormesh(xedges2,yedges2, heatmap2*112674 , vmin=v_min, vmax=v_max, norm=mpl.colors.LogNorm(), cmap=plt.cm.get_cmap('viridis'))
ax2.set_ylim(-lim, lim)
ax2.set_xlim(-lim, lim)
#ax2.text(15, 1.4, 'D')
ax2.set_aspect(1)

ax3.pcolormesh(xedges3,yedges3, heatmap3*112674, vmin=v_min, vmax=v_max, norm=mpl.colors.LogNorm(), cmap=plt.cm.get_cmap('viridis'))
ax3.set_ylim(-lim, lim)
ax3.set_xlim(-lim, lim)
#ax3.text(15, 1.4, 't=0.5')
ax3.set_aspect(1)

ax4.pcolormesh(xedges4,yedges4, heatmap4*112674, vmin=v_min, vmax=v_max, norm=mpl.colors.LogNorm(), cmap=plt.cm.get_cmap('viridis'))
ax4.set_ylim(-lim, lim)
ax4.set_xlim(-lim, lim)
#ax4.text(15, 1.4, 'H')
ax4.set_aspect(1)

ax5.pcolormesh(xedges5,yedges5, heatmap5*112674, vmin=v_min, vmax=v_max, norm=mpl.colors.LogNorm(), cmap=plt.cm.get_cmap('viridis'))
ax5.set_ylim(-lim, lim)
ax5.set_xlim(-lim, lim)
#ax5.text(15, 1.4, 't=1')
ax5.set_aspect(1)

ax6.pcolormesh(xedges6,yedges6, heatmap6*112674, vmin=v_min, vmax=v_max, norm=mpl.colors.LogNorm(), cmap=plt.cm.get_cmap('viridis'))
ax6.set_ylim(-lim, lim)
ax6.set_xlim(-lim, lim)
#ax6.text(15, 1.4, 'J')
ax6.set_aspect(1)
#set label

ax1.set_ylabel(ylabel)
ax3.set_ylabel(ylabel)
ax5.set_ylabel(ylabel)
ax5.set_xlabel(xlabel)
ax6.set_xlabel(xlabel)
ax1.set_title(title+', '+str(time[0])+' Gyr')
ax2.set_title(str(time[1])+' Gyr')
ax3.set_title(str(time[2])+' Gyr')
ax4.set_title(str(time[3])+' Gyr')
ax5.set_title(str(time[4])+' Gyr')
ax6.set_title(str(time[5])+' Gyr')

fig.tight_layout()

# Colorbar
fig.subplots_adjust(right=0.87)
cbar_ax = fig.add_axes([0.90, 0.15, 0.01, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label(cbarlabel, rotation=270)


# save the figure to a png file
plt.savefig(pic_name, dpi=500)  # dpi sets the size of the image. higher dpi = bigger image
# plt.show()

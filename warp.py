#####
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

# Parameters
galaxy_name = 'Af_v1'
content = 's'  # 'g' for gas or 's' for stars
time = 3.0  # in Gyr
if content == 'g':
    fileName = 'g000564r_5-6_warp.out'
    fileName2 = 'g000564r_10-11_warp.out'
    title = "Gas particles of run " + str(galaxy_name) + ", t=" + str(time) + " Gyr"
elif content == 's':
    fileName = 's000564r_5-6_warp.out'
    fileName2 = 's000564r_10-11_warp.out'
    title = "Star particles of run " + str(galaxy_name) + ", t=" + str(time) + " Gyr"

# Read data
phase1, mean1 = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=(0, 1), unpack=True)
phase2, mean2 = np.loadtxt(str(galaxy_name) + "/" + fileName2, usecols=(0, 1), unpack=True)

# Plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(phase1, mean1, color='g', label='between 5 and 6 kpc')
ax.scatter(phase2, mean2, color='k', label='between 10 and 11 kpc')
ax.set_ylabel("z$_{mean}$ [kpc]")
ax.set_xlabel("Phase [rad]")
ax.set_title(title)
ax.legend()
fig.tight_layout()

# Save
plt.savefig(str(galaxy_name) + "-" + content + "_" + str(time) + "_Gyr_warp.png", dpi=500)

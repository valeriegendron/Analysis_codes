import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os

# Parameters
galaxy_name = 'Af_v1'
picName = str(galaxy_name) + "-sfr_system.png"

print("Reading")
# Lists containing dump number and corresponding time
dumps, time = np.loadtxt(str(galaxy_name)+"/tzstep.dat", skiprows=1, usecols=(0, 1), unpack=True)
str_dumps = []  # list containing dumps number in string format
for i in range(0, len(dumps)):
    str_dumps.append("00"+str(int(dumps[i])))

total_smass = [0]  # will contain the total star mass for each time step
for index in range(1, len(dumps)):  # skipping the first dump (no stars)
    print("Reading dump " + str(int(dumps[index])) + " ...")
    for fileName in os.listdir(str(galaxy_name)):
        if fileName.startswith("s00"):
            if fileName.endswith(str_dumps[index]):
                smass = 0
                smass_list = np.loadtxt(str(galaxy_name) + "/" + fileName, usecols=6, unpack=True)
                for i in range(0, len(smass_list)):
                    smass += smass_list[i]

                total_smass.append(smass)
        else:
            continue

print("Computing")
sfr = []  # will contain sfr in M_sun/yr at each time step
for i in range(1, len(total_smass)):  # skipping first dump
    mass_var = total_smass[i] - total_smass[i-1]  # in 10^12 M_sun units
    sfr.append((mass_var*10**(12))/(0.02*10**9))  # to get sfr in M_sun/yr and NOT (10^12 M_sun)/(0.02 Gyr)

print("Plotting")
time = time.tolist()
del time[0]  # remove time 0 from list

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(time, sfr, color='blue')
ax.set_xlabel("Time [Gyr]")
ax.set_ylabel("SFR [M$_\odot$/yr]")
ax.set_title("SFR for whole system, run " + str(galaxy_name))
fig.tight_layout()

print('Saving')
plt.savefig(picName, dpi=500)

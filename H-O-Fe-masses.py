# Author: Jérémi Lesage (winter 2021)
# Modified by Valérie Gendron (summer 2021)
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Parametres
galaxy_name = 'im_hh'
file_choice = 'f'  # f: radius = 1kpc (fibre), g: radius = 10 kpc (global), h: 2kpc slice (height)
if file_choice == 'f':
    constant = '1 kpc radius'
elif file_choice == 'g':
    constant = '10 kpc radius'
elif file_choice == 'h':
    constant = '2 kpc slice'
file_fibre = f"{galaxy_name}/Z_f.out"  # radius = 1 kpc
# file_global = f"{galaxy_name}/Z_g.out"  # radius = 10 kpc
# file_height = f"{galaxy_name}/Z_h"  # 2kpc slice
columns = (0, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22)

# Lecture des donnees
time, H_in, H_out, H_SF, H_SN, H_var, O_in, O_out, O_SF, O_SN, O_var, O_H, Fe_in, Fe_out, Fe_SF, Fe_SN, Fe_var, Fe_H = \
    np.loadtxt(f"{galaxy_name}/Z_{file_choice}.out", usecols=columns, unpack=True)

# GRAPHIQUES
# Masses de H, de O et de Fe selon le temps
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex='all')
ax1.plot(time, H_in, color='#FDE725FF', label='Input mass')
ax1.hlines(y=0.0, xmin=time[0], xmax=time[-1], linestyles='dashed')
ax1.plot(time, H_out, color='#95D840FF', label='Output mass')
ax1.plot(time, H_SF, color='#29AF7FFF', label='Mass consumed in SF')
ax1.plot(time, H_SN, color='#287D8EFF', label='Mass from SN feedback')
ax1.plot(time, H_var, color='#440154FF', label='Total mass variation')
ax1.tick_params(direction='in', right=True, top=True, labelright=False, labeltop=False)
ax1.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
ax1.margins(x=0.0)
ax1.legend(fontsize=8, frameon=True, loc=(1.05, 0.20))
# galaxy_name = 'i_hh'
ax1.set_title(f'Galaxy {galaxy_name} in constant {constant}')
ax1.set_ylabel('H mass [M$_\odot$]')
ax1.set_ylim([-2e8, 2e8])

ax2.hlines(y=0.0, xmin=time[0], xmax=time[-1], linestyles='dashed')
ax2.plot(time, O_in, color='#FDE725FF')
ax2.plot(time, O_out, color='#95D840FF')
ax2.plot(time, O_SF, color='#29AF7FFF')
ax2.plot(time, O_SN, color='#287D8EFF')
ax2.plot(time, O_var, color='#440154FF')
ax2.tick_params(direction='in', right=True, top=True, labelright=False, labeltop=False)
ax2.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
ax2.margins(x=0.0)
ax2.set_ylabel('O mass [M$_\odot$]')
ax2.set_ylim([-1.5e6, 1.5e6])

ax3.hlines(y=0.0, xmin=time[0], xmax=time[-1], linestyles='dashed')
ax3.plot(time, Fe_in, color='#FDE725FF')
ax3.plot(time, Fe_out, color='#95D840FF')
ax3.plot(time, Fe_SF, color='#29AF7FFF')
ax3.plot(time, Fe_SN, color='#287D8EFF')
ax3.plot(time, Fe_var, color='#440154FF')
ax3.tick_params(direction='in', right=True, top=True, labelright=False, labeltop=False)
ax3.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
ax3.margins(x=0.0)
ax3.set_ylabel('Fe mass [M$_\odot$]')
ax3.set_xlabel('Time [Gyr]')
ax3.set_ylim([-1.5e5, 1.5e5])
plt.tight_layout()
# galaxy_name = 'im_hh'
plt.savefig(f'{galaxy_name}-H-O-Fe_masses_{constant}', dpi=500)
plt.show()


# Metallicite en fonction du temps
# fig2, (ax1, ax2) = plt.subplots(2, 1, sharex='all')
# ax1.plot(time, O_H, color='k')
# ax2.plot(time, Fe_H, color='k')
# ax1.set_title(f'Galaxy {galaxy_name} in constant {constant}')
# ax2.set_xlabel('Time [Gyr]')
# ax1.set_ylabel('[O/H]')
# ax2.set_ylabel('[Fe/H]')
# ax1.tick_params(direction='in', right=True, top=True, labelright=False, labeltop=False)
# ax2.tick_params(direction='in', right=True, top=True, labelright=False, labeltop=False)
# ax1.margins(x=0.0)
# ax2.margins(x=0.0)
# plt.tight_layout()
# plt.savefig(f'{galaxy_name}_metallicite_{constant}', dpi=500)
# plt.show()

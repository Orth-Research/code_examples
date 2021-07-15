import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', **{'family':'sans-serif', 'size' : 12})
rc('text', usetex=True)

plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)
plt.rc('axes', labelsize=12)

# define colors
color_red = (0.73, 0.13869999999999993, 0.)
color_orange = (1., 0.6699999999999999, 0.)
color_green = (0.14959999999999996, 0.43999999999999995, 0.12759999999999994)
color_blue = (0.06673600000000002, 0.164512, 0.776)
color_purple = (0.25091600000000003, 0.137378, 0.29800000000000004)
color_ocker = (0.6631400000000001, 0.71, 0.1491)
color_pink = (0.71, 0.1491, 0.44730000000000003)
color_brown = (0.651, 0.33331200000000005, 0.054683999999999955)
color_red2 = (0.766, 0.070, 0.183)
color_turquoise = (0., 0.684, 0.676)
color_yellow = (0.828, 0.688, 0.016)
color_grey = (0.504, 0.457, 0.410)

width = 1.5*3.375
height = width / 1.618

# one could also save them in the example_mp.py program into a parameter file and read them in here (instead of manually setting)
parameter_1 = 1
parameter_2 = 2

h5_file_location = "."
h5_group = "Output"

my_path = f"{h5_file_location}"
my_file = f"{h5_file_location}/output_example.h5"

with h5py.File(my_file, "r") as f:
    observable = [f[f"/{h5_group}/variable_1"][()].T, f[f"/{h5_group}/observable"][()].T]

fig = plt.figure(1,figsize = [width,height])
ax1 = plt.subplot(1,1,1)

ax1.plot(observable[0], observable[1], marker = 'o', markersize = 4, linestyle = '-', linewidth = 1.,  color = color_red, label = '')
ax1.grid(which = 'major', linestyle = ':', linewidth = 1., alpha = 0.4)
ax1.grid(which = 'minor', linestyle = ':', linewidth = 1., alpha = 0.2)
ax1.set_xlabel("variable1 " + r"$x_1$ (units)")
ax1.set_ylabel("observable (units)")
ax1.set_title(f"p1={parameter_1}, p2={parameter_2}")
#ax1.legend(loc = 'best')

plt.tight_layout()

fig.savefig(my_path + "/Plot-observable.png", format='png', dpi = 600, bbox_inches="tight")

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os


matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True
})


pwd = os.getcwd()

save_directory = os.path.join(pwd, 'paper/images/')

def f(x, width):
    return np.exp(- np.square(x)/np.square(width))




x_values = np.arange(-20, 20, 0.1)
axes = [-20, 20, -0.5, 1.5]

plt.figure()
# plt.suptitle('Gauskurve')
plt.axis(axes)
plt.hlines(0, -20, 20, lw=1)
plt.axvline(0, -2, 2, color='k', lw=1)
plt.plot(x_values, f(x_values, 1), label='$\sigma=1$')
plt.plot(x_values, f(x_values, 5), label='$\sigma=5$')
plt.plot(x_values, f(x_values, 10), label='$\sigma=10$')
plt.legend(loc='upper left')
plt.savefig(save_directory+'exponentail.pdf')
plt.show()


import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

'''
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
'''

pwd = os.getcwd()

save_directory = os.path.join(pwd, 'paper/images/')
print(save_directory)


def f(x):
    return x**3-x**2

def e(x):
    return np.exp(-(x-2/3)**2)

x_values = np.arange(-2,3, 0.1)

plt.figure()
plt.suptitle('test')


axes = [-1.5, 2.5, -1, 1.5]

text = 'Example of the influence of the distance function. On the left, the function f(x)=x^3-x^2 is plotted, which has a minimum at $x=\frac{2}/{3}$. The middle figure shows a RBF kernel centered at $\frac{2}{3}. If we add the two functions together in the right plot, we can see that the local minimum is smoothed out by the exponential function. If we move away from the minimum, we can see that the two functions get closer together again.'

plt.subplot(131)
plt.figtext(0.5, 0, text, horizontalalignment='center')
plt.axis(axes)
plt.plot(x_values, f(x_values))

plt.subplot(132)
plt.axis(axes)
plt.yticks([])
plt.plot(x_values, e(x_values))

plt.subplot(133)
plt.axis(axes)
plt.yticks([])
plt.plot(x_values, e(x_values)+f(x_values))
plt.plot(x_values, f(x_values), color='r')


# plt.savefig(save_directory + 'test.pdf', bbox_inches='tight')

plt.show()







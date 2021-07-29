#%%
# MIT License

# Copyright (c) 2020 Hernan Reisin

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from termStructureTreasury import data


def EjemploInterpoladorPoligonal(x,y):
    f = interpolate.interp1d(x, y)
    xForPlot = np.linspace(0.1, 30, num=1001, endpoint=True)    
    plt.figure(1)
    plt.plot(x, y, 'o', linewidth=0, label="data")
    plt.plot(xForPlot, f(xForPlot), '-', label="poligonal")

def EjemploInterpoladorEscalonPrevio(x,y):
    f = interpolate.interp1d(x, y, kind='previous')
    xForPlot = np.linspace(0.1, 30, num=1001, endpoint=True)    
    plt.figure(2)
    plt.plot(x, y, 'o', linewidth=0, label="data")
    plt.plot(xForPlot, f(xForPlot), '-', label="escalon previous")

def EjemploInterpoladorEscalonPosterior(x,y):
    f = interpolate.interp1d(x, y, kind='next')
    xForPlot = np.linspace(0.1, 30, num=1001, endpoint=True)    
    plt.figure(3)
    plt.plot(x, y, 'o', linewidth=0, label="data")
    plt.plot(xForPlot, f(xForPlot), '--', label="escalon next")

def EjemploSplineInterpolator(x, y):
    tck1 = interpolate.splrep(x, y, s=0)
    tck2 = interpolate.splrep(x, y, s=1)
    xForPlot = np.linspace(0, 30, num=1001, endpoint=True)
    yForPlot1 = interpolate.splev(xForPlot, tck1, der=0)
    yForPlot2 = interpolate.splev(xForPlot, tck2, der=0)
    plt.figure(4)
    plt.plot(x, y, 'o', linewidth=0, label="data")
    plt.plot(xForPlot, yForPlot1, '-', label="Spline smoothness=0")
    plt.plot(xForPlot, yForPlot2, '--', label="Spline smoothness=1")
    plt.legend()



def main():
    xdata = data.timeToMaturity
    ydata = data.yieldOnJuly1
    EjemploInterpoladorPoligonal(xdata, ydata)
    EjemploInterpoladorEscalonPrevio(xdata, ydata)
    EjemploInterpoladorEscalonPosterior(xdata, ydata)
    #EjemploSplineInterpolator(xdata, ydata)

if __name__ == "__main__": 
    main()


# %%

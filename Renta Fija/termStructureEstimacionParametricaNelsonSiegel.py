#%%
# # MIT License

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

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from termStructureTreasury import data


def nelsonSiegelEnLaForward(T, b0, b1, b2, t1):
    return b0 + (b1 + b2 * T) * np.exp(-T/t1)


def nelsonSiegelEnElRate(T, b0, b1, b2, t1):
    return b0 + (b1 + b2) * t1/T * (1 - np.exp(-T/t1)) - b2 * np.exp(-T/t1)


def plotNelsonSiegel():
    b0 = 7
    b1 = -4.13
    T = np.linspace(0, 20, num=1001, endpoint=True)
    plt.figure(1)
    plt.plot(T, nelsonSiegelEnLaForward(T, b0, b1, b2=1.5, t1=2), color='black', label='beta2=1.5')
    plt.plot(T, nelsonSiegelEnLaForward(T, b0, b1, b2=0.5, t1=2), color='cyan', label='beta2=0.5')
    plt.plot(T, nelsonSiegelEnLaForward(T, b0, b1, b2=0.0, t1=2), color='red', label='beta2=0.0')
    plt.plot(T, nelsonSiegelEnLaForward(T, b0, b1, b2=-0.5, t1=2), color='blue', label='beta2=-0.5')
    plt.plot(T, nelsonSiegelEnLaForward(T, b0, b1, b2=-2.0, t1=2), color='green', label='beta2=-2.0')
    plt.plot(T, nelsonSiegelEnLaForward(T, b0, b1, b2=-3.0, t1=2), color='orange', label='beta2=-3.0')
    plt.plot(T, nelsonSiegelEnLaForward(T, b0, b1, b2=-4.0, t1=2), color='gray', label='beta2=-4.0')
    plt.legend()


def fitNelsonSiegel():
    xdata = data.timeToMaturity
    ydata = data.yieldOnJuly1
    popt, pcov = curve_fit(nelsonSiegelEnElRate, xdata, ydata)
    [b0, b1, b2, t1] = popt
    print([b0, b1, b2, t1])
    
    T = np.linspace(0, 40, num=1001, endpoint=True)
    plt.figure(2)
    plt.plot(xdata, ydata, color='black', marker="o", linewidth=0,label='Yield US 1.JUL.2019')
    plt.plot(T, nelsonSiegelEnElRate(T, b0, b1, b2, t1), color='cyan', label='Nelson-Siegel Fit')
    plt.legend()
    
    
    
def main():
    plotNelsonSiegel()
    fitNelsonSiegel()
    
    
if __name__ == "__main__": 
    main()
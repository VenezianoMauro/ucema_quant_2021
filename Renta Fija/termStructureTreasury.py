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

import matplotlib.pyplot as plt
import numpy as np


class data:
    timeToMaturity = [30/350, 60/360, 90/360, 180/360, 1, 2, 3, 5, 7, 10, 20, 30]
    yieldOnJuly1 = [2.17, 2.16, 2.21, 2.10, 1.94, 1.78, 1.74, 1.79, 1.90, 2.03, 2.34, 2.55]
    yieldOnJuly2 = [2.21, 2.17, 2.20, 2.09, 1.91, 1.77, 1.71, 1.75, 1.85, 1.98, 2.29, 2.51]
    yieldOnJuly3 = [2.25, 2.20, 2.21, 2.08, 1.91, 1.77, 1.71, 1.74, 1.83, 1.96, 2.25, 2.47]
    yieldOnJuly5 = [2.26, 2.22, 2.23, 2.14, 1.98, 1.87, 1.82, 1.84, 1.93, 2.04, 2.34, 2.54]


def plotTermStructures():
    plt.plot( data.timeToMaturity, data.yieldOnJuly1, marker='.', markersize=10, color='skyblue', linewidth=1, label='1.JUL.2019')
    plt.plot( data.timeToMaturity, data.yieldOnJuly2, marker='v', markersize=5, color='olive', linewidth=1, label='2.JUL.2019')
    plt.plot( data.timeToMaturity, data.yieldOnJuly3, marker='o', markersize=5, color='red', linewidth=1, label='3.JUL.2019')
    plt.plot( data.timeToMaturity, data.yieldOnJuly5, marker='^', markersize=5, color='green', linewidth=1, label='5.JUL.2019')
    plt.legend()
    
def main():  
    plotTermStructures()
    
    
    
    
if __name__ == "__main__": 
    main()
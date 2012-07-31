#!/usr/bin/python
"""
Solve the 2D Shubert function.
"""

from __future__ import division
from DIRECT import solve
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

def obj(x, user_data):
    """Two Dimensional Shubert Function"""
    
    j = np.arange(1, 6)
    
    tmp1 = np.dot(j, np.cos((j+1)*x[0] + j))
    tmp2 = np.dot(j, np.cos((j+1)*x[1] + j))
    
    return tmp1 * tmp2, 0


if __name__ == '__main__':

    l = [-10, -10]
    u = [10, 10]

    x, fmin, ierror = solve(
                        obj,
                        l,
                        u
                        )

    print 'Optimal point:', x
    print 'Optimal value:', fmin
    print 'Exit status:', ierror
    
    #
    # Plot the results.
    #
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    X, Y = np.mgrid[x[0]-2:x[0]+2:50j, x[1]-2:x[1]+2:50j]
    Z = np.zeros_like(X)

    for i in range(X.size):
        Z.ravel()[i] = obj([X.flatten()[i], Y.flatten()[i]], None)[0]
        
    ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet)
    ax.scatter(x[0], x[1], fmin, c='r', marker='o')
    ax.set_title('Two Dimensional Shubert Function')
    plt.show()
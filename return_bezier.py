import numpy as np
import matplotlib.pyplot as plt


def return_bezier(x, y, z):
    cells = 1000

    n_control_points = len(x)

    n = n_control_points - 1
    i = 0
    t = np.linspace(0, 1, cells)

    b = []

    xBezier = np.zeros((1, cells))
    yBezier = np.zeros((1, cells))
    zBezier = np.zeros((1, cells))

    def Ni(n, i):
        return np.math.factorial(n) / (np.math.factorial(i) * np.math.factorial(n-i))

    def basisFunction(n, i, t):
        J = np.array(Ni(n, i) * (t**i) * (1-t) ** (n-i))
        return J

    for k in range(0, n_control_points):
        b.append(basisFunction(n, i, t))

        xBezier = basisFunction(n, i, t) * x[k] + xBezier
        yBezier = basisFunction(n, i, t) * y[k] + yBezier
        zBezier = basisFunction(n, i, t) * z[k] + zBezier

        i += 1

    fig1 = plt.figure(figsize=(4, 4))
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.scatter(x, y, z, c='black')
    ax1.plot(xBezier[0], yBezier[0], zBezier[0], c='blue')
    plt.show()
    return xBezier[0], yBezier[0], zBezier[0]

import numpy as np
import matplotlib.pyplot as plt
import math
import time


def new_bezier(x, y, z, xPreviousBezier, yPreviousBezier, zPreviousBezier, requested_goal, current_pos):

    closest_k = []

    minimum_length = math.sqrt(xPreviousBezier[len(xPreviousBezier)-1]**2 + yPreviousBezier[len(
        yPreviousBezier)-1]**2 + zPreviousBezier[len(zPreviousBezier)-1]**2)

    minimum_j = 0

    # Find relative positions of controls points to previous bezier
    for i in range(0, len(x)):
        current_goal = [x[i], y[i], z[i]]
        minimum_k = 0
        for k in range(0, len(xPreviousBezier)):
            current_length = math.sqrt((xPreviousBezier[k]-current_goal[0])**2 + (
                yPreviousBezier[k]-current_goal[1])**2 + (zPreviousBezier[k]-current_goal[2])**2)
            if current_length <= minimum_length:
                minimum_length = current_length
                minimum_k = k
        closest_k.append(minimum_k)

    # Find closest point to added control point on previous bezier
    for j in range(0, len(xPreviousBezier)):
        current_length = math.sqrt((xPreviousBezier[j]-requested_goal[0])**2 + (
            yPreviousBezier[j]-requested_goal[1])**2 + (zPreviousBezier[j]-requested_goal[2])**2)
        if current_length < minimum_length:
            minimum_length = current_length
            minimum_j = j

    for b in range(0, len(closest_k)):
        if minimum_j < closest_k[b]:
            x.insert(b, requested_goal[0])
            y.insert(b, requested_goal[1])
            z.insert(b, requested_goal[2])

    cells = len(xPreviousBezier)

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

    # for line in b:
    #     plt.plot(t, line)
    # plt.show()

    fig1 = plt.figure(figsize=(4, 4))
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.scatter(x, y, z, c='black')
    ax1.scatter(current_pos[0], current_pos[1], current_pos[2], c='blue')
    ax1.plot(xBezier[0], yBezier[0], zBezier[0], c='red')
    plt.show()
    return xBezier[0], yBezier[0], zBezier[0]

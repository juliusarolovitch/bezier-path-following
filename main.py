# Julius Arolovitch, for CMU Biorobotics MedSnake/HARP
# Bezier curve path following for entered points in R3

from return_bezier import return_bezier
from new_bezier import new_bezier
from calculate_angles import theta_calc, phi_calc
from bezier_main import bezier_main
import os
import math
import time

os.system('clear')

x = [0]
y = [0]
z = [0]

while 1:
    try:
        os.system('clear')
        x.append(int(input("Input x coordinate of point: ")))
        y.append(int(input("Input y coordinate of point: ")))
        z.append(int(input("Input z coordinate of point: ")))
        os.system('clear')
    except:
        os.system('clear')
        print("There was an error in entering your point. You may have entered a letter. Program shutting down... ")
        exit()

    try:
        if input("Would you like to enter more points? y for yes: ").lower() != "y":
            os.system('clear')
            print("Point entry complete.")
            break
    except:
        os.system('clear')
        print(
            "There was an error in understanding your response. Continuing onwards.")
        break

x_bezier = x.copy()
y_bezier = y.copy()
z_bezier = z.copy()

# All units in mm
current_pos = [0, 0, 0]
link_length = 6
actuations = 0
actuation_limit = 32
previous_vector = [0, 0, 0]
phi_array = []
theta_array = []

for k in range(0, len(x)):
    print(f"x is {x}")
    print(f"k is {k}")
    print(f"length of x is {len(x)}")

    v_dif = [x[k+1] - current_pos[0], y[k+1] -
             current_pos[1], z[k+1] - current_pos[2]]
    mag_v_dif = math.sqrt(v_dif[0]**2 + v_dif[1]**2 + v_dif[2]**2)
    un_vector = [0, 0, 0]
    for s in range(0, 3):
        un_vector[s] = v_dif[s]/mag_v_dif

    n_actuations = math.ceil(mag_v_dif/link_length)

    theta = theta_calc(
        (current_pos[0], current_pos[1], current_pos[2]), (v_dif[0], v_dif[1], v_dif[2]))
    if v_dif[0] - previous_vector[0] < 0 and v_dif[1] - previous_vector[1] < 0:
        theta = theta + math.pi
    elif v_dif[0] - previous_vector[0] > 0 and v_dif[1] - previous_vector[1] < 0:
        theta = theta + math.pi

    phi = abs(phi_calc((current_pos[0], current_pos[1],
                        current_pos[2]), (v_dif[0], v_dif[1], v_dif[2])))

    current_pos = [current_pos[0] + un_vector[0]*link_length*n_actuations, current_pos[1] +
                   un_vector[1]*link_length*n_actuations, current_pos[2] + un_vector[2]*link_length*n_actuations]

    if actuations > actuation_limit:
        print("Full extension achieved.")
        print(f"Current position is {current_pos}")
        exit()
    if phi > math.pi/6:
        print(
            f"Diverting to bezier curve following, current position is {current_pos}")
        bezier_main(x_bezier, y_bezier, z_bezier, actuations)
        break
    else:
        theta_array.append(theta)
        phi_array.append(phi)
        actuations += 1
        for i in range(0, n_actuations):
            actuations += 1
            theta_array.append(0)
            phi_array.append(0)
        print(f"Length of x bezier is {len(x_bezier)}")
        if len(x_bezier) != 1:
            x_bezier.pop(k+1)
            y_bezier.pop(k+1)
            z_bezier.pop(k+1)
        x_bezier.pop(k)
        y_bezier.pop(k)
        z_bezier.pop(k)
        x_bezier.insert(0, current_pos[0])
        y_bezier.insert(0, current_pos[1])
        z_bezier.insert(0, current_pos[2])

        if len(x_bezier) == 1:
            print(
                f"Path following complete, current position is {current_pos}")
            quit()

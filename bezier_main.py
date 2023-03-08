
from return_bezier import return_bezier
from new_bezier import new_bezier
from calculate_angles import theta_calc, phi_calc
import math
import time


def bezier_main(x, y, z, actuations):
    current_pos = [x[0], y[0], z[0]]
    path_length = 0
    link_length = 6
    k = 0
    actuation_limit = 32
    previous_vector = [0, 0, 0]
    phi_array = []
    theta_array = []
    curvature_limit = math.pi/6
    phi = 0

    xBezier, yBezier, zBezier = return_bezier(x, y, z)

    while 1:
        if k == len(xBezier):
            print("End of curve reached")
            print(f"Phi array is {phi_array}")
            print(f"Theta array is {theta_array}")
            break
        elif actuations > actuation_limit:
            print("Snake fully extended")
            print(f"Phi array is {phi_array}")
            print(f"Theta array is {theta_array}")
            break
        path_length = math.sqrt((xBezier[k]-current_pos[0])**2 + (
            yBezier[k]-current_pos[1])**2 + (zBezier[k] - current_pos[2])**2)

        if path_length > link_length:
            vector = [xBezier[k] - current_pos[0], yBezier[k] -
                      current_pos[1], zBezier[k] - current_pos[2]]
            print("advanced!")
            mag_vector = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
            un_vector = [vector[0]/mag_vector,
                         vector[1]/mag_vector, vector[2]/mag_vector]
            current_pos = [current_pos[0] + un_vector[0]*link_length, current_pos[1] +
                           un_vector[1]*link_length, current_pos[2] + un_vector[2]*link_length]

            # Theta and phi calculation
            theta = theta_calc(vector, previous_vector)
            if vector[0] - previous_vector[0] < 0 and vector[1] - previous_vector[1] < 0:
                theta = theta + math.pi
            elif vector[0] - previous_vector[0] > 0 and vector[1] - previous_vector[1] < 0:
                theta = theta + math.pi
            phi_prev = phi
            phi = phi_calc(vector, previous_vector)
            time.sleep(.5)
            if abs(phi_prev-phi) > curvature_limit:
                print(f"The calculated phi is {phi}")
                request_control_point_add = (current_pos[0] + link_length*math.cos(curvature_limit),
                                             current_pos[1] + link_length*math.sin(curvature_limit)*math.cos(theta), current_pos[2] + link_length*math.sin(curvature_limit)*math.sin(theta))
                xBezier, yBezier, zBezier = new_bezier(
                    x, y, z, xBezier, yBezier, zBezier, request_control_point_add, current_pos)
                previous_vector = [0, 0, 0]
            else:
                previous_vector = vector
                actuations += 1
                phi_array.append(phi)
                theta_array.append(theta)
            path_length = 0

        else:
            k += 1

    return theta_array, phi_array

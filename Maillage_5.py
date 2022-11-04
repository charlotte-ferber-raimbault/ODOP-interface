# -*- coding: utf-8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def fibonacci_sphere(samples):

    points = []
    phi = math.pi * (3. - math.sqrt(5.))  # golden angle in radians

    for i in range(samples):
        x=0
        y=0
        z = 1 - (i / float(samples - 1)) # z goes from 1 to 0
        radius = math.sqrt(1 - z * z)  # radius at z

        theta = phi * i  # golden angle increment

        x = x + theta
        y = y + theta
        radius

        points.append((x, y, radius))

    return points
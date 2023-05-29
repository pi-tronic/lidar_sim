#!/usr/bin/env python3
import numpy as np
import pygame
import math

class LaserSensor:
    def __init__(self, range, map, uncertainty):
        self.range = range
        self.speed = 4 # rounds per second
        self.sigma = np.array([uncertainty[0], uncertainty[1]])
        self.position = (0, 0)
        self.map = map
        self.w, self.h = pygame.display.get_surface().get_size()
        self.sensedObstacle = []

    def distance(self, obstaclePosition):
        p_x = (obstaclePosition[0] - self.position[0]) **2
        p_y = (obstaclePosition[1] - self.position[1]) **2
        
        return math.sqrt(p_x + p_y)
    
    def uncertainty_add(self, distance, angle):
        mean = np.array([distance, angle])
        covariance = np.diag(self.sigma **2)
        distance, angle = np.random.multivariate_normal(mean, covariance)
        distance = max(distance, 0)
        angle = max(angle, 0)

        return [distance, angle]
    
    def sense_obstacles(self):
        data = []
        x1, y1 = self.position[0], self.position[1]
        for angle in np.linspace(0, 2*math.pi, 60, False):
            x2, y2 = (x1 + self.range * math.cos(angle), y1 - self.range * math.sin(angle))
            for i in range(100):
                u = i / 100
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                if 0 < x < self.w and 0 < y < self.h:
                    color = self.map.get_at((x, y))
                    if (color[0], color[1], color[2]) == (0, 0, 0):
                        distance = self.distance((x, y))
                        output = self.uncertainty_add(distance, angle)
                        output.append(self.position)
                        # store the measurements
                        data.append(output)

                        break

        if len(data) > 0:
            return data
        else:
            return False
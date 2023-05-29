#!/usr/bin/env python3

# add own directory to path
from os import getcwd
from sys import path
path.append(getcwd())

import pygame
import math
import numpy as np

class Cartographer():
    def __init__(self):
        self.scale = 10
        self.position = (0, 0) # mouse position
        self.w, self.h = pygame.display.get_surface().get_size()

        # colors
        self.obstacle = (0, 0, 0)
        self.free = (255, 255, 255)
        self.unknown = (70, 100, 80)

    def create_map(self, scan):
        if scan:
            data = []
            x1, y1 = self.position[0]/self.scale, self.position[1]/self.scale
            for obstacle in scan:
                x2, y2 = self.AD2pos(obstacle[0], obstacle[1], obstacle[2])
                x2, y2 = x2/self.scale, y2/self.scale
                
                # mark obstacle
                data.append([(x2, y2), self.obstacle])

                # mark free space
                line = self.getPixelsofLine(x1, y1, x2, y2)
                for pixel in line:
                    if pixel not in data:
                        data.append([pixel, self.free])

            if len(data) > 0:
                return data
            else:
                return False
        
        return False
    
    def AD2pos(self, distance, angle, robotPosition):
        x = distance * math.cos(angle) + robotPosition[0]
        y = -distance * math.sin(angle) + robotPosition[1]

        return (int(x), int(y))
        
    def getPixelsofLine(self, x1, y1, x2, y2):
        pixels = []

        dx = x2 - x1
        dy = y2 - y1
        D = 2*dy - dx
        y = y1

        for x in range(int(x1), int(x2)):
            pixels.append((x, y))
            if D > 0:
                y = y + 1
                D = D - 2*dx
            D = D + 2*dy

        return pixels
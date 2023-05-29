#!/usr/bin/env python3
import pygame
import math

class BuildEnvironment:
    def __init__(self, mapDimensions):
        pygame.init()
        self.pointCloud = []
        self.globalMap = []
        self.externalMap = pygame.image.load('map.png')
        self.map_w, self.map_h = mapDimensions
        self.MapWindowName = 'LiDAR Emulator'
        pygame.display.set_caption(self.MapWindowName)
        self.map = pygame.display.set_mode((self.map_w, self.map_h))
        self.map.blit(self.externalMap, (0,0))
        self.scale = 10

        # colors
        self.black = (0, 0, 0)
        self.grey = (70, 70, 70)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.unknown = (70, 100, 80)

    def AD2pos(self, distance, angle, robotPosition):
        x = distance * math.cos(angle) + robotPosition[0]
        y = -distance * math.sin(angle) + robotPosition[1]

        return (int(x), int(y))
    
    def dataStorage(self, scan_data, map_data):
        if scan_data:
            print(len(self.pointCloud))
            self.pointCloud = []
            for element in scan_data:
                point = self.AD2pos(element[0], element[1], element[2])
                if point not in self.pointCloud:
                    self.pointCloud.append(point)
        
        if map_data:
            print(len(self.globalMap))
            for information in map_data:
                if information not in self.globalMap:
                    color = pygame.display.get_surface().get_at((int(information[0][0]), int(information[0][1])))
                    if (color[0], color[1], color[2]) != self.black:
                        self.globalMap.append(information)

    def show_map(self):
        self.infoMap = pygame.Surface((1600/self.scale, 1110/self.scale))
        self.infoMap.fill(self.unknown)
        for information in self.globalMap:
            print(information)
            self.infoMap.set_at((int(information[0][0]), int(information[0][1])), information[1])
        self.infoMap = pygame.transform.scale(self.infoMap,(1600, 1110))

    def show_sensorData(self):
        # self.infoMap = self.map.copy()
        # self.infoMap.fill(self.black)
        for point in self.pointCloud:
            self.infoMap.set_at((int(point[0]), int(point[1])), self.red)
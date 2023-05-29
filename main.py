#!/usr/bin/env python3

# add own directory to path
from os import getcwd
from sys import path
path.append(getcwd())

import env, sensors, mapping
import pygame

# map: 1600x1110
environment = env.BuildEnvironment((1600, 1110))
environment.originalMap = environment.map.copy()
laser = sensors.LaserSensor(200, environment.originalMap, uncertainty=(0.5, 0.01))
cartographer = mapping.Cartographer()
environment.map.fill((0, 0, 0))
environment.infoMap = environment.map.copy()

running = True
while running:
    sensorON = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_focused():
            sensorON = True
        elif not pygame.mouse.get_focused():
            sensorON = False

    if sensorON:
        position = pygame.mouse.get_pos()
        laser.position = position
        cartographer.position = position
        sensor_data = laser.sense_obstacles()
        map_data = cartographer.create_map(sensor_data)
        environment.dataStorage(sensor_data, map_data)
        environment.show_map()
        environment.show_sensorData()

    # environment.map.blit(environment.originalMap, (0, 0))
    environment.map.blit(environment.infoMap, (0, 0))

    pygame.display.update()
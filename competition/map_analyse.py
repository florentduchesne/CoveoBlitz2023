from game_message import *
from actions import *

import numpy as np
import matplotlib.pyplot as plt

def position_generator_1d(position: Position):
    for x in range(-1, 1):
        for y in range(-1, 1):
            yield Position(position.x + x, position.y + y)

def position_generator_2d(position: Position):
    for x in range(-2, 2):
        for y in range(-2, 2):
            yield Position(position.x + x, position.y + y)

def parcourir_chemins(game_message: GameMessage):
    arr = np.zeros((game_message.map.height, game_message.map.width))
    for chemin in game_message.map.paths:
        print('chemin', chemin)
        for tuile1 in chemin.tiles:
            print('tuile1', tuile1)
            for tuile2 in position_generator_2d(tuile1):
                if tuile2.x < 0 or tuile2.x >= game_message.map.width or tuile2.y < 0 or tuile2.y >= game_message.map.height:
                    continue
                is_valid = True
                for tower in game_message.playAreas[game_message.teamId].towers:
                    if tuile2 == tower.position:
                        is_valid = False
                #print(game_message.map.obstacles)
                for path in game_message.map.paths:
                    if tuile2 in path.tiles:
                        is_valid = False
                if tuile2 in game_message.map.obstacles:
                    is_valid = False
                if is_valid:
                    arr[tuile2.y, tuile2.x] += 1
    #plt.imshow(arr)
    #plt.show()
    return arr



def get_meilleure_position(heat_array):

    bestPosX = -1
    bestPosY = -1
    bestPosScore = -1

    for j in range(len(heat_array)):
        for i in range(len(heat_array[j])):
            if heat_array[j][i] > bestPosScore:
                bestPosX = i
                bestPosY = j
                bestPosScore = heat_array[j][i]

    return Position(bestPosX, bestPosY)
            
            
            
            


            
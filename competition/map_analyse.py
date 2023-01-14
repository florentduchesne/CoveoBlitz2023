from game_message import *
from actions import *

import numpy as np
import matplotlib.pyplot as plt
import random

def position_generator_1d(position: Position):
    for x in range(-1, 2):
        for y in range(-1, 2):
            yield Position(position.x + x, position.y + y)

def position_generator_2d(position: Position):
    for x in range(-2, 3):
        for y in range(-2, 3):
            yield Position(position.x + x, position.y + y)

def parcourir_chemins(game_message: GameMessage, id_chemin:int, portee:int):
    arr = np.zeros((game_message.map.height, game_message.map.width))
    chemin = game_message.map.paths[id_chemin]
    for tuile1 in chemin.tiles:
        position_generator = position_generator_2d if portee == 2 else position_generator_1d
        for tuile2 in position_generator(tuile1):
            if tuile2.x < 0 or tuile2.x >= game_message.map.width or tuile2.y < 0 or tuile2.y >= game_message.map.height:
                continue
            is_valid = True
            for tower in game_message.playAreas[game_message.teamId].towers:
                if tuile2 == tower.position:
                    is_valid = False
            for path in game_message.map.paths:
                if tuile2 in path.tiles:
                    is_valid = False
            if tuile2 in game_message.map.obstacles:
                is_valid = False
            if is_valid:
                arr[tuile2.y, tuile2.x] += 1
    for chemin2 in game_message.map.paths:
        if chemin2 != chemin:
            for tuile1 in chemin2.tiles:
                position_generator = position_generator_2d if portee == 2 else position_generator_1d
                for tuile2 in position_generator(tuile1):
                    if tuile2.x < 0 or tuile2.x >= game_message.map.width or tuile2.y < 0 or tuile2.y >= game_message.map.height:
                        continue
                    if arr[tuile2.y, tuile2.x] == 0:
                        continue
                    is_valid = True
                    for tower in game_message.playAreas[game_message.teamId].towers:
                        if tuile2 == tower.position:
                            is_valid = False
                    for path in game_message.map.paths:
                        if tuile2 in path.tiles:
                            is_valid = False
                    if tuile2 in game_message.map.obstacles:
                        is_valid = False
                    if is_valid:
                        arr[tuile2.y, tuile2.x] += 1
    return arr


def get_meilleure_position(heat_array):
    positions = np.where(heat_array == heat_array.max())
    i = random.randint(0, len(positions[0]) - 1)
    return Position(int(positions[1][i]), int(positions[0][i]))
   
def economiser(gm: GameMessage):
    teamId = gm.teamId
    area = gm.playAreas.get(teamId)

    nbAttaque = 0
    nbEnnemie = 0
    for ennemie in area.enemies:
        if not ennemie.isKilled and not ennemie.hasEndedPath:
            nbEnnemie += 1
            
    for tower in area.towers:
        if tower.type == TowerType.SPEAR_SHOOTER:
            nbAttaque += 2
        else:
            nbAttaque += 11 #depende des autres types de tour
    return nbAttaque > nbEnnemie

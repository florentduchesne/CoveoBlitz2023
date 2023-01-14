from game_message import *


def get_ennemies_type(game_message: GameMessage) -> EnemyType:
    round = game_message.round
    enemy_type = EnemyType.LVL1

    if round <= 3:
        enemy_type = EnemyType.LVL2
    elif round <= 4:
        enemy_type = EnemyType.LVL5
    elif round <= 5:
        enemy_type = EnemyType.LVL3
    elif round <= 7:
        enemy_type = EnemyType.LVL4
    elif round <= 9:
        enemy_type = EnemyType.LVL5
    elif round <= 11:
        enemy_type = EnemyType.LVL8

    return enemy_type

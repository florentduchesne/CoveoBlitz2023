from game_message import *


def get_ennemies_type(game_message: GameMessage) -> EnemyType:
    teamId = game_message.teamId
    money = game_message.teamInfos[teamId].money
    reinforcements = game_message.teamInfos[teamId].sentReinforcements
    shop = game_message.shop

    enemy_type = get_ennemies_by_round(game_message)
    enemy_info = shop.reinforcements.get(enemy_type)

    if len(reinforcements) < 6:
        if enemy_info is not None and enemy_info.price <= money and len(reinforcements) < 6:
            return enemy_type
        elif len(reinforcements) < 3 and len(shop.reinforcements) > 0:
            max_bonus = -1
            for enemy in shop.reinforcements:
                enemy_info = shop.reinforcements.get(enemy)
                if enemy_info.price <= money and enemy_info.payoutBonus > max_bonus:
                    max_bonus = enemy_info.payoutBonus
                    enemy_type = enemy

        return enemy_type
    else:
        return None


def get_ennemies_by_round(game_message: GameMessage) -> EnemyType:
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
    else:
        enemy_type = EnemyType.LVL8

    return enemy_type

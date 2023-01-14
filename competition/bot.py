from game_message import *
from actions import *
import map_analyse
import strat_ennemies

class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
    
    def sortOtherTeams(self, gm: GameMessage):
        teams = list()
        teamId = gm.teamId
        for otherTeamId in gm.teams:
            if teamId != otherTeamId:
                teams.append(gm.teamInfos.get(otherTeamId))
        
        teams.sort(key=lambda x : x.hp, reverse=True)
        return teams

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        other_team_ids = [team for team in game_message.teams if team != game_message.teamId]
        actions = list()
        
        heatmap = map_analyse.parcourir_chemins(game_message)
        position = map_analyse.get_meilleure_position(heatmap)
        otherTeams = self.sortOtherTeams(game_message)

        #actions.append(SellAction(Position(0, 0)))
        actions.append(BuildAction(TowerType.SPEAR_SHOOTER, position))

        if other_team_ids:
            ennemies_type = strat_ennemies.get_ennemies_type(game_message)
            actions.append(SendReinforcementsAction(ennemies_type, otherTeams[0].id))

        return actions

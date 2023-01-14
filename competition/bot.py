from game_message import *
from actions import *
import map_analyse
import strat_ennemies

class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        self.liste_achat = Bot.liste_achat()
        self.prochain_achat = next(self.liste_achat)

    def liste_achat():
        types_tours = [TowerType.SPEAR_SHOOTER, TowerType.BOMB_SHOOTER]
        i = 0
        for _ in range(20):
            yield TowerType.SPEAR_SHOOTER
        while True:
            if i == len(types_tours):
                i = 0
            yield types_tours[i]
            i += 1
            
    
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
        
        #nb_tours = len(game_message.playAreas[game_message.teamId].towers)
        
        otherTeams = self.sortOtherTeams(game_message)
        
        print(game_message.shop.towers[self.prochain_achat].price)
        print(game_message.teamInfos[game_message.teamId].money)
        if game_message.shop.towers[self.prochain_achat].price <= game_message.teamInfos[game_message.teamId].money:
            actions.append(BuildAction(self.prochain_achat, position))
            self.prochain_achat = next(self.liste_achat)

        if other_team_ids:
            ennemies_type = strat_ennemies.get_ennemies_type(game_message)
            actions.append(SendReinforcementsAction(ennemies_type, otherTeams[0].id))

        return actions

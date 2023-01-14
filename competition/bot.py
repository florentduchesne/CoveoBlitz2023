from game_message import *
from actions import *
import map_analyse
import strat_ennemies
import numpy as np

class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        self.liste_achat = Bot.liste_achat()
        self.prochain_achat = next(self.liste_achat)
        self.prochain_chemin = 0

    def liste_achat():
        types_tours = [TowerType.SPEAR_SHOOTER, TowerType.BOMB_SHOOTER]
        i = 0
        for _ in range(200):
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
        
        chemin_depart = self.prochain_chemin
        
        heatmap = map_analyse.parcourir_chemins(game_message, self.prochain_chemin, 2)
        while heatmap.max() == 0:#aucune tour possible autour du chemin selectionne
            self.prochain_chemin += 1
            if self.prochain_chemin == len(game_message.map.paths):
                self.prochain_chemin = 0
            if chemin_depart == self.prochain_chemin:
                #on a remplit le plateau au complet, on devrait commencer a remplacer des tours
                break
            heatmap = map_analyse.parcourir_chemins(game_message, self.prochain_chemin, 2)
        position = map_analyse.get_meilleure_position(heatmap)
        
        otherTeams = self.sortOtherTeams(game_message)
        
        if game_message.shop.towers[self.prochain_achat].price <= game_message.teamInfos[game_message.teamId].money:
            actions.append(BuildAction(self.prochain_achat, position))
            self.prochain_achat = next(self.liste_achat)
            self.prochain_chemin += 1
            if self.prochain_chemin == len(game_message.map.paths):
                self.prochain_chemin = 0

        if other_team_ids:
            ennemies_type = strat_ennemies.get_ennemies_type(game_message)
            actions.append(SendReinforcementsAction(ennemies_type, otherTeams[0].id))

        return actions

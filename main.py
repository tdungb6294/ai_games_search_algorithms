from CheckersGame import *
from CheckersSolver import CheckersSolver
from Player import alpha_beta_player, random_player, custom_player

game_object = CheckersGame()

game_object.play_game(custom_player, random_player)


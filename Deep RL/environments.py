# environments.py

#L'environnement définit les règles du jeu, les états possibles, et les actions autorisées.

import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3))  # 3x3 grid, 0 = empty, 1 = player 1 (X), -1 = player 2 (O)
        self.current_player = 1  # Player 1 starts first
    
    def reset(self):
        """ Reset the board to start a new game. """
        self.board = np.zeros((3, 3))
        self.current_player = 1
        return self.get_state()
    
    def get_state(self):
        """ Return the current state of the game as a vector (flattened board). """
        return self.board.flatten()
    
    def available_actions(self):
        """ Return a list of available actions (indices of empty cells). """
        return np.argwhere(self.board == 0)
    
    def step(self, action):
        """ Make a move and switch the current player. Return the new state, reward, and if game is done. """
        row, col = action
        if self.board[row, col] == 0:
            self.board[row, col] = self.current_player
            if self.check_winner(self.current_player):
                return self.get_state(), 1 * self.current_player, True  # Player wins
            if len(self.available_actions()) == 0:
                return self.get_state(), 0, True  # Draw
            self.current_player *= -1  # Switch player
            return self.get_state(), 0, False
        else:
            raise ValueError("Invalid action!")
    
    def check_winner(self, player):
        """ Check if a player has won the game. """
        for i in range(3):
            if np.all(self.board[i, :] == player) or np.all(self.board[:, i] == player):
                return True
        if self.board[0, 0] == player and self.board[1, 1] == player and self.board[2, 2] == player:
            return True
        if self.board[0, 2] == player and self.board[1, 1] == player and self.board[2, 0] == player:
            return True
        return False
    
#Les états et actions sont déjà définis dans la classe TicTacToe :

#État : La méthode get_state() retourne un vecteur aplati représentant la grille de jeu (de taille 9).
#Actions : La méthode available_actions() retourne les indices des cellules vides. 
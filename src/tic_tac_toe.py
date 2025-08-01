from typing import List

class TicTacToe:
    # Constants
    EMPTY = ' '
    PLAYER_X = 'X'
    PLAYER_O = 'O'

    def __init__(self):
        """Initialize the game"""
        self.reset_board()
        pass

    def reset_board(self):
        """Reset board and current player"""
        self.board = [self.EMPTY] * 9
        self.current_player = self.PLAYER_X
        pass

    def is_valid_move(self, position: int) -> bool:
        """
        Check if position is valid and empty.

        Args:
            position (int): Position on board (1-9)

        Returns:
            bool: True if position is valid and empty, False otherwise
        """
        if position < 1 or position > 9:
            return False
        
        return self.board[position - 1] == self.EMPTY

    def make_move(self, position):
        """
        Make a move at the specified position and switch players
        
        Args:
            position (int): Position on board (1-9)
        """
        self.board[position - 1] = self.current_player
        self._switch_player()

    def _switch_player(self):
        """Private method to alternate current player"""
        self.current_player = self.PLAYER_O if self.current_player == self.PLAYER_X else self.PLAYER_X

    def get_display_value(self, position: int) -> str:
        """
        Return display value for position.

        Args:
            position (int): Position on board (1-9)

        Returns:
            str: Position number if empty, player symbol if occupied
        """
            
        board_value = self.board[position - 1]

        if board_value != self.EMPTY:
            return board_value
        
        return str(position)
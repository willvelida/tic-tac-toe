from typing import List, Optional
from enum import Enum

class GameMode(Enum):
    HUMAN_VS_HUMAN = 'human_vs_human'
    HUMAN_VS_AI = 'human_vs_ai'

class TicTacToe:
    # Constants
    EMPTY = ' '
    PLAYER_X = 'X'
    PLAYER_O = 'O'

    def __init__(self, mode: GameMode = GameMode.HUMAN_VS_AI):
        """Initialize the game"""
        self.mode = mode
        self.reset_board()

    def reset_board(self):
        """Reset board and current player"""
        self.board = [self.EMPTY] * 9
        self.current_player = self.PLAYER_X

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
        if not self.is_valid_move(position):
            if not (1 <= position <= 9):
                raise ValueError(f"Invalid position {position}: must be between 1 and 9")
            else:
                raise ValueError(f"Position {position} is already occupied by '{self.board[position-1]}'")

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
    
    def check_winner(self):
        """
        Check if there's a winner on the board

        Returns:
            str or None: 'X' or 'O' if there's a winner, None otherwise
        """
        winning_combinations = [
            # Rows
            [0,1,2], [3,4,5],[6,7,8],
            # Columns
            [0,3,6], [1,4,7],[2,5,8],
            # Diagonals
            [0,4,8],[2,4,6]
        ]

        for combination in winning_combinations:
            if self._check_line(combination):
                return self.board[combination[0]]
            
        return None

    def _check_line(self, positions: List[int]) -> bool:
        """
        Check if three positions have the same non-empty symbol

        Args:
            positions (List[int]): List of board indices to check (0-8)

        Returns:
            bool: True if all positions have same non-empty symbol
        """
        first = self.board[positions[0]]
        return (first != self.EMPTY and
                first == self.board[positions[1]] and
                first == self.board[positions[2]])
    
    def is_board_full(self) -> bool:
        """
        Check if the board is completely full

        Returns:
            bool: True if all positions are occupied, False otherwise
        """
        return self.EMPTY not in self.board
    
    def is_draw(self) -> bool:
        """
        Check if the game is a draw (board full with no winner)

        Returns:
            bool: True if game is a draw, otherwise False
        """
        return self.is_board_full() and self.check_winner() is None
    
    def get_game_state(self) -> dict:
        """
        Get the current state of the game.

        Returns:
            dict: Game state information with keys:
                - 'state': 'ongoing', 'won', or 'draw'
                - 'winner': 'X', 'O' or None
        """
        winner = self.check_winner()
        if winner:
            return {'state': 'won', 'winner': winner}
        
        if self.is_draw():
            return {'state':'draw', 'winner': None}
        
        return {'state': 'ongoing', 'winner': None}

    def get_game_mode(self) -> GameMode:
        """
        Get the current game mode.

        Returns:
            GameMode: The current game mode
        """
        return self.mode

    def is_ai_mode(self) -> bool:
        """
        Check if the game is in AI mode.

        Returns:
            bool: True if playing against AI, False otherwise
        """
        return self.mode == GameMode.HUMAN_VS_AI
    
    def find_winning_move(self, player_symbol: str) -> Optional[int]:
        """
        Find a position where the player can win in one move.

        Args:
            player_symbol (str): 'X' or 'O'

        Returns:
            Optional[int]: Position 1-9 where player can win, or None if no winning move
        """
        winning_combinations = [
            [0,1,2], [3,4,5], [6,7,8],  # Rows
            [0,3,6], [1,4,7], [2,5,8],  # Columns
            [0,4,8], [2,4,6]           # Diagonals
        ]

        for combo in winning_combinations:
            player_count = 0
            empty_count = 0
            empty_position = None

            for pos in combo:
                if self.board[pos] == player_symbol:
                    player_count += 1
                elif self.board[pos] == self.EMPTY:
                    empty_count += 1
                    empty_position = pos
            
            if player_count == 2 and empty_count == 1:
                return empty_position + 1
            
        return None
    
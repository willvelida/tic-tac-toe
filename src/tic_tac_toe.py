from typing import List, Optional
from enum import Enum

class GameMode(Enum):
    HUMAN_VS_HUMAN = 'human_vs_human'
    HUMAN_VS_AI = 'human_vs_ai'

class TicTacToe:
    """
    Core Tic-Tac-Toe game engine with board management and game logic.
    
    This class handles the complete game state including board representation,
    move validation, win detection, and player turn management. Supports both
    human vs human and human vs AI game modes.
    
    Example:
        Basic game setup and play:
        
        >>> from src.tic_tac_toe import TicTacToe, GameMode
        >>> 
        >>> # Create a new game
        >>> game = TicTacToe(GameMode.HUMAN_VS_HUMAN)
        >>> 
        >>> # Make some moves
        >>> game.make_move(1)  # X plays position 1
        >>> game.make_move(5)  # O plays center
        >>> game.make_move(2)  # X plays position 2
        >>> 
        >>> # Check game state
        >>> winner = game.check_winner()
        >>> if winner:
        >>>     print(f"Winner: {winner}")
        >>> elif game.is_draw():
        >>>     print("Game is a draw!")
        
    Attributes:
        EMPTY (str): Symbol representing empty board position (' ')
        PLAYER_X (str): Symbol for player X
        PLAYER_O (str): Symbol for player O
        board (List[str]): 9-element list representing 3x3 board
        current_player (str): Current player's symbol ('X' or 'O')
        mode (GameMode): Current game mode (HUMAN_VS_HUMAN or HUMAN_VS_AI)
    """
    # Constants
    EMPTY = ' '
    PLAYER_X = 'X'
    PLAYER_O = 'O'

    def __init__(self, mode: GameMode = GameMode.HUMAN_VS_AI):
        """
        Initialize a new Tic-Tac-Toe game instance.
        
        Creates a fresh game with the specified mode and resets the board to 
        starting state. The game begins with player X's turn.
        
        Args:
            mode (GameMode, optional): Game mode to use. Defaults to GameMode.HUMAN_VS_AI.
                Can be HUMAN_VS_HUMAN or HUMAN_VS_AI.
                
        Example:
            >>> game = TicTacToe()  # Defaults to Human vs AI
            >>> game2 = TicTacToe(GameMode.HUMAN_VS_HUMAN)
        """
        self.mode = mode
        self.reset_board()

    def reset_board(self):
        """
        Reset the game board to initial state and set starting player.
        
        Clears all positions on the board to empty spaces and sets the current
        player to X (first player). This method is called during initialization
        and can be used to start a new game while keeping the same instance.
        
        Example:
            >>> game = TicTacToe()
            >>> game.make_move(1)  # Make some moves
            >>> game.make_move(2)
            >>> game.reset_board()  # Start fresh
            >>> game.current_player
            'X'
        """
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
            
        Raises:
            ValueError: If position is not between 1-9
            ValueError: If position is already occupied
            
        Example:
            >>> game = TicTacToe()
            >>> game.make_move(5)  # Place X in center
            >>> game.current_player
            'O'
        """
        if not self.is_valid_move(position):
            if not (1 <= position <= 9):
                raise ValueError(f"Invalid position {position}: must be between 1 and 9")
            else:
                raise ValueError(f"Position {position} is already occupied by '{self.board[position-1]}'")

        self.board[position - 1] = self.current_player
        self._switch_player()

    def _switch_player(self):
        """
        Switch current player from X to O or O to X.
        
        Private method called automatically after each valid move to alternate
        turns between players. Ensures proper game flow and turn management.
        
        Side Effects:
            Updates self.current_player to the opposite player
        """
        self.current_player = self.PLAYER_O if self.current_player == self.PLAYER_X else self.PLAYER_X

    def get_display_value(self, position: int) -> str:
        """
        Return display value for position.

        Args:
            position (int): Position on board (1-9)

        Returns:
            str: Position number if empty, player symbol if occupied
            
        Example:
            >>> game = TicTacToe()
            >>> game.get_display_value(1)  # Empty position
            '1'
            >>> game.make_move(1)
            >>> game.get_display_value(1)  # Occupied position
            'X'
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
            
        Raises:
            ValueError: If player_symbol is not 'X' or 'O'
            
        Example:
            >>> game = TicTacToe()
            >>> game.board = ['X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            >>> game.find_winning_move('X')
            3  # Position 3 completes the top row
        """
        if player_symbol not in [self.PLAYER_X, self.PLAYER_O]:
            raise ValueError(f"Invalid player symbol '{player_symbol}'. Must be 'X' or 'O'.")
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
    
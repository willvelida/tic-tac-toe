from abc import ABC, abstractmethod
from typing import List
import random
import time
from enum import Enum

from src.tic_tac_toe import TicTacToe

class DifficultyLevel(Enum):
    """AI Difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Player(ABC):
    """Abstract base class for all player types (Human, AI)"""

    def __init__(self, symbol: str):
        if symbol not in [TicTacToe.PLAYER_X, TicTacToe.PLAYER_O]:
            raise ValueError(f"Invalid symbol '{symbol}'. Must be 'X' or 'O'.")
        self.symbol = symbol

    @classmethod
    def choose_symbol(cls):
        """
        Allow player to choose their symbol (X or O).

        Returns:
            str: Selected player symbol ('X' or 'O')
        """
        while True:
            print("\nChoose your option:")
            print("1. Player X")
            print("2. Player O")
            print("3. Random")
            print("4. Quit Game")

            try:
                choice = input("Enter your choice (1-4): ").strip()
                
                if choice == '1':
                    return TicTacToe.PLAYER_X
                elif choice == '2':
                    return TicTacToe.PLAYER_O
                elif choice == '3':
                    # Random selection between X and O
                    return random.choice([TicTacToe.PLAYER_X, TicTacToe.PLAYER_O])
                elif choice == '4':
                    print("Thanks for playing! Goodbye!")
                    raise SystemExit(0)
                else:
                    print(f"Invalid choice '{choice}'. Please enter 1, 2, 3, or 4.")
            except (EOFError, KeyboardInterrupt):
                print("\nGame cancelled. Goodbye!")
                raise SystemExit(0)

    @abstractmethod
    def get_move(self, board: List[str]) -> int:
        pass

class HumanPlayer(Player):
    """Human player implementation"""

    def get_move(self, board: List[str]) -> int:
        """
        Get move from human via console input.

        Args:
            board: Current board state

        Returns:
            int: Position 1-9 chosen by player

        Raises:
            ValueError: If input cannot be converted to integer
        """
        return int(input())
    
class AIPlayer(Player):
    """AI Player implementation with configurable difficulty levels"""

    def __init__(self, symbol: str, difficulty: DifficultyLevel, enable_delay: bool = True):
        """
        Initialize AI Player with symbol and difficulty level

        Args:
            symbol (str): Player symbol ('X' or 'O')
            difficulty (DifficultyLevel): AI Difficulty level
            enable_delay (bool): Whether to enable move delay simulation (default: True)

        Raises:
            ValueError: If symbol is invalid
            TypeError: If difficulty is not a DifficultyLevel enum
        """
        super().__init__(symbol)

        if not isinstance(difficulty, DifficultyLevel):
            raise TypeError(f"Difficulty must be a DifficultyLevel enum, got {type(difficulty)}")
        
        self.difficulty = difficulty
        self.enable_delay = enable_delay
        # Create a single TicTacToe instance for board analysis (optimization)
        self._game_analyzer = TicTacToe()

    def get_move(self, board: List[str]) -> int:
        """
        Get AI move using strategic randomness based on difficulty level.
    
        Args:
            board (List[str]): Current board state (9 elements)
    
        Returns:
            int: Position 1-9 for AI move
    
        Raises:
            ValueError: If no valid moves are available
            ValueError: If board is invalid format
        """
        if len(board) != 9:
            raise ValueError(f"Board must have exactly 9 positions, got {len(board)}")
        
        available_moves = [i + 1 for i in range(9) if board[i] == TicTacToe.EMPTY]
    
        if not available_moves:
            raise ValueError("No valid moves available on the board")
        
        if self.enable_delay:
            self._simulate_thinking_delay()
        
        # Get optimal play probability based on difficulty
        optimal_probability = self._get_optimal_probability()
        
        # Decide whether to play optimally or suboptimally
        if random.random() < optimal_probability:
            # Play optimally - use full minimax
            return self._get_best_move_minimax(board)
        else:
            # Play suboptimally but reasonably
            return self._get_reasonable_suboptimal_move(board, available_moves)
    
    def _get_optimal_probability(self) -> float:
        """Get probability of making optimal moves based on difficulty."""
        if self.difficulty == DifficultyLevel.EASY:
            return 0.3  # 30% optimal moves
        elif self.difficulty == DifficultyLevel.MEDIUM:
            return 0.7  # 70% optimal moves
        else:  # HARD
            return 1.0  # 100% optimal moves
    
    def _get_best_move_minimax(self, board: List[str]) -> int:
        """Find the best move using minimax with early termination optimization."""
        # Early termination optimization: Check for obvious moves first
        
        # Create a temporary game analyzer with the current board state
        from src.tic_tac_toe import TicTacToe
        temp_game = TicTacToe()
        temp_game.board = board.copy()
        
        # 1. Check for immediate wins
        winning_move = temp_game.find_winning_move(self.symbol)
        if winning_move is not None:
            return winning_move
        
        # 2. Check for immediate blocks (opponent wins)
        opponent_symbol = self._get_opponent_symbol()
        blocking_move = temp_game.find_winning_move(opponent_symbol)
        if blocking_move is not None:
            return blocking_move
        
        # 3. Prefer center on empty board (existing optimization)
        if all(pos == TicTacToe.EMPTY for pos in board) and board[4] == TicTacToe.EMPTY:
            return 5  # Center position
        
        # 4. Fall back to full minimax for complex positions
        best_score = float('-inf')
        best_moves = []  # Track all equally good moves
    
        for position in range(1, 10):
            if board[position - 1] == TicTacToe.EMPTY:
                # Simulate this move
                simulated_board = board.copy()
                simulated_board[position - 1] = self.symbol
    
                # Evaluate this move (opponent's turn next, unlimited depth)
                score = self._minimax(simulated_board, float('inf'), False)
    
                if score > best_score:
                    best_score = score
                    best_moves = [position]  # New best move(s)
                elif score == best_score:
                    best_moves.append(position)  # Equally good move
    
        # Randomly choose among equally optimal moves
        return random.choice(best_moves)
    
    def _get_reasonable_suboptimal_move(self, board: List[str], available_moves: List[int]) -> int:
        """
        Get a reasonable but suboptimal move for easier difficulties.
        
        Args:
            board (List[str]): Current board state
            available_moves (List[int]): Available positions
            
        Returns:
            int: A reasonable suboptimal move
        """
        # Strategy: Avoid the absolute worst moves, but don't play optimally
        move_scores = []
        
        for position in available_moves:
            # Simulate this move
            simulated_board = board.copy()
            simulated_board[position - 1] = self.symbol
            
            # Use limited depth for suboptimal play
            score = self._minimax(simulated_board, 2, False)  # Only look 2 moves ahead
            move_scores.append((position, score))
        
        # Sort moves by score (best to worst)
        move_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Choose from top 50% of moves (reasonable but not necessarily optimal)
        reasonable_moves = move_scores[:max(1, len(move_scores) // 2)]
        reasonable_positions = [move[0] for move in reasonable_moves]
        
        return random.choice(reasonable_positions)
    
    def _get_opponent_symbol(self) -> str:
        """
        Get the opponent's symbol.
    
        Returns:
            str: The opponent's symbol ('X' or 'O')
        """
        return TicTacToe.PLAYER_O if self.symbol == TicTacToe.PLAYER_X else TicTacToe.PLAYER_X
    
    def _minimax(self, board: List[str], depth: int, is_maximizing: bool) -> int:
        """
        Minimax algorithm implementation with unlimited depth for optimal play.
    
        Args:
            board (List[str]): Current board state
            depth (int): Remaining search depth (can be infinite)
            is_maximizing (bool): True if AI's turn, False if opponent's turn
    
        Returns:
            int: Score for this position
        """
        # Check terminal conditions first (early termination optimization)
        winner = self._check_winner(board)
        if winner == self.symbol:
            return 10 + (depth if depth != float('inf') else 0)  # Prefer faster wins
        elif winner == self._get_opponent_symbol():
            return -10 - (depth if depth != float('inf') else 0)  # Prefer slower losses
        elif self._is_board_full(board):
            return 0  # Draw
        
        # If we've reached depth limit (for suboptimal play), return heuristic evaluation
        if depth <= 0:
            return self._evaluate_position(board)
        
        if is_maximizing:  # AI's turn
            max_eval = float('-inf')
            for position in range(9):
                if board[position] == TicTacToe.EMPTY:
                    # Simulate AI move
                    new_board = board.copy()
                    new_board[position] = self.symbol
                    eval_score = self._minimax(new_board, depth - 1, False)
                    max_eval = max(max_eval, eval_score)
            return max_eval
        else:  # Opponent's turn
            min_eval = float('inf')
            for position in range(9):
                if board[position] == TicTacToe.EMPTY:
                    # Simulate opponent move
                    new_board = board.copy()
                    new_board[position] = self._get_opponent_symbol()
                    eval_score = self._minimax(new_board, depth - 1, True)
                    min_eval = min(min_eval, eval_score)
            return min_eval
    
    def _check_winner(self, board: List[str]) -> str:
        """
        Check if there's a winner on the board (optimized reusable instance).
    
        Args:
            board (List[str]): Board state to check
    
        Returns:
            str or None: 'X', 'O' if there's a winner, None otherwise
        """
        # Temporarily set the board for analysis
        original_board = self._game_analyzer.board
        self._game_analyzer.board = board
        
        try:
            result = self._game_analyzer.check_winner()
            return result
        finally:
            # Always restore the original board state
            self._game_analyzer.board = original_board
    
    def _is_board_full(self, board: List[str]) -> bool:
        """
        Check if the board is completely full (optimized reusable instance).
    
        Args:
            board (List[str]): Board state to check
    
        Returns:
            bool: True if all positions are occupied
        """
        # Temporarily set the board for analysis
        original_board = self._game_analyzer.board
        self._game_analyzer.board = board
        
        try:
            result = self._game_analyzer.is_board_full()
            return result
        finally:
            # Always restore the original board state
            self._game_analyzer.board = original_board
    
    def _evaluate_position(self, board: List[str]) -> int:
        """
        Evaluate a non-terminal position when depth limit is reached.
    
        Args:
            board (List[str]): Board state to evaluate
    
        Returns:
            int: Heuristic score for the position
        """
        # For suboptimal play, just return neutral score
        # This can be enhanced later with positional heuristics
        return 0
    
    def _simulate_thinking_delay(self) -> None:
        """
        Simulate AI thinking time with random delay and message display.

        Provides a more natural user experience by showing the AI is "thinking"
        before making a move
        """
        delay = random.uniform(0.5, 2.0)

        print("AI opponent is thinking...")

        time.sleep(delay)
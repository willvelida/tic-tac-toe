from abc import ABC, abstractmethod
from typing import List
import random

from src.tic_tac_toe import TicTacToe

class Player(ABC):
    """Abstract base class for all player types (Human, AI)"""

    def __init__(self, symbol: str):
        self.symbol = symbol

    @classmethod
    def choose_symbol(cls):
        """
        Allow player to choose thier symbol (X or 0).

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
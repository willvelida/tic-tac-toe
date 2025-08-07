from typing import List, Optional, Callable
from src.tic_tac_toe import TicTacToe, GameMode
from src.player import DifficultyLevel
import random

class TerminalUI:
    """
    Terminal-based user interface for Tic-Tac-Toe game.
    
    Handles all user input/output including board display, input validation,
    and error handling with retry loops.
    """
    
    def display_board(self, game: TicTacToe) -> None:
        """
        Display the game board with ASCII art formatting.
        
        Args:
            game (TicTacToe): Game instance to display board for
        """
        print("\n" + "="*25)
        print("      TIC-TAC-TOE")  
        print("="*25)
        print()
        
        # Create display board using game's get_display_value method
        display_values = [game.get_display_value(i) for i in range(1, 10)]
        
        # ASCII art board with grid
        print(f"   {display_values[0]} │ {display_values[1]} │ {display_values[2]} ")
        print("  ───┼───┼───")
        print(f"   {display_values[3]} │ {display_values[4]} │ {display_values[5]} ")  
        print("  ───┼───┼───")
        print(f"   {display_values[6]} │ {display_values[7]} │ {display_values[8]} ")
        print()
    
    def get_valid_position(self, game: TicTacToe) -> int:
        """
        Get valid position from user with retry loop and validation.
        
        Args:
            game (TicTacToe): Game instance for move validation
            
        Returns:
            int: Valid position (1-9) chosen by player
            
        Raises:
            SystemExit: If user cancels the game
        """
        while True:
            try:
                prompt = f"Player {game.current_player}, enter position (1-9): "
                user_input = input(prompt).strip()
                
                if not user_input:
                    self.show_error("Please enter a position")
                    continue
                
                position = int(user_input)
                
                # Validate range first
                if position < 1 or position > 9:
                    self.show_error("Position must be between 1 and 9")
                    continue
                
                # Check if position is available using game logic
                if game.is_valid_move(position):
                    return position
                else:
                    self.show_error(f"Position {position} is already taken!")
                    
            except ValueError:
                self.show_error("Please enter a valid number between 1 and 9")
            except (EOFError, KeyboardInterrupt):
                self.show_message("\nGame cancelled. Goodbye!")
                raise SystemExit(0)
    
    def get_game_mode(self) -> GameMode:
        """
        Get game mode selection from user.
        
        Returns:
            GameMode: Selected game mode
            
        Raises:
            SystemExit: If user chooses to quit
        """
        while True:
            print("\n" + "="*30)
            print("         GAME MODE")
            print("="*30)
            print("1. Human vs Human")
            print("2. Human vs AI")
            print("3. Quit Game")
            print()
            
            try:
                choice = input("Select game mode (1-3): ").strip()
                
                if choice == '1':
                    return GameMode.HUMAN_VS_HUMAN
                elif choice == '2':
                    return GameMode.HUMAN_VS_AI
                elif choice == '3':
                    self.show_message("Thanks for playing! Goodbye!")
                    raise SystemExit(0)
                else:
                    self.show_error("Invalid choice. Please enter 1, 2, or 3.")
                    
            except (EOFError, KeyboardInterrupt):
                self.show_message("\nGame cancelled. Goodbye!")
                raise SystemExit(0)
    
    def get_player_symbol(self) -> str:
        """
        Get player symbol choice (X or O) for AI games.
        
        Returns:
            str: Selected player symbol ('X' or 'O')
            
        Raises:
            SystemExit: If user chooses to quit
        """
        while True:
            print("\n" + "="*30)
            print("      CHOOSE YOUR SYMBOL")
            print("="*30)
            print("1. Play as X (goes first)")
            print("2. Play as O (goes second)")
            print("3. Random choice")
            print("4. Back to main menu")
            print()
            
            try:
                choice = input("Enter your choice (1-4): ").strip()
                
                if choice == '1':
                    return TicTacToe.PLAYER_X
                elif choice == '2':
                    return TicTacToe.PLAYER_O
                elif choice == '3':                   
                    symbol = random.choice([TicTacToe.PLAYER_X, TicTacToe.PLAYER_O])
                    self.show_message(f"Random choice: You are player {symbol}")
                    return symbol
                elif choice == '4':
                    return None  # Signal to go back to main menu
                else:
                    self.show_error("Invalid choice. Please enter 1, 2, 3, or 4.")
                    
            except (EOFError, KeyboardInterrupt):
                self.show_message("\nGame cancelled. Goodbye!")
                raise SystemExit(0)
    
    def get_ai_difficulty(self) -> DifficultyLevel:
        """
        Get AI difficulty selection from user.
        
        Returns:
            DifficultyLevel: Selected difficulty level
        """
        while True:
            print("\n" + "="*30)
            print("       AI DIFFICULTY")
            print("="*30)
            print("1. Easy   - AI makes mistakes")
            print("2. Medium - AI plays well most of the time")
            print("3. Hard   - AI plays perfectly")
            print()
            
            try:
                choice = input("Select difficulty (1-3): ").strip()
                
                if choice == '1':
                    return DifficultyLevel.EASY
                elif choice == '2':
                    return DifficultyLevel.MEDIUM
                elif choice == '3':
                    return DifficultyLevel.HARD
                else:
                    self.show_error("Invalid choice. Please enter 1, 2, or 3.")
                    
            except (EOFError, KeyboardInterrupt):
                self.show_message("\nGame cancelled. Goodbye!")
                raise SystemExit(0)
    
    def display_game_result(self, game_state: dict) -> None:
        """
        Display final game result with appropriate message.
        
        Args:
            game_state (dict): Game state with 'state' and 'winner' keys
        """
        print("\n" + "="*30)
        print("        GAME OVER!")
        print("="*30)
        
        if game_state['state'] == 'won':
            winner = game_state['winner']
            print(f"🎉 Player {winner} wins! 🎉")
            print(f"Congratulations to the {winner} player!")
        elif game_state['state'] == 'draw':
            print("🤝 It's a draw! 🤝")
            print("Great game - you both played well!")
        else:
            print("Game ended unexpectedly.")
        
        print("="*30)
    
    def show_message(self, message: str) -> None:
        """
        Display a general message to user.
        
        Args:
            message (str): Message to display
        """
        print(f"💬 {message}")
    
    def show_error(self, error_message: str) -> None:
        """
        Display error message to user with formatting.
        
        Args:
            error_message (str): Error message to display
        """
        print(f"❌ {error_message}")
    
    def show_ai_status(self, status_message: str) -> None:
        """
        Display AI status message (callback for AI thinking delay).
        
        Args:
            status_message (str): Status message from AI
        """
        print(f"🤖 {status_message}")
    
    def display_turn_info(self, current_player_symbol: str, is_ai: bool = False) -> None:
        """
        Display whose turn it is.
        
        Args:
            current_player_symbol (str): Symbol of current player
            is_ai (bool): Whether current player is AI
        """
        player_type = "AI" if is_ai else "Human"
        print(f"\n🎮 {player_type} Player {current_player_symbol}'s turn")
#!/usr/bin/env python3
"""
Tic-Tac-Toe Game - Terminal Implementation

A complete tic-tac-toe game with human vs human and human vs AI modes.
Features clean architecture with separated UI, game logic, and player strategies.

Usage:
    python main.py
    python -m src.main

Author: willvelida
"""
from src.terminal_ui import TerminalUI
from src.game_controller import GameController
import sys


def display_welcome_message(ui: TerminalUI) -> None:
    """
    Display welcome message and game instructions.
    
    Args:
        ui (TerminalUI): UI instance for displaying messages
    """
    ui.show_message("Welcome to Tic-Tac-Toe!")
    print("\n" + "="*50)
    print("🎮 WELCOME TO TIC-TAC-TOE 🎮")
    print("="*50)
    print()
    print("📋 HOW TO PLAY:")
    print("   • Choose your game mode")
    print("   • Enter positions 1-9 to make moves")
    print("   • Position layout:")
    print("     1 │ 2 │ 3")
    print("     ──┼───┼──")
    print("     4 │ 5 │ 6")
    print("     ──┼───┼──")
    print("     7 │ 8 │ 9")
    print()
    print("🎯 GAME MODES:")
    print("   • Human vs Human - Play with a friend")
    print("   • Human vs AI - Challenge the computer")
    print()
    print("💡 TIP: Press Ctrl+C anytime to quit")
    print("="*50)


def play_single_game() -> bool:
    """
    Play a single game of tic-tac-toe.
    
    Returns:
        bool: True if user wants to play again, False to quit
    """
    try:
        # Initialize UI and controller
        ui = TerminalUI()
        controller = GameController(ui)
        
        # Play the game
        controller.play()
        
        # Ask if user wants to play again
        return ask_play_again(ui)
        
    except SystemExit:
        # User chose to quit during game
        return False
    except KeyboardInterrupt:
        print("\n\n🚪 Game interrupted. Thanks for playing!")
        return False
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please report this issue if it persists.")
        return False


def ask_play_again(ui: TerminalUI) -> bool:
    """
    Ask user if they want to play another game.
    
    Args:
        ui (TerminalUI): UI instance for user interaction
        
    Returns:
        bool: True if user wants to play again, False otherwise
    """
    while True:
        print("\n" + "="*30)
        print("      PLAY AGAIN?")
        print("="*30)
        print("1. Play another game")
        print("2. Exit")
        print()
        
        try:
            choice = input("Enter your choice (1-2): ").strip()
            
            if choice == '1':
                return True
            elif choice == '2':
                ui.show_message("Thanks for playing Tic-Tac-Toe! Goodbye! 👋")
                return False
            else:
                ui.show_error("Invalid choice. Please enter 1 or 2.")
                
        except (EOFError, KeyboardInterrupt):
            print("\n🚪 Thanks for playing! Goodbye!")
            return False


def main() -> None:
    """
    Main entry point for the Tic-Tac-Toe game.
    
    Handles the game loop, welcome message, and cleanup.
    """
    try:
        # Initialize UI for welcome message
        ui = TerminalUI()
        
        # Show welcome message
        display_welcome_message(ui)
        
        # Main game loop
        while True:
            if not play_single_game():
                break
                
    except KeyboardInterrupt:
        print("\n\n🚪 Thanks for playing Tic-Tac-Toe! Goodbye! 👋")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        print("The game will now exit.")
        sys.exit(1)


def run_demo_game() -> None:
    """
    Run a demonstration game for testing purposes.
    
    This function can be used for automated testing or demonstration.
    """
    print("🎮 Running Tic-Tac-Toe Demo...")
    print("Note: This is a demo mode - use main() for interactive play")
    
    try:
        ui = TerminalUI()
        controller = GameController(ui)
        
        # Show game statistics
        print("\n📊 Game Statistics:")
        stats = controller.get_game_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"Demo failed: {e}")


if __name__ == "__main__":
    # Check for demo mode
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo_game()
    else:
        main()
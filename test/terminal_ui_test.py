"""
Test suite for TerminalUI class.

This module contains comprehensive tests for the TerminalUI class,
focusing on input validation, output verification, and edge cases.
"""

import unittest
from unittest.mock import Mock, patch, call
from io import StringIO
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.terminal_ui import TerminalUI
from src.tic_tac_toe import TicTacToe, GameMode
from src.player import DifficultyLevel


class TestTerminalUIDisplayMethods(unittest.TestCase):
    """Test display methods that output to console."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.ui = TerminalUI()
        self.mock_game = Mock(spec=TicTacToe)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_board_empty(self, mock_stdout) -> None:
        """Test displaying empty board."""
        # Arrange
        self.mock_game.get_display_value.side_effect = lambda i: str(i)
        
        # Act
        self.ui.display_board(self.mock_game)
        
        # Assert
        output = mock_stdout.getvalue()
        self.assertIn("TIC-TAC-TOE", output)
        self.assertIn("1 │ 2 │ 3", output)
        self.assertIn("4 │ 5 │ 6", output)
        self.assertIn("7 │ 8 │ 9", output)
        self.assertIn("───┼───┼───", output)
        
        # Verify get_display_value called for all positions
        expected_calls = [call(i) for i in range(1, 10)]
        self.mock_game.get_display_value.assert_has_calls(expected_calls)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_board_with_moves(self, mock_stdout) -> None:
        """Test displaying board with X and O moves."""
        # Arrange
        board_values = ['X', 'O', '3', 'X', '5', 'O', '7', '8', '9']
        self.mock_game.get_display_value.side_effect = lambda i: board_values[i-1]
        
        # Act
        self.ui.display_board(self.mock_game)
        
        # Assert
        output = mock_stdout.getvalue()
        self.assertIn("X │ O │ 3", output)
        self.assertIn("X │ 5 │ O", output)
        self.assertIn("7 │ 8 │ 9", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_game_result_winner(self, mock_stdout) -> None:
        """Test displaying game result when there's a winner."""
        # Arrange
        game_state = {'state': 'won', 'winner': 'X'}
        
        # Act
        self.ui.display_game_result(game_state)
        
        # Assert
        output = mock_stdout.getvalue()
        self.assertIn("GAME OVER!", output)
        self.assertIn("Player X wins!", output)
        self.assertIn("🎉", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_game_result_draw(self, mock_stdout) -> None:
        """Test displaying game result for a draw."""
        # Arrange
        game_state = {'state': 'draw', 'winner': None}
        
        # Act
        self.ui.display_game_result(game_state)
        
        # Assert
        output = mock_stdout.getvalue()
        self.assertIn("GAME OVER!", output)
        self.assertIn("It's a draw!", output)
        self.assertIn("🤝", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_message(self, mock_stdout) -> None:
        """Test showing general messages."""
        # Act
        self.ui.show_message("Test message")
        
        # Assert
        output = mock_stdout.getvalue()
        self.assertIn("💬 Test message", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_error(self, mock_stdout) -> None:
        """Test showing error messages."""
        # Act
        self.ui.show_error("Error occurred")
        
        # Assert
        output = mock_stdout.getvalue()
        self.assertIn("❌ Error occurred", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_ai_status(self, mock_stdout) -> None:
        """Test showing AI status messages."""
        # Act
        self.ui.show_ai_status("AI is thinking...")
        
        # Assert
        output = mock_stdout.getvalue()
        self.assertIn("🤖 AI is thinking...", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_turn_info_human(self, mock_stdout) -> None:
        """Test displaying turn info for human player."""
        # Act
        self.ui.display_turn_info('X', is_ai=False)
        
        # Assert
        output = mock_stdout.getvalue()
        self.assertIn("🎮 Human Player X's turn", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_turn_info_ai(self, mock_stdout) -> None:
        """Test displaying turn info for AI player."""
        # Act
        self.ui.display_turn_info('O', is_ai=True)
        
        # Assert
        output = mock_stdout.getvalue()
        self.assertIn("🎮 AI Player O's turn", output)


class TestTerminalUIInputMethods(unittest.TestCase):
    """Test input methods that require user interaction."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.ui = TerminalUI()
        self.mock_game = Mock(spec=TicTacToe)
    
    @patch('builtins.input')
    def test_get_valid_position_valid_input(self, mock_input) -> None:
        """Test getting valid position with correct input."""
        # Arrange
        mock_input.return_value = '5'
        self.mock_game.current_player = 'X'
        self.mock_game.is_valid_move.return_value = True
        
        # Act
        position = self.ui.get_valid_position(self.mock_game)
        
        # Assert
        self.assertEqual(position, 5)
        mock_input.assert_called_once_with("Player X, enter position (1-9): ")
        self.mock_game.is_valid_move.assert_called_once_with(5)
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_valid_position_invalid_then_valid(self, mock_stdout, mock_input) -> None:
        """Test getting position with invalid input followed by valid."""
        # Arrange
        mock_input.side_effect = ['invalid', '10', '5']
        self.mock_game.current_player = 'O'
        self.mock_game.is_valid_move.return_value = True
        
        # Act
        position = self.ui.get_valid_position(self.mock_game)
        
        # Assert
        self.assertEqual(position, 5)
        self.assertEqual(mock_input.call_count, 3)
        
        # Check error messages were shown
        output = mock_stdout.getvalue()
        self.assertIn("❌ Please enter a valid number", output)
        self.assertIn("❌ Position must be between 1 and 9", output)
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_valid_position_taken_position(self, mock_stdout, mock_input) -> None:
        """Test getting position when position is already taken."""
        # Arrange
        mock_input.side_effect = ['3', '7']
        self.mock_game.current_player = 'X'
        self.mock_game.is_valid_move.side_effect = [False, True]
        
        # Act
        position = self.ui.get_valid_position(self.mock_game)
        
        # Assert
        self.assertEqual(position, 7)
        self.assertEqual(mock_input.call_count, 2)
        
        # Check error message for taken position
        output = mock_stdout.getvalue()
        self.assertIn("❌ Position 3 is already taken!", output)
    
    @patch('builtins.input')
    def test_get_valid_position_keyboard_interrupt(self, mock_input) -> None:
        """Test handling KeyboardInterrupt during position input."""
        # Arrange
        self.mock_game.current_player = 'X'
        mock_input.side_effect = KeyboardInterrupt()
        
        # Act & Assert
        with self.assertRaises(SystemExit):
            self.ui.get_valid_position(self.mock_game)
    
    @patch('builtins.input')
    def test_get_game_mode_human_vs_human(self, mock_input) -> None:
        """Test selecting human vs human game mode."""
        # Arrange
        mock_input.return_value = '1'
        
        # Act
        mode = self.ui.get_game_mode()
        
        # Assert
        self.assertEqual(mode, GameMode.HUMAN_VS_HUMAN)
    
    @patch('builtins.input')
    def test_get_game_mode_human_vs_ai(self, mock_input) -> None:
        """Test selecting human vs AI game mode."""
        # Arrange
        mock_input.return_value = '2'
        
        # Act
        mode = self.ui.get_game_mode()
        
        # Assert
        self.assertEqual(mode, GameMode.HUMAN_VS_AI)
    
    @patch('builtins.input')
    def test_get_game_mode_quit(self, mock_input) -> None:
        """Test quitting from game mode selection."""
        # Arrange
        mock_input.return_value = '3'
        
        # Act & Assert
        with self.assertRaises(SystemExit):
            self.ui.get_game_mode()
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_game_mode_invalid_then_valid(self, mock_stdout, mock_input) -> None:
        """Test invalid game mode selection followed by valid."""
        # Arrange
        mock_input.side_effect = ['4', 'invalid', '1']
        
        # Act
        mode = self.ui.get_game_mode()
        
        # Assert
        self.assertEqual(mode, GameMode.HUMAN_VS_HUMAN)
        
        # Check error messages
        output = mock_stdout.getvalue()
        self.assertIn("❌ Invalid choice", output)
    
    @patch('builtins.input')
    def test_get_player_symbol_x(self, mock_input) -> None:
        """Test selecting X symbol."""
        # Arrange
        mock_input.return_value = '1'
        
        # Act
        symbol = self.ui.get_player_symbol()
        
        # Assert
        self.assertEqual(symbol, TicTacToe.PLAYER_X)
    
    @patch('builtins.input')
    def test_get_player_symbol_o(self, mock_input) -> None:
        """Test selecting O symbol."""
        # Arrange
        mock_input.return_value = '2'
        
        # Act
        symbol = self.ui.get_player_symbol()
        
        # Assert
        self.assertEqual(symbol, TicTacToe.PLAYER_O)
    
    @patch('builtins.input')
    def test_get_player_symbol_back_to_menu(self, mock_input) -> None:
        """Test going back to main menu from symbol selection."""
        # Arrange
        mock_input.return_value = '4'
        
        # Act
        symbol = self.ui.get_player_symbol()
        
        # Assert
        self.assertIsNone(symbol)
    
    @patch('builtins.input')
    @patch('random.choice')
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_player_symbol_random(self, mock_stdout, mock_choice, mock_input) -> None:
        """Test random symbol selection."""
        # Arrange
        mock_input.return_value = '3'
        mock_choice.return_value = TicTacToe.PLAYER_X
        
        # Act
        symbol = self.ui.get_player_symbol()
        
        # Assert
        self.assertEqual(symbol, TicTacToe.PLAYER_X)
        mock_choice.assert_called_once_with([TicTacToe.PLAYER_X, TicTacToe.PLAYER_O])
        
        # Check random choice message
        output = mock_stdout.getvalue()
        self.assertIn("Random choice: You are player X", output)
    
    @patch('builtins.input')
    def test_get_ai_difficulty_easy(self, mock_input) -> None:
        """Test selecting easy AI difficulty."""
        # Arrange
        mock_input.return_value = '1'
        
        # Act
        difficulty = self.ui.get_ai_difficulty()
        
        # Assert
        self.assertEqual(difficulty, DifficultyLevel.EASY)
    
    @patch('builtins.input')
    def test_get_ai_difficulty_medium(self, mock_input) -> None:
        """Test selecting medium AI difficulty."""
        # Arrange
        mock_input.return_value = '2'
        
        # Act
        difficulty = self.ui.get_ai_difficulty()
        
        # Assert
        self.assertEqual(difficulty, DifficultyLevel.MEDIUM)
    
    @patch('builtins.input')
    def test_get_ai_difficulty_hard(self, mock_input) -> None:
        """Test selecting hard AI difficulty."""
        # Arrange
        mock_input.return_value = '3'
        
        # Act
        difficulty = self.ui.get_ai_difficulty()
        
        # Assert
        self.assertEqual(difficulty, DifficultyLevel.HARD)
    
    @patch('builtins.input')
    def test_get_ai_difficulty_keyboard_interrupt(self, mock_input) -> None:
        """Test handling KeyboardInterrupt during difficulty selection."""
        # Arrange
        mock_input.side_effect = KeyboardInterrupt()
        
        # Act & Assert
        with self.assertRaises(SystemExit):
            self.ui.get_ai_difficulty()
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_ai_difficulty_invalid_then_valid(self, mock_stdout, mock_input) -> None:
        """Test invalid difficulty selection followed by valid."""
        # Arrange
        mock_input.side_effect = ['4', 'invalid', '2']
        
        # Act
        difficulty = self.ui.get_ai_difficulty()
        
        # Assert
        self.assertEqual(difficulty, DifficultyLevel.MEDIUM)
        output = mock_stdout.getvalue()
        self.assertIn("❌ Invalid choice", output)
    
    @patch('builtins.input')
    def test_get_player_symbol_keyboard_interrupt(self, mock_input) -> None:
        """Test handling KeyboardInterrupt during symbol selection."""
        # Arrange
        mock_input.side_effect = KeyboardInterrupt()
        
        # Act & Assert
        with self.assertRaises(SystemExit):
            self.ui.get_player_symbol()
    
    @patch('builtins.input')
    @patch('random.choice')
    def test_get_player_symbol_random_choice_o(self, mock_choice, mock_input) -> None:
        """Test random symbol selection choosing O."""
        # Arrange
        mock_input.return_value = '3'
        mock_choice.return_value = TicTacToe.PLAYER_O
        
        # Act
        symbol = self.ui.get_player_symbol()
        
        # Assert
        self.assertEqual(symbol, TicTacToe.PLAYER_O)


class TestTerminalUIEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.ui = TerminalUI()
        self.mock_game = Mock(spec=TicTacToe)
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_valid_position_empty_input(self, mock_stdout, mock_input) -> None:
        """Test handling empty input for position."""
        # Arrange
        mock_input.side_effect = ['', '  ', '5']
        self.mock_game.current_player = 'X'
        self.mock_game.is_valid_move.return_value = True
        
        # Act
        position = self.ui.get_valid_position(self.mock_game)
        
        # Assert
        self.assertEqual(position, 5)
        
        # Check error messages for empty input
        output = mock_stdout.getvalue()
        self.assertIn("❌ Please enter a position", output)
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_valid_position_zero_and_negative(self, mock_stdout, mock_input) -> None:
        """Test handling zero and negative position input."""
        # Arrange
        mock_input.side_effect = ['0', '-1', '5']
        self.mock_game.current_player = 'X'
        self.mock_game.is_valid_move.return_value = True
        
        # Act
        position = self.ui.get_valid_position(self.mock_game)
        
        # Assert
        self.assertEqual(position, 5)
        
        # Check error messages
        output = mock_stdout.getvalue()
        self.assertEqual(output.count("❌ Position must be between 1 and 9"), 2)
    
    @patch('builtins.input')
    def test_eof_error_handling(self, mock_input) -> None:
        """Test handling EOFError (Ctrl+D on Unix)."""
        # Arrange
        self.mock_game.current_player = 'X'  # <-- ADD THIS LINE
        mock_input.side_effect = EOFError()
        
        # Act & Assert
        with self.assertRaises(SystemExit):
            self.ui.get_valid_position(self.mock_game)
    
    def test_display_game_result_unknown_state(self) -> None:
        """Test displaying result with unknown game state."""
        # Arrange
        game_state = {'state': 'unknown', 'winner': None}
        
        # Act & Assert (should not raise exception)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.ui.display_game_result(game_state)
            output = mock_stdout.getvalue()
            self.assertIn("Game ended unexpectedly", output)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
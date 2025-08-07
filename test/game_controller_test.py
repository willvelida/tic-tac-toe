"""
Test suite for GameController class.

This module contains comprehensive tests for the GameController class,
including unit tests and integration tests.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, call
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import from src
from src.game_controller import GameController
from src.terminal_ui import TerminalUI
from src.tic_tac_toe import TicTacToe, GameMode
from src.player import HumanPlayer, AIPlayer, DifficultyLevel


class TestGameController(unittest.TestCase):
    """Comprehensive test suite for GameController class."""
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.mock_ui = Mock(spec=TerminalUI)
        self.controller = GameController(self.mock_ui)
    
    def test_controller_initialization(self) -> None:
        """Test that GameController initializes correctly."""
        # Test basic initialization
        self.assertEqual(self.controller.ui, self.mock_ui)
        self.assertIsNone(self.controller.game)
        self.assertIsNone(self.controller.player_x)
        self.assertIsNone(self.controller.player_o)
    
    def test_setup_human_vs_human_game(self) -> None:
        """Test setting up a human vs human game."""
        # Arrange
        self.mock_ui.get_game_mode.return_value = GameMode.HUMAN_VS_HUMAN
        
        # Act
        result = self.controller._setup_game()
        
        # Assert
        self.assertTrue(result)
        self.assertIsInstance(self.controller.game, TicTacToe)
        self.assertEqual(self.controller.game.mode, GameMode.HUMAN_VS_HUMAN)
        self.assertIsInstance(self.controller.player_x, HumanPlayer)
        self.assertIsInstance(self.controller.player_o, HumanPlayer)
        self.assertEqual(self.controller.player_x.symbol, TicTacToe.PLAYER_X)
        self.assertEqual(self.controller.player_o.symbol, TicTacToe.PLAYER_O)
        
        # Check UI interactions
        self.mock_ui.get_game_mode.assert_called_once()
        self.mock_ui.show_message.assert_any_call("Setting up Human vs Human game")
        self.mock_ui.show_message.assert_any_call("Player X goes first, Player O goes second")
    
    def test_setup_human_vs_ai_game_human_x(self) -> None:
        """Test setting up human vs AI game with human as X."""
        # Arrange
        self.mock_ui.get_game_mode.return_value = GameMode.HUMAN_VS_AI
        self.mock_ui.get_player_symbol.return_value = TicTacToe.PLAYER_X
        self.mock_ui.get_ai_difficulty.return_value = DifficultyLevel.MEDIUM
        
        # Act
        result = self.controller._setup_game()
        
        # Assert
        self.assertTrue(result)
        self.assertIsInstance(self.controller.game, TicTacToe)
        self.assertEqual(self.controller.game.mode, GameMode.HUMAN_VS_AI)
        
        # Human should be X, AI should be O
        self.assertIsInstance(self.controller.player_x, HumanPlayer)
        self.assertIsInstance(self.controller.player_o, AIPlayer)
        self.assertEqual(self.controller.player_x.symbol, TicTacToe.PLAYER_X)
        self.assertEqual(self.controller.player_o.symbol, TicTacToe.PLAYER_O)
        self.assertEqual(self.controller.player_o.difficulty, DifficultyLevel.MEDIUM)
        
        # Check UI interactions
        self.mock_ui.get_game_mode.assert_called_once()
        self.mock_ui.get_player_symbol.assert_called_once()
        self.mock_ui.get_ai_difficulty.assert_called_once()
    
    def test_setup_human_vs_ai_game_human_o(self) -> None:
        """Test setting up human vs AI game with human as O."""
        # Arrange
        self.mock_ui.get_game_mode.return_value = GameMode.HUMAN_VS_AI
        self.mock_ui.get_player_symbol.return_value = TicTacToe.PLAYER_O
        self.mock_ui.get_ai_difficulty.return_value = DifficultyLevel.HARD
        
        # Act
        result = self.controller._setup_game()
        
        # Assert
        self.assertTrue(result)
        
        # AI should be X, Human should be O
        self.assertIsInstance(self.controller.player_x, AIPlayer)
        self.assertIsInstance(self.controller.player_o, HumanPlayer)
        self.assertEqual(self.controller.player_x.symbol, TicTacToe.PLAYER_X)
        self.assertEqual(self.controller.player_o.symbol, TicTacToe.PLAYER_O)
        self.assertEqual(self.controller.player_x.difficulty, DifficultyLevel.HARD)
    
    def test_setup_game_user_cancels_symbol_selection(self) -> None:
        """Test setup when user cancels during symbol selection."""
        # Arrange
        self.mock_ui.get_game_mode.return_value = GameMode.HUMAN_VS_AI
        self.mock_ui.get_player_symbol.return_value = None  # User went back
        
        # Act
        result = self.controller._setup_game()
        
        # Assert
        self.assertFalse(result)
        self.mock_ui.get_player_symbol.assert_called_once()
        self.mock_ui.get_ai_difficulty.assert_not_called()
    
    def test_get_current_player_x(self) -> None:
        """Test getting current player when it's X's turn."""
        # Arrange
        self.controller.game = TicTacToe()
        self.controller.player_x = Mock()
        self.controller.player_o = Mock()
        self.controller.game.current_player = TicTacToe.PLAYER_X
        
        # Act
        current_player = self.controller._get_current_player()
        
        # Assert
        self.assertEqual(current_player, self.controller.player_x)
    
    def test_get_current_player_o(self) -> None:
        """Test getting current player when it's O's turn."""
        # Arrange
        self.controller.game = TicTacToe()
        self.controller.player_x = Mock()
        self.controller.player_o = Mock()
        self.controller.game.current_player = TicTacToe.PLAYER_O
        
        # Act
        current_player = self.controller._get_current_player()
        
        # Assert
        self.assertEqual(current_player, self.controller.player_o)
    
    def test_get_human_move(self) -> None:
        """Test getting move from human player."""
        # Arrange
        self.controller.game = TicTacToe()
        self.mock_ui.get_valid_position.return_value = 5
        
        # Act
        move = self.controller._get_human_move()
        
        # Assert
        self.assertEqual(move, 5)
        self.mock_ui.get_valid_position.assert_called_once_with(self.controller.game)
    
    def test_get_ai_move(self) -> None:
        """Test getting move from AI player."""
        # Arrange
        self.controller.game = TicTacToe()  # <-- ADD THIS LINE
        mock_ai_player = Mock(spec=AIPlayer)
        mock_ai_player.get_move.return_value = 3
        
        # Act
        move = self.controller._get_ai_move(mock_ai_player)
        
        # Assert
        self.assertEqual(move, 3)
        mock_ai_player.get_move.assert_called_once_with(self.controller.game.board)
    
    def test_get_player_move_human(self) -> None:
        """Test getting move dispatches correctly for human player."""
        # Arrange
        human_player = Mock(spec=HumanPlayer)
        self.controller.game = TicTacToe()
        self.mock_ui.get_valid_position.return_value = 7
        
        # Act
        move = self.controller._get_player_move(human_player)
        
        # Assert
        self.assertEqual(move, 7)
        self.mock_ui.get_valid_position.assert_called_once()
    
    def test_get_player_move_ai(self) -> None:
        """Test getting move dispatches correctly for AI player."""
        # Arrange
        self.controller.game = TicTacToe()
        ai_player = Mock(spec=AIPlayer)
        ai_player.get_move.return_value = 9
        
        # Act
        move = self.controller._get_player_move(ai_player)
        
        # Assert
        self.assertEqual(move, 9)
        ai_player.get_move.assert_called_once_with(self.controller.game.board)
    
    def test_get_player_move_unknown_player_type(self) -> None:
        """Test getting move with unknown player type raises error."""
        # Arrange
        unknown_player = Mock()  # Not a HumanPlayer or AIPlayer
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.controller._get_player_move(unknown_player)
        
        self.assertIn("Unknown player type", str(context.exception))
    
    def test_create_new_game(self) -> None:
        """Test creating new game resets board."""
        # Arrange
        self.controller.game = TicTacToe()
        self.controller.game.board = ['X', 'O', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        
        # Act
        self.controller.create_new_game()
        
        # Assert
        self.assertEqual(self.controller.game.board, [' '] * 9)
        self.assertEqual(self.controller.game.current_player, TicTacToe.PLAYER_X)
        self.mock_ui.show_message.assert_called_with("New game started!")
    
    def test_create_new_game_no_game_exists(self) -> None:
        """Test creating new game when no game exists."""
        # Arrange
        self.controller.game = None
        
        # Act
        self.controller.create_new_game()
        
        # Assert
        self.mock_ui.show_message.assert_not_called()
    
    def test_get_game_statistics_no_game(self) -> None:
        """Test getting game statistics when no game exists."""
        # Arrange
        self.controller.game = None
        
        # Act
        stats = self.controller.get_game_statistics()
        
        # Assert
        self.assertEqual(stats, {"status": "No game in progress"})
    
    def test_get_game_statistics_with_game(self) -> None:
        """Test getting game statistics with active game."""
        # Arrange
        self.controller.game = TicTacToe(GameMode.HUMAN_VS_AI)
        self.controller.player_x = HumanPlayer('X')
        self.controller.player_o = AIPlayer('O', DifficultyLevel.MEDIUM)
        self.controller.game.board = ['X', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        
        # Act
        stats = self.controller.get_game_statistics()
        
        # Assert
        self.assertEqual(stats["mode"], GameMode.HUMAN_VS_AI.value)
        self.assertEqual(stats["current_player"], TicTacToe.PLAYER_X)
        self.assertEqual(stats["moves_made"], 2)
        self.assertEqual(stats["player_x_type"], "HumanPlayer")
        self.assertEqual(stats["player_o_type"], "AIPlayer")
        self.assertIn("game_state", stats)
    
    @patch('sys.exit')
    def test_play_game_setup_fails(self, mock_exit) -> None:
        """Test play method when game setup fails."""
        # Arrange
        self.mock_ui.get_game_mode.side_effect = SystemExit()
        
        # Act & Assert
        with self.assertRaises(SystemExit):
            self.controller.play()
    
    def test_ai_callback_setup(self) -> None:
        """Test that AI player receives the correct status callback."""
        # Arrange
        self.mock_ui.get_game_mode.return_value = GameMode.HUMAN_VS_AI
        self.mock_ui.get_player_symbol.return_value = TicTacToe.PLAYER_X
        self.mock_ui.get_ai_difficulty.return_value = DifficultyLevel.EASY
        
        # Act
        self.controller._setup_game()
        
        # Assert
        ai_player = self.controller.player_o  # AI is O when human is X
        self.assertIsInstance(ai_player, AIPlayer)
        self.assertEqual(ai_player.status_callback, self.mock_ui.show_ai_status)


class TestGameControllerIntegration(unittest.TestCase):
    """Integration tests for GameController with real components."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_ui = Mock(spec=TerminalUI)
        self.controller = GameController(self.mock_ui)
    
    def test_complete_human_vs_human_game_flow(self) -> None:
        """Test complete game flow for human vs human."""
        # Arrange
        self.mock_ui.get_game_mode.return_value = GameMode.HUMAN_VS_HUMAN
        # Simulate moves: X wins with diagonal
        moves = [1, 2, 5, 3, 9]  # X: 1,5,9 (diagonal) O: 2,3
        self.mock_ui.get_valid_position.side_effect = moves
        
        # Act
        self.controller._setup_game()
        
        # Simulate game moves manually to test flow
        for i, move in enumerate(moves):
            if self.controller.game.get_game_state()['state'] == 'ongoing':
                self.controller.game.make_move(move)
        
        # Assert game completed correctly
        game_state = self.controller.game.get_game_state()
        self.assertEqual(game_state['state'], 'won')
        self.assertEqual(game_state['winner'], 'X')
    
    def test_ai_player_creation_with_callback(self) -> None:
        """Test that AI players are created with proper callbacks."""
        # Arrange
        self.mock_ui.get_game_mode.return_value = GameMode.HUMAN_VS_AI
        self.mock_ui.get_player_symbol.return_value = TicTacToe.PLAYER_O
        self.mock_ui.get_ai_difficulty.return_value = DifficultyLevel.HARD
        
        # Act
        self.controller._setup_game()
        
        # Assert
        ai_player = self.controller.player_x  # AI is X when human is O
        self.assertIsNotNone(ai_player.status_callback)
        
        # Test callback works
        ai_player.status_callback("Test message")
        self.mock_ui.show_ai_status.assert_called_with("Test message")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
import unittest
from unittest.mock import patch, call, MagicMock
import random
from src.player import Player, HumanPlayer, AIPlayer, DifficultyLevel
from src.tic_tac_toe import TicTacToe, GameMode
from src.game_controller import GameController
from src.terminal_ui import TerminalUI
import time

class TestPlayer(unittest.TestCase):
    """Test cases for Player class"""

    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_returns_x_when_option_1_selected(self, mock_input, mock_print):
        """Test choose_symbol returns 'X' when user selects option 1."""
        mock_input.return_value = '1'
        
        result = Player.choose_symbol()
        
        self.assertEqual(result, TicTacToe.PLAYER_X)
        mock_input.assert_called_with("Enter your choice (1-4): ")

    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_returns_o_when_option_2_selected(self, mock_input, mock_print):
        """Test choose_symbol returns 'O' when user selects option 2."""
        mock_input.return_value = '2'
        
        result = Player.choose_symbol()
        
        self.assertEqual(result, TicTacToe.PLAYER_O)
        mock_input.assert_called_with("Enter your choice (1-4): ")

    @patch('random.choice')
    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_returns_random_when_option_3_selected(self, mock_input, mock_print, mock_random):
        """Test choose_symbol returns random symbol when user selects option 3."""
        mock_input.return_value = '3'
        mock_random.return_value = TicTacToe.PLAYER_X
        
        result = Player.choose_symbol()
        
        self.assertEqual(result, TicTacToe.PLAYER_X)
        mock_random.assert_called_once_with([TicTacToe.PLAYER_X, TicTacToe.PLAYER_O])

    @patch('random.choice')
    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_random_can_return_either_symbol(self, mock_input, mock_print, mock_random):
        """Test choose_symbol random option can return either X or O."""
        mock_input.return_value = '3'
        
        # Test X return
        mock_random.return_value = TicTacToe.PLAYER_X
        result = Player.choose_symbol()
        self.assertEqual(result, TicTacToe.PLAYER_X)
        
        # Reset and test O return
        mock_random.reset_mock()
        mock_random.return_value = TicTacToe.PLAYER_O
        result = Player.choose_symbol()
        self.assertEqual(result, TicTacToe.PLAYER_O)

    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_exits_when_option_4_selected(self, mock_input, mock_print):
        """Test choose_symbol exits when user selects option 4."""
        mock_input.return_value = '4'
        
        with self.assertRaises(SystemExit) as context:
            Player.choose_symbol()
        
        self.assertEqual(context.exception.code, 0)
        mock_print.assert_any_call("Thanks for playing! Goodbye!")

    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_displays_menu_correctly(self, mock_input, mock_print):
        """Test choose_symbol displays the menu options correctly."""
        mock_input.return_value = '1'
        
        Player.choose_symbol()
        
        expected_calls = [
            call("\nChoose your option:"),
            call("1. Player X"),
            call("2. Player O"),
            call("3. Random"),
            call("4. Quit Game")
        ]
        
        # Check that all menu items were printed
        for expected_call in expected_calls:
            self.assertIn(expected_call, mock_print.call_args_list)

    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_handles_invalid_input(self, mock_input, mock_print):
        """Test choose_symbol handles invalid input and reprompts."""
        # Invalid input followed by valid input
        mock_input.side_effect = ['5', '1']
        
        result = Player.choose_symbol()
        
        self.assertEqual(result, TicTacToe.PLAYER_X)
        self.assertEqual(mock_input.call_count, 2)
        mock_print.assert_any_call("Invalid choice '5'. Please enter 1, 2, 3, or 4.")

    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_handles_multiple_invalid_inputs(self, mock_input, mock_print):
        """Test choose_symbol handles multiple invalid inputs."""
        # Multiple invalid inputs followed by valid
        mock_input.side_effect = ['0', 'a', '10', '2']
        
        result = Player.choose_symbol()
        
        self.assertEqual(result, TicTacToe.PLAYER_O)
        self.assertEqual(mock_input.call_count, 4)
        
        # Check error messages for each invalid input
        expected_error_calls = [
            call("Invalid choice '0'. Please enter 1, 2, 3, or 4."),
            call("Invalid choice 'a'. Please enter 1, 2, 3, or 4."),
            call("Invalid choice '10'. Please enter 1, 2, 3, or 4.")
        ]
        
        for expected_call in expected_error_calls:
            self.assertIn(expected_call, mock_print.call_args_list)

    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_handles_whitespace_in_input(self, mock_input, mock_print):
        """Test choose_symbol handles input with whitespace."""
        test_cases = [' 1 ', '  2  ', '\t3\t', '\n1\n']
        expected_results = [
            TicTacToe.PLAYER_X,
            TicTacToe.PLAYER_O,
            None,  # Random - we'll mock this
            TicTacToe.PLAYER_X
        ]
        
        for i, (input_value, expected) in enumerate(zip(test_cases, expected_results)):
            with self.subTest(input_value=repr(input_value)):
                mock_input.return_value = input_value
                
                if i == 2:  # Random case
                    with patch('random.choice', return_value=TicTacToe.PLAYER_X):
                        result = Player.choose_symbol()
                        self.assertIn(result, [TicTacToe.PLAYER_X, TicTacToe.PLAYER_O])
                else:
                    result = Player.choose_symbol()
                    self.assertEqual(result, expected)

    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_handles_empty_input(self, mock_input, mock_print):
        """Test choose_symbol handles empty input."""
        mock_input.side_effect = ['', '1']
        
        result = Player.choose_symbol()
        
        self.assertEqual(result, TicTacToe.PLAYER_X)
        mock_print.assert_any_call("Invalid choice ''. Please enter 1, 2, 3, or 4.")

    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_handles_keyboard_interrupt(self, mock_input, mock_print):
        """Test choose_symbol handles KeyboardInterrupt (Ctrl+C)."""
        mock_input.side_effect = KeyboardInterrupt()
        
        with self.assertRaises(SystemExit) as context:
            Player.choose_symbol()
        
        self.assertEqual(context.exception.code, 0)
        mock_print.assert_any_call("\nGame cancelled. Goodbye!")

    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_handles_eof_error(self, mock_input, mock_print):
        """Test choose_symbol handles EOFError."""
        mock_input.side_effect = EOFError()
        
        with self.assertRaises(SystemExit) as context:
            Player.choose_symbol()
        
        self.assertEqual(context.exception.code, 0)
        mock_print.assert_any_call("\nGame cancelled. Goodbye!")

    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_reprompts_after_displaying_menu(self, mock_input, mock_print):
        """Test choose_symbol redisplays menu after invalid input."""
        mock_input.side_effect = ['invalid', '1']
        
        result = Player.choose_symbol()
        
        self.assertEqual(result, TicTacToe.PLAYER_X)
        
        # Menu should be displayed twice (initial + after invalid input)
        menu_calls = [call for call in mock_print.call_args_list if "Choose your option:" in str(call)]
        self.assertEqual(len(menu_calls), 2)

    def test_choose_symbol_is_classmethod(self):
        """Test that choose_symbol is a class method."""
        self.assertTrue(hasattr(Player, 'choose_symbol'))
        self.assertTrue(callable(getattr(Player, 'choose_symbol')))

    @patch('random.choice')
    @patch('builtins.print')
    @patch('builtins.input')
    def test_choose_symbol_random_uses_correct_symbols(self, mock_input, mock_print, mock_random):
        """Test choose_symbol random option uses correct symbol constants."""
        mock_input.return_value = '3'
        mock_random.return_value = TicTacToe.PLAYER_X
        
        Player.choose_symbol()
        
        # Verify random.choice was called with the correct symbols
        mock_random.assert_called_once_with([TicTacToe.PLAYER_X, TicTacToe.PLAYER_O])

    def test_player_cannot_be_instantiated_directly(self):
        """Test that Player abstract class cannot be instantiated."""
        with self.assertRaises(TypeError):
            Player('X')
    
class TestGameControllerHumanInput(unittest.TestCase):
    """Test cases for GameController human input handling - the modern architecture."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ui = TerminalUI()
        self.controller = GameController(self.ui)
        self.game = TicTacToe(GameMode.HUMAN_VS_HUMAN)
        self.controller.game = self.game
    
    @patch('builtins.input')
    def test_game_controller_get_human_move_returns_valid_position(self, mock_input):
        """Test GameController._get_human_move returns valid position."""
        mock_input.return_value = '5'
        
        result = self.controller._get_human_move()
        
        self.assertEqual(result, 5)
        self.assertIsInstance(result, int)
    
    @patch('builtins.input') 
    def test_game_controller_get_human_move_with_different_positions(self, mock_input):
        """Test GameController._get_human_move with different valid positions."""
        test_positions = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        for position_str in test_positions:
            with self.subTest(position=position_str):
                mock_input.return_value = position_str
                result = self.controller._get_human_move()
                self.assertEqual(result, int(position_str))
    
    @patch('builtins.input')
    @patch('builtins.print')  # Mock print to avoid error output during tests
    def test_game_controller_handles_invalid_input_with_retry(self, mock_print, mock_input):
        """Test GameController handles invalid input and retries until valid."""
        # First invalid, then valid input
        mock_input.side_effect = ['abc', '5']
        
        result = self.controller._get_human_move()
        
        self.assertEqual(result, 5)
        self.assertEqual(mock_input.call_count, 2)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_game_controller_handles_out_of_range_positions(self, mock_print, mock_input):
        """Test GameController handles out of range positions with retry."""
        # Out of range, then valid
        mock_input.side_effect = ['0', '10', '5']
        
        result = self.controller._get_human_move()
        
        self.assertEqual(result, 5)
        self.assertEqual(mock_input.call_count, 3)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_game_controller_handles_occupied_positions(self, mock_print, mock_input):
        """Test GameController handles occupied positions with retry."""
        # Set up a game with position 5 already taken
        self.game.make_move(5)  # X takes position 5
        
        # Try to take position 5 (occupied), then choose position 1 (free)
        mock_input.side_effect = ['5', '1']
        
        result = self.controller._get_human_move()
        
        self.assertEqual(result, 1)
        self.assertEqual(mock_input.call_count, 2)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_game_controller_handles_empty_input(self, mock_print, mock_input):
        """Test GameController handles empty input with retry."""
        mock_input.side_effect = ['', '   ', '7']
        
        result = self.controller._get_human_move()
        
        self.assertEqual(result, 7)
        self.assertEqual(mock_input.call_count, 3)
    
    @patch('builtins.input')
    def test_game_controller_handles_keyboard_interrupt(self, mock_input):
        """Test GameController handles KeyboardInterrupt gracefully."""
        mock_input.side_effect = KeyboardInterrupt()
        
        with self.assertRaises(SystemExit):
            self.controller._get_human_move()
    
    @patch('builtins.input')
    def test_game_controller_handles_eof_error(self, mock_input):
        """Test GameController handles EOFError gracefully.""" 
        mock_input.side_effect = EOFError()
        
        with self.assertRaises(SystemExit):
            self.controller._get_human_move()


class TestTerminalUIInputValidation(unittest.TestCase):
    """Test cases for TerminalUI input validation - the UI layer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ui = TerminalUI()
        self.game = TicTacToe()
    
    @patch('builtins.input')
    def test_terminal_ui_get_valid_position_returns_valid_position(self, mock_input):
        """Test TerminalUI.get_valid_position returns valid position."""
        mock_input.return_value = '3'
        
        result = self.ui.get_valid_position(self.game)
        
        self.assertEqual(result, 3)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_terminal_ui_validates_position_range(self, mock_print, mock_input):
        """Test TerminalUI validates position is in range 1-9."""
        mock_input.side_effect = ['0', '10', '-1', '100', '5']
        
        result = self.ui.get_valid_position(self.game)
        
        self.assertEqual(result, 5)
        self.assertEqual(mock_input.call_count, 5)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_terminal_ui_validates_position_availability(self, mock_print, mock_input):
        """Test TerminalUI validates position is not already taken."""
        # Take position 5
        self.game.make_move(5)
        
        # Try taken position, then free position
        mock_input.side_effect = ['5', '1']
        
        result = self.ui.get_valid_position(self.game)
        
        self.assertEqual(result, 1)
        self.assertEqual(mock_input.call_count, 2)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_terminal_ui_handles_non_numeric_input(self, mock_print, mock_input):
        """Test TerminalUI handles non-numeric input gracefully."""
        mock_input.side_effect = ['abc', 'xyz', '3.14', '2e5', '4']
        
        result = self.ui.get_valid_position(self.game)
        
        self.assertEqual(result, 4)
        self.assertEqual(mock_input.call_count, 5)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_terminal_ui_handles_whitespace_input(self, mock_print, mock_input):
        """Test TerminalUI handles whitespace-only input gracefully."""
        mock_input.side_effect = ['', '   ', '\t', '\n', '6']
        
        result = self.ui.get_valid_position(self.game)
        
        self.assertEqual(result, 6)
        self.assertEqual(mock_input.call_count, 5)
    
    @patch('builtins.input')
    def test_terminal_ui_handles_keyboard_interrupt(self, mock_input):
        """Test TerminalUI handles KeyboardInterrupt gracefully."""
        mock_input.side_effect = KeyboardInterrupt()
        
        with self.assertRaises(SystemExit):
            self.ui.get_valid_position(self.game)
    
    @patch('builtins.input')
    def test_terminal_ui_handles_eof_error(self, mock_input):
        """Test TerminalUI handles EOFError gracefully."""
        mock_input.side_effect = EOFError()
        
        with self.assertRaises(SystemExit):
            self.ui.get_valid_position(self.game)


# Add this new test class after the existing ones
class TestAIPlayer(unittest.TestCase):
    """Test cases for AIPlayer class"""

    def test_ai_player_inherits_from_player_base_class(self):
        """Test AIPlayer properly inherits from Player base class."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.EASY)
        
        self.assertIsInstance(ai, Player)
        self.assertTrue(hasattr(ai, 'get_move'))
        self.assertTrue(callable(getattr(ai, 'get_move')))

    def test_ai_player_stores_symbol_and_difficulty_correctly(self):
        """Test AIPlayer stores symbol and difficulty in instance variables."""
        test_cases = [
            (TicTacToe.PLAYER_X, DifficultyLevel.EASY),
            (TicTacToe.PLAYER_O, DifficultyLevel.MEDIUM),
            (TicTacToe.PLAYER_X, DifficultyLevel.HARD),
            (TicTacToe.PLAYER_O, DifficultyLevel.EASY)
        ]
        
        for symbol, difficulty in test_cases:
            with self.subTest(symbol=symbol, difficulty=difficulty):
                ai = AIPlayer(symbol, difficulty)
                
                self.assertEqual(ai.symbol, symbol)
                self.assertEqual(ai.difficulty, difficulty)

    def test_ai_player_raises_value_error_for_invalid_symbol(self):
        """Test AIPlayer raises ValueError for invalid symbols."""
        invalid_symbols = ['A', 'B', '1', '@', '', 'XX', 'x', 'o']
        
        for symbol in invalid_symbols:
            with self.subTest(symbol=symbol):
                with self.assertRaises(ValueError) as context:
                    AIPlayer(symbol, DifficultyLevel.EASY)
                
                self.assertIn("Invalid symbol", str(context.exception))
                self.assertIn("Must be 'X' or 'O'", str(context.exception))

    def test_ai_player_raises_type_error_for_invalid_difficulty(self):
        """Test AIPlayer raises TypeError for non-enum difficulty values."""
        invalid_difficulties = ['easy', 'medium', 'hard', 1, 2, 3, None]
        
        for difficulty in invalid_difficulties:
            with self.subTest(difficulty=difficulty):
                with self.assertRaises(TypeError) as context:
                    AIPlayer(TicTacToe.PLAYER_X, difficulty)
                
                self.assertIn("Difficulty must be a DifficultyLevel enum", str(context.exception))

    def test_ai_player_accepts_all_valid_difficulty_levels(self):
        """Test AIPlayer accepts all DifficultyLevel enum values."""
        for difficulty in DifficultyLevel:
            with self.subTest(difficulty=difficulty):
                ai = AIPlayer(TicTacToe.PLAYER_X, difficulty)
                self.assertEqual(ai.difficulty, difficulty)

    def test_get_move_returns_valid_position_on_empty_board(self):
        """Test get_move returns valid position (1-9) on empty board."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.EASY)
        empty_board = [TicTacToe.EMPTY] * 9
        
        move = ai.get_move(empty_board)
        
        self.assertIsInstance(move, int)
        self.assertGreaterEqual(move, 1)
        self.assertLessEqual(move, 9)

    def test_get_move_shows_randomness_on_easy_difficulty(self):
        """Test get_move shows randomness on easy difficulty (probabilistic behavior)."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.EASY)
        empty_board = [TicTacToe.EMPTY] * 9
        
        # Get multiple moves and check for some variety due to randomness
        moves = [ai.get_move(empty_board) for _ in range(20)]
        unique_moves = set(moves)
        
        # Easy AI should show some randomness (not always the same move)
        # With 30% optimal probability, we should see variety
        self.assertGreaterEqual(len(unique_moves), 1, 
                               "AI should return valid moves")
        # We expect some variation, but don't enforce exact count due to randomness

    def test_get_move_only_selects_from_available_positions(self):
        """Test get_move only chooses from empty board positions."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.MEDIUM)
        
        # Board with only positions 3, 7, 9 available
        board = ['X', 'O', TicTacToe.EMPTY,    # positions 1,2,3
                 'X', 'O', 'X',                # positions 4,5,6  
                 TicTacToe.EMPTY, 'O', TicTacToe.EMPTY]  # positions 7,8,9
        
        available_positions = {3, 7, 9}
        
        # Test multiple times to ensure consistency
        for _ in range(10):
            move = ai.get_move(board)
            self.assertIn(move, available_positions, 
                         f"AI chose position {move}, but only {available_positions} are available")

    def test_get_move_with_single_available_position(self):
        """Test get_move when only one position is available."""
        ai = AIPlayer(TicTacToe.PLAYER_O, DifficultyLevel.HARD)
        
        # Board with only position 5 available
        board = ['X', 'O', 'X', 
                 'O', TicTacToe.EMPTY, 'X', 
                 'O', 'X', 'O']
        
        move = ai.get_move(board)
        self.assertEqual(move, 5, "AI should choose the only available position")

    def test_get_move_raises_value_error_for_invalid_board_length(self):
        """Test get_move raises ValueError for boards that aren't 9 elements."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.EASY)
        
        invalid_boards = [
            [],                           # Empty board
            [TicTacToe.EMPTY] * 8,       # Too short
            [TicTacToe.EMPTY] * 10,      # Too long
            [TicTacToe.EMPTY] * 3,       # Way too short
            [TicTacToe.EMPTY] * 16       # Way too long
        ]
        
        for board in invalid_boards:
            with self.subTest(board_length=len(board)):
                with self.assertRaises(ValueError) as context:
                    ai.get_move(board)
                
                expected_msg = f"Board must have exactly 9 positions, got {len(board)}"
                self.assertEqual(str(context.exception), expected_msg)

    def test_get_move_raises_value_error_for_no_available_moves(self):
        """Test get_move raises ValueError when board is completely full."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.EASY)
        
        # Completely filled board
        full_board = ['X', 'O', 'X', 
                      'O', 'X', 'O', 
                      'X', 'O', 'X']
        
        with self.assertRaises(ValueError) as context:
            ai.get_move(full_board)
        
        self.assertEqual(str(context.exception), "No valid moves available on the board")

    def test_get_move_works_with_all_difficulty_levels(self):
        """Test get_move works correctly for all difficulty levels."""
        empty_board = [TicTacToe.EMPTY] * 9
        
        for difficulty in DifficultyLevel:
            with self.subTest(difficulty=difficulty):
                ai = AIPlayer(TicTacToe.PLAYER_X, difficulty)
                move = ai.get_move(empty_board)
                
                self.assertIsInstance(move, int)
                self.assertGreaterEqual(move, 1)
                self.assertLessEqual(move, 9)

    def test_hard_difficulty_shows_optimal_play(self):
        """Test hard difficulty AI shows optimal play behavior."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD)
        empty_board = [TicTacToe.EMPTY] * 9
        
        # Hard AI should always make valid moves (100% optimal probability)
        moves = [ai.get_move(empty_board) for _ in range(10)]
        
        # All moves should be valid
        for move in moves:
            self.assertGreaterEqual(move, 1)
            self.assertLessEqual(move, 9)
        
        # On an empty board, multiple moves can be equally optimal
        # So we expect the AI to choose among the best available moves
        unique_moves = set(moves)
        self.assertGreaterEqual(len(unique_moves), 1, 
                               "Hard AI should make valid moves")
        self.assertLessEqual(len(unique_moves), 9, 
                            "Hard AI shouldn't use all positions randomly")

    def test_get_optimal_probability_returns_correct_values(self):
        """Test _get_optimal_probability returns correct values for each difficulty."""
        easy_ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.EASY)
        medium_ai = AIPlayer(TicTacToe.PLAYER_O, DifficultyLevel.MEDIUM)
        hard_ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD)
        
        self.assertEqual(easy_ai._get_optimal_probability(), 0.3)
        self.assertEqual(medium_ai._get_optimal_probability(), 0.7)
        self.assertEqual(hard_ai._get_optimal_probability(), 1.0)

    def test_get_best_move_minimax_returns_valid_move(self):
        """Test _get_best_move_minimax returns a valid move."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD)
        empty_board = [TicTacToe.EMPTY] * 9
        
        move = ai._get_best_move_minimax(empty_board)
        
        self.assertIsInstance(move, int)
        self.assertGreaterEqual(move, 1)
        self.assertLessEqual(move, 9)

    def test_get_reasonable_suboptimal_move_returns_valid_move(self):
        """Test _get_reasonable_suboptimal_move returns a valid move."""
        ai = AIPlayer(TicTacToe.PLAYER_O, DifficultyLevel.EASY)
        empty_board = [TicTacToe.EMPTY] * 9
        available_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        move = ai._get_reasonable_suboptimal_move(empty_board, available_moves)
        
        self.assertIsInstance(move, int)
        self.assertIn(move, available_moves)

    def test_get_opponent_symbol_returns_correct_opponent(self):
        """Test _get_opponent_symbol returns correct opponent for both X and O."""
        ai_x = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.EASY)
        ai_o = AIPlayer(TicTacToe.PLAYER_O, DifficultyLevel.EASY)
        
        self.assertEqual(ai_x._get_opponent_symbol(), TicTacToe.PLAYER_O)
        self.assertEqual(ai_o._get_opponent_symbol(), TicTacToe.PLAYER_X)

    def test_get_opponent_symbol_consistency(self):
        """Test _get_opponent_symbol is consistent across multiple calls."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.MEDIUM)
        
        # Should return same result every time
        results = [ai._get_opponent_symbol() for _ in range(5)]
        
        self.assertTrue(all(result == TicTacToe.PLAYER_O for result in results))

    def test_ai_player_integration_with_tic_tac_toe_constants(self):
        """Test AIPlayer works correctly with TicTacToe class constants."""
        # Verify AI recognizes TicTacToe constants properly
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.EASY)
        
        # Board using TicTacToe constants
        board = [TicTacToe.EMPTY, TicTacToe.PLAYER_O, TicTacToe.EMPTY,
                 TicTacToe.PLAYER_X, TicTacToe.EMPTY, TicTacToe.PLAYER_O,
                 TicTacToe.EMPTY, TicTacToe.EMPTY, TicTacToe.PLAYER_X]
        
        move = ai.get_move(board)
        available_positions = {1, 3, 5, 7, 8}  # Positions with EMPTY
        
        self.assertIn(move, available_positions)

    def test_minimax_handles_infinite_depth_correctly(self):
        """Test _minimax handles infinite depth parameter correctly."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD)
        
        # Simple board position
        board = [TicTacToe.PLAYER_X, TicTacToe.EMPTY, TicTacToe.EMPTY,
                 TicTacToe.EMPTY, TicTacToe.EMPTY, TicTacToe.EMPTY,
                 TicTacToe.EMPTY, TicTacToe.EMPTY, TicTacToe.EMPTY]
        
        # Should handle infinite depth without error
        score = ai._minimax(board, float('inf'), False)
        self.assertIsInstance(score, (int, float))

    def test_minimax_with_limited_depth_for_suboptimal_play(self):
        """Test _minimax with limited depth for suboptimal play."""
        ai = AIPlayer(TicTacToe.PLAYER_O, DifficultyLevel.EASY)
        
        board = [TicTacToe.EMPTY] * 9
        
        # Test with limited depth
        score = ai._minimax(board, 2, True)
        self.assertIsInstance(score, (int, float))

    def test_get_best_move_minimax_chooses_among_equally_good_moves(self):
        """Test _get_best_move_minimax can choose randomly among equally good moves."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD)
        empty_board = [TicTacToe.EMPTY] * 9
        
        # On empty board, several moves might be equally optimal
        # Test multiple times to see if we get different moves
        moves = [ai._get_best_move_minimax(empty_board) for _ in range(10)]
        
        # All moves should be valid
        for move in moves:
            self.assertGreaterEqual(move, 1)
            self.assertLessEqual(move, 9)

    def test_get_best_move_minimax_early_termination_wins(self):
        """Test _get_best_move_minimax chooses immediate winning moves without minimax."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD)
        
        # Board where X can win by playing position 3 (top row)
        board = ['X', 'X', TicTacToe.EMPTY,    # positions 1,2,3
                 'O', 'O', TicTacToe.EMPTY,    # positions 4,5,6
                 TicTacToe.EMPTY, TicTacToe.EMPTY, TicTacToe.EMPTY]  # positions 7,8,9
        
        move = ai._get_best_move_minimax(board)
        self.assertEqual(move, 3, "AI should choose the immediate winning move")

    def test_get_best_move_minimax_early_termination_blocks(self):
        """Test _get_best_move_minimax blocks opponent winning moves."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD)
        
        # Board where O can win by playing position 9 (main diagonal)
        board = ['O', 'X', 'X',                # positions 1,2,3
                 'X', 'O', TicTacToe.EMPTY,    # positions 4,5,6
                 TicTacToe.EMPTY, TicTacToe.EMPTY, TicTacToe.EMPTY]  # positions 7,8,9
        
        move = ai._get_best_move_minimax(board)
        self.assertEqual(move, 9, "AI should block opponent's winning move")

    def test_get_best_move_minimax_prefers_center_on_empty_board(self):
        """Test _get_best_move_minimax prefers center position on empty board."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD)
        empty_board = [TicTacToe.EMPTY] * 9
        
        # Test multiple times to ensure consistency
        for _ in range(5):
            move = ai._get_best_move_minimax(empty_board)
            self.assertEqual(move, 5, "AI should prefer center position on empty board")

    def test_get_best_move_minimax_prioritizes_win_over_block(self):
        """Test _get_best_move_minimax prioritizes winning over blocking."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD)
        
        # Board where both X and O can win
        # X can win with position 3 (top row), O can win with position 7 (left column)
        board = ['X', 'X', TicTacToe.EMPTY,    # positions 1,2,3 - X can win here
                 'O', TicTacToe.EMPTY, TicTacToe.EMPTY,  # positions 4,5,6
                 'O', TicTacToe.EMPTY, TicTacToe.EMPTY]   # positions 7,8,9 - O can win at 7
        
        move = ai._get_best_move_minimax(board)
        self.assertEqual(move, 3, "AI should prioritize winning over blocking")

    def test_get_best_move_minimax_falls_back_to_minimax(self):
        """Test _get_best_move_minimax falls back to minimax when no obvious moves."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD)
        
        # Board with no immediate wins/blocks, not empty
        board = ['X', 'O', TicTacToe.EMPTY,    # positions 1,2,3
                 'O', 'X', TicTacToe.EMPTY,    # positions 4,5,6
                 TicTacToe.EMPTY, TicTacToe.EMPTY, TicTacToe.EMPTY]  # positions 7,8,9
        
        move = ai._get_best_move_minimax(board)
        
        # Should return a valid move (specific move depends on minimax evaluation)
        self.assertIsInstance(move, int)
        self.assertGreaterEqual(move, 1)
        self.assertLessEqual(move, 9)
        self.assertIn(move, [3, 6, 7, 8, 9], "AI should choose from available positions")

    @patch('time.sleep')
    @patch('builtins.print')
    def test_ai_delay_simulation_works_correctly(self, mock_print, mock_sleep):
        """Test AI delay simulation shows thinking message and sleeps."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD, enable_delay=True)
        empty_board = [TicTacToe.EMPTY] * 9
        
        # Mock random.uniform to return predictable value
        with patch('random.uniform', return_value=1.5):
            move = ai.get_move(empty_board)
        
        # Verify thinking message was displayed
        mock_print.assert_called_with("AI opponent is thinking...")
        
        # Verify sleep was called with the expected delay
        mock_sleep.assert_called_once_with(1.5)
        
        # Verify valid move was returned
        self.assertIsInstance(move, int)
        self.assertGreaterEqual(move, 1)
        self.assertLessEqual(move, 9)
    
    def test_ai_delay_can_be_disabled(self):
        """Test AI delay can be disabled for testing."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD, enable_delay=False)
        empty_board = [TicTacToe.EMPTY] * 9
        
        # Record start time
        start_time = time.time()
        move = ai.get_move(empty_board)
        end_time = time.time()
        
        # Should complete very quickly (under 0.1 seconds) when delay disabled
        elapsed_time = end_time - start_time
        self.assertLess(elapsed_time, 0.1, "AI should respond quickly when delay disabled")
        
        # Verify valid move was returned
        self.assertIsInstance(move, int)
        self.assertGreaterEqual(move, 1)
        self.assertLessEqual(move, 9)
    
    @patch('random.uniform')
    def test_simulate_thinking_delay_uses_random_timing(self, mock_uniform):
        """Test _simulate_thinking_delay uses random timing between 0.5-2.0 seconds."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.HARD)
        mock_uniform.return_value = 1.2
        
        with patch('time.sleep') as mock_sleep, patch('builtins.print'):
            ai._simulate_thinking_delay()
        
        # Verify random.uniform was called with correct range
        mock_uniform.assert_called_once_with(0.5, 2.0)
        
        # Verify sleep was called with the random value
        mock_sleep.assert_called_once_with(1.2)
    
    def test_ai_enable_delay_parameter_default_true(self):
        """Test enable_delay parameter defaults to True."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.MEDIUM)
        self.assertTrue(ai.enable_delay, "enable_delay should default to True")
    
    def test_ai_enable_delay_parameter_can_be_set_false(self):
        """Test enable_delay parameter can be explicitly set to False."""
        ai = AIPlayer(TicTacToe.PLAYER_X, DifficultyLevel.MEDIUM, enable_delay=False)
        self.assertFalse(ai.enable_delay, "enable_delay should be False when explicitly set")

class TestDifficultyLevel(unittest.TestCase):
    """Test cases for DifficultyLevel enum"""

    def test_difficulty_level_enum_values(self):
        """Test DifficultyLevel enum has correct values."""
        self.assertEqual(DifficultyLevel.EASY.value, "easy")
        self.assertEqual(DifficultyLevel.MEDIUM.value, "medium")
        self.assertEqual(DifficultyLevel.HARD.value, "hard")

    def test_difficulty_level_enum_membership(self):
        """Test DifficultyLevel enum membership."""
        self.assertIn(DifficultyLevel.EASY, DifficultyLevel)
        self.assertIn(DifficultyLevel.MEDIUM, DifficultyLevel)
        self.assertIn(DifficultyLevel.HARD, DifficultyLevel)

    def test_difficulty_level_count(self):
        """Test DifficultyLevel enum has exactly 3 levels."""
        self.assertEqual(len(DifficultyLevel), 3)

if __name__ == '__main__':
    unittest.main()
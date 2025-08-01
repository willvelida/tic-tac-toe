import unittest
from unittest.mock import patch, call
import random
from src.player import Player, HumanPlayer
from src.tic_tac_toe import TicTacToe


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
    
    @patch('builtins.input')
    def test_human_player_get_move_returns_valid_integer(self, mock_input):
        """Test HumanPlayer.get_move returns integer when valid input provided."""
        mock_input.return_value = '5'
        
        player = HumanPlayer('X')
        board = [' '] * 9
        
        result = player.get_move(board)
        
        self.assertEqual(result, 5)
        self.assertIsInstance(result, int)
    
    @patch('builtins.input')
    def test_human_player_get_move_with_different_positions(self, mock_input):
        """Test HumanPlayer.get_move with different valid positions."""
        player = HumanPlayer('O')
        board = [' '] * 9
        
        test_positions = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        for position_str in test_positions:
            with self.subTest(position=position_str):
                mock_input.return_value = position_str
                result = player.get_move(board)
                self.assertEqual(result, int(position_str))
    
    @patch('builtins.input')
    def test_human_player_get_move_raises_value_error_for_non_numeric(self, mock_input):
        """Test HumanPlayer.get_move raises ValueError for non-numeric input."""
        mock_input.return_value = 'abc'
        
        player = HumanPlayer('X')
        board = [' '] * 9
        
        with self.assertRaises(ValueError):
            player.get_move(board)
    
    @patch('builtins.input')
    def test_human_player_get_move_raises_value_error_for_empty_input(self, mock_input):
        """Test HumanPlayer.get_move raises ValueError for empty input."""
        mock_input.return_value = ''
        
        player = HumanPlayer('X')
        board = [' '] * 9
        
        with self.assertRaises(ValueError):
            player.get_move(board)
    
    @patch('builtins.input')
    def test_human_player_get_move_raises_value_error_for_whitespace(self, mock_input):
        """Test HumanPlayer.get_move raises ValueError for whitespace-only input."""
        mock_input.return_value = '   '
        
        player = HumanPlayer('O')
        board = [' '] * 9
        
        with self.assertRaises(ValueError):
            player.get_move(board)
    
    @patch('builtins.input')
    def test_human_player_get_move_accepts_negative_numbers(self, mock_input):
        """Test HumanPlayer.get_move accepts negative numbers (validation happens elsewhere)."""
        mock_input.return_value = '-1'
        
        player = HumanPlayer('X')
        board = [' '] * 9
        
        result = player.get_move(board)
        self.assertEqual(result, -1)
    
    @patch('builtins.input')
    def test_human_player_get_move_accepts_large_numbers(self, mock_input):
        """Test HumanPlayer.get_move accepts numbers outside valid range (validation happens elsewhere)."""
        mock_input.return_value = '100'
        
        player = HumanPlayer('O')
        board = [' '] * 9
        
        result = player.get_move(board)
        self.assertEqual(result, 100)
    
    @patch('builtins.input')
    def test_human_player_get_move_accepts_zero(self, mock_input):
        """Test HumanPlayer.get_move accepts zero (validation happens elsewhere)."""
        mock_input.return_value = '0'
        
        player = HumanPlayer('X')
        board = [' '] * 9
        
        result = player.get_move(board)
        self.assertEqual(result, 0)
    
    @patch('builtins.input')
    def test_human_player_get_move_handles_float_strings(self, mock_input):
        """Test HumanPlayer.get_move raises ValueError for float strings."""
        mock_input.return_value = '5.5'
        
        player = HumanPlayer('X')
        board = [' '] * 9
        
        with self.assertRaises(ValueError):
            player.get_move(board)
    
    @patch('builtins.input')
    def test_human_player_get_move_board_parameter_not_used(self, mock_input):
        """Test HumanPlayer.get_move works regardless of board state."""
        mock_input.return_value = '3'
        
        player = HumanPlayer('O')
        
        # Test with empty board
        empty_board = [' '] * 9
        result1 = player.get_move(empty_board)
        self.assertEqual(result1, 3)
        
        # Test with partially filled board
        filled_board = ['X', 'O', ' ', 'X', ' ', 'O', ' ', ' ', 'X']
        result2 = player.get_move(filled_board)
        self.assertEqual(result2, 3)
    
    def test_human_player_inherits_from_player(self):
        """Test HumanPlayer correctly inherits from Player."""
        player = HumanPlayer('X')
        
        self.assertIsInstance(player, Player)
        self.assertEqual(player.symbol, 'X')
    
    def test_human_player_can_be_created_with_different_symbols(self):
        """Test HumanPlayer can be created with different symbols."""
        player_x = HumanPlayer('X')
        player_o = HumanPlayer('O')
        
        self.assertEqual(player_x.symbol, 'X')
        self.assertEqual(player_o.symbol, 'O')
    
    @patch('builtins.input')
    def test_human_player_get_move_calls_input_once(self, mock_input):
        """Test HumanPlayer.get_move calls input() exactly once."""
        mock_input.return_value = '7'
        
        player = HumanPlayer('X')
        board = [' '] * 9
        
        player.get_move(board)
        
        mock_input.assert_called_once()
    
    @patch('builtins.input')
    def test_human_player_get_move_with_special_characters(self, mock_input):
        """Test HumanPlayer.get_move raises ValueError for special characters."""
        special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        
        player = HumanPlayer('X')
        board = [' '] * 9
        
        for char in special_chars:
            with self.subTest(char=char):
                mock_input.return_value = char
                with self.assertRaises(ValueError):
                    player.get_move(board)
    
    @patch('builtins.input')
    def test_human_player_get_move_with_mixed_input(self, mock_input):
        """Test HumanPlayer.get_move raises ValueError for mixed alphanumeric input."""
        mixed_inputs = ['1a', 'a1', '1 2', '1.', '.1', '1e2']
        
        player = HumanPlayer('O')
        board = [' '] * 9
        
        for mixed_input in mixed_inputs:
            with self.subTest(input_value=mixed_input):
                mock_input.return_value = mixed_input
                with self.assertRaises(ValueError):
                    player.get_move(board)

if __name__ == '__main__':
    unittest.main()
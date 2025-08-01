import unittest
from src.tic_tac_toe import TicTacToe

class TestTicTacToe(unittest.TestCase):
    """Test cases for TicTacToe"""

    def setUp(self) -> None:
        self.game = TicTacToe()

    def test_board_init_creates_empty_3x3_grid(self) -> None:
        # Test that board has exactly 9 positions
        self.assertEqual(len(self.game.board), 9)

        # Test that all positions are empty
        for position in self.game.board:
            self.assertEqual(position, TicTacToe.EMPTY)

    def test_current_player_starts_as_x(self) -> None:
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_X)

    def test_reset_board_clears_existing_game(self):
        # Arrange
        self.game.board[0] = 'X'
        self.game.board[4] = 'O'
        self.game.current_player = 'O'

        # Act
        self.game.reset_board()

        # Assert
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_X)
        for position in self.game.board:
            self.assertEqual(position, TicTacToe.EMPTY)

    def test_is_valid_move_with_empty_position(self) -> None:
        for position in range(1, 10):
            self.assertTrue(
                self.game.is_valid_move(position),
                f"Position {position} should be valid when empty"
            )

    def test_is_valid_move_with_occupied_position(self) -> None:
        self.game.board[0] = TicTacToe.PLAYER_X

        self.assertFalse(
            self.game.is_valid_move(1),
            "Position 1 should be invalid when occupied"
        )

        for position in range(2, 10):
            self.assertTrue(
                self.game.is_valid_move(position),
                f"Position {position} should still be valid when empty"
            )

    def test_is_valid_move_with_multiple_occupied_positions(self) -> None:
        """Test is_valid_move with multiple occupied positions."""
        # Place pieces at positions 1, 5, and 9
        self.game.board[0] = TicTacToe.PLAYER_X  # Position 1
        self.game.board[4] = TicTacToe.PLAYER_O  # Position 5
        self.game.board[8] = TicTacToe.PLAYER_X  # Position 9
        
        # Occupied positions should be invalid
        occupied_positions = [1, 5, 9]
        for position in occupied_positions:
            self.assertFalse(
                self.game.is_valid_move(position),
                f"Position {position} should be invalid when occupied"
            )
        
        # Empty positions should still be valid
        empty_positions = [2, 3, 4, 6, 7, 8]
        for position in empty_positions:
            self.assertTrue(
                self.game.is_valid_move(position),
                f"Position {position} should be valid when empty"
            )
    
    def test_is_valid_move_with_invalid_position_numbers(self) -> None:
        """Test is_valid_move returns False for out-of-range positions."""
        # Test various invalid position numbers
        invalid_positions = [0, -1, -5, 10, 11, 15, 100]
        
        for position in invalid_positions:
            self.assertFalse(
                self.game.is_valid_move(position),
                f"Position {position} should be invalid (out of range)"
            )

    def test_is_valid_move_boundary_conditions(self) -> None:
        """Test is_valid_move at boundary positions (1 and 9)."""
        # Test position 1 (minimum valid)
        self.assertTrue(
            self.game.is_valid_move(1),
            "Position 1 should be valid"
        )
        
        # Test position 9 (maximum valid)
        self.assertTrue(
            self.game.is_valid_move(9),
            "Position 9 should be valid"
        )
        
        # Test just outside boundaries
        self.assertFalse(
            self.game.is_valid_move(0),
            "Position 0 should be invalid"
        )
        
        self.assertFalse(
            self.game.is_valid_move(10),
            "Position 10 should be invalid"
        )

    def test_is_valid_move_after_reset(self) -> None:
        """Test is_valid_move after board reset."""
        # Fill some positions
        self.game.board[0] = TicTacToe.PLAYER_X
        self.game.board[4] = TicTacToe.PLAYER_O
        
        # Verify positions are occupied
        self.assertFalse(self.game.is_valid_move(1))
        self.assertFalse(self.game.is_valid_move(5))
        
        # Reset board
        self.game.reset_board()
        
        # All positions should be valid again
        for position in range(1, 10):
            self.assertTrue(
                self.game.is_valid_move(position),
                f"Position {position} should be valid after reset"
            )
   
    def test_get_display_value_returns_symbols_for_occupied_positions(self) -> None:
        """Test get_display_value returns player symbols for occupied positions."""
        # Set up occupied positions
        self.game.board[0] = TicTacToe.PLAYER_X  # Position 1
        self.game.board[4] = TicTacToe.PLAYER_O  # Position 5
        
        # Should return symbols, not error messages
        self.assertEqual(self.game.get_display_value(1), TicTacToe.PLAYER_X)
        self.assertEqual(self.game.get_display_value(5), TicTacToe.PLAYER_O)

    def test_get_display_value_returns_position_numbers_for_empty_positions(self) -> None:
        """Test get_display_value return position numbers for empty positions"""
        for position in range(1, 10):
            expected = str(position)
            actual = self.game.get_display_value(position)
            self.assertEqual(actual, expected,
                             f"Empty position {position} should return '{expected}'")
            
    def test_switch_player_alternates_from_x_to_o(self) -> None:
        """Test _switch_player changes current player from X to O."""
        # Start with X (default)
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_X)
        
        # Switch should change to O
        self.game._switch_player()
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_O)
    
    def test_switch_player_alternates_from_o_to_x(self) -> None:
        """Test _switch_player changes current player from O to X."""
        # Start with O
        self.game.current_player = TicTacToe.PLAYER_O
        
        # Switch should change to X
        self.game._switch_player()
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_X)
    
    def test_switch_player_alternates_multiple_times(self) -> None:
        """Test _switch_player alternates correctly through multiple switches."""
        # Start with X
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_X)
        
        # X -> O
        self.game._switch_player()
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_O)
        
        # O -> X
        self.game._switch_player()
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_X)
        
        # X -> O
        self.game._switch_player()
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_O)
    
    def test_make_move_switches_players_correctly(self) -> None:
        """Test make_move method switches players after each move."""
        # Start with X
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_X)
        
        # Make move, should switch to O
        self.game.make_move(1)
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_O)
        
        # Make another move, should switch back to X
        self.game.make_move(2)
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_X)

    def test_make_move_places_current_player_symbol_on_board(self) -> None:
        self.game.make_move(1)
        self.assertEqual(self.game.board[0], TicTacToe.PLAYER_X)

        self.game.make_move(5)
        self.assertEqual(self.game.board[4], TicTacToe.PLAYER_O)

if __name__ == '__main__':
    unittest.main()

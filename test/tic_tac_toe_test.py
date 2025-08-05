import unittest
from src.tic_tac_toe import TicTacToe, GameMode

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
    
    def test_make_move_success_places_current_player_symbol(self) -> None:
        """Test make_move successfully places current player's symbol."""
        # Start with X
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_X)
        
        # Make move at position 1
        self.game.make_move(1)
        
        # Verify X is placed at position 1 (index 0)
        self.assertEqual(self.game.board[0], TicTacToe.PLAYER_X)
    
    def test_make_move_switches_players_after_successful_move(self) -> None:
        """Test make_move switches current player after successful move."""
        # Start with X
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_X)
        
        # Make move, should switch to O
        self.game.make_move(1)
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_O)
        
        # Make another move, should switch back to X
        self.game.make_move(2)
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_X)
    
    def test_make_move_sequence_alternates_symbols_correctly(self) -> None:
        """Test make_move sequence places X and O alternately."""
        # Make moves at positions 1, 2, 3
        self.game.make_move(1)  # X
        self.game.make_move(2)  # O  
        self.game.make_move(3)  # X
        
        # Verify correct symbols placed
        self.assertEqual(self.game.board[0], TicTacToe.PLAYER_X)  # Position 1
        self.assertEqual(self.game.board[1], TicTacToe.PLAYER_O)  # Position 2
        self.assertEqual(self.game.board[2], TicTacToe.PLAYER_X)  # Position 3
    
    def test_make_move_raises_value_error_for_out_of_range_positions(self) -> None:
        """Test make_move raises ValueError for positions outside 1-9 range."""
        invalid_positions = [0, -1, -5, 10, 11, 100]
        
        for position in invalid_positions:
            with self.subTest(position=position):
                with self.assertRaises(ValueError) as context:
                    self.game.make_move(position)
                
                expected_message = f"Invalid position {position}: must be between 1 and 9"
                self.assertEqual(str(context.exception), expected_message)
    
    def test_make_move_raises_value_error_for_occupied_positions(self) -> None:
        """Test make_move raises ValueError for already occupied positions."""
        # Place X at position 1
        self.game.make_move(1)
        
        # Try to place another piece at position 1
        with self.assertRaises(ValueError) as context:
            self.game.make_move(1)
        
        expected_message = f"Position 1 is already occupied by 'X'"
        self.assertEqual(str(context.exception), expected_message)
    
    def test_make_move_raises_value_error_for_multiple_occupied_positions(self) -> None:
        """Test make_move raises ValueError for different occupied positions."""
        # Set up board with some moves
        self.game.make_move(1)  # X
        self.game.make_move(5)  # O
        self.game.make_move(9)  # X
        
        # Test trying to place at each occupied position
        test_cases = [
            (1, 'X'),
            (5, 'O'), 
            (9, 'X')
        ]
        
        for position, symbol in test_cases:
            with self.subTest(position=position, symbol=symbol):
                with self.assertRaises(ValueError) as context:
                    self.game.make_move(position)
                
                expected_message = f"Position {position} is already occupied by '{symbol}'"
                self.assertEqual(str(context.exception), expected_message)
    
    def test_make_move_does_not_change_board_on_invalid_move(self) -> None:
        """Test make_move doesn't change board state when invalid move attempted."""
        # Make one valid move
        self.game.make_move(1)
        original_board = self.game.board.copy()
        original_player = self.game.current_player
        
        # Try invalid move (position already occupied)
        with self.assertRaises(ValueError):
            self.game.make_move(1)
        
        # Verify board and current player unchanged
        self.assertEqual(self.game.board, original_board)
        self.assertEqual(self.game.current_player, original_player)
    
    def test_make_move_does_not_change_board_on_out_of_range(self) -> None:
        """Test make_move doesn't change board state for out of range positions."""
        original_board = self.game.board.copy()
        original_player = self.game.current_player
        
        # Try invalid move (out of range)
        with self.assertRaises(ValueError):
            self.game.make_move(10)
        
        # Verify board and current player unchanged
        self.assertEqual(self.game.board, original_board)
        self.assertEqual(self.game.current_player, original_player)
    
    def test_make_move_all_valid_positions(self) -> None:
        """Test make_move works for all valid positions 1-9."""
        # Reset to ensure clean start
        self.game.reset_board()
        
        # Test each position
        for position in range(1, 10):
            with self.subTest(position=position):
                # Reset board for each test
                self.game.reset_board()
                
                # Make move at position
                self.game.make_move(position)
                
                # Verify correct placement (convert to 0-based index)
                self.assertEqual(self.game.board[position - 1], TicTacToe.PLAYER_X)
                
                # Verify player switched
                self.assertEqual(self.game.current_player, TicTacToe.PLAYER_O)
    
    def test_make_move_with_type_annotations(self) -> None:
        """Test make_move handles integer positions correctly."""
        # Test with explicit integers
        positions = [1, 2, 3, 4, 5]
        
        for i, position in enumerate(positions):
            # Make move
            self.game.make_move(position)
            
            # Verify placement
            expected_symbol = TicTacToe.PLAYER_X if i % 2 == 0 else TicTacToe.PLAYER_O
            self.assertEqual(self.game.board[position - 1], expected_symbol)
    
    def test_make_move_error_messages_are_descriptive(self) -> None:
        """Test make_move error messages provide clear information."""
        # Test out of range error message
        with self.assertRaises(ValueError) as context:
            self.game.make_move(0)
        self.assertIn("must be between 1 and 9", str(context.exception))
        self.assertIn("Invalid position 0", str(context.exception))
        
        # Test occupied position error message
        self.game.make_move(5)  # Place X at position 5
        with self.assertRaises(ValueError) as context:
            self.game.make_move(5)
        self.assertIn("is already occupied", str(context.exception))
        self.assertIn("Position 5", str(context.exception))
        self.assertIn("'X'", str(context.exception))
    
    def test_make_move_boundary_positions(self) -> None:
        """Test make_move works correctly at boundary positions."""
        # Test position 1 (minimum valid)
        self.game.make_move(1)
        self.assertEqual(self.game.board[0], TicTacToe.PLAYER_X)
        
        # Reset and test position 9 (maximum valid)
        self.game.reset_board()
        self.game.make_move(9)
        self.assertEqual(self.game.board[8], TicTacToe.PLAYER_X)
    
    def test_make_move_after_board_reset(self) -> None:
        """Test make_move works correctly after board reset."""
        # Make some moves
        self.game.make_move(1)
        self.game.make_move(2)
        
        # Reset board
        self.game.reset_board()
        
        # Make move at previously occupied position
        self.game.make_move(1)  # Should work without error
        
        # Verify correct placement and player
        self.assertEqual(self.game.board[0], TicTacToe.PLAYER_X)
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_O)
    
    def test_make_move_full_game_scenario(self) -> None:
        """Test make_move in a realistic game scenario."""
        # Simulate a partial game
        moves = [1, 2, 3, 4, 5]  # X, O, X, O, X
        expected_symbols = [TicTacToe.PLAYER_X, TicTacToe.PLAYER_O, TicTacToe.PLAYER_X, 
                           TicTacToe.PLAYER_O, TicTacToe.PLAYER_X]
        
        for i, position in enumerate(moves):
            self.game.make_move(position)
            
            # Verify correct symbol placed
            self.assertEqual(self.game.board[position - 1], expected_symbols[i])
        
        # Verify final player state
        self.assertEqual(self.game.current_player, TicTacToe.PLAYER_O)
        
        # Verify trying to use occupied positions fails
        for position in moves:
            with self.assertRaises(ValueError):
                self.game.make_move(position)
    
    def test_check_winner_returns_none_for_empty_board(self) -> None:
        """Test check_winner returns None for empty board."""
        result = self.game.check_winner()
        self.assertIsNone(result)
    
    def test_check_winner_returns_none_for_no_winner(self) -> None:
        """Test check_winner returns None when no winner exists."""
        # Set up board with no winning combination
        self.game.board = ['X', 'O', 'X', 
                           'O', 'X', 'O', 
                           'O', 'X', ' ']
        
        result = self.game.check_winner()
        self.assertIsNone(result)
    
    def test_check_winner_detects_x_wins_top_row(self) -> None:
        """Test check_winner detects X winning in top row."""
        # X wins with positions 1, 2, 3 (indices 0, 1, 2)
        self.game.board = ['X', 'X', 'X',
                           'O', 'O', ' ',
                           ' ', ' ', ' ']
        
        result = self.game.check_winner()
        self.assertEqual(result, TicTacToe.PLAYER_X)
    
    def test_check_winner_detects_x_wins_middle_row(self) -> None:
        """Test check_winner detects X winning in middle row."""
        # X wins with positions 4, 5, 6 (indices 3, 4, 5)
        self.game.board = ['O', 'O', ' ',
                           'X', 'X', 'X',
                           ' ', ' ', ' ']
        
        result = self.game.check_winner()
        self.assertEqual(result, TicTacToe.PLAYER_X)
    
    def test_check_winner_detects_x_wins_bottom_row(self) -> None:
        """Test check_winner detects X winning in bottom row."""
        # X wins with positions 7, 8, 9 (indices 6, 7, 8)
        self.game.board = ['O', 'O', ' ',
                           ' ', ' ', ' ',
                           'X', 'X', 'X']
        
        result = self.game.check_winner()
        self.assertEqual(result, TicTacToe.PLAYER_X)
    
    def test_check_winner_detects_o_wins_left_column(self) -> None:
        """Test check_winner detects O winning in left column."""
        # O wins with positions 1, 4, 7 (indices 0, 3, 6)
        self.game.board = ['O', 'X', 'X',
                           'O', 'X', ' ',
                           'O', ' ', ' ']
        
        result = self.game.check_winner()
        self.assertEqual(result, TicTacToe.PLAYER_O)
    
    def test_check_winner_detects_o_wins_middle_column(self) -> None:
        """Test check_winner detects O winning in middle column."""
        # O wins with positions 2, 5, 8 (indices 1, 4, 7)
        self.game.board = ['X', 'O', 'X',
                           ' ', 'O', ' ',
                           ' ', 'O', 'X']
        
        result = self.game.check_winner()
        self.assertEqual(result, TicTacToe.PLAYER_O)
    
    def test_check_winner_detects_o_wins_right_column(self) -> None:
        """Test check_winner detects O winning in right column."""
        # O wins with positions 3, 6, 9 (indices 2, 5, 8)
        self.game.board = ['X', 'X', 'O',
                           ' ', ' ', 'O',
                           ' ', ' ', 'O']
        
        result = self.game.check_winner()
        self.assertEqual(result, TicTacToe.PLAYER_O)
    
    def test_check_winner_detects_x_wins_main_diagonal(self) -> None:
        """Test check_winner detects X winning on main diagonal."""
        # X wins with positions 1, 5, 9 (indices 0, 4, 8)
        self.game.board = ['X', 'O', 'O',
                           ' ', 'X', ' ',
                           ' ', ' ', 'X']
        
        result = self.game.check_winner()
        self.assertEqual(result, TicTacToe.PLAYER_X)
    
    def test_check_winner_detects_x_wins_anti_diagonal(self) -> None:
        """Test check_winner detects X winning on anti-diagonal."""
        # X wins with positions 3, 5, 7 (indices 2, 4, 6)
        self.game.board = ['O', 'O', 'X',
                           ' ', 'X', ' ',
                           'X', ' ', ' ']
        
        result = self.game.check_winner()
        self.assertEqual(result, TicTacToe.PLAYER_X)
    
    def test_check_winner_detects_o_wins_main_diagonal(self) -> None:
        """Test check_winner detects O winning on main diagonal."""
        # O wins with positions 1, 5, 9 (indices 0, 4, 8)
        self.game.board = ['O', 'X', 'X',
                           ' ', 'O', ' ',
                           ' ', ' ', 'O']
        
        result = self.game.check_winner()
        self.assertEqual(result, TicTacToe.PLAYER_O)
    
    def test_check_winner_detects_o_wins_anti_diagonal(self) -> None:
        """Test check_winner detects O winning on anti-diagonal."""
        # O wins with positions 3, 5, 7 (indices 2, 4, 6)
        self.game.board = ['X', 'X', 'O',
                           ' ', 'O', ' ',
                           'O', ' ', ' ']
        
        result = self.game.check_winner()
        self.assertEqual(result, TicTacToe.PLAYER_O)
    
    def test_check_winner_returns_first_winner_found(self) -> None:
        """Test check_winner returns first winner when multiple winning combinations exist."""
        # Set up board where X has multiple winning combinations
        # Top row and main diagonal both have X
        self.game.board = ['X', 'X', 'X',
                           'O', 'X', 'O',
                           'O', 'O', 'X']
        
        result = self.game.check_winner()
        self.assertEqual(result, TicTacToe.PLAYER_X)
    
    def test_check_winner_realistic_game_scenarios(self) -> None:
        """Test check_winner with realistic game progression scenarios."""
        # Scenario 1: X wins after 5 moves
        moves_x_wins = [(1, 'X'), (2, 'O'), (4, 'X'), (5, 'O'), (7, 'X')]  # X wins diagonal
        
        self.game.reset_board()
        for position, expected_player in moves_x_wins[:-1]:  # All moves except the last
            if expected_player == 'X':
                self.game.current_player = TicTacToe.PLAYER_X
            else:
                self.game.current_player = TicTacToe.PLAYER_O
            self.game.board[position - 1] = expected_player
        
        # Before final move, no winner
        self.assertIsNone(self.game.check_winner())
        
        # Final move creates winner
        self.game.board[6] = 'X'  # Position 7
        self.assertEqual(self.game.check_winner(), TicTacToe.PLAYER_X)
    
    def test_check_line_returns_true_for_matching_symbols(self) -> None:
        """Test _check_line returns True when all positions have same non-empty symbol."""
        # Set up board with X in positions 0, 1, 2
        self.game.board[0] = TicTacToe.PLAYER_X
        self.game.board[1] = TicTacToe.PLAYER_X
        self.game.board[2] = TicTacToe.PLAYER_X
        
        result = self.game._check_line([0, 1, 2])
        self.assertTrue(result)
    
    def test_check_line_returns_false_for_different_symbols(self) -> None:
        """Test _check_line returns False when positions have different symbols."""
        # Set up board with mixed symbols
        self.game.board[0] = TicTacToe.PLAYER_X
        self.game.board[1] = TicTacToe.PLAYER_O
        self.game.board[2] = TicTacToe.PLAYER_X
        
        result = self.game._check_line([0, 1, 2])
        self.assertFalse(result)
    
    def test_check_line_returns_false_for_empty_positions(self) -> None:
        """Test _check_line returns False when positions contain empty spaces."""
        # Leave positions empty (default state)
        result = self.game._check_line([0, 1, 2])
        self.assertFalse(result)
    
    def test_check_line_returns_false_for_partial_match_with_empty(self) -> None:
        """Test _check_line returns False when some positions are empty."""
        # Set up board with two X's and one empty
        self.game.board[0] = TicTacToe.PLAYER_X
        self.game.board[1] = TicTacToe.PLAYER_X
        # board[2] remains empty
        
        result = self.game._check_line([0, 1, 2])
        self.assertFalse(result)
    
    def test_check_line_works_with_o_symbols(self) -> None:
        """Test _check_line works correctly with O symbols."""
        # Set up board with O in positions 3, 4, 5
        self.game.board[3] = TicTacToe.PLAYER_O
        self.game.board[4] = TicTacToe.PLAYER_O
        self.game.board[5] = TicTacToe.PLAYER_O
        
        result = self.game._check_line([3, 4, 5])
        self.assertTrue(result)
    
    def test_check_line_with_all_winning_combinations(self) -> None:
        """Test _check_line works with all possible winning combinations."""
        winning_combinations = [
            # Rows
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            # Columns  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            # Diagonals
            [0, 4, 8], [2, 4, 6]
        ]
        
        for combination in winning_combinations:
            with self.subTest(combination=combination):
                # Reset board
                self.game.reset_board()
                
                # Fill the combination with X
                for pos in combination:
                    self.game.board[pos] = TicTacToe.PLAYER_X
                
                # Should return True for this combination
                result = self.game._check_line(combination)
                self.assertTrue(result, f"Failed for combination {combination}")
    
    def test_check_winner_integration_with_make_move(self) -> None:
        """Test check_winner integration with make_move for complete game flow."""
        # Play a game where X wins
        moves = [1, 2, 4, 5, 7]  # X wins diagonal: positions 1, 4, 7
        
        for i, position in enumerate(moves):
            # Check no winner before final move
            if i < len(moves) - 1:
                self.assertIsNone(self.game.check_winner())
            
            self.game.make_move(position)
            
            # After X's winning move, should detect winner
            if i == 4:  # After X's third move (winning move)
                self.assertEqual(self.game.check_winner(), TicTacToe.PLAYER_X)
    
    def test_check_winner_after_board_reset(self) -> None:
        """Test check_winner returns None after board reset."""
        # Set up a winning board
        self.game.board = ['X', 'X', 'X',
                           'O', 'O', ' ',
                           ' ', ' ', ' ']
        
        # Verify winner detected
        self.assertEqual(self.game.check_winner(), TicTacToe.PLAYER_X)
        
        # Reset board
        self.game.reset_board()
        
        # Should return None after reset
        self.assertIsNone(self.game.check_winner())
    
    def test_check_winner_return_type(self) -> None:
        """Test check_winner returns correct types."""
        # Empty board should return None
        result = self.game.check_winner()
        self.assertIsNone(result)
        
        # Winning board should return string
        self.game.board = ['X', 'X', 'X',
                           'O', 'O', ' ',
                           ' ', ' ', ' ']
        
        result = self.game.check_winner()
        self.assertIsInstance(result, str)
        self.assertIn(result, [TicTacToe.PLAYER_X, TicTacToe.PLAYER_O])


    def test_get_game_state_returns_ongoing_for_empty_board(self) -> None:
        """Test get_game_state returns ongoing state for empty board."""
        result = self.game.get_game_state()
        
        expected = {'state': 'ongoing', 'winner': None}
        self.assertEqual(result, expected)
    
    def test_get_game_state_returns_ongoing_for_partial_board(self) -> None:
        """Test get_game_state returns ongoing state for partially filled board."""
        # Make some moves without creating a winner
        self.game.board = ['X', 'O', ' ',
                           'O', 'X', ' ',
                           ' ', ' ', ' ']
        
        result = self.game.get_game_state()
        
        expected = {'state': 'ongoing', 'winner': None}
        self.assertEqual(result, expected)
    
    def test_get_game_state_returns_won_for_x_winner(self) -> None:
        """Test get_game_state returns won state when X wins."""
        # Set up board where X wins top row
        self.game.board = ['X', 'X', 'X',
                           'O', 'O', ' ',
                           ' ', ' ', ' ']
        
        result = self.game.get_game_state()
        
        expected = {'state': 'won', 'winner': 'X'}
        self.assertEqual(result, expected)
    
    def test_get_game_state_returns_won_for_o_winner(self) -> None:
        """Test get_game_state returns won state when O wins."""
        # Set up board where O wins left column
        self.game.board = ['O', 'X', 'X',
                           'O', 'X', ' ',
                           'O', ' ', ' ']
        
        result = self.game.get_game_state()
        
        expected = {'state': 'won', 'winner': 'O'}
        self.assertEqual(result, expected)
    
    def test_get_game_state_returns_draw_for_full_board_no_winner(self) -> None:
        """Test get_game_state returns draw state for full board with no winner."""
        # Set up board that is full but has no winner
        self.game.board = ['X', 'O', 'X',
                           'O', 'X', 'O',
                           'O', 'X', 'O']
        
        result = self.game.get_game_state()
        
        expected = {'state': 'draw', 'winner': None}
        self.assertEqual(result, expected)
    
    def test_get_game_state_returns_dict_type(self) -> None:
        """Test get_game_state returns dictionary type."""
        result = self.game.get_game_state()
        
        self.assertIsInstance(result, dict)
        self.assertIn('state', result)
        self.assertIn('winner', result)
    
    def test_get_game_state_valid_state_values(self) -> None:
        """Test get_game_state returns only valid state values."""
        valid_states = ['ongoing', 'won', 'draw']
        
        # Test ongoing state
        result = self.game.get_game_state()
        self.assertIn(result['state'], valid_states)
        
        # Test won state
        self.game.board = ['X', 'X', 'X',
                           'O', 'O', ' ',
                           ' ', ' ', ' ']
        result = self.game.get_game_state()
        self.assertIn(result['state'], valid_states)
        
        # Test draw state
        self.game.board = ['X', 'O', 'X',
                           'O', 'X', 'O',
                           'O', 'X', 'O']
        result = self.game.get_game_state()
        self.assertIn(result['state'], valid_states)
    
    def test_get_game_state_winner_values_are_correct(self) -> None:
        """Test get_game_state winner values are correct or None."""
        valid_winners = [TicTacToe.PLAYER_X, TicTacToe.PLAYER_O, None]
        
        # Test ongoing game (winner should be None)
        result = self.game.get_game_state()
        self.assertIn(result['winner'], valid_winners)
        self.assertIsNone(result['winner'])
        
        # Test X winner
        self.game.board = ['X', 'X', 'X',
                           'O', 'O', ' ',
                           ' ', ' ', ' ']
        result = self.game.get_game_state()
        self.assertEqual(result['winner'], TicTacToe.PLAYER_X)
        
        # Test draw (winner should be None)
        self.game.board = ['X', 'O', 'X',
                           'O', 'X', 'O',
                           'O', 'X', 'O']
        result = self.game.get_game_state()
        self.assertIsNone(result['winner'])
    
    def test_get_game_state_with_realistic_game_progression(self) -> None:
        """Test get_game_state during realistic game progression."""
        # Test ongoing game progression
        moves = [1, 2, 4, 5]  # Partial game
        
        for position in moves:
            self.game.make_move(position)
            result = self.game.get_game_state()
            self.assertEqual(result['state'], 'ongoing')
            self.assertIsNone(result['winner'])
        
        # Make winning move for X (position 7 completes diagonal)
        self.game.make_move(7)  # X wins with positions 1, 4, 7
        
        result = self.game.get_game_state()
        self.assertEqual(result['state'], 'won')
        self.assertEqual(result['winner'], TicTacToe.PLAYER_X)
    
    def test_get_game_state_all_winning_combinations(self) -> None:
        """Test get_game_state correctly identifies won state for all winning combinations."""
        winning_combinations = [
            # Rows
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            # Columns
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            # Diagonals
            [0, 4, 8], [2, 4, 6]
        ]
        
        for combination in winning_combinations:
            with self.subTest(combination=combination):
                # Reset board
                self.game.reset_board()
                
                # Set up winning combination for X
                for pos in combination:
                    self.game.board[pos] = TicTacToe.PLAYER_X
                
                result = self.game.get_game_state()
                
                self.assertEqual(result['state'], 'won')
                self.assertEqual(result['winner'], TicTacToe.PLAYER_X)
    
    def test_get_game_state_after_board_reset(self) -> None:
        """Test get_game_state returns ongoing after board reset."""
        # Set up winning board
        self.game.board = ['X', 'X', 'X',
                           'O', 'O', ' ',
                           ' ', ' ', ' ']
        
        # Verify won state
        result = self.game.get_game_state()
        self.assertEqual(result['state'], 'won')
        
        # Reset board
        self.game.reset_board()
        
        # Should return ongoing state
        result = self.game.get_game_state()
        expected = {'state': 'ongoing', 'winner': None}
        self.assertEqual(result, expected)
    
    def test_get_game_state_draw_scenarios(self) -> None:
        """Test get_game_state correctly identifies various draw scenarios."""
        draw_scenarios = [
            # Draw scenario 1
            ['X', 'O', 'X',
             'O', 'O', 'X',
             'O', 'X', 'O'],
            # Draw scenario 2
            ['O', 'X', 'O',
             'X', 'X', 'O',
             'X', 'O', 'X'],
            # Draw scenario 3
            ['X', 'O', 'X',
             'O', 'X', 'O',
             'O', 'X', 'O']
        ]
        
        for i, scenario in enumerate(draw_scenarios):
            with self.subTest(scenario=i):
                self.game.board = scenario
                result = self.game.get_game_state()
                self.assertEqual(result['state'], 'draw')
                self.assertIsNone(result['winner'])
    
    def test_get_game_state_priority_winner_over_full_board(self) -> None:
        """Test get_game_state returns won state even when board is full."""
        # Set up full board where X wins
        self.game.board = ['X', 'X', 'X',
                           'O', 'O', 'X',
                           'O', 'X', 'O']
        
        result = self.game.get_game_state()
        
        # Should return won, not draw, even though board is full
        self.assertEqual(result['state'], 'won')
        self.assertEqual(result['winner'], TicTacToe.PLAYER_X)
    
    def test_get_game_state_integration_with_other_methods(self) -> None:
        """Test get_game_state integration with is_draw and check_winner methods."""
        # Test that get_game_state uses check_winner correctly
        self.game.board = ['O', 'O', 'O',
                           'X', 'X', ' ',
                           ' ', ' ', ' ']
        
        # Verify check_winner returns O
        self.assertEqual(self.game.check_winner(), TicTacToe.PLAYER_O)
        
        # Verify get_game_state reflects this
        result = self.game.get_game_state()
        self.assertEqual(result['state'], 'won')
        self.assertEqual(result['winner'], TicTacToe.PLAYER_O)
        
        # Test that get_game_state uses is_draw correctly
        self.game.board = ['X', 'O', 'X',
                           'O', 'X', 'O',
                           'O', 'X', 'O']
        
        # Verify is_draw returns True
        self.assertTrue(self.game.is_draw())
        
        # Verify get_game_state reflects this
        result = self.game.get_game_state()
        self.assertEqual(result['state'], 'draw')
        self.assertIsNone(result['winner'])
    
    def test_get_game_state_winner_key_consistency(self) -> None:
        """Test get_game_state uses 'winner' key consistently across all states."""
        # Test ongoing state
        result = self.game.get_game_state()
        self.assertIn('winner', result)
        self.assertIsNone(result['winner'])
        
        # Test won state
        self.game.board = ['X', 'X', 'X',
                           'O', 'O', ' ',
                           ' ', ' ', ' ']
        result = self.game.get_game_state()
        self.assertIn('winner', result)
        self.assertEqual(result['winner'], TicTacToe.PLAYER_X)
        
        # Test draw state
        self.game.board = ['X', 'O', 'X',
                           'O', 'X', 'O',
                           'O', 'X', 'O']
        result = self.game.get_game_state()
        self.assertIn('winner', result)
        self.assertIsNone(result['winner'])
    
    def test_get_game_state_complete_game_flow(self) -> None:
        """Test get_game_state through complete game flow from start to finish."""
        # Start: should be ongoing
        result = self.game.get_game_state()
        self.assertEqual(result, {'state': 'ongoing', 'winner': None})
        
        # After first move: still ongoing
        self.game.make_move(5)  # X center
        result = self.game.get_game_state()
        self.assertEqual(result, {'state': 'ongoing', 'winner': None})
        
        # After second move: still ongoing
        self.game.make_move(1)  # O top-left
        result = self.game.get_game_state()
        self.assertEqual(result, {'state': 'ongoing', 'winner': None})
        
        # Continue until X wins
        self.game.make_move(3)  # X top-right
        self.game.make_move(2)  # O top-center
        self.game.make_move(7)  # X bottom-left (wins diagonal)
        
        # Should now be won
        result = self.game.get_game_state()
        self.assertEqual(result, {'state': 'won', 'winner': TicTacToe.PLAYER_X})
    
    def test_get_game_state_return_type_structure(self) -> None:
        """Test get_game_state returns correct dictionary structure."""
        result = self.game.get_game_state()
        
        # Should be a dictionary with exactly 2 keys
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.assertIn('state', result)
        self.assertIn('winner', result)
        
        # Values should be correct types
        self.assertIsInstance(result['state'], str)
        self.assertTrue(result['winner'] is None or isinstance(result['winner'], str))

    def test_is_board_full_returns_false_for_empty_board(self) -> None:
        """Test is_board_full returns False for empty board."""
        result = self.game.is_board_full()
        self.assertFalse(result)

    def test_is_board_full_returns_false_for_partially_filled_board(self) -> None:
        """Test is_board_full returns False for partially filled board."""
        # Fill some positions
        self.game.board[0] = TicTacToe.PLAYER_X
        self.game.board[4] = TicTacToe.PLAYER_O
        self.game.board[8] = TicTacToe.PLAYER_X
        
        result = self.game.is_board_full()
        self.assertFalse(result)

    def test_is_board_full_returns_true_for_completely_full_board(self) -> None:
        """Test is_board_full returns True when all positions are occupied."""
        # Fill entire board
        self.game.board = ['X', 'O', 'X',
                           'O', 'X', 'O', 
                           'X', 'O', 'X']
        
        result = self.game.is_board_full()
        self.assertTrue(result)

    def test_is_board_full_returns_false_with_one_empty_position(self) -> None:
        """Test is_board_full returns False when only one position is empty."""
        # Fill all but one position
        self.game.board = ['X', 'O', 'X',
                           'O', 'X', 'O',
                           'X', 'O', ' ']  # Last position empty
        
        result = self.game.is_board_full()
        self.assertFalse(result)

    def test_is_draw_returns_false_for_empty_board(self) -> None:
        """Test is_draw returns False for empty board."""
        result = self.game.is_draw()
        self.assertFalse(result)

    def test_is_draw_returns_false_for_partially_filled_board(self) -> None:
        """Test is_draw returns False for partially filled board."""
        # Fill some positions without creating winner
        self.game.board[0] = TicTacToe.PLAYER_X
        self.game.board[4] = TicTacToe.PLAYER_O
        self.game.board[8] = TicTacToe.PLAYER_X
        
        result = self.game.is_draw()
        self.assertFalse(result)

    def test_is_draw_returns_false_for_full_board_with_winner(self) -> None:
        """Test is_draw returns False when board is full but has a winner."""
        # Create full board with X winning top row
        self.game.board = ['X', 'X', 'X',
                           'O', 'O', 'X',
                           'O', 'X', 'O']
        
        result = self.game.is_draw()
        self.assertFalse(result)

    def test_is_draw_returns_true_for_full_board_without_winner(self) -> None:
        """Test is_draw returns True when board is full with no winner."""
        # Create full board with no winning combinations
        self.game.board = ['X', 'O', 'X',
                           'O', 'X', 'O',
                           'O', 'X', 'O']
        
        result = self.game.is_draw()
        self.assertTrue(result)

        """Test get_game_mode returns default mode when no mode specified."""
        game = TicTacToe()  # Default should be HUMAN_VS_AI
        result = game.get_game_mode()
        
        self.assertEqual(result, GameMode.HUMAN_VS_AI)
        self.assertIsInstance(result, GameMode)
    
    def test_get_game_mode_returns_human_vs_human_when_specified(self) -> None:
        """Test get_game_mode returns HUMAN_VS_HUMAN when explicitly set."""
        game = TicTacToe(mode=GameMode.HUMAN_VS_HUMAN)
        result = game.get_game_mode()
        
        self.assertEqual(result, GameMode.HUMAN_VS_HUMAN)
        self.assertIsInstance(result, GameMode)
    
    def test_get_game_mode_returns_human_vs_ai_when_specified(self) -> None:
        """Test get_game_mode returns HUMAN_VS_AI when explicitly set."""
        game = TicTacToe(mode=GameMode.HUMAN_VS_AI)
        result = game.get_game_mode()
        
        self.assertEqual(result, GameMode.HUMAN_VS_AI)
        self.assertIsInstance(result, GameMode)
    
    def test_get_game_mode_persists_after_reset(self) -> None:
        """Test get_game_mode persists the same mode after board reset."""
        # Test with HUMAN_VS_HUMAN mode
        game = TicTacToe(mode=GameMode.HUMAN_VS_HUMAN)
        original_mode = game.get_game_mode()
        
        game.reset_board()
        mode_after_reset = game.get_game_mode()
        
        self.assertEqual(original_mode, mode_after_reset)
        self.assertEqual(mode_after_reset, GameMode.HUMAN_VS_HUMAN)
    
    def test_get_game_mode_persists_after_moves(self) -> None:
        """Test get_game_mode persists the same mode after making moves."""
        game = TicTacToe(mode=GameMode.HUMAN_VS_HUMAN)
        original_mode = game.get_game_mode()
        
        # Make some moves
        game.make_move(1)
        game.make_move(2)
        game.make_move(3)
        
        mode_after_moves = game.get_game_mode()
        
        self.assertEqual(original_mode, mode_after_moves)
        self.assertEqual(mode_after_moves, GameMode.HUMAN_VS_HUMAN)
    
    def test_is_ai_mode_returns_true_for_human_vs_ai(self) -> None:
        """Test is_ai_mode returns True when mode is HUMAN_VS_AI."""
        game = TicTacToe(mode=GameMode.HUMAN_VS_AI)
        result = game.is_ai_mode()
        
        self.assertTrue(result)
        self.assertIsInstance(result, bool)
    
    def test_is_ai_mode_returns_false_for_human_vs_human(self) -> None:
        """Test is_ai_mode returns False when mode is HUMAN_VS_HUMAN."""
        game = TicTacToe(mode=GameMode.HUMAN_VS_HUMAN)
        result = game.is_ai_mode()
        
        self.assertFalse(result)
        self.assertIsInstance(result, bool)
    
    def test_is_ai_mode_returns_true_for_default_mode(self) -> None:
        """Test is_ai_mode returns True for default mode (HUMAN_VS_AI)."""
        game = TicTacToe()  # Default mode
        result = game.is_ai_mode()
        
        self.assertTrue(result)
    
    def test_is_ai_mode_persists_after_reset(self) -> None:
        """Test is_ai_mode returns consistent result after board reset."""
        # Test with HUMAN_VS_HUMAN mode
        game = TicTacToe(mode=GameMode.HUMAN_VS_HUMAN)
        original_ai_mode = game.is_ai_mode()
        
        game.reset_board()
        ai_mode_after_reset = game.is_ai_mode()
        
        self.assertEqual(original_ai_mode, ai_mode_after_reset)
        self.assertFalse(ai_mode_after_reset)
    
    def test_is_ai_mode_persists_after_moves(self) -> None:
        """Test is_ai_mode returns consistent result after making moves."""
        game = TicTacToe(mode=GameMode.HUMAN_VS_AI)
        original_ai_mode = game.is_ai_mode()
        
        # Make some moves
        game.make_move(1)
        game.make_move(2)
        
        ai_mode_after_moves = game.is_ai_mode()
        
        self.assertEqual(original_ai_mode, ai_mode_after_moves)
        self.assertTrue(ai_mode_after_moves)
    
    def test_game_mode_consistency_between_methods(self) -> None:
        """Test consistency between get_game_mode and is_ai_mode methods."""
        # Test HUMAN_VS_AI mode
        game_ai = TicTacToe(mode=GameMode.HUMAN_VS_AI)
        self.assertEqual(game_ai.get_game_mode(), GameMode.HUMAN_VS_AI)
        self.assertTrue(game_ai.is_ai_mode())
        
        # Test HUMAN_VS_HUMAN mode
        game_human = TicTacToe(mode=GameMode.HUMAN_VS_HUMAN)
        self.assertEqual(game_human.get_game_mode(), GameMode.HUMAN_VS_HUMAN)
        self.assertFalse(game_human.is_ai_mode())
    
    def test_game_mode_with_game_state_integration(self) -> None:
        """Test game mode methods work correctly with other game functionality."""
        # Test that game mode doesn't affect basic game functionality
        game = TicTacToe(mode=GameMode.HUMAN_VS_HUMAN)
        
        # Verify mode is set correctly
        self.assertEqual(game.get_game_mode(), GameMode.HUMAN_VS_HUMAN)
        self.assertFalse(game.is_ai_mode())
        
        # Verify game functionality still works
        self.assertTrue(game.is_valid_move(1))
        game.make_move(1)
        self.assertEqual(game.board[0], TicTacToe.PLAYER_X)
        
        # Verify mode is still correct after game operations
        self.assertEqual(game.get_game_mode(), GameMode.HUMAN_VS_HUMAN)
        self.assertFalse(game.is_ai_mode())
    
    def test_game_mode_enum_values(self) -> None:
        """Test that GameMode enum values are correct."""
        # Test enum values
        self.assertEqual(GameMode.HUMAN_VS_HUMAN.value, 'human_vs_human')
        self.assertEqual(GameMode.HUMAN_VS_AI.value, 'human_vs_ai')
        
        # Test that both modes work with TicTacToe
        game_human = TicTacToe(mode=GameMode.HUMAN_VS_HUMAN)
        game_ai = TicTacToe(mode=GameMode.HUMAN_VS_AI)
        
        self.assertNotEqual(game_human.get_game_mode(), game_ai.get_game_mode())
    
    def test_game_mode_return_types(self) -> None:
        """Test that game mode methods return correct types."""
        game = TicTacToe(mode=GameMode.HUMAN_VS_AI)
        
        # Test get_game_mode return type
        mode_result = game.get_game_mode()
        self.assertIsInstance(mode_result, GameMode)
        
        # Test is_ai_mode return type
        ai_result = game.is_ai_mode()
        self.assertIsInstance(ai_result, bool)

    def test_find_winning_move_detects_row_win_for_x(self) -> None:
        """Test find_winning_move detects X can win by completing a row."""
        # X can win top row by playing position 3
        self.game.board = ['X', 'X', ' ',  # positions 1,2,3
                           'O', 'O', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        
        result = self.game.find_winning_move('X')
        self.assertEqual(result, 3)
    
    def test_find_winning_move_detects_column_win_for_o(self) -> None:
        """Test find_winning_move detects O can win by completing a column."""
        # O can win left column by playing position 7
        self.game.board = ['O', 'X', 'X',  # positions 1,2,3
                           'O', 'X', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        
        result = self.game.find_winning_move('O')
        self.assertEqual(result, 7)
    
    def test_find_winning_move_detects_diagonal_win(self) -> None:
        """Test find_winning_move detects diagonal win opportunity."""
        # X can win main diagonal by playing position 9
        self.game.board = ['X', 'O', 'O',  # positions 1,2,3
                           ' ', 'X', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        
        result = self.game.find_winning_move('X')
        self.assertEqual(result, 9)
    
    def test_find_winning_move_returns_none_when_no_win_available(self) -> None:
        """Test find_winning_move returns None when no immediate win exists."""
        # Board where no player can win in one move
        self.game.board = ['X', 'O', 'X',  # positions 1,2,3  
                        'O', 'X', 'O',  # positions 4,5,6
                        'O', 'X', 'O']  # positions 7,8,9
        
        result_x = self.game.find_winning_move('X')
        result_o = self.game.find_winning_move('O')
        
        self.assertIsNone(result_x)
        self.assertIsNone(result_o)
    
    def test_find_winning_move_returns_none_for_empty_board(self) -> None:
        """Test find_winning_move returns None on empty board."""
        result = self.game.find_winning_move('X')
        self.assertIsNone(result)

    def test_find_winning_move_detects_all_row_wins(self) -> None:
        """Test find_winning_move detects wins in all three rows."""
        # Top row win
        self.game.board = ['X', 'X', ' ',  # positions 1,2,3
                           ' ', ' ', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        self.assertEqual(self.game.find_winning_move('X'), 3)
        
        # Middle row win
        self.game.board = [' ', ' ', ' ',  # positions 1,2,3
                           'O', 'O', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        self.assertEqual(self.game.find_winning_move('O'), 6)
        
        # Bottom row win
        self.game.board = [' ', ' ', ' ',  # positions 1,2,3
                           ' ', ' ', ' ',  # positions 4,5,6
                           'X', 'X', ' ']  # positions 7,8,9
        self.assertEqual(self.game.find_winning_move('X'), 9)

    def test_find_winning_move_detects_all_column_wins(self) -> None:
        """Test find_winning_move detects wins in all three columns."""
        # Left column win
        self.game.board = ['X', ' ', ' ',  # positions 1,2,3
                           'X', ' ', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        self.assertEqual(self.game.find_winning_move('X'), 7)
        
        # Middle column win
        self.game.board = [' ', 'O', ' ',  # positions 1,2,3
                           ' ', 'O', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        self.assertEqual(self.game.find_winning_move('O'), 8)
        
        # Right column win
        self.game.board = [' ', ' ', 'X',  # positions 1,2,3
                           ' ', ' ', 'X',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        self.assertEqual(self.game.find_winning_move('X'), 9)

    def test_find_winning_move_detects_both_diagonal_wins(self) -> None:
        """Test find_winning_move detects wins in both diagonals."""
        # Main diagonal win (positions 1,5,9)
        self.game.board = ['X', ' ', ' ',  # positions 1,2,3
                           ' ', 'X', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        self.assertEqual(self.game.find_winning_move('X'), 9)
        
        # Anti-diagonal win (positions 3,5,7)
        self.game.board = [' ', ' ', 'O',  # positions 1,2,3
                           ' ', 'O', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        self.assertEqual(self.game.find_winning_move('O'), 7)

    def test_find_winning_move_with_different_gap_positions(self) -> None:
        """Test find_winning_move when gap is in different positions of a line."""
        # Gap at beginning of row
        self.game.board = [' ', 'X', 'X',  # positions 1,2,3
                           ' ', ' ', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        self.assertEqual(self.game.find_winning_move('X'), 1)
        
        # Gap in middle of row
        self.game.board = ['O', ' ', 'O',  # positions 1,2,3
                           ' ', ' ', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        self.assertEqual(self.game.find_winning_move('O'), 2)
        
        # Gap at end of row (already tested in other tests)

    def test_find_winning_move_prioritizes_first_found_win(self) -> None:
        """Test find_winning_move returns first winning move found when multiple exist."""
        # Multiple winning opportunities for X
        self.game.board = ['X', 'X', ' ',  # positions 1,2,3 - top row win
                           'X', 'O', ' ',  # positions 4,5,6 - left column win
                           ' ', 'O', ' ']  # positions 7,8,9
        
        # Should return position 3 (first row combination checked)
        result = self.game.find_winning_move('X')
        self.assertIn(result, [3, 7])  # Either top row or left column win

    def test_find_winning_move_ignores_opponent_pieces(self) -> None:
        """Test find_winning_move only considers the specified player's pieces."""
        # Board with mixed X and O
        self.game.board = ['X', 'O', ' ',  # positions 1,2,3
                           'X', 'O', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        
        # X can win left column, O can win middle column
        result_x = self.game.find_winning_move('X')
        result_o = self.game.find_winning_move('O')
        
        self.assertEqual(result_x, 7)  # X wins left column
        self.assertEqual(result_o, 8)  # O wins middle column

    def test_find_winning_move_with_blocked_lines(self) -> None:
        """Test find_winning_move when some lines are blocked by opponent."""
        # Lines blocked by opponent pieces - no immediate win possible
        self.game.board = ['X', 'O', 'X',  # positions 1,2,3 - top row blocked
                           'O', 'X', 'O',  # positions 4,5,6 - middle row blocked
                           'O', 'X', 'X']  # positions 7,8,9 - bottom row blocked
        
        # No player can win in one move
        result = self.game.find_winning_move('X')
        self.assertIsNone(result)  # No immediate win possible

    def test_find_winning_move_with_full_board_scenarios(self) -> None:
        """Test find_winning_move with nearly full board."""
        # Board with only one empty position, but no win possible
        self.game.board = ['X', 'O', 'X',  # positions 1,2,3
                           'O', 'X', 'O',  # positions 4,5,6
                           'O', 'X', 'O']  # positions 7,8,9 - changed last to O
        
        result_x = self.game.find_winning_move('X')
        result_o = self.game.find_winning_move('O')
        
        self.assertIsNone(result_x)
        self.assertIsNone(result_o)

    def test_find_winning_move_return_type(self) -> None:
        """Test find_winning_move returns correct types."""
        # Test when win is found
        self.game.board = ['X', 'X', ' ',  # positions 1,2,3
                           ' ', ' ', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        
        result = self.game.find_winning_move('X')
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 9)
        
        # Test when no win is found
        result_none = self.game.find_winning_move('O')
        self.assertIsNone(result_none)

    def test_find_winning_move_with_invalid_player_symbol(self) -> None:
        """Test find_winning_move behavior with invalid player symbols."""
        # Test with invalid symbols - should not find wins
        self.game.board = ['X', 'X', ' ',  # positions 1,2,3
                           ' ', ' ', ' ',  # positions 4,5,6
                           ' ', ' ', ' ']  # positions 7,8,9
        
        # Invalid symbols should return None
        result_invalid = self.game.find_winning_move('Z')
        self.assertIsNone(result_invalid)
        
        result_empty = self.game.find_winning_move('')
        self.assertIsNone(result_empty)

if __name__ == '__main__':
    unittest.main()

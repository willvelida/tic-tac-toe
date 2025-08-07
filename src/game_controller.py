from typing import Optional, Tuple
from src.tic_tac_toe import TicTacToe, GameMode
from src.player import Player, HumanPlayer, AIPlayer, DifficultyLevel
from src.terminal_ui import TerminalUI

class GameController:
    """
    Game controller that orchestrates the interaction between UI, game logic, and players.
    
    Handles game flow, player management, and coordinates between different components
    while maintaining clean separation of concerns.
    """
    
    def __init__(self, ui: TerminalUI):
        """
        Initialize the game controller.
        
        Args:
            ui (TerminalUI): Terminal UI instance for user interaction
        """
        self.ui = ui
        self.game: Optional[TicTacToe] = None
        self.player_x: Optional[Player] = None
        self.player_o: Optional[Player] = None
    
    def play(self) -> None:
        """
        Main entry point to start the game.
        
        Handles game setup, main game loop, and cleanup.
        """
        try:
            # Game setup phase
            if not self._setup_game():
                return  # User chose to quit during setup
            
            # Main game loop
            self._run_game_loop()
            
            # Display final result
            game_state = self.game.get_game_state()
            self.ui.display_game_result(game_state)
            
        except SystemExit:
            # Clean exit requested by user
            raise
        except Exception as e:
            self.ui.show_error(f"An unexpected error occurred: {e}")
            raise
    
    def _setup_game(self) -> bool:
        """
        Set up the game including mode selection and player creation.
        
        Returns:
            bool: True if setup completed successfully, False if user quit
        """
        # Get game mode
        game_mode = self.ui.get_game_mode()
        self.game = TicTacToe(game_mode)
        
        if game_mode == GameMode.HUMAN_VS_HUMAN:
            return self._setup_human_vs_human()
        elif game_mode == GameMode.HUMAN_VS_AI:
            return self._setup_human_vs_ai()
        else:
            self.ui.show_error("Invalid game mode selected")
            return False
    
    def _setup_human_vs_human(self) -> bool:
        """
        Set up human vs human game.
        
        Returns:
            bool: True if setup completed successfully
        """
        self.ui.show_message("Setting up Human vs Human game")
        self.ui.show_message("Player X goes first, Player O goes second")
        
        # Create human players
        self.player_x = HumanPlayer(TicTacToe.PLAYER_X)
        self.player_o = HumanPlayer(TicTacToe.PLAYER_O)
        
        return True
    
    def _setup_human_vs_ai(self) -> bool:
        """
        Set up human vs AI game with symbol and difficulty selection.
        
        Returns:
            bool: True if setup completed successfully, False if user went back
        """
        # Get player symbol choice
        human_symbol = self.ui.get_player_symbol()
        if human_symbol is None:
            return False  # User chose to go back to main menu
        
        # Get AI difficulty
        ai_difficulty = self.ui.get_ai_difficulty()
        
        # Determine AI symbol (opposite of human)
        ai_symbol = TicTacToe.PLAYER_O if human_symbol == TicTacToe.PLAYER_X else TicTacToe.PLAYER_X
        
        # Create players with AI callback for status messages
        human_player = HumanPlayer(human_symbol)
        ai_player = AIPlayer(ai_symbol, ai_difficulty, 
                           status_callback=self.ui.show_ai_status)
        
        # Assign players based on symbols (X always goes first)
        if human_symbol == TicTacToe.PLAYER_X:
            self.player_x = human_player
            self.player_o = ai_player
        else:
            self.player_x = ai_player
            self.player_o = human_player
        
        # Show setup confirmation
        self.ui.show_message(f"Game setup complete!")
        self.ui.show_message(f"Human: {human_symbol}, AI: {ai_symbol} ({ai_difficulty.value})")
        self.ui.show_message(f"Player {TicTacToe.PLAYER_X} goes first")
        
        return True
    
    def _run_game_loop(self) -> None:
        """
        Run the main game loop until game ends.
        
        Handles turn alternation, move processing, and game state checking.
        """
        while True:
            # Display current board
            self.ui.display_board(self.game)
            
            # Check if game is over
            game_state = self.game.get_game_state()
            if game_state['state'] != 'ongoing':
                break
            
            # Get current player and process their move
            current_player = self._get_current_player()
            
            # Display turn information
            is_ai = isinstance(current_player, AIPlayer)
            self.ui.display_turn_info(self.game.current_player, is_ai)
            
            # Get and process move
            move = self._get_player_move(current_player)
            
            try:
                self.game.make_move(move)
            except ValueError as e:
                # This shouldn't happen with proper validation, but just in case
                self.ui.show_error(f"Invalid move: {e}")
                continue
        
        # Display final board
        self.ui.display_board(self.game)
    
    def _get_current_player(self) -> Player:
        """
        Get the current player object based on the game's current player symbol.
        
        Returns:
            Player: Current player object
        """
        if self.game.current_player == TicTacToe.PLAYER_X:
            return self.player_x
        else:
            return self.player_o
    
    def _get_player_move(self, player: Player) -> int:
        """
        Get a move from the specified player.
        
        Args:
            player (Player): Player to get move from
            
        Returns:
            int: Position (1-9) chosen by player
        """
        if isinstance(player, HumanPlayer):
            return self._get_human_move()
        elif isinstance(player, AIPlayer):
            return self._get_ai_move(player)
        else:
            raise ValueError(f"Unknown player type: {type(player)}")
    
    def _get_human_move(self) -> int:
        """
        Get a move from human player using UI with validation and retry.
        
        Returns:
            int: Valid position (1-9) chosen by human player
        """
        return self.ui.get_valid_position(self.game)
    
    def _get_ai_move(self, ai_player: AIPlayer) -> int:
        """
        Get a move from AI player.
        
        Args:
            ai_player (AIPlayer): AI player to get move from
            
        Returns:
            int: Position (1-9) chosen by AI
        """
        # AI calculates move based on current board state
        # The AI status callback will be triggered automatically during thinking delay
        return ai_player.get_move(self.game.board)
    
    def create_new_game(self) -> None:
        """
        Reset the game state for a new game with same players.
        """
        if self.game:
            self.game.reset_board()
            self.ui.show_message("New game started!")
    
    def get_game_statistics(self) -> dict:
        """
        Get current game statistics and state information.
        
        Returns:
            dict: Game statistics including current state, mode, and players
        """
        if not self.game:
            return {"status": "No game in progress"}
        
        return {
            "mode": self.game.get_game_mode().value,
            "current_player": self.game.current_player,
            "game_state": self.game.get_game_state(),
            "moves_made": 9 - self.game.board.count(TicTacToe.EMPTY),
            "player_x_type": type(self.player_x).__name__,
            "player_o_type": type(self.player_o).__name__
        }
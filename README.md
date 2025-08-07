# Terminal Tic-Tac-Toe

A console-based terminal game implementation of classic tic-tac-toe in Python, built with clean architecture principles and comprehensive test coverage.

## Overview

This project implements a terminal-based tic-tac-toe game using object-oriented design patterns. The current implementation focuses on core game mechanics with a robust, extensible architecture that supports future enhancements.

## Technology Requirements

### System Requirements
- **Python**: 3.6 or higher
- **Operating System**: Cross-platform (Windows, macOS, Linux)
- **Terminal**: Any standard terminal/command prompt

### Dependencies
- **Standard Library Only**: No external packages required
- **Testing**: Built-in `unittest` module
- **Type Hints**: Native Python typing support

### Development Tools (Optional)
```bash
# For enhanced testing
pip install pytest

# For code formatting
pip install black

# For linting
pip install pylint
```

## Architecture

### System Architecture
```
┌─────────────────────────────────────────────────────┐
│                  Terminal UI                        │
│              (TerminalUI Class)                     │
│  • Enhanced Board Display  • Input Validation      │
│  • Game Mode Selection     • Status Messages       │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│               Game Controller                       │
│            (GameController Class)                   │
│  • Game Flow Orchestration  • Component Coordination│
│  • Player Management        • UI Integration        │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                Player Layer                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Player    │  │ HumanPlayer │  │  AIPlayer   │  │
│  │ (Abstract)  │  │             │  │ (Complete)  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                Game Engine                          │
│                TicTacToe Class                      │
│  • Board Management    • Move Validation           │
│  • Player Turns        • Game State                │
└─────────────────────────────────────────────────────┘
```

### Class Architecture
```
TerminalUI
├── display_board(board) → None
├── display_message(message, message_type) → None
├── get_game_mode() → str
├── get_player_symbol() → str
├── get_valid_position(board) → int
├── display_welcome() → None
├── display_winner(winner, player1_symbol, player2_symbol) → None
├── display_draw() → None
└── ask_play_again() → bool

GameController
├── ui: TerminalUI
├── game: TicTacToe
├── player1: Player
├── player2: Player
├── __init__(ui) → None
├── play() → None
├── _setup_game() → None
├── _play_game() → None
├── _get_player_move(player) → int
└── _ai_status_callback(message) → None

Player (ABC)
├── symbol: str
├── get_move(board) → int [abstract]
└── choose_symbol() → str [classmethod factory]
    │
    ├── HumanPlayer
    │   └── get_move(board) → int [raises NotImplementedError - uses GameController]
    │
    └── AIPlayer
        ├── difficulty: DifficultyLevel
        ├── opponent_symbol: str
        ├── status_callback: Optional[Callable]
        ├── get_move(board) → int
        ├── _get_best_move_minimax(board) → int
        ├── _minimax(board, depth, is_maximizing) → int
        ├── _evaluate_position(board) → int
        ├── _apply_difficulty_filter(move, board) → int
        └── _simulate_thinking_delay() → None

TicTacToe
├── EMPTY = ' '
├── PLAYER_X = 'X'  
├── PLAYER_O = 'O'
├── board: List[str]
├── current_player: str
├── game_mode: GameMode
├── reset_board() → None
├── is_valid_move(position) → bool
├── make_move(position) → None [Enhanced: auto player switching]
├── check_winner() → Optional[str]
├── _check_line(positions) → Optional[str] [Helper method]
├── is_board_full() → bool
├── is_draw() → bool
├── get_game_state() → Dict[str, str]
├── get_game_mode() → GameMode
├── is_ai_mode() → bool
├── get_display_value(position) → str
└── display_board() → None

GameMode (Enum)
├── HUMAN_VS_HUMAN = 'human_vs_human'
└── HUMAN_VS_AI = 'human_vs_ai'
└── HUMAN_VS_AI = 'human_vs_ai'

DifficultyLevel (Enum)
├── EASY = 'easy'
├── MEDIUM = 'medium'
└── HARD = 'hard'
```

### Design Patterns Used
- **Model-View-Controller (MVC)**: Clear separation between UI (TerminalUI), Controller (GameController), and Model (TicTacToe)
- **Abstract Factory Pattern**: `Player.choose_symbol()` for player creation
- **Template Method Pattern**: Abstract `Player.get_move()` implementation
- **Strategy Pattern**: Polymorphic player handling with minimax AI
- **Observer Pattern**: Callback system for AI status messages
- **Single Responsibility**: Each class has one clear purpose
- **Dependency Injection**: UI and callback dependencies injected into controllers
- **Enum Pattern**: Type-safe game modes and difficulty levels

## Current Implementation Status

### ✅ Completed (Phase 1, 2, 3 & 4)
- **Core Game Engine**: Complete TicTacToe class with board management and game logic
- **Player System**: Abstract Player base class with HumanPlayer and AIPlayer implementations
- **AI Intelligence**: Minimax algorithm with game tree evaluation and multiple difficulty levels
- **Game Logic**: Complete win/draw detection algorithms with all 8 winning combinations
- **Move Validation**: Multi-layer validation with range and occupancy checking  
- **Game State Management**: Dictionary-based state tracking for extensibility
- **Game Mode System**: Enum-based HUMAN_VS_HUMAN and HUMAN_VS_AI modes
- **AI Features**: Three difficulty levels (Easy 30%, Medium 70%, Hard 100% optimal)
- **Performance Optimization**: Early termination strategy reducing ~90% of minimax calls
- **Terminal UI System**: Complete TerminalUI class with enhanced board display and input validation
- **Game Controller**: MVC architecture with GameController orchestrating all components
- **Enhanced User Experience**: ASCII art board, game mode selection, player symbol choice
- **Callback System**: AI status messages integrated through dependency injection
- **Comprehensive Testing**: 153+ tests with 100% pass rate across all components
- **Code Quality**: PEP 8 compliant with full type hints and clean architecture

### 🔄 In Development (Phase 5)
- **Statistics Tracking**: Game statistics and performance analytics
- **Replay System**: Game replay functionality with move history
- **Enhanced Features**: Additional gameplay modes and customization options

## Installation & Testing

### Quick Start
```bash
# Clone repository
git clone https://github.com/willvelida/tic-tac-toe.git
cd tic-tac-toe

# Run the game
python src/main.py

# Run comprehensive test suite
python -m unittest discover test/ -v

# Expected output: 153+ tests passing ✅
```

### Test Coverage
```bash
# TicTacToe core functionality and game logic: 59 tests
python -m unittest test.tic_tac_toe_test -v

# Player system (Human + AI): 46 tests  
python -m unittest test.player_test -v

# Game Controller orchestration: 20+ tests
python -m unittest test.game_controller_test -v

# Terminal UI components: 28+ tests
python -m unittest test.terminal_ui_test -v

# Total: 153+ comprehensive tests with 100% pass rate
```

## Code Examples

### Complete Game Setup (Recommended)
```python
from src.terminal_ui import TerminalUI
from src.game_controller import GameController

# Complete game with enhanced UI
ui = TerminalUI()
controller = GameController(ui)
controller.play()  # Full game experience with menus and validation
```

### Manual Game Setup
```python
from src.tic_tac_toe import TicTacToe, GameMode
from src.player import HumanPlayer, AIPlayer, DifficultyLevel
from src.terminal_ui import TerminalUI

# Initialize components
ui = TerminalUI()
game = TicTacToe(mode=GameMode.HUMAN_VS_AI)
human_player = HumanPlayer('X')
ai_player = AIPlayer('O', DifficultyLevel.HARD)

# Display enhanced board
ui.display_board(game.board)

# Get validated user input
position = ui.get_valid_position(game.board)
game.make_move(position)

# AI move with status callback
def status_callback(message):
    ui.display_message(message, "info")

ai_player.status_callback = status_callback
ai_move = ai_player.get_move(game.board)
game.make_move(ai_move)
```

### Basic Game Operations
```python
from src.tic_tac_toe import TicTacToe, GameMode

# Initialize game with mode selection
game = TicTacToe(mode=GameMode.HUMAN_VS_HUMAN)

# Game operations
game.reset_board()

# Make moves with validation
if game.is_valid_move(5):
    game.make_move(5)  # Automatically switches players
    
# Check game state
state = game.get_game_state()
print(f"Game state: {state['state']}")  # 'ongoing', 'won', or 'draw'

# Win detection
winner = game.check_winner()
if winner:
    print(f"Winner: {winner}")
    
# Draw detection
if game.is_draw():
    print("Game is a draw!")
```

### Player Creation
```python
from src.player import Player, HumanPlayer, AIPlayer, DifficultyLevel

# Interactive symbol selection
symbol = Player.choose_symbol()  # Menu: X, O, Random, Quit
player = HumanPlayer(symbol)

# AI player creation
ai_player = AIPlayer('O', DifficultyLevel.HARD)
```

### AI Gameplay Examples
```python
from src.player import AIPlayer, DifficultyLevel
from src.tic_tac_toe import TicTacToe, GameMode
from src.terminal_ui import TerminalUI

# Create AI game with UI integration
ui = TerminalUI()
game = TicTacToe(mode=GameMode.HUMAN_VS_AI)

# AI with status callback for user feedback
def ai_status_callback(message):
    ui.display_message(message, "info")

ai = AIPlayer('O', DifficultyLevel.MEDIUM, status_callback=ai_status_callback)

# AI makes intelligent moves with user feedback
move = ai.get_move(game.board)  # Shows "AI is thinking..." message

# Different AI difficulties
easy_ai = AIPlayer('O', DifficultyLevel.EASY)    # 30% optimal play
medium_ai = AIPlayer('O', DifficultyLevel.MEDIUM) # 70% optimal play  
hard_ai = AIPlayer('O', DifficultyLevel.HARD)     # 100% optimal play

# AI features realistic thinking delays and status messages
```

## Project Structure
```
tic-tac-toe/
├── src/
│   ├── __init__.py
│   ├── tic_tac_toe.py      # Core game engine
│   ├── player.py           # Player class hierarchy (Human + AI)
│   ├── terminal_ui.py      # Terminal user interface
│   ├── game_controller.py  # Game flow orchestration
│   └── main.py            # Application entry point
├── test/
│   ├── __init__.py
│   ├── tic_tac_toe_test.py # Game engine tests (59)
│   ├── player_test.py      # Player system tests (46)
│   ├── game_controller_test.py # Controller tests (20+)
│   └── terminal_ui_test.py # UI component tests (28+)
├── docs/                   # Project documentation
│   ├── phase-*-*.md       # Implementation phase plans
│   └── pr-*.md           # Pull request documentation
├── LICENSE                 # MIT License
└── README.md              # This file
```

## Quality Metrics

- **Test Coverage**: 153+ tests passing (100% pass rate)
- **Architecture**: Clean MVC separation with dependency injection
- **AI Intelligence**: Minimax algorithm with 3 difficulty levels
- **Performance**: Early termination optimization (~90% minimax call reduction)
- **User Experience**: Enhanced terminal UI with ASCII art and input validation
- **Code Quality**: PEP 8 compliant with defensive programming patterns
- **Type Safety**: Full type hint coverage with enum-based configurations
- **Documentation**: Comprehensive docstrings for all classes and methods
- **Testing**: Mock-based unit tests with integration scenario coverage
- **Maintainability**: Single responsibility principle with clear interfaces
- **Extensibility**: Plugin-ready architecture for future UI implementations
- **Gameplay**: O(1) game operations with sub-second AI response times

## Contributing

This project follows systematic development phases. See the `docs/` directory for detailed implementation plans and architectural decisions.

### Development Standards
- Test-driven development (TDD)
- PEP 8 code style compliance
- Comprehensive docstrings
- Type hints for all functions

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Current Status**: Phase 4 Complete | 153+ Tests Passing ✅ | Enhanced Terminal UI Ready

# Terminal Tic-Tac-Toe

A console-based terminal game implementation of classic tic-tac-toe in Python, built with clean architecture principles and comprehensive test coverage.

## Overview

This project implements a terminal-based tic-tac-toe game using object-oriented design patterns. The implementation features a robust, extensible architecture with complete testing coverage and professional-grade documentation.

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

## Quick Start

### Installation & Running
```bash
# Clone repository
git clone https://github.com/willvelida/tic-tac-toe.git
cd tic-tac-toe

# Run the game (recommended way)
python main.py

# Run demo mode
python main.py --demo

# Run comprehensive test suite
python -m unittest discover test -v

# Expected output: 234 tests passing ✅
```

### Game Features
- **Human vs Human**: Play with a friend locally
- **Human vs AI**: Challenge intelligent AI with 3 difficulty levels
- **Smart AI**: Minimax algorithm with early termination optimization
- **Session Statistics**: Track wins, losses, and draws across games
- **Enhanced UI**: ASCII art board with clear position indicators
- **Input Validation**: Comprehensive error handling and retry logic
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Architecture

### Project Structure
```
tic-tac-toe/
├── main.py                 # ✨ Entry point (run from here)
├── src/
│   ├── __init__.py
│   ├── tic_tac_toe.py      # Core game engine
│   ├── player.py           # Player class hierarchy (Human + AI)
│   ├── terminal_ui.py      # Terminal user interface
│   └── game_controller.py  # Game flow orchestration
├── test/
│   ├── __init__.py
│   ├── tic_tac_toe_test.py # Game engine tests (109)
│   ├── player_test.py      # Player system tests (66)
│   ├── game_controller_test.py # Controller tests (30)
│   └── terminal_ui_test.py # UI component tests (29)
├── docs/                   # Project documentation
│   ├── phase-*-*.md       # Implementation phase plans
│   └── conversation-transcript.md # Development history
├── LICENSE                 # MIT License
└── README.md              # This file
```

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
├── display_board(game) → None
├── get_game_mode() → GameMode
├── get_ai_difficulty() → DifficultyLevel
├── get_valid_position(game) → int
├── show_message(message) → None
├── show_error(message) → None
└── display_game_result(winner, is_draw) → None

GameController
├── ui: TerminalUI
├── game: TicTacToe
├── play() → None
├── get_game_statistics() → dict
└── _get_human_move() → int

Player (ABC)
├── symbol: str
├── get_move(board) → int [abstract]
└── choose_symbol() → str [classmethod factory]
    │
    ├── HumanPlayer
    │   └── get_move(board) → int [uses GameController for input]
    │
    └── AIPlayer
        ├── difficulty: DifficultyLevel
        ├── enable_delay: bool
        ├── get_move(board) → int
        ├── _get_best_move_minimax(board) → int
        ├── _minimax(board, depth, is_maximizing) → int
        └── _simulate_thinking_delay() → None

TicTacToe
├── EMPTY = ' '
├── PLAYER_X = 'X'  
├── PLAYER_O = 'O'
├── board: List[str]
├── current_player: str
├── game_mode: GameMode
├── make_move(position) → None
├── check_winner() → Optional[str]
├── is_board_full() → bool
├── is_draw() → bool
├── get_game_state() → str
└── reset_board() → None

GameMode (Enum)
├── HUMAN_VS_HUMAN = 'human_vs_human'
└── HUMAN_VS_AI = 'human_vs_ai'

DifficultyLevel (Enum)
├── EASY = 'easy'    # 30% optimal play
├── MEDIUM = 'medium' # 70% optimal play
└── HARD = 'hard'     # 100% optimal play
```

### Design Patterns Used
- **Model-View-Controller (MVC)**: Clear separation between UI (TerminalUI), Controller (GameController), and Model (TicTacToe)
- **Abstract Factory Pattern**: `Player.choose_symbol()` for player creation
- **Template Method Pattern**: Abstract `Player.get_move()` implementation
- **Strategy Pattern**: Polymorphic player handling with minimax AI
- **Single Responsibility**: Each class has one clear purpose
- **Dependency Injection**: UI dependencies injected into controllers
- **Enum Pattern**: Type-safe game modes and difficulty levels

## Current Implementation Status

### ✅ Phase 6 Complete - Testing & Documentation
- **Comprehensive Testing**: 234 tests with 100% pass rate across all components
- **Test Coverage**: Win conditions, draw conditions, input validation, AI behavior, and game modes
- **Modern Architecture**: Clean imports with main.py at project root
- **Performance Verified**: AI response times under 2 seconds consistently
- **Cross-Platform**: Tested on Windows (primary), compatible with macOS and Linux
- **Documentation**: Complete README with installation, usage, and API examples
- **Code Quality**: PEP 8 compliant with comprehensive docstrings and type hints

### ✅ Previous Phases (1-5)
- **Core Game Engine**: Complete TicTacToe class with board management and game logic
- **Player System**: Abstract Player base class with HumanPlayer and AIPlayer implementations
- **AI Intelligence**: Minimax algorithm with game tree evaluation and three difficulty levels
- **Game Logic**: Complete win/draw detection algorithms with all 8 winning combinations
- **Move Validation**: Multi-layer validation with range and occupancy checking  
- **Game State Management**: Robust state tracking for extensibility
- **Game Mode System**: Enum-based HUMAN_VS_HUMAN and HUMAN_VS_AI modes
- **AI Features**: Three difficulty levels (Easy 30%, Medium 70%, Hard 100% optimal)
- **Performance Optimization**: Early termination strategy reducing ~90% of minimax calls
- **Terminal UI System**: Complete TerminalUI class with enhanced board display and input validation
- **Game Controller**: MVC architecture with GameController orchestrating all components
- **Enhanced User Experience**: ASCII art board, game mode selection, player symbol choice
- **Session Statistics**: Real-time tracking of games played with comprehensive error handling
- **Game Flow Polish**: Welcome messages, AI announcements, smooth restart functionality
- **Production Quality**: Robust error recovery and graceful degradation for edge cases

## Installation & Testing

### Quick Start
```bash
# Clone repository
git clone https://github.com/willvelida/tic-tac-toe.git
cd tic-tac-toe

# Run the game
python main.py

# Run demo mode
python main.py --demo

# Run comprehensive test suite
python -m unittest discover test -v

# Expected output: 234 tests passing ✅
```

### Test Coverage Summary
```bash
# All tests (recommended)
python -m unittest discover test -v

# Individual test modules:
# TicTacToe core game logic: 109 tests
python -m unittest test.tic_tac_toe_test -v

# Player system (Human + AI with modern architecture): 66 tests  
python -m unittest test.player_test -v

# Game Controller orchestration: 30 tests
python -m unittest test.game_controller_test -v

# Terminal UI components: 29 tests
python -m unittest test.terminal_ui_test -v

# Total: 234 comprehensive tests with 100% pass rate
```

### Performance Testing
```bash
# Test AI response times (should be under 2 seconds)
python main.py --demo

# Manual performance verification:
# 1. Start a Human vs AI game
# 2. Observe AI thinking messages
# 3. Verify responses are quick and responsive
```

## Code Examples

### Complete Game Setup (Recommended)
```python
from src.terminal_ui import TerminalUI
from src.game_controller import GameController

# Complete game with enhanced UI
ui = TerminalUI()
controller = GameController(ui)
controller.play()  # Full game experience
```

### Basic Game Operations
```python
from src.tic_tac_toe import TicTacToe, GameMode

# Initialize game with mode selection
game = TicTacToe(GameMode.HUMAN_VS_HUMAN)

# Game operations
game.reset_board()

# Make moves with validation
if game.is_valid_move(5):
    game.make_move(5)  # Automatically switches players
    
# Check game state
winner = game.check_winner()
if winner:
    print(f"Winner: {winner}")
elif game.is_draw():
    print("Game is a draw!")
else:
    print("Game continues...")
```

### Player Creation and Symbol Selection
```python
from src.player import Player, HumanPlayer, AIPlayer, DifficultyLevel

# Interactive symbol selection with menu
symbol = Player.choose_symbol()  # Menu: X, O, Random, Quit
player = HumanPlayer(symbol)

# AI player creation with difficulty levels
easy_ai = AIPlayer('O', DifficultyLevel.EASY)    # 30% optimal play
medium_ai = AIPlayer('O', DifficultyLevel.MEDIUM) # 70% optimal play  
hard_ai = AIPlayer('O', DifficultyLevel.HARD)     # 100% optimal play
```

### Advanced AI Features
```python
from src.player import AIPlayer, DifficultyLevel
from src.tic_tac_toe import TicTacToe, GameMode

# AI with thinking delay simulation
ai = AIPlayer('O', DifficultyLevel.HARD, enable_delay=True)
game = TicTacToe(GameMode.HUMAN_VS_AI)

# AI makes intelligent moves with realistic delays
move = ai.get_move(game.board)  # Shows "AI opponent is thinking..."

# Disable delay for testing
test_ai = AIPlayer('X', DifficultyLevel.EASY, enable_delay=False)
fast_move = test_ai.get_move(game.board)  # Instant response
```

### Terminal UI Integration
```python
from src.terminal_ui import TerminalUI
from src.tic_tac_toe import TicTacToe, GameMode

# Enhanced terminal interface
ui = TerminalUI()
game = TicTacToe(GameMode.HUMAN_VS_HUMAN)

# Display beautiful ASCII board
ui.display_board(game)

# Get validated user input with retry logic
position = ui.get_valid_position(game)  # Handles errors gracefully

# Show messages to user
ui.show_message("Welcome to Tic-Tac-Toe!")
ui.show_error("Invalid position. Try again.")

# Display game results
winner = game.check_winner()
is_draw = game.is_draw()
ui.display_game_result(winner, is_draw)
```

## Project Structure
```
tic-tac-toe/
├── main.py                 # ✨ Entry point (run from here)
├── src/
│   ├── __init__.py
│   ├── tic_tac_toe.py      # Core game engine
│   ├── player.py           # Player class hierarchy (Human + AI)
│   ├── terminal_ui.py      # Terminal user interface
│   └── game_controller.py  # Game flow orchestration
├── test/
│   ├── __init__.py
│   ├── tic_tac_toe_test.py # Game engine tests (109)
│   ├── player_test.py      # Player system tests (66)
│   ├── game_controller_test.py # Controller tests (30)
│   └── terminal_ui_test.py # UI component tests (29)
├── docs/                   # Project documentation
│   ├── phase-*-*.md       # Implementation phase plans
│   └── conversation-transcript.md # Development history
├── LICENSE                 # MIT License
└── README.md              # This file
```

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# ❌ ModuleNotFoundError: No module named 'src'
python src/main.py  # Wrong - don't run from src directory

# ✅ Correct way to run
python main.py      # Run from project root directory
```

**Python Version Issues**
```bash
# Check your Python version
python --version    # Should be 3.6 or higher

# If using multiple Python versions
python3 main.py     # Use python3 explicitly
```

**Terminal Display Issues**
- **Windows**: Use Command Prompt or PowerShell, avoid Git Bash for best display
- **macOS/Linux**: Any standard terminal should work
- **Special Characters**: Ensure terminal supports Unicode for emoji display

**AI Response Times**
- Normal: AI responds within 1-2 seconds
- If slow: Disable thinking delay with `enable_delay=False` in AI constructor
- Performance varies by system, but should remain under 2 seconds

### Getting Help

1. **Check test results**: `python -m unittest discover test -v`
2. **Verify installation**: All tests should pass (234/234)
3. **Review examples**: See code examples above for proper usage
4. **Check Python version**: Ensure Python 3.6+ is installed

## Quality Metrics

- **Test Coverage**: 234 tests passing (100% pass rate)
- **Architecture**: Clean MVC separation with dependency injection
- **AI Intelligence**: Minimax algorithm with 3 difficulty levels and early termination optimization
- **Performance**: AI response times consistently under 2 seconds
- **User Experience**: Enhanced terminal UI with ASCII art and comprehensive input validation
- **Code Quality**: PEP 8 compliant with defensive programming patterns and comprehensive error handling
- **Type Safety**: Full type hint coverage with enum-based configurations
- **Documentation**: Comprehensive docstrings and API documentation
- **Testing**: Mock-based unit tests with integration scenario coverage
- **Maintainability**: Single responsibility principle with clear interfaces
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Modernization**: Clean project structure with main.py at root, fixed import architecture

## Contributing

This project follows systematic development phases documented in the `docs/` directory. 

### Development Standards
- **Test-Driven Development (TDD)**: All features backed by comprehensive tests
- **PEP 8 Compliance**: Clean, readable Python code
- **Type Hints**: Full type annotation coverage
- **Documentation**: Comprehensive docstrings for all methods
- **Error Handling**: Defensive programming with graceful degradation

### Phase 6 Achievements
- ✅ **234 comprehensive tests** covering all functionality
- ✅ **Modern project structure** with main.py at root
- ✅ **Performance verification** with AI response time validation
- ✅ **Complete documentation** with installation and usage examples
- ✅ **Cross-platform compatibility** tested and verified

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Current Status**: Phase 6 Complete | 234 Tests Passing ✅ | Production Ready 🚀

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
│                   Terminal UI                       │
│                 (Future Phase)                      │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                Player Layer                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Player    │  │ HumanPlayer │  │  AIPlayer   │  │
│  │ (Abstract)  │  │             │  │  (Future)   │  │
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
Player (ABC)
├── symbol: str
├── get_move(board) → int [abstract]
└── choose_symbol() → str [classmethod factory]
    │
    ├── HumanPlayer
    │   ├── get_move(board) → int
    │   └── Input validation & error handling
    │
    └── AIPlayer
        ├── difficulty: DifficultyLevel
        ├── opponent_symbol: str
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

DifficultyLevel (Enum)
├── EASY = 'easy'
├── MEDIUM = 'medium'
└── HARD = 'hard'
```

### Design Patterns Used
- **Abstract Factory Pattern**: `Player.choose_symbol()` for player creation
- **Template Method Pattern**: Abstract `Player.get_move()` implementation
- **Strategy Pattern**: Polymorphic player handling with minimax AI
- **Single Responsibility**: Each class has one clear purpose
- **Enum Pattern**: Type-safe game modes and difficulty levels

## Current Implementation Status

### ✅ Completed (Phase 1, 2 & 3)
- **Core Game Engine**: Complete TicTacToe class with board management and game logic
- **Player System**: Abstract Player base class with HumanPlayer and AIPlayer implementations
- **AI Intelligence**: Minimax algorithm with game tree evaluation and multiple difficulty levels
- **Game Logic**: Complete win/draw detection algorithms with all 8 winning combinations
- **Move Validation**: Multi-layer validation with range and occupancy checking  
- **Game State Management**: Dictionary-based state tracking for extensibility
- **Game Mode System**: Enum-based HUMAN_VS_HUMAN and HUMAN_VS_AI modes
- **Input Validation**: Comprehensive error handling and edge case coverage
- **AI Features**: Three difficulty levels (Easy 30%, Medium 70%, Hard 100% optimal)
- **Performance Optimization**: Early termination strategy reducing ~90% of minimax calls
- **Test Suite**: 105 tests with 100% pass rate (Phase 1: 16, Phase 2: 43, Phase 3: 46 tests)
- **Code Quality**: PEP 8 compliant with full type hints and defensive programming

### 🔄 In Development (Phase 4)
- **Enhanced UI**: Improved terminal interface with grid formatting and color coding
- **Game Messages**: Status updates and user guidance throughout gameplay
- **Input Validation**: Enhanced error handling and user-friendly messages

## Installation & Testing

### Quick Start
```bash
# Clone repository
git clone https://github.com/willvelida/tic-tac-toe.git
cd tic-tac-toe

# Run comprehensive test suite (Phase 1, 2 & 3)
python -m unittest discover test/ -v

# Expected output: 105/105 tests passing ✅
```

### Test Coverage
```bash
# TicTacToe core functionality and game logic: 59 tests
python -m unittest test.tic_tac_toe_test -v

# Player system (Human + AI): 46 tests  
python -m unittest test.player_test -v

# Total: 105 comprehensive tests with 100% pass rate
```

## Code Examples

### Basic Game Operations
```python
from src.tic_tac_toe import TicTacToe, GameMode
from src.player import HumanPlayer

# Initialize game with mode selection
game = TicTacToe(mode=GameMode.HUMAN_VS_HUMAN)
player = HumanPlayer('X')

# Game operations
game.reset_board()
game.display_board()

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

# Create AI game
game = TicTacToe(mode=GameMode.HUMAN_VS_AI)
ai = AIPlayer('O', DifficultyLevel.MEDIUM)

# AI makes intelligent moves
move = ai.get_move(game.board)  # Returns optimal position (1-9)

# Different AI difficulties
easy_ai = AIPlayer('O', DifficultyLevel.EASY)    # 30% optimal play
medium_ai = AIPlayer('O', DifficultyLevel.MEDIUM) # 70% optimal play  
hard_ai = AIPlayer('O', DifficultyLevel.HARD)     # 100% optimal play

# AI features realistic thinking delays
# Displays "AI is thinking..." during move calculation
```

## Project Structure
```
tic-tac-toe/
├── src/
│   ├── tic_tac_toe.py      # Core game engine
│   └── player.py           # Player class hierarchy (Human + AI)
├── test/
│   ├── tic_tac_toe_test.py # Game engine tests (59)
│   └── player_test.py      # Player system tests (46)
├── docs/                   # Project documentation
├── LICENSE                 # MIT License
└── README.md              # This file
```

## Quality Metrics

- **Test Coverage**: 105/105 tests passing (100%)
- **AI Intelligence**: Minimax algorithm with 3 difficulty levels
- **Performance**: Early termination optimization (~90% minimax call reduction)
- **Code Quality**: PEP 8 compliant with defensive programming patterns
- **Type Safety**: Full type hint coverage with enum-based game modes and difficulty levels
- **Documentation**: Comprehensive docstrings for all classes and methods
- **Architecture**: Clean separation of concerns with extensible design
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

**Current Status**: Phase 3 Complete | 105/105 Tests Passing ✅ | AI Implementation Ready

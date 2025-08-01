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
    └── HumanPlayer
        ├── get_move(board) → int
        └── Input validation & error handling

TicTacToe
├── EMPTY = ' '
├── PLAYER_X = 'X'  
├── PLAYER_O = 'O'
├── board: List[str]
├── current_player: str
├── reset_board() → None
├── is_valid_move(position) → bool
├── make_move(position, symbol) → None
├── get_display_value(position) → str
└── display_board() → None
```

### Design Patterns Used
- **Abstract Factory Pattern**: `Player.choose_symbol()` for player creation
- **Template Method Pattern**: Abstract `Player.get_move()` implementation
- **Strategy Pattern**: Polymorphic player handling
- **Single Responsibility**: Each class has one clear purpose

## Current Implementation Status

### ✅ Completed (Phase 1)
- **Core Game Engine**: Complete TicTacToe class with board management
- **Player System**: Abstract Player base class and HumanPlayer implementation
- **Input Validation**: Comprehensive error handling and edge case coverage
- **Test Suite**: 47 tests with 100% pass rate
- **Code Quality**: PEP 8 compliant with full type hints

### 🔄 In Development
- **Game Logic**: Win/draw detection algorithms
- **AI Player**: Intelligent computer opponent
- **Enhanced UI**: Improved terminal interface

## Installation & Testing

### Quick Start
```bash
# Clone repository
git clone https://github.com/willvelida/tic-tac-toe.git
cd tic-tac-toe

# Run comprehensive test suite
python -m unittest discover test/ -v

# Expected output: 47/47 tests passing ✅
```

### Test Coverage
```bash
# TicTacToe core functionality: 16 tests
python -m unittest test.tic_tac_toe_test -v

# Player system: 31 tests  
python -m unittest test.player_test -v
```

## Code Examples

### Basic Game Operations
```python
from src.tic_tac_toe import TicTacToe
from src.player import HumanPlayer

# Initialize game
game = TicTacToe()
player = HumanPlayer('X')

# Game operations
game.reset_board()
game.display_board()
if game.is_valid_move(5):
    game.make_move(5, player.symbol)
```

### Player Creation
```python
from src.player import Player

# Interactive symbol selection
symbol = Player.choose_symbol()  # Menu: X, O, Random, Quit
player = HumanPlayer(symbol)
```

## Project Structure
```
tic-tac-toe/
├── src/
│   ├── tic_tac_toe.py      # Core game engine
│   └── player.py           # Player class hierarchy
├── test/
│   ├── tic_tac_toe_test.py # Game engine tests (16)
│   └── player_test.py      # Player system tests (31)
├── docs/                   # Project documentation
├── LICENSE                 # MIT License
└── README.md              # This file
```

## Quality Metrics

- **Test Coverage**: 47/47 tests passing (100%)
- **Code Style**: PEP 8 compliant
- **Type Safety**: Full type hint coverage
- **Documentation**: Comprehensive docstrings
- **Architecture**: Clean separation of concerns

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

**Current Status**: Phase 1 Complete | 47/47 Tests Passing ✅

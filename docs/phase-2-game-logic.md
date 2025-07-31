---
goal: Implement game logic including move validation and win detection
phase: 2
version: 1.0
date_created: 2025-07-31
last_updated: 2025-07-31
owner: willvelida
status: 'Planned'
tags: ['phase-2', 'logic', 'validation', 'win-detection']
---

# Phase 2: Game Logic

![Status: Planned](https://img.shields.io/badge/status-Planned-blue)

This phase implements the core game logic including move validation, win detection, draw detection, and game state management.

## Implementation Steps

1. **TASK-007**: Implement move validation (check if position is empty and valid)
   - Create `is_valid_move(position)` method
   - Check if position is within range (1-9)
   - Verify position is not already occupied
   - Return boolean indicating move validity

2. **TASK-008**: Implement place_move method to update board state
   - Create `make_move(position, player_symbol)` method
   - Update board with player symbol at specified position
   - Convert 1-9 position to board array index (0-8)
   - Return success/failure status

3. **TASK-009**: Create win detection algorithm for all possible winning combinations
   - Implement `check_winner()` method
   - Check all 3 rows for three in a row
   - Check all 3 columns for three in a row
   - Check both diagonals for three in a row
   - Return winning player symbol or None

4. **TASK-010**: Implement draw detection (board full with no winner)
   - Create `is_board_full()` method to check if all positions occupied
   - Implement `is_draw()` method combining board full check with no winner
   - Return boolean indicating draw state

5. **TASK-011**: Create game state tracking (ongoing, won, draw)
   - Implement `get_game_state()` method
   - Return enum or string: 'ongoing', 'won', 'draw'
   - Include winner information when game is won

6. **TASK-012**: Implement game mode selection system
   - Create `GameMode` enum or constants for 'human_vs_human', 'human_vs_ai'
   - Add game mode attribute to TicTacToe class
   - Implement mode selection logic in game initialization

## Test-Driven Development (TDD) Tests

- **TEST-P2-001**: Test move validation rejects positions outside range (0, 10, -1, etc.)
- **TEST-P2-002**: Test move validation rejects occupied positions
- **TEST-P2-003**: Test move validation accepts valid empty positions (1-9)
- **TEST-P2-004**: Test make_move correctly places symbol on board
- **TEST-P2-005**: Test make_move converts position numbers to array indices correctly
- **TEST-P2-006**: Test win detection for all 3 horizontal rows
- **TEST-P2-007**: Test win detection for all 3 vertical columns
- **TEST-P2-008**: Test win detection for both diagonal lines
- **TEST-P2-009**: Test win detection returns correct winner (X or O)
- **TEST-P2-010**: Test win detection returns None when no winner
- **TEST-P2-011**: Test draw detection when board is full with no winner
- **TEST-P2-012**: Test draw detection returns False when board not full
- **TEST-P2-013**: Test draw detection returns False when there is a winner
- **TEST-P2-014**: Test game state returns 'ongoing' for incomplete games
- **TEST-P2-015**: Test game state returns 'won' with correct winner
- **TEST-P2-016**: Test game state returns 'draw' for tied games
- **TEST-P2-017**: Test game mode selection and storage

## Alternatives Considered

- **ALT-P2-001**: Use bit manipulation for win detection optimization - Rejected as premature optimization for 3x3 grid
- **ALT-P2-002**: Store all winning combinations in lookup table - Accepted as clean and readable approach
- **ALT-P2-003**: Implement game state as finite state machine - Deferred as current approach is simpler

## Risks & Assumptions

- **RISK-P2-001**: Win detection algorithm may have bugs with edge cases - Mitigation: Comprehensive test coverage for all winning combinations
- **RISK-P2-002**: Position numbering (1-9) vs array indexing (0-8) may cause off-by-one errors - Mitigation: Clear conversion logic and thorough testing
- **ASSUMPTION-P2-001**: Players will input positions as numbers 1-9 rather than coordinates
- **ASSUMPTION-P2-002**: Game state tracking is sufficient without move history

## Acceptance Criteria

- [ ] Move validation correctly identifies valid and invalid moves
- [ ] Board updates correctly when valid moves are made
- [ ] Win detection correctly identifies all possible winning combinations
- [ ] Win detection correctly identifies the winning player
- [ ] Draw detection correctly identifies tied games
- [ ] Game state tracking correctly reflects current game status
- [ ] All position-to-index conversions work correctly
- [ ] All tests pass with 100% coverage for implemented functionality
- [ ] Code follows PEP 8 style guidelines
- [ ] All methods have comprehensive docstrings

## Next Phase

Once Phase 2 is complete, proceed to [Phase 3: AI Implementation](phase-3-ai-implementation.md) to implement the intelligent AI opponent.

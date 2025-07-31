---
goal: Implement AI opponent with minimax algorithm and difficulty levels
phase: 3
version: 1.0
date_created: 2025-07-31
last_updated: 2025-07-31
owner: willvelida
status: 'Planned'
tags: ['phase-3', 'ai', 'minimax', 'strategy']
---

# Phase 3: AI Implementation

![Status: Planned](https://img.shields.io/badge/status-Planned-blue)

This phase implements an intelligent AI opponent using the minimax algorithm with multiple difficulty levels and realistic gameplay behavior.

## Implementation Steps

1. **TASK-013**: Create `AIPlayer` class implementing intelligent gameplay
   - Inherit from `Player` base class established in Phase 1
   - Initialize with difficulty level parameter
   - Implement concrete `get_move()` method using AI strategy
   - Store AI symbol (X or O) and opponent symbol

2. **TASK-014**: Implement minimax algorithm for optimal move calculation
   - Create `minimax(board, depth, is_maximizing)` method
   - Implement recursive game tree traversal
   - Return best move score for current position
   - Handle terminal states (win, loss, draw)

3. **TASK-015**: Add game tree evaluation with win/loss/draw scoring
   - Implement `evaluate_position(board)` method
   - Return +10 for AI win, -10 for AI loss, 0 for draw
   - Account for depth to prefer shorter wins and longer losses
   - Create `get_best_move(board)` method to find optimal position

4. **TASK-016**: Implement difficulty levels (easy, medium, hard) with different strategies
   - **Easy**: Mix of random moves and basic strategy (30% optimal)
   - **Medium**: Occasionally suboptimal moves (70% optimal)
   - **Hard**: Always optimal play using full minimax
   - Create `DifficultyLevel` enum with appropriate constants

5. **TASK-017**: Add move delay simulation for realistic AI response timing
   - Implement configurable delay (0.5-2 seconds) before AI moves
   - Use `time.sleep()` with random variation for natural feel
   - Display "AI is thinking..." message during delay
   - Allow delay to be disabled for testing

6. **TASK-018**: Optimize AI performance for 3x3 board size
   - Implement memoization/caching for repeated positions
   - Add early termination for obvious moves
   - Optimize terminal state detection
   - Ensure AI response time stays under 2 seconds

## Test-Driven Development (TDD) Tests

- **TEST-P3-001**: Test AIPlayer can be instantiated with X or O symbol
- **TEST-P3-002**: Test AIPlayer inherits from Player base class correctly
- **TEST-P3-003**: Test minimax algorithm returns correct scores for terminal positions
- **TEST-P3-004**: Test minimax algorithm chooses winning move when available
- **TEST-P3-005**: Test minimax algorithm blocks opponent winning move
- **TEST-P3-006**: Test minimax algorithm prefers center on empty board
- **TEST-P3-007**: Test position evaluation returns correct scores (+10, -10, 0)
- **TEST-P3-008**: Test get_best_move returns valid position (1-9)
- **TEST-P3-009**: Test get_best_move never suggests occupied position
- **TEST-P3-010**: Test easy difficulty makes suboptimal moves sometimes
- **TEST-P3-011**: Test medium difficulty balances optimal and suboptimal play
- **TEST-P3-012**: Test hard difficulty never loses with optimal play
- **TEST-P3-013**: Test AI response time is under 2 seconds for all positions
- **TEST-P3-014**: Test AI move delay simulation works correctly
- **TEST-P3-015**: Test AI can play as both X and O effectively

## Alternatives Considered

- **ALT-P3-001**: Neural network-based AI using machine learning - Rejected due to complexity and external dependencies requirement
- **ALT-P3-002**: Simple random AI instead of minimax - Rejected as it wouldn't provide challenging gameplay
- **ALT-P3-003**: Alpha-beta pruning optimization - Deferred as 3x3 board is small enough for basic minimax
- **ALT-P3-004**: Monte Carlo Tree Search (MCTS) - Rejected as minimax is more appropriate for perfect information game

## Risks & Assumptions

- **RISK-P3-001**: AI algorithm may be too slow for real-time gameplay - Mitigation: Optimize minimax with alpha-beta pruning if needed
- **RISK-P3-002**: AI may be too difficult or too easy for average players - Mitigation: Implement multiple difficulty levels with different strategies
- **RISK-P3-003**: Memory usage may increase with complex AI calculations - Mitigation: Limit search depth and optimize data structures
- **RISK-P3-004**: Minimax implementation may have bugs leading to poor play - Mitigation: Extensive testing with known optimal positions
- **ASSUMPTION-P3-001**: Minimax algorithm is appropriate for tic-tac-toe (perfect information, zero-sum game)
- **ASSUMPTION-P3-002**: AI response time under 2 seconds is acceptable for user experience
- **ASSUMPTION-P3-003**: Players want varying difficulty levels rather than just optimal play

## Acceptance Criteria

- [ ] AIPlayer class successfully inherits from Player base class
- [ ] Minimax algorithm correctly evaluates game positions
- [ ] AI never loses on hard difficulty when playing optimally
- [ ] AI provides appropriate challenge on easy and medium difficulties
- [ ] AI response time is consistently under 2 seconds
- [ ] AI can play effectively as both X and O
- [ ] Move delay simulation provides realistic user experience
- [ ] All difficulty levels function as designed
- [ ] All tests pass with 100% coverage for implemented functionality
- [ ] Code follows PEP 8 style guidelines
- [ ] All methods have comprehensive docstrings

## Next Phase

Once Phase 3 is complete, proceed to [Phase 4: User Interface](phase-4-user-interface.md) to implement the terminal display and input handling.

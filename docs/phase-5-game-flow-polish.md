---
goal: Implement complete game flow with restart functionality and polish features
phase: 5
version: 1.0
date_created: 2025-07-31
last_updated: 2025-07-31
owner: willvelida
status: 'Planned'
tags: ['phase-5', 'game-flow', 'polish', 'ux']
---

# Phase 5: Game Flow & Polish

![Status: Planned](https://img.shields.io/badge/status-Planned-blue)

This phase implements the complete game experience including restart functionality, welcome messages, main game loop, and user experience polish features.

## Implementation Steps

1. **TASK-026**: Implement game restart functionality
   - Create `restart_game()` method to reset game state
   - Prompt user if they want to play again after game ends
   - Handle restart input validation (yes/no options)
   - Maintain game mode and difficulty settings across restarts

2. **TASK-027**: Add welcome message and game instructions
   - Create `display_welcome()` method with game title
   - Show brief instructions on how to play
   - Explain position numbering system (1-9)
   - Display game mode options and controls

3. **TASK-028**: Create main game loop with exit option
   - Implement `main()` function as application entry point
   - Create outer loop for multiple games (restart functionality)
   - Handle graceful exit when user chooses to quit
   - Ensure proper cleanup and resource management

4. **TASK-029**: Add input sanitization and error handling
   - Strip whitespace from all user inputs
   - Handle edge cases like empty input, special characters
   - Implement try-catch blocks for input conversion errors
   - Provide informative error messages for all failure modes

5. **TASK-030**: Implement clear screen functionality for better UX
   - Create `clear_screen()` method using os.system or ANSI codes
   - Clear screen between games and at appropriate transitions
   - Maintain cross-platform compatibility (Windows, Mac, Linux)
   - Make screen clearing optional/configurable

6. **TASK-031**: Add AI move announcements and visual feedback
   - Display "AI is thinking..." message during AI turn
   - Announce AI move after it's made ("AI chose position X")
   - Add delay/animation for better user experience
   - Show AI difficulty level in status messages

7. **TASK-032**: Implement game statistics tracking (wins/losses/draws)
   - Create `GameStats` class to track session statistics
   - Count wins, losses, and draws for human player
   - Display statistics at game end or on request
   - Reset statistics option for new sessions

## Test-Driven Development (TDD) Tests

- **TEST-P5-001**: Test game restart resets board to initial state
- **TEST-P5-002**: Test game restart maintains selected game mode
- **TEST-P5-003**: Test game restart maintains AI difficulty setting
- **TEST-P5-004**: Test restart prompt accepts yes/no input correctly
- **TEST-P5-005**: Test welcome message displays all required information
- **TEST-P5-006**: Test game instructions are clear and complete
- **TEST-P5-007**: Test main game loop handles multiple games correctly
- **TEST-P5-008**: Test main game loop exits gracefully on user request
- **TEST-P5-009**: Test input sanitization removes whitespace correctly
- **TEST-P5-010**: Test error handling for empty input
- **TEST-P5-011**: Test error handling for special characters
- **TEST-P5-012**: Test clear screen functionality works on target platforms
- **TEST-P5-013**: Test AI move announcements display correctly
- **TEST-P5-014**: Test AI thinking message shows during delays
- **TEST-P5-015**: Test game statistics track wins/losses/draws correctly
- **TEST-P5-016**: Test statistics display formatting is clear
- **TEST-P5-017**: Test statistics reset functionality works correctly

## Alternatives Considered

- **ALT-P5-001**: Persistent statistics storage in file - Deferred to keep implementation simple initially
- **ALT-P5-002**: Advanced animations and terminal effects - Rejected to maintain broad terminal compatibility
- **ALT-P5-003**: Configuration file for user preferences - Deferred as not essential for initial version
- **ALT-P5-004**: Command line arguments for game modes - Deferred to Phase 6 documentation considerations

## Risks & Assumptions

- **RISK-P5-001**: Clear screen functionality may not work on all terminals - Mitigation: Implement fallback method and make feature optional
- **RISK-P5-002**: Game statistics may consume memory in long sessions - Mitigation: Statistics are minimal and reset between sessions
- **RISK-P5-003**: AI delay timing may feel too slow or too fast for users - Mitigation: Make delays configurable with reasonable defaults
- **ASSUMPTION-P5-001**: Users want the option to play multiple games in succession
- **ASSUMPTION-P5-002**: Session-based statistics are sufficient (no persistent storage needed)
- **ASSUMPTION-P5-003**: Clear screen functionality improves user experience

## Acceptance Criteria

- [ ] Game restart functionality works correctly without bugs
- [ ] Welcome message and instructions are clear and helpful
- [ ] Main game loop handles multiple games and exit correctly
- [ ] Input sanitization handles all edge cases gracefully
- [ ] Error handling provides clear feedback for all failure modes
- [ ] Clear screen functionality works on target platforms
- [ ] AI move announcements enhance user experience
- [ ] Game statistics track and display correctly
- [ ] All user interactions feel polished and professional
- [ ] Game flow feels smooth and intuitive
- [ ] All tests pass with 100% coverage for implemented functionality
- [ ] Code follows PEP 8 style guidelines
- [ ] All methods have comprehensive docstrings

## Next Phase

Once Phase 5 is complete, proceed to [Phase 6: Testing & Documentation](phase-6-testing-documentation.md) to ensure comprehensive testing coverage and complete project documentation.

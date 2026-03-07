# UI API Guide: How to Use GameController

## ⚠️ IMPORTANT: Always Use GameController

**The UI must ONLY interact with the game through `GameController`.**

Do NOT directly call:
- ❌ `apply_move()`
- ❌ `is_terminal_state()`
- ❌ `apply_final_payout()`
- ❌ Modify `GameState` directly

## Why GameController?

The `GameController` class prevents critical bugs like:
- Making moves after the game has ended
- Skipping terminal state checks between moves
- Making illegal moves
- Missing bank payout logic
- AI moving on player's turn (or vice versa)

**Without the controller**, you could accidentally do:
```python
# ❌ BAD - Direct function calls
state = apply_move(state, 3)  # 18 → 6
state = apply_move(state, 2)  # 6 → 3 (GAME SHOULD HAVE ENDED AT 6!)
```

**With the controller**, it's impossible:
```python
# ✅ GOOD - Controller enforces rules
controller.make_move(3)  # 18 → 6, game ends
controller.make_move(2)  # Raises RuntimeError: "Game is already over"
```

---

## Complete API Reference

### 1. Initialization

```python
from src.logic.game_controller import GameController

controller = GameController()
```

### 2. Generate Starting Numbers

```python
numbers = controller.generate_starting_numbers()
# Returns: [12006, 18432, 15000, 10008, 19998]
```

### 3. Start Game

```python
# Player chooses a number and who goes first
chosen_number = 12006
player_goes_first = True

state = controller.start_game(chosen_number, player_goes_first)

# state: GameState(
#     current_number=12006,
#     player_points=0,
#     ai_points=0,
#     bank_points=0,
#     is_player_turn=True
# )
```

### 4. Check Game Status

```python
# Is game over?
if controller.is_game_over:
    winner = controller.winner  # 'AI', 'Player', or 'Tie'
    print(f"Game over! Winner: {winner}")

# Get current state
state = controller.state

# Get legal moves
legal_moves = controller.get_legal_moves()
# Returns: [] if game over, or [2], [3], or [2, 3]
```

### 5. Make Player Move

```python
try:
    state, game_ended = controller.make_move(divisor=2)

    if game_ended:
        print(f"Game over! Winner: {controller.winner}")
        print(f"Final score - Player: {state.player_points}, AI: {state.ai_points}")
    else:
        print(f"Number: {state.current_number}")
        print(f"Player: {state.player_points}, AI: {state.ai_points}, Bank: {state.bank_points}")

except RuntimeError as e:
    print(f"Error: {e}")  # e.g., "Game is already over"
except ValueError as e:
    print(f"Invalid move: {e}")  # e.g., "Illegal move: 3"
```

### 6. Make AI Move

```python
try:
    move, metrics, game_ended = controller.make_ai_move(depth=15)

    print(f"AI chose: {move}")
    print(f"Nodes generated: {metrics.nodes_generated}")
    print(f"Nodes evaluated: {metrics.nodes_evaluated}")
    print(f"Time: {metrics.elapsed_ms:.2f}ms")

    if game_ended:
        print(f"Game over! Winner: {controller.winner}")

except RuntimeError as e:
    print(f"Error: {e}")
```

### 7. Get Game Summary

```python
summary = controller.get_game_summary()

# Before game starts:
# {
#     "game_started": False,
#     "message": "Game not started"
# }

# During game:
# {
#     "game_started": True,
#     "current_number": 12006,
#     "player_points": 3,
#     "ai_points": 2,
#     "bank_points": 1,
#     "is_player_turn": True,
#     "is_game_over": False,
#     "legal_moves": [2, 3]
# }

# After game ends:
# {
#     ... (same as above) ...
#     "is_game_over": True,
#     "winner": "AI",
#     "legal_moves": []
# }
```

---

## Complete UI Game Loop Example

```python
from src.logic.game_controller import GameController

def main():
    controller = GameController()

    # 1. Generate and display starting numbers
    numbers = controller.generate_starting_numbers()
    print(f"Choose a starting number: {numbers}")

    # 2. Player chooses
    chosen = int(input("Enter chosen number: "))
    player_first = input("Do you want to go first? (y/n): ").lower() == 'y'

    # 3. Start game
    controller.start_game(chosen, player_first)
    print(f"\nGame started with {chosen}")

    # 4. Game loop
    while not controller.is_game_over:
        state = controller.state

        # Display current status
        print(f"\nNumber: {state.current_number}")
        print(f"Player: {state.player_points} | AI: {state.ai_points} | Bank: {state.bank_points}")

        if state.is_player_turn:
            # Player's turn
            legal_moves = controller.get_legal_moves()
            print(f"Legal moves: {legal_moves}")

            try:
                move = int(input("Your move (2 or 3): "))
                state, game_ended = controller.make_move(move)
                print(f"You divided by {move} → {state.current_number}")

            except (ValueError, RuntimeError) as e:
                print(f"Error: {e}")
                continue

        else:
            # AI's turn
            print("AI is thinking...")
            move, metrics, game_ended = controller.make_ai_move(depth=15)
            print(f"AI divided by {move} → {controller.state.current_number}")
            print(f"(took {metrics.elapsed_ms:.0f}ms, evaluated {metrics.nodes_evaluated} nodes)")

    # 5. Game over
    final_state = controller.state
    print(f"\n{'='*50}")
    print("GAME OVER!")
    print(f"Final Score - Player: {final_state.player_points}, AI: {final_state.ai_points}")
    print(f"Winner: {controller.winner}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
```

---

## Error Handling

The controller raises exceptions for invalid operations:

| Error | When | How to Handle |
|-------|------|---------------|
| `RuntimeError: "Game not started"` | Trying to make moves before calling `start_game()` | Call `start_game()` first |
| `RuntimeError: "Game is already over"` | Trying to make moves after game ends | Check `controller.is_game_over` before moves |
| `RuntimeError: "player's turn"` | AI trying to move on player's turn | Check `state.is_player_turn` |
| `ValueError: "Illegal move"` | Move not in legal moves | Use `get_legal_moves()` to validate |

---

## Testing Your UI

Use the integration tests as examples:
```bash
pytest src/Test/test_game_controller.py -v
```

Key test to study: `test_prevents_moves_after_reaching_terminal_number` - this shows the exact bug that would happen without the controller.

---

## Summary

✅ **DO:**
- Use `GameController` for ALL game operations
- Check `is_game_over` before making moves
- Use `get_legal_moves()` to validate player input
- Handle exceptions properly

❌ **DON'T:**
- Call `apply_move()` directly
- Manually check `is_terminal_state()`
- Modify `GameState` fields
- Skip error handling

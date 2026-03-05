### Bridge between UI and logic

from data.data import GameState
import logic.logic


# UI should hold current GameState in session
# UI receives GameState that is ready for player move AND receives is_game_over flag
# If is_game_over => UI checks who won, shows message
def api_apply_move(currentState: GameState, divisor: int):
    # Apply player move
    # ...

    # Check for game over => apply bank points, set flag currentState.is_game_over = true

    # not game over ? Apply AI move
    # ...

    # Check for game over => apply bank points, set flag currentState.is_game_over = true

    # return new state
    pass

def api_start_new_state():
    # Return fresh state, defined in data.py
    pass

def api_is_move_legal(currentState: GameState, divisor: int):
    # Call from logic and return bool
    pass

def api_get_starting_numbers():
    # call from logic 5 random numbers

    # return list
    pass

# We might not need this if we pass starting_number in api_start_new_state(starting_number: int)
def api_choose_starting_number(currentState: GameState, starting_number: int):
    # Apply number to state

    # Return state
    pass
from src.data.data import GameState
from src.logic.logic import apply_final_payout


def evaluate_terminal_state(state: GameState) -> float:
    """Evaluates terminal state from AI perspective"""
    final_state = apply_final_payout(state)
    return float(final_state.ai_points - final_state.player_points)


def evaluate_heuristic(state: GameState) -> float:
    score_diff = state.ai_points - state.player_points

    bank_value = 0.0
    distance_to_end = state.current_number - 10

    # If the end is too far (> 100 distance), the bank value is simply ignored (0.0).
    if 0 < distance_to_end <= 100:
        # Since subtractions (-5, -7) average to -6, dividing by 6 is our mathematically safest bet.
        estimated_turns_left = distance_to_end / 6.0

        # If the number of turns is ODD, the player making the CURRENT move IS likely to finish.
        is_even_turns = (int(estimated_turns_left) % 2 == 0)
        
        # Calculate if the AI is likely to be the one picking up the bank points
        if state.is_player_turn:
            ai_likely_to_win_bank = is_even_turns 
        else:
            ai_likely_to_win_bank = not is_even_turns

        bank_weight = 0.8 if ai_likely_to_win_bank else -0.5
        bank_value = state.bank_points * bank_weight

    turn_bonus = 0.5 if not state.is_player_turn else 0.0

    return score_diff + bank_value + turn_bonus

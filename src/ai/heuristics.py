from src.data.data import GameState
from src.logic.logic import apply_final_payout


def evaluate_terminal_state(state: GameState) -> float:
    """Evaluates terminal state from AI perspective"""
    final_state = apply_final_payout(state)
    return float(final_state.ai_points - final_state.player_points)


def evaluate_heuristic(state: GameState) -> float:
    """
    Heuristic evaluation for non-terminal states.

    Components:
    1. Score difference (main component)
    2. Bank value (weighted by proximity to end)
    3. Turn advantage (small bonus if AI's turn)
    """
    # Main component: current score difference
    score_diff = state.ai_points - state.player_points

    # Bank value weighted by proximity to end
    # Higher weight when number is smaller (closer to end)
    bank_weight = 0.5 if state.current_number < 100 else 0.3
    bank_value = state.bank_points * bank_weight

    # Turn advantage: small bonus if it's AI's turn
    turn_bonus = 0.5 if not state.is_player_turn else 0

    return score_diff + bank_value + turn_bonus

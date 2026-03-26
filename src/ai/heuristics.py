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
    2. Dynamic Bank Parity (evaluate if AI will actually claim the bank)
    3. Turn advantage (small bonus if it is the AI's turn)
    """
    # 1. Base Score Difference
    score_diff = state.ai_points - state.player_points

    # 2. Dynamic Bank Parity Evaluation
    bank_value = 0.0
    distance_to_end = state.current_number - 10
    
    # We only care about predicting bank outcomes when we are close to the finish.
    # If the end is too far (> 100 distance), the bank value is simply ignored (0.0).
    if 0 < distance_to_end <= 100:
        # Why / 6.0? While players CAN divide (which causes huge jumps), our Alpha-Beta search 
        # tree perfectly predicts those divisions within its search depth limit. 
        # The heuristic is ONLY used when the end of the game is unseen beyond our depth limit!
        # An "unseen" end almost always implies a long, slow chain of inescapable subtractions 
        # (since division would have teleported us into a terminal state the AI could see). 
        # Since subtractions (-5, -7) average to -6, dividing by 6 is our mathematically safest bet.
        estimated_turns_left = distance_to_end / 6.0
        
        # If the number of turns is EVEN, the player making the CURRENT move is NOT likely to finish.
        # If the number of turns is ODD, the player making the CURRENT move IS likely to finish.
        is_even_turns = (int(estimated_turns_left) % 2 == 0)
        
        # Calculate if the AI is likely to be the one picking up the bank points
        if state.is_player_turn:
            ai_likely_to_win_bank = is_even_turns 
        else:
            ai_likely_to_win_bank = not is_even_turns
            
        # If we think we'll win the bank, it's highly positive.
        # If we think the opponent will win it, it's an active negative threat!
        bank_weight = 0.8 if ai_likely_to_win_bank else -0.5
        bank_value = state.bank_points * bank_weight

    # 3. Turn advantage: small bonus if it's AI's turn to move next
    turn_bonus = 0.5 if not state.is_player_turn else 0.0

    return score_diff + bank_value + turn_bonus

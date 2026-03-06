from typing import List
from amazing_ai_spele.src.data.data import GameState

def generate_starting_numbers() -> List[int]:
    import random
    start = 10002 # Pirmais skaitlis kas dalās ar 6 un ir >= 10000
    end   = 19998 # Pēdējais skaitlis kas dalās ar 6 un ir <= 20000
    divisible_by_6 = list(range(start, end + 1, 6))

    return random.sample(divisible_by_6, 5)

def is_valid_move(current_number: int, divisor: int) -> bool:
    return current_number % divisor == 0

def apply_move(current_state: GameState, divisor: int) -> GameState:
    new_number = current_state.current_number // divisor
    points_to_last = 3 if divisor == 3 else 0
    points_to_next = 2 if divisor == 2 else 0
    points_to_bank = 1 if new_number % 5 == 0 else 0

    return GameState(
        current_number  = new_number,
        player_points   = current_state.player_points + (points_to_last if current_state.is_player_turn else points_to_next),
        ai_points       = current_state.ai_points + (points_to_next if current_state.is_player_turn else points_to_last),
        bank_points     = current_state.bank_points + points_to_bank,
        is_player_turn  = not current_state.is_player_turn,
        is_game_over = False
    )

def is_game_over(current_number: int) -> bool:
    if current_number % 2 != 0 and current_number % 3 != 0:
        return True
    return current_number <= 10


def calculate_final_payout(final_state: GameState) -> GameState:
    new_state = final_state
    if(new_state.is_player_turn):
        new_state.ai_points += final_state.bank_points
    else:
        new_state.player_points += final_state.bank_points
    final_state.bank_points=0
    return new_state


def alpha_beta(state: GameState, depth: int, alpha: float, beta: float, is_maximizing: bool) -> int:

    if depth == 0 or is_game_over(state.current_number):
        return state.ai_points - state.player_points ##Ai is maximizer

    moves = []
    if is_valid_move(state.current_number, 3):
        moves.append(3)
    if is_valid_move(state.current_number, 2):
        moves.append(2)

    if not moves:
        return state.ai_points - state.player_points

    if is_maximizing:
        max_eval = float('-inf')
        for divisor in moves:
            new_state = apply_move(state, divisor)
            curr_eval = alpha_beta(new_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, curr_eval)
            alpha = max(alpha, curr_eval)
            if beta <= alpha:
                break

        return max_eval

    else:
        min_eval = float('inf')
        for divisor in moves:
            new_state = apply_move(state, divisor)
            curr_eval = alpha_beta(new_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, curr_eval)
            beta = min(beta, curr_eval)
            if beta <= alpha:
                break

        return min_eval



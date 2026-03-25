from src.logic.logic import is_valid_move, apply_move, is_terminal_state, apply_final_payout,generate_starting_numbers
from src.data.data import GameState
from src.ai.search import find_best_move_alpha_beta, find_best_move_minimax, minimax_search, alpha_beta_search
from src.ai.metrics import AIMetrics
import random

def simulate_game_alpha_beta(start_number):
    """Simulates a game between human and AI"""
    state = GameState(
        current_number=start_number,
        player_points=0,
        ai_points=0,
        bank_points=0,
        is_player_turn=True
    )

    print("Starting number:", start_number)

    total_generated = 0
    total_evaluated = 0
    total_pruned = 0
    total_time = 0
    ai_moves = 0

    while not is_terminal_state(state):
        if state.is_player_turn:
            valid_moves = [d for d in (2, 3)
                           if is_valid_move(state.current_number, d)]

            if not valid_moves:
                print("No valid moves. Game over.")
                break

            if len(valid_moves) == 1:
                move = valid_moves[0]
                print("Only one move available. Auto move:", move)
            else:
                while True:
                    move = int(input("Enter move (2 or 3): "))
                    if move in valid_moves:
                        break
                    print("Invalid move. Try again.")
            print("Player move:", move)

        else:
            move, metrics = find_best_move_alpha_beta(state, depth=15)
            print(f"AI move: {move} (score: {metrics.best_score:.2f}, "
                  f"nodes: {metrics.nodes_generated}, "
                  f"evaluated: {metrics.nodes_evaluated}, "
                  f"time: {metrics.elapsed_ms:.2f}ms)")
            total_generated += metrics.nodes_generated
            total_evaluated += metrics.nodes_evaluated
            total_pruned += metrics.pruned_branches
            total_time += metrics.elapsed_ms
            ai_moves += 1

        state = apply_move(state, move)
        print(f"Number: {state.current_number} | Player: {state.player_points} | "
              f"AI: {state.ai_points} | Bank: {state.bank_points}")

    final_state = apply_final_payout(state)

    if final_state.ai_points > final_state.player_points:
        winner = "AI"
    elif final_state.player_points > final_state.ai_points:
        winner = "PLAYER"
    else:
        winner = "TIE"

    final_metrics = AIMetrics()
    final_metrics.nodes_generated = total_generated
    final_metrics.nodes_evaluated = total_evaluated
    final_metrics.best_move = metrics.best_move
    final_metrics.best_score = metrics.best_score
    final_metrics.elapsed_ms = total_time / ai_moves if ai_moves else 0
    final_metrics.pruned_branches = total_pruned
    return winner, final_metrics


def simulate_game_minimax(start_number):
    """Simulates AI vs player using Minimax"""

    state = GameState(
        current_number=start_number,
        player_points=0,
        ai_points=0,
        bank_points=0,
        is_player_turn=True
    )
    print("Starting number:", start_number)

    total_generated = 0
    total_evaluated = 0
    total_time = 0
    ai_moves = 0

    while not is_terminal_state(state):
        if state.is_player_turn:
            valid_moves = [d for d in (2, 3)
                           if is_valid_move(state.current_number, d)]

            if not valid_moves:
                print("No valid moves. Game over.")
                break

            if len(valid_moves) == 1:
                move = valid_moves[0]
                print("Only one move available. Auto move:", move)
            else:
                while True:
                    move = int(input("Enter move (2 or 3): "))
                    if move in valid_moves:
                        break
                    print("Invalid move. Try again.")
            print("Player move:", move)

        else:
            move, metrics = find_best_move_minimax(state, depth=15)
            print(f"AI move: {move} (score: {metrics.best_score:.2f}, "
                  f"nodes: {metrics.nodes_generated}, "
                  f"evaluated: {metrics.nodes_evaluated}, "
                  f"time: {metrics.elapsed_ms:.2f}ms)")

            total_generated += metrics.nodes_generated
            total_evaluated += metrics.nodes_evaluated
            total_time += metrics.elapsed_ms
            ai_moves += 1

        state = apply_move(state, move)
        print(f"Number: {state.current_number} | Player: {state.player_points} | "
              f"AI: {state.ai_points} | Bank: {state.bank_points}")

    final_state = apply_final_payout(state)

    if final_state.ai_points > final_state.player_points:
        winner = "AI"
    elif final_state.player_points > final_state.ai_points:
        winner = "PLAYER"
    else:
        winner = "TIE"

    final_metrics = AIMetrics()
    final_metrics.nodes_generated = total_generated
    final_metrics.nodes_evaluated = total_evaluated
    final_metrics.best_move = metrics.best_move
    final_metrics.best_score = metrics.best_score
    final_metrics.elapsed_ms = total_time / ai_moves if ai_moves else 0

    return winner, final_metrics

#print(simulate_game_minimax(random.choice(generate_starting_numbers())))
#print(simulate_game_alpha_beta(random.choice(generate_starting_numbers())))
#print(simulate_game_minimax(20995200))
#print(simulate_game_alpha_beta(20995200))

from src.logic.logic import is_valid_move, apply_move, is_terminal_state, apply_final_payout
from src.data.data import GameState
from src.ai.search import find_best_move_alpha_beta


def simulate_game(start_number):
    """Simulates a game between human and AI"""
    state = GameState(
        current_number=start_number,
        player_points=0,
        ai_points=0,
        bank_points=0,
        is_player_turn=True
    )

    print("\nStarting number:", start_number)

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

        state = apply_move(state, move)
        print(f"Number: {state.current_number} | Player: {state.player_points} | "
              f"AI: {state.ai_points} | Bank: {state.bank_points}")

    print("\nGAME OVER")
    final_state = apply_final_payout(state)
    print(f"Final state: Player: {final_state.player_points}, AI: {final_state.ai_points}")

    if final_state.ai_points > final_state.player_points:
        print("AI WINS!")
    elif final_state.player_points > final_state.ai_points:
        print("PLAYER WINS!")
    else:
        print("TIE!")


# Uncomment to test:
# simulate_game(10002)
# simulate_game(10008)
# simulate_game(19998)

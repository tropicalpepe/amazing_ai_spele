from amazing_ai_spele.src.logic.logic import is_valid_move,alpha_beta,calculate_final_payout,apply_move,is_game_over,GameState

def find_best_move_using_alpha(state):
    best_move = None
    best_value = float("-inf")

    for divisor in (2, 3):
        if not is_valid_move(state.current_number, divisor):
            continue

        value = alpha_beta(
            apply_move(state, divisor),
            15,
            float("-inf"),
            float("inf"),
            False
        )

        if value > best_value:
            best_value, best_move = value, divisor

    return best_move


def simulate_game(start_number):
    state = GameState(
        current_number=start_number,
        player_points=0,
        ai_points=0,
        bank_points=0,
        is_player_turn=True,
        is_game_over=False
    )

    print("\nStarting number:", start_number)

    while not is_game_over(state.current_number):
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
            move = find_best_move_using_alpha(state)
            print("AI move:", move)

        state = apply_move(state, move)
        print("Number:", state.current_number,"| Player:", state.player_points,"| AI:", state.ai_points)

    print("GAME OVER")
    final_st = calculate_final_payout(state)
    print("Final state:", final_st)

#simulate_game(10002)
#simulate_game(10008)
#simulate_game(19998)
import random
from src.logic.game_controller import GameController

def run_simulation(algorithm="Alpha-Beta", depth=5, player_mode="random"):
    controller = GameController()
    numbers = controller.generate_starting_numbers()
    start_num = random.choice(numbers)
    
    # AI starts first to simplify (but doesn't matter)
    controller.start_game(start_num, player_starts=False)
    
    nodes_gen = 0
    nodes_eval = 0
    time_ms = 0.0
    moves = 0
    
    while not controller.is_game_over:
        summary = controller.get_game_summary()
        legal = summary["legal_moves"]
        if summary["is_player_turn"]:
            if player_mode == "random":
                move = random.choice(legal)
            elif player_mode == "greedy":
                # Prefer /3, then -5, then /2, then -7
                if 3 in legal: move = 3
                elif -5 in legal: move = -5
                elif 2 in legal: move = 2
                else: move = -7
            
            controller.make_move(move)
        else:
            if algorithm == "Alpha-Beta":
                move, metrics, ended = controller.make_ai_move(depth)
            else:
                # Minimax wrapper in controller logic assumes depth too
                # we just use Alpha-Beta for the experiment
                move, metrics, ended = controller.make_ai_move(depth)
            
            nodes_gen += metrics.nodes_generated
            nodes_eval += metrics.nodes_evaluated
            time_ms += metrics.elapsed_ms
            moves += 1

    summary = controller.get_game_summary()
    return {
        "winner": summary["winner"],
        "ai_score": summary["ai_points"],
        "player_score": summary["player_points"],
        "bank": summary["bank_points"],
        "moves_by_ai": moves,
        "avg_time_ms": time_ms / max(1, moves),
        "total_nodes_evaluated": nodes_eval,
        "total_nodes_generated": nodes_gen,
    }

if __name__ == "__main__":
    print("Running 10 Alpha-Beta matches (Depth 6) against Random Player...")
    wins = {"AI": 0, "Player": 0, "Tie": 0}
    
    for i in range(10):
        res = run_simulation("Alpha-Beta", 6, "random")
        wins[res["winner"]] += 1
        print(f"Game {i+1}: Winner={res['winner']}, AI={res['ai_score']} Player={res['player_score']} | Avg Time={res['avg_time_ms']:.1f}ms NodesEval={res['total_nodes_evaluated']}")
    
    print("\nSummary:", wins)

import sys
import random
from pathlib import Path

# Pievienojam saiti uz saknes klasi, lai skripts atpazītu importus
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.logic.game_controller import GameController


def simulate_game(algorithm: str, depth: int) -> dict:
    """Spēlē vienu no sākuma līdz beigām (Random vs AI). Reģistrē metrikas."""
    controller = GameController()
    numbers = controller.generate_starting_numbers()
    start_num = random.choice(numbers)
    
    # AI iet pirmais = False
    controller.start_game(start_num, player_starts=False)
    
    total_nodes_generated = 0
    total_nodes_evaluated = 0
    total_pruned_branches = 0
    total_time_ms = 0.0
    ai_moves_count = 0
    
    while not controller.is_game_over:
        state = controller.state
        
        if state.is_player_turn:
            legal = controller.get_legal_moves()
            human_move = random.choice(legal)  # Random moves
            controller.make_move(human_move)
        else:
            # AI turn (high timeout to prevent limits ruining experiments)
            move, metrics, ended = controller.make_ai_move(
                depth=depth, 
                algorithm=algorithm, 
                timeout=1000.0
            )
            
            # Reģistrējam datus
            if metrics:
                total_nodes_generated += metrics.nodes_generated
                total_nodes_evaluated += metrics.nodes_evaluated
                total_time_ms += metrics.elapsed_ms
                if hasattr(metrics, "pruned_branches"):
                    total_pruned_branches += metrics.pruned_branches
            
            ai_moves_count += 1
            
    avg_turn_time = total_time_ms / max(1, ai_moves_count)
            
    # AI uzvara vai zaudējums
    ai_won = False
    if controller.winner == "AI":
        ai_won = True
        
    return {
        "algo": algorithm,
        "depth": depth,
        "ai_won": ai_won,
        "nodes_gen": total_nodes_generated,
        "nodes_eval": total_nodes_evaluated,
        "pruned": total_pruned_branches,
        "avg_time_ms": avg_turn_time
    }


def run_all_experiments():
    results = []
    
    # Mēs vācam datus pa 5 spēlēm katrā setā (8 un 13 dziļums abiem algoritmiem)
    configurations = [
        ("Minimax", 8),
        ("Minimax", 13),
        ("Alpha-Beta", 8),
        ("Alpha-Beta", 13)
    ]
    
    print(f"=========================================")
    print(f"Uzsāku autonomo eksperimentu simulāciju...")
    print(f"=========================================\n")
    
    for algo, depth in configurations:
        print(f"Simulēju 5 spēles: {algo} (Depth: {depth})...")
        wins = 0
        nodes_gen_list = []
        nodes_eval_list = []
        avg_time_list = []
        pruned_list = []
        
        for i in range(5):
            res = simulate_game(algo, depth)
            if res["ai_won"]:
                wins += 1
            nodes_gen_list.append(res["nodes_gen"])
            nodes_eval_list.append(res["nodes_eval"])
            avg_time_list.append(res["avg_time_ms"])
            pruned_list.append(res["pruned"])
            
            print(f"   => Spēle {i+1}/5 pabeigta ({res['avg_time_ms']:.1f} ms/gājiens)")
            
        
        # Apkopojums
        summary = {
            "algo": algo,
            "depth": depth,
            "wins": wins,
            "avg_gen": sum(nodes_gen_list)/5,
            "avg_eval": sum(nodes_eval_list)/5,
            "avg_time": sum(avg_time_list)/5,
            "avg_pruned": sum(pruned_list)/5
        }
        results.append(summary)
        print(f"--- REZULTĀTI {algo} D={depth} ---")
        print(f"  Uzvaras (AI vs Random): {summary['wins']}/5")
        print(f"  Vid. mezgli (Gen): {summary['avg_gen']:.1f}")
        print(f"  Vid. mezgli (Eval): {summary['avg_eval']:.1f}")
        print(f"  Vid. izpildes laiks: {summary['avg_time']:.2f} ms")
        if algo == "Alpha-Beta":
            print(f"  Vid. apgrieztie zari: {summary['avg_pruned']:.1f}")
        print("\n")


if __name__ == "__main__":
    run_all_experiments()

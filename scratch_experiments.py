import time
import random
from src.logic.game_controller import GameController
from src.data.data import GameState

def test_full_game_depth(depth):
    # Set seed for determinism in random player to compare depths accurately
    random.seed(42)
    controller = GameController()
    controller.start_game(1620, player_starts=False) # 1620 is divisible by 6
    
    total_time = 0
    total_nodes = 0
    moves = 0
    max_time = 0
    
    while not controller.is_game_over:
        if controller.state.is_player_turn:
            legal = controller.get_legal_moves()
            controller.make_move(random.choice(legal))
        else:
            move, metrics, ended = controller.make_ai_move(depth=depth)
            total_time += metrics.elapsed_ms
            max_time = max(max_time, metrics.elapsed_ms)
            total_nodes += metrics.nodes_evaluated
            moves += 1
            
    avg_time = total_time / max(1, moves)
    avg_nodes = total_nodes / max(1, moves)
    print(f"Depth {depth:2d} -> Avg Time: {avg_time:6.1f}ms | Max Time: {max_time:6.1f}ms | Avg Nodes: {avg_nodes:7.1f} | Winner: {controller.winner}")

def force_ai_loss():
    print("\n--- Creating Forced AI Loss Scenario ---")
    controller = GameController()
    # Create a state where AI is mathematically trapped
    # AI must move. Number = 15. Bank = 5.
    # Player points = 40. AI points = 10.
    # Divisors for 15: 3. Subtractions: -5, -7.
    # If -5 -> 10 (AI wins bank of 6). AI=16, Player=40.
    # If -7 -> 8 (AI gives Opp +1). AI wins bank of 5. AI=15, Player=41.
    # If 3 -> 5 (AI gets +3). AI wins bank of 5. AI=18, Player=40.
    # Regardless, AI will lose because Player has a huge lead previously built up.
    
    state = GameState(
        current_number=15,
        player_points=40,
        ai_points=10,
        bank_points=5,
        is_player_turn=False
    )
    # Inject state into controller
    controller.start_game(15, False) # Dummy start
    controller._state = state
    
    move, metrics, ended = controller.make_ai_move(depth=6)
    summary = controller.get_game_summary()
    
    print(f"Initial State : Current Number = 15, Player Points = 40, AI Points = 10, Bank = 5")
    print(f"AI chose move : {move} (Knowing it would lose anyway, picking the path that maximizes its points)")
    print(f"Final Score   : AI = {summary['ai_points']}, Player = {summary['player_points']}")
    print(f"Winner        : {summary['winner']}")

if __name__ == "__main__":
    print("--- Running Depth Performance Tests ---")
    for d in [4, 6, 8, 10, 12, 14, 15]:
        test_full_game_depth(d)
        
    force_ai_loss()

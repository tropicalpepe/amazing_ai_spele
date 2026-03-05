from dataclasses import dataclass

@dataclass
class GameState:
    current_number: int
    player_points: int
    ai_points: int
    bank_points: int
    is_player_turn: bool
    is_game_over: bool

def create_initial_state(chosen_number: int, player_starts: bool) -> GameState:
    return GameState(
        current_number=chosen_number,
        player_points=0,
        ai_points=0,
        bank_points=0,
        is_player_turn=player_starts,
        is_game_over=False
    )
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class GameState:
    current_number: int
    player_points: int
    ai_points: int
    bank_points: int
    is_player_turn: bool

def create_initial_state(chosen_number: int, player_starts: bool) -> GameState:
    return GameState(
        current_number=chosen_number,
        player_points=0,
        ai_points=0,
        bank_points=0,
        is_player_turn=player_starts
    )

@dataclass
class GameTreeNode:
    """Represents a node in the game tree"""
    state: GameState
    depth: int
    children: Dict[int, 'GameTreeNode']  # Maps move (divisor) to child node
    evaluation: Optional[float] = None
    best_move: Optional[int] = None
    is_terminal: Optional[bool] = None
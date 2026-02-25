from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class GameState:
    """
    Nemainīgs (immutable) datu objekts, kas atspoguļo vienu spēles mirkli.
    UI un Loģikas komandas izmantos šo, lai nolasītu datus.
    """
    current_number: int
    player_points: int
    ai_points: int
    bank_points: int
    is_player_turn: bool

class GameTreeNode:
    """
    Koka mezgls, kas satur spēles stāvokli un norādes uz nākamajiem iespējamajiem gājieniem.
    """
    def __init__(self, state: GameState, depth: int):
        self.state: GameState = state
        self.depth: int = depth
        # Atslēga ir dalītājs (2 vai 3), vērtība ir nākamais mezgls.
        # Ja gājiens nav iespējams, atslēga neeksistē.
        self.children: Dict[int, 'GameTreeNode'] = {}

def build_game_tree(initial_state: GameState, max_depth: int) -> GameTreeNode:
    """
    Rekursīvi (vai iteratīvi) uzģenerē spēles koku no dotā stāvokļa 
    līdz norādītajam dziļumam.
"""
    from logic import is_valid_move, apply_move, is_game_over

def build_recursive(state: GameState, depth: int)-> GameTreeNode:
  node = GameTreeNode(state, depth)

  if depth >=max_depth:
    return node

if is_game_over(state.current_number):
  return node

  for divisor in(2,3):
    if is_valid_move(state.current_number, divisor):
      next_state = apply_move(state, divisor)
      node.children[divisor]= build_recursive(next_state, depth + 1)

  return node

  return build_recursive(initial_state, 0)

    pass

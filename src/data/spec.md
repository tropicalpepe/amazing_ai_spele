# Specifikācija: Datu Struktūras (Data Team)

**Atbildība:** Spēles stāvokļa uzturēšana un lēmumu koka ģenerēšana AI vajadzībām.
**Atkarības:** Koka ģenerēšanai jāizmanto `apply_move` un `is_valid_move` no Loģikas komandas.

## Koda Līgumi (Interfaces)

```python
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
    
    Algoritms (Pseudocode):
        1. Izveido GameTreeNode ar initial_state.
        2. Ja depth == max_depth vai is_game_over(state), atgriež mezglu.
        3. Pārbauda is_valid_move dalīšanai ar 2. Ja derīgs -> apply_move -> rekursīvi pievieno kā bērnu.
        4. Pārbauda is_valid_move dalīšanai ar 3. Ja derīgs -> apply_move -> rekursīvi pievieno kā bērnu.
        5. Atgriež pamatmezglu (root).
        
    Args:
        initial_state (GameState): Koka saknes stāvoklis.
        max_depth (int): Cik gājienus uz priekšu ģenerēt (lookahead).
        
    Returns:
        GameTreeNode: Pilnībā uzbūvēts koks līdz norādītajam dziļumam.
    """
    pass
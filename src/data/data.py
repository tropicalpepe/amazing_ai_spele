from dataclasses import dataclass
from typing import Dict, Optional

@dataclass(frozen=True)
class GameState:
    """
    Nemainīgs (immutable) datu objekts, kas atspoguļo vienu spēles mirkli.
    UI un Loģikas komandas izmantos šo, lai nolasītu datus.
    Izmantojot 'frozen=True', mēs garantējam, ka neviens netīšām neizmainīs
    esošo stāvokli, kas ir kritiski svarīgi koka ģenerēšanai.
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
        self.children: Dict[int, 'GameTreeNode'] = {}

def build_game_tree(initial_state: GameState, max_depth: int) -> GameTreeNode:
    """
    Rekursīvi uzģenerē spēles koku no dotā stāvokļa līdz norādītajam dziļumam.
    """
    # Importējam loģiku šeit iekšā, lai izvairītos no cikliskajiem importiem (circular imports).
    # Loģikas komandai savā failā būs jāimportē GameState no šī faila.
    from logic import is_valid_move, apply_move, is_game_over

    def build_recursive(state: GameState, current_depth: int) -> GameTreeNode:
        # 1. Izveidojam mezglu pašreizējam stāvoklim
        node = GameTreeNode(state, current_depth)

        # 2. Pārbaudām, vai esam sasnieguši spēles beigas vai maksimālo dziļumu.
        # Pievienota drošības pārbaude (state.current_number <= 10) gadījumam,
        # ja Loģikas komanda vēl nav izdzēsusi savu "pass" no is_game_over funkcijas.
        game_over_result = is_game_over(state.current_number)
        is_over = game_over_result if game_over_result is not None else (state.current_number <= 10)

        if current_depth >= max_depth or is_over:
            return node

        # 3. Pārbaudām dalītājus 2 un 3 un veidojam sazarojumus

        for divisor in (2, 3):
            if is_valid_move(state.current_number, divisor):
                # Izpildām gājienu, iegūstot JAUNU GameState objektu
                next_state = apply_move(state, divisor)

                # Rekursīvi izsaucam funkciju jaunajam stāvoklim un pievienojam kā bērnu
                node.children[divisor] = build_recursive(next_state, current_depth + 1)

        return node

    # Sākam rekursiju no saknes (root) ar dziļumu 0
    return build_recursive(initial_state, 0)

def create_initial_state(chosen_number: int, player_starts: bool) -> GameState:
    """
    Palīgfunkcija ērtai sākuma stāvokļa izveidei.
    Izsaucama brīdī, kad UI komanda paziņo, kuru skaitli lietotājs izvēlējies.
    """
    return GameState(
        current_number=chosen_number,
        player_points=0,
        ai_points=0,
        bank_points=0,
        is_player_turn=player_starts
    )
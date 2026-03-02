from typing import List

# Pagaidam kamer nav data.py atstajam GameState seit
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

def generate_starting_numbers() -> List[int]:
    import random
    start = 10002 # Pirmais skaitlis kas dalās ar 6 un ir >= 10000
    end   = 19998 # Pēdējais skaitlis kas dalās ar 6 un ir <= 20000
    divisible_by_6 = list(range(start, end + 1, 6))

    return random.sample(divisible_by_6, 5)

def is_valid_move(current_number: int, divisor: int) -> bool:
    return current_number % divisor == 0

def apply_move(current_state: GameState, divisor: int) -> GameState:
    new_number     = current_state.current_number // divisor
    points_to_last = 3 if divisor == 3 else 0
    points_to_next = 2 if divisor == 2 else 0
    points_to_bank = 1 if new_number % 5 == 0 else 0

    return GameState(
        current_number  = new_number,
        player_points   = current_state.player_points + (points_to_last if current_state.is_player_turn else points_to_next),
        ai_points       = current_state.ai_points + (points_to_next if current_state.is_player_turn else points_to_last),
        bank_points     = current_state.bank_points + points_to_bank,
        is_player_turn  = not current_state.is_player_turn
    )

def is_game_over(current_number: int) -> bool:
    """
    Pārbauda, vai ir iestājies spēles beigu nosacījums.
    
    Args:
        current_number (int): Skaitlis PĒC gājiena izpildes.
        
    Returns:
        bool: True, ja current_number <= 10.
    """
    pass

def calculate_final_payout(final_state: 'GameState') -> 'GameState':
    """
    Izpilda bankas punktu sadali spēles beigās.
    
    Args:
        final_state (GameState): Spēles stāvoklis brīdī, kad is_game_over == True.
        
    Returns:
        GameState: Gala stāvoklis ar tukšu banku un atjauninātiem spēlētāju punktiem.
    """
    pass
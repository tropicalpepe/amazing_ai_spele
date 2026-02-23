# Specifikācija: Spēles Loģika (Logic Team)

**Atbildība:** Spēles matemātika, gājienu validācija un punktu aprēķins.
**Atkarības:** Izmanto `GameState` objektu no Datu komandas.

## Koda Līgumi (Interfaces)

```python
from typing import List
# Piezīme: Importēs GameState no Datu komandas moduļa
# from data.game_state import GameState

def generate_starting_numbers() -> List[int]:
    """
    Ģenerē sākotnējo skaitļu sarakstu spēles sākumam.
    
    Returns:
        List[int]: Precīzi 5 unikāli skaitļi diapazonā [10000, 20000], 
                   kas dalās ar 6 bez atlikuma.
    """
    pass

def is_valid_move(current_number: int, divisor: int) -> bool:
    """
    Pārbauda, vai izvēlētais dalītājs ir atļauts pašreizējam skaitlim.
    
    Args:
        current_number (int): Pašreizējais spēles skaitlis.
        divisor (int): Skaitlis, ar ko dalīt (sagaidāms 2 vai 3).
        
    Returns:
        bool: True, ja dalījums ir bez atlikuma (current_number % divisor == 0), 
              pretējā gadījumā False.
    """
    pass

def apply_move(current_state: 'GameState', divisor: int) -> 'GameState':
    """
    Izpilda gājienu un aprēķina jauno stāvokli. NEMODIFICĒ esošo stāvokli, 
    bet atgriež pilnīgi jaunu GameState objektu.
    
    Noteikumi:
        - Jaunais skaitlis = current_number / divisor
        - Ja divisor == 2: pretiniekam +2 punkti.
        - Ja divisor == 3: gājiena veicējam +3 punkti.
        - Ja jaunais skaitlis beidzas ar 0 vai 5: bankai +1 punkts.
        - is_player_turn tiek nomainīts uz pretējo.
        
    Args:
        current_state (GameState): Esošais spēles stāvoklis pirms gājiena.
        divisor (int): Dalītājs (2 vai 3).
        
    Returns:
        GameState: Jauns objekts ar atjauninātajiem punktiem un skaitli.
    """
    pass

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
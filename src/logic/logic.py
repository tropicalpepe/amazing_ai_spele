from typing import List
from src.data.data import GameState


def generate_starting_numbers() -> List[int]:
    """Generates 5 random numbers divisible by 6 in range [10000, 20000]"""
    import random
    start = 10002  # First number divisible by 6 and >= 10000
    end = 19998    # Last number divisible by 6 and <= 20000
    divisible_by_6 = list(range(start, end + 1, 6))

    return random.sample(divisible_by_6, 5)


# ===== Move Generation and Validation =====

def get_legal_moves(state: GameState) -> List[int]:
    """
    Returns list of legal divisors for current state.

    Returns:
        List of valid divisors: [], [2], [3], or [2, 3]
    """
    moves = []
    if state.current_number % 3 == 0:
        moves.append(3)
    if state.current_number % 2 == 0:
        moves.append(2)
    return moves


def is_valid_move(current_number: int, divisor: int) -> bool:
    """Checks if a divisor is valid for the current number"""
    return current_number % divisor == 0


# ===== State Transitions =====

def apply_move(current_state: GameState, divisor: int) -> GameState:
    """
    Applies a move and returns new game state.

    Scoring rules:
    - Divide by 2: opponent gets 2 points
    - Divide by 3: current player gets 3 points
    - Result ends in 0 or 5: 1 point to bank

    Args:
        current_state: Current game state
        divisor: The divisor to apply (2 or 3)

    Returns:
        New game state after the move
    """
    new_number = current_state.current_number // divisor
    points_to_current = 3 if divisor == 3 else 0
    points_to_opponent = 2 if divisor == 2 else 0
    points_to_bank = 1 if new_number % 5 == 0 else 0

    return GameState(
        current_number=new_number,
        player_points=current_state.player_points + (points_to_current if current_state.is_player_turn else points_to_opponent),
        ai_points=current_state.ai_points + (points_to_opponent if current_state.is_player_turn else points_to_current),
        bank_points=current_state.bank_points + points_to_bank,
        is_player_turn=not current_state.is_player_turn
    )


# ===== Terminal State Detection =====

def is_terminal_state(state: GameState) -> bool:
    """
    Checks if game is over.

    Game ends when:
    - Current number <= 10
    - No legal moves available

    Args:
        state: Game state to check

    Returns:
        True if game is over, False otherwise
    """
    if state.current_number <= 10:
        return True
    return len(get_legal_moves(state)) == 0


# ===== Final Payout and Winner Determination =====

def apply_final_payout(state: GameState) -> GameState:
    """
    Awards bank points to the player who made the final move.

    The player whose turn it is NOT gets the bank (they just moved).

    Args:
        state: Terminal game state

    Returns:
        State with bank awarded to the last player
    """
    if state.is_player_turn:
        # AI made the last move (now it's player's turn)
        return GameState(
            current_number=state.current_number,
            player_points=state.player_points,
            ai_points=state.ai_points + state.bank_points,
            bank_points=0,
            is_player_turn=state.is_player_turn
        )
    else:
        # Player made the last move (now it's AI's turn)
        return GameState(
            current_number=state.current_number,
            player_points=state.player_points + state.bank_points,
            ai_points=state.ai_points,
            bank_points=0,
            is_player_turn=state.is_player_turn
        )


def determine_winner(state: GameState) -> str:
    """
    Determines the winner of the game.

    Args:
        state: Terminal game state

    Returns:
        'AI', 'Player', or 'Tie'
    """
    final_state = apply_final_payout(state)
    if final_state.ai_points > final_state.player_points:
        return 'AI'
    elif final_state.player_points > final_state.ai_points:
        return 'Player'
    else:
        return 'Tie'

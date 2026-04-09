"""
Game Controller - Encapsulates complete game logic and flow.

This class ensures the game rules are followed correctly and prevents
the UI from making mistakes like applying moves after the game ends.

The UI should ONLY interact with the game through this controller.
"""

from typing import Optional, List, Tuple
from src.data.data import GameState, create_initial_state
from src.logic.logic import (
    generate_starting_numbers,
    get_legal_moves,
    apply_move,
    is_terminal_state,
    apply_final_payout,
    determine_winner
)
from src.ai.search import find_best_move_alpha_beta, find_best_move_minimax
from src.ai.metrics import AIMetrics


class GameController:
    """
    Manages complete game flow and enforces rules.

    This is the single source of truth for game state and transitions.
    The UI should never directly call apply_move() or modify state.
    """

    def __init__(self):
        self._state: Optional[GameState] = None
        self._is_game_over: bool = False
        self._winner: Optional[str] = None

    @property
    def state(self) -> Optional[GameState]:
        """Current game state (read-only for UI)"""
        return self._state

    @property
    def is_game_over(self) -> bool:
        """Whether the game has ended"""
        return self._is_game_over

    @property
    def winner(self) -> Optional[str]:
        """Winner of the game ('AI', 'Player', 'Tie', or None if not over)"""
        return self._winner

    def generate_starting_numbers(self) -> List[int]:
        """Generate 5 random starting numbers"""
        return generate_starting_numbers()

    def start_game(self, chosen_number: int, player_starts: bool) -> GameState:
        self._state = create_initial_state(chosen_number, player_starts)
        self._is_game_over = False
        self._winner = None
        return self._state

    def get_legal_moves(self) -> List[int]:
        """
        Get legal moves for current state.

        Returns:
            List of legal divisors, or empty list if game is over
        """
        if self._state is None:
            raise RuntimeError("Game not started. Call start_game() first.")

        if self._is_game_over:
            return []

        return get_legal_moves(self._state)

    def make_move(self, move_value: int) -> Tuple[GameState, bool]:
        """
        Apply a move and update game state.

        Args:
            move_value: 2,3,-5,-7

        Returns:
            Tuple of (new_state, game_ended)

        Raises:
            RuntimeError: If game not started or already over
            ValueError: If move is not legal
        """
        if self._state is None:
            raise RuntimeError("Game not started. Call start_game() first.")

        if self._is_game_over:
            raise RuntimeError("Game is already over. Cannot make more moves.")

        legal_moves = get_legal_moves(self._state)
        if move_value not in legal_moves:
            raise ValueError(f"Illegal move: {move_value}. Legal moves: {legal_moves}")

        # Apply the move
        self._state = apply_move(self._state, move_value)

        # Check if game ended
        if is_terminal_state(self._state):
            self._is_game_over = True
            self._state = apply_final_payout(self._state)
            self._winner = determine_winner(self._state)
            return self._state, True

        return self._state, False

    def make_ai_move(self, depth: int = 15, algorithm: str = "Alpha-Beta", timeout: float = 10.0) -> Tuple[int, AIMetrics, bool]:
        """
        Let AI make a move.

        Returns:
            Tuple of (move, metrics, game_ended)

        Raises:
            RuntimeError: If game not started, already over, or not AI's turn
        """
        if self._state is None:
            raise RuntimeError("Game not started. Call start_game() first.")

        if self._is_game_over:
            raise RuntimeError("Game is already over. Cannot make more moves.")

        if self._state.is_player_turn:
            raise RuntimeError("It's the player's turn, not AI's turn.")

        # Get AI move
        if algorithm == "Minimax":
            move, metrics = find_best_move_minimax(self._state, depth, timeout)
        else:
            move, metrics = find_best_move_alpha_beta(self._state, depth, timeout)

        if move is None:
            raise RuntimeError("AI could not find a valid move.")

        # Apply the move
        self._state = apply_move(self._state, move)

        # Check if game ended
        if is_terminal_state(self._state):
            self._is_game_over = True
            self._state = apply_final_payout(self._state)
            self._winner = determine_winner(self._state)
            return move, metrics, True

        return move, metrics, False

    def get_game_summary(self) -> dict:
        """
        Get summary of current game state.

        Returns:
            Dictionary with game information
        """
        if self._state is None:
            return {
                "game_started": False,
                "message": "Game not started"
            }

        summary = {
            "game_started": True,
            "current_number": self._state.current_number,
            "player_points": self._state.player_points,
            "ai_points": self._state.ai_points,
            "bank_points": self._state.bank_points,
            "is_player_turn": self._state.is_player_turn,
            "is_game_over": self._is_game_over,
            "legal_moves": self.get_legal_moves(),
        }

        if self._is_game_over:
            summary["winner"] = self._winner

        return summary

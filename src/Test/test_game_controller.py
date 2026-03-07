"""
Integration tests for GameController.

These tests verify that the controller properly enforces game rules
and prevents common mistakes like continuing to play after game ends.
"""

import pytest
from src.logic.game_controller import GameController


class TestGameControllerFlow:
    """Test complete game flow through controller"""

    def test_must_start_game_before_moves(self):
        """Should raise error if trying to make moves before starting game"""
        controller = GameController()

        with pytest.raises(RuntimeError, match="Game not started"):
            controller.make_move(2)

        with pytest.raises(RuntimeError, match="Game not started"):
            controller.make_ai_move()

    def test_complete_game_flow(self):
        """Test a complete game from start to finish"""
        controller = GameController()

        # Start game
        state = controller.start_game(72, player_starts=True)
        assert state.current_number == 72
        assert controller.is_game_over == False

        # Player move: 72 → 36
        state, game_ended = controller.make_move(2)
        assert state.current_number == 36
        assert game_ended == False
        assert controller.is_game_over == False

        # AI move: 36 → 12
        move, metrics, game_ended = controller.make_ai_move()
        assert controller.state.current_number == 12
        assert game_ended == False
        assert controller.is_game_over == False

        # Player move: 12 → 6 (game ends)
        state, game_ended = controller.make_move(2)
        assert state.current_number == 6
        assert game_ended == True
        assert controller.is_game_over == True
        assert controller.winner in ['AI', 'Player', 'Tie']

    def test_cannot_make_moves_after_game_ends(self):
        """Should raise error if trying to move after game is over"""
        controller = GameController()
        controller.start_game(18, player_starts=True)

        # Make move that ends game: 18 → 6
        state, game_ended = controller.make_move(3)
        assert game_ended == True
        assert controller.is_game_over == True

        # Try to make another move - should fail
        with pytest.raises(RuntimeError, match="Game is already over"):
            controller.make_move(2)

    def test_cannot_make_ai_move_after_game_ends(self):
        """Should raise error if AI tries to move after game is over"""
        controller = GameController()
        controller.start_game(18, player_starts=False)

        # AI makes move that ends game: 18 → 6
        move, metrics, game_ended = controller.make_ai_move()
        assert game_ended == True
        assert controller.is_game_over == True

        # Try to make another AI move - should fail
        with pytest.raises(RuntimeError, match="Game is already over"):
            controller.make_ai_move()

    def test_get_legal_moves_returns_empty_after_game_ends(self):
        """Should return empty list for legal moves after game ends"""
        controller = GameController()
        controller.start_game(18, player_starts=True)

        # Before end
        moves = controller.get_legal_moves()
        assert len(moves) > 0

        # Make move that ends game
        controller.make_move(3)

        # After end
        moves = controller.get_legal_moves()
        assert moves == []

    def test_cannot_make_illegal_move(self):
        """Should raise error for illegal moves"""
        controller = GameController()
        controller.start_game(27, player_starts=True)  # 27 only divisible by 3

        with pytest.raises(ValueError, match="Illegal move"):
            controller.make_move(2)

    def test_ai_cannot_move_on_player_turn(self):
        """AI should not be able to move when it's player's turn"""
        controller = GameController()
        controller.start_game(72, player_starts=True)

        with pytest.raises(RuntimeError, match="player's turn"):
            controller.make_ai_move()

    def test_game_summary_before_start(self):
        """Should return appropriate summary before game starts"""
        controller = GameController()
        summary = controller.get_game_summary()

        assert summary["game_started"] == False
        assert "message" in summary

    def test_game_summary_during_game(self):
        """Should return complete summary during game"""
        controller = GameController()
        controller.start_game(72, player_starts=True)

        summary = controller.get_game_summary()
        assert summary["game_started"] == True
        assert summary["current_number"] == 72
        assert summary["is_game_over"] == False
        assert len(summary["legal_moves"]) > 0

    def test_game_summary_after_game_ends(self):
        """Should include winner in summary after game ends"""
        controller = GameController()
        controller.start_game(18, player_starts=True)
        controller.make_move(3)  # Ends game

        summary = controller.get_game_summary()
        assert summary["is_game_over"] == True
        assert "winner" in summary
        assert summary["winner"] in ['AI', 'Player', 'Tie']
        assert summary["legal_moves"] == []


class TestGameControllerPreventsTestMistake:
    """
    Tests specifically designed to catch the mistake we found in test_requirements.py
    where moves were made after the game should have ended.
    """

    def test_prevents_moves_after_reaching_terminal_number(self):
        """
        This is the exact scenario from the broken test.
        Controller should prevent moves after reaching <= 10.
        """
        controller = GameController()
        controller.start_game(18, player_starts=True)

        # Player divides by 3 → 6 (game should end)
        state, game_ended = controller.make_move(3)
        assert state.current_number == 6
        assert game_ended == True
        assert controller.is_game_over == True

        # This is what the broken test tried to do - should fail!
        with pytest.raises(RuntimeError, match="Game is already over"):
            controller.make_move(2)  # Would be 6 → 3

        # And this too
        with pytest.raises(RuntimeError, match="Game is already over"):
            controller.make_ai_move()

    def test_enforces_terminal_check_between_all_moves(self):
        """Verify game checks terminal state after EVERY move"""
        controller = GameController()
        controller.start_game(72, player_starts=True)

        # Move 1: 72 → 36
        _, ended = controller.make_move(2)
        assert ended == False
        assert controller.is_game_over == False

        # Move 2: 36 → 12
        _, _, ended = controller.make_ai_move()
        assert ended == False
        assert controller.is_game_over == False

        # Move 3: 12 → 6 (terminal!)
        _, ended = controller.make_move(2)
        assert ended == True
        assert controller.is_game_over == True

        # Cannot continue
        with pytest.raises(RuntimeError):
            controller.make_move(2)

    def test_multiple_games_in_sequence(self):
        """Can start new game after previous game ends"""
        controller = GameController()

        # First game
        controller.start_game(18, player_starts=True)
        controller.make_move(3)  # Ends at 6
        assert controller.is_game_over == True

        # Start new game - should work
        controller.start_game(72, player_starts=False)
        assert controller.is_game_over == False
        assert controller.state.current_number == 72

        # Can make moves in new game
        move, metrics, ended = controller.make_ai_move()
        assert ended == False


class TestGameControllerWithBank:
    """Test bank payout through controller"""

    def test_bank_awarded_correctly_at_game_end(self):
        """Bank should be awarded to correct player when game ends"""
        controller = GameController()
        controller.start_game(120, player_starts=True)

        # 120 → 60 (ends in 0, bank gets 1)
        controller.make_move(2)
        assert controller.state.bank_points == 1
        assert controller.state.player_points == 0
        assert controller.state.ai_points == 2

        # 60 → 20 (AI divides by 3, ends in 0, bank gets 1)
        controller.make_ai_move()
        assert controller.state.bank_points == 2
        assert controller.state.player_points == 0  # AI divided by 3, so AI gets 3
        assert controller.state.ai_points == 5  # Had 2, got 3

        # 20 → 10 (ends in 0, bank gets 1, game ends!)
        state, game_ended = controller.make_move(2)
        assert game_ended == True

        # Bank should be awarded (applied in make_move automatically)
        # Player made last move (divided by 2), so player gets bank
        assert state.bank_points == 0  # Bank cleared
        assert state.player_points == 0 + 3  # Had 0, got 3 bank
        assert state.ai_points == 7  # Had 5, got 2 as opponent


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

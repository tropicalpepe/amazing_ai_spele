"""
End-to-end tests verifying all requirements from requirements.md

Tests cover:
1. Initial number generation (10,000-20,000, divisible by 6)
2. Player selection and turn management
3. Move validation (divide by 2 or 3, only if whole number)
4. Scoring rules:
   - Divide by 2: opponent gets 2 points
   - Divide by 3: current player gets 3 points
   - Result ends in 0 or 5: 1 point to bank
5. Terminal condition (number <= 10)
6. Bank payout to final player
7. Winner determination
8. AI integration with game tree
"""

import pytest
from src.data.data import GameState, create_initial_state
from src.logic.logic import (
    generate_starting_numbers,
    get_legal_moves,
    is_valid_move,
    apply_move,
    is_terminal_state,
    apply_final_payout,
    determine_winner
)
from src.ai.search import find_best_move_alpha_beta, build_game_tree


class TestInitialSetup:
    """Test Requirement: Initial number generation and setup"""

    def test_generate_starting_numbers_count(self):
        """Should generate exactly 5 numbers"""
        numbers = generate_starting_numbers()
        assert len(numbers) == 5

    def test_generate_starting_numbers_range(self):
        """Numbers should be in range [10000, 20000]"""
        numbers = generate_starting_numbers()
        for num in numbers:
            assert 10000 <= num <= 20000

    def test_generate_starting_numbers_divisible_by_6(self):
        """Numbers must be divisible by both 2 and 3 (i.e., by 6)"""
        numbers = generate_starting_numbers()
        for num in numbers:
            assert num % 2 == 0, f"{num} not divisible by 2"
            assert num % 3 == 0, f"{num} not divisible by 3"
            assert num % 6 == 0, f"{num} not divisible by 6"

    def test_generate_starting_numbers_uniqueness(self):
        """Generated numbers should be unique"""
        numbers = generate_starting_numbers()
        assert len(numbers) == len(set(numbers))

    def test_create_initial_state_player_starts(self):
        """Initial state should correctly set player as first"""
        state = create_initial_state(12000, player_starts=True)
        assert state.current_number == 12000
        assert state.player_points == 0
        assert state.ai_points == 0
        assert state.bank_points == 0
        assert state.is_player_turn == True

    def test_create_initial_state_ai_starts(self):
        """Initial state should correctly set AI as first"""
        state = create_initial_state(12000, player_starts=False)
        assert state.is_player_turn == False


class TestMoveValidation:
    """Test Requirement: Move validation (divide by 2 or 3, only integers)"""

    def test_valid_move_divisible_by_2(self):
        """Should allow division by 2 when result is whole number"""
        assert is_valid_move(12, 2) == True
        assert is_valid_move(100, 2) == True

    def test_valid_move_divisible_by_3(self):
        """Should allow division by 3 when result is whole number"""
        assert is_valid_move(12, 3) == True
        assert is_valid_move(99, 3) == True

    def test_invalid_move_not_divisible_by_2(self):
        """Should reject division by 2 when result is not whole number"""
        assert is_valid_move(11, 2) == False
        assert is_valid_move(99, 2) == False

    def test_invalid_move_not_divisible_by_3(self):
        """Should reject division by 3 when result is not whole number"""
        assert is_valid_move(10, 3) == False
        assert is_valid_move(100, 3) == False

    def test_get_legal_moves_both_valid(self):
        """When both moves valid, return both"""
        state = GameState(18, 0, 0, 0, True)
        moves = get_legal_moves(state)
        assert 2 in moves
        assert 3 in moves
        assert len(moves) == 2

    def test_get_legal_moves_only_2_valid(self):
        """When only divisible by 2"""
        state = GameState(16, 0, 0, 0, True)
        moves = get_legal_moves(state)
        assert moves == [2]

    def test_get_legal_moves_only_3_valid(self):
        """When only divisible by 3"""
        state = GameState(27, 0, 0, 0, True)
        moves = get_legal_moves(state)
        assert moves == [3]

    def test_get_legal_moves_none_valid(self):
        """When neither divisor works"""
        state = GameState(11, 0, 0, 0, True)
        moves = get_legal_moves(state)
        assert moves == []


class TestScoringRules:
    """Test Requirement: Scoring rules"""

    def test_divide_by_2_opponent_gets_2_points_player_turn(self):
        """Divide by 2: opponent (AI) gets 2 points when player moves"""
        state = GameState(100, 5, 3, 0, is_player_turn=True)
        new_state = apply_move(state, 2)
        assert new_state.player_points == 5  # Player gets 0
        assert new_state.ai_points == 5      # AI gets 2 (3 + 2)

    def test_divide_by_2_opponent_gets_2_points_ai_turn(self):
        """Divide by 2: opponent (Player) gets 2 points when AI moves"""
        state = GameState(100, 5, 3, 0, is_player_turn=False)
        new_state = apply_move(state, 2)
        assert new_state.player_points == 7  # Player gets 2 (5 + 2)
        assert new_state.ai_points == 3      # AI gets 0

    def test_divide_by_3_current_player_gets_3_points_player_turn(self):
        """Divide by 3: current player gets 3 points when player moves"""
        state = GameState(99, 5, 3, 0, is_player_turn=True)
        new_state = apply_move(state, 3)
        assert new_state.player_points == 8  # Player gets 3 (5 + 3)
        assert new_state.ai_points == 3      # AI gets 0

    def test_divide_by_3_current_player_gets_3_points_ai_turn(self):
        """Divide by 3: current player gets 3 points when AI moves"""
        state = GameState(99, 5, 3, 0, is_player_turn=False)
        new_state = apply_move(state, 3)
        assert new_state.player_points == 5  # Player gets 0
        assert new_state.ai_points == 6      # AI gets 3 (3 + 3)

    def test_bank_receives_1_point_when_result_ends_in_0(self):
        """Bank gets 1 point when result ends in 0"""
        state = GameState(60, 0, 0, 0, True)
        new_state = apply_move(state, 2)  # 60/2 = 30 (ends in 0)
        assert new_state.bank_points == 1

        state = GameState(60, 0, 0, 0, True)
        new_state = apply_move(state, 3)  # 60/3 = 20 (ends in 0)
        assert new_state.bank_points == 1

    def test_bank_receives_1_point_when_result_ends_in_5(self):
        """Bank gets 1 point when result ends in 5"""
        state = GameState(30, 0, 0, 5, True)
        new_state = apply_move(state, 2)  # 30/2 = 15 (ends in 5)
        assert new_state.bank_points == 6  # 5 + 1

        state = GameState(45, 0, 0, 5, True)
        new_state = apply_move(state, 3)  # 45/3 = 15 (ends in 5)
        assert new_state.bank_points == 6  # 5 + 1

    def test_bank_no_point_when_result_ends_in_other(self):
        """Bank gets 0 points when result doesn't end in 0 or 5"""
        state = GameState(36, 0, 0, 0, True)
        new_state = apply_move(state, 2)  # 36/2 = 18 (ends in 8)
        assert new_state.bank_points == 0

        new_state2 = apply_move(new_state, 3)  # 18/3 = 6 (ends in 6)
        assert new_state2.bank_points == 0

    def test_turn_switches_after_move(self):
        """Turn should switch after each move"""
        state = GameState(100, 0, 0, 0, is_player_turn=True)
        new_state = apply_move(state, 2)
        assert new_state.is_player_turn == False

        new_state2 = apply_move(new_state, 2)
        assert new_state2.is_player_turn == True


class TestTerminalConditions:
    """Test Requirement: Game ends when number <= 10"""

    def test_terminal_when_number_equals_10(self):
        """Game should end when number is exactly 10"""
        state = GameState(10, 10, 15, 5, True)
        assert is_terminal_state(state) == True

    def test_terminal_when_number_less_than_10(self):
        """Game should end when number < 10"""
        state = GameState(5, 10, 15, 5, True)
        assert is_terminal_state(state) == True

        state = GameState(1, 10, 15, 5, True)
        assert is_terminal_state(state) == True

    def test_not_terminal_when_number_greater_than_10(self):
        """Game should continue when number > 10 and has legal moves"""
        state = GameState(12, 10, 15, 5, True)  # 12 is divisible by 2 and 3
        assert is_terminal_state(state) == False

        state = GameState(1000, 10, 15, 5, True)
        assert is_terminal_state(state) == False

    def test_terminal_when_no_legal_moves(self):
        """Game should end when no legal moves available"""
        state = GameState(11, 10, 15, 5, True)  # 11 is prime, not divisible by 2 or 3
        assert is_terminal_state(state) == True


class TestBankPayout:
    """Test Requirement: Final player gets bank points"""

    def test_bank_payout_to_ai_when_ai_made_last_move(self):
        """AI should get bank when AI made the final move"""
        # After AI moves, it becomes player's turn
        state = GameState(10, 5, 8, 10, is_player_turn=True)
        final_state = apply_final_payout(state)
        assert final_state.ai_points == 18     # 8 + 10
        assert final_state.player_points == 5
        assert final_state.bank_points == 0

    def test_bank_payout_to_player_when_player_made_last_move(self):
        """Player should get bank when player made the final move"""
        # After player moves, it becomes AI's turn
        state = GameState(10, 5, 8, 10, is_player_turn=False)
        final_state = apply_final_payout(state)
        assert final_state.player_points == 15  # 5 + 10
        assert final_state.ai_points == 8
        assert final_state.bank_points == 0

    def test_bank_payout_when_bank_is_zero(self):
        """Bank payout should work correctly when bank is 0"""
        state = GameState(10, 5, 8, 0, is_player_turn=True)
        final_state = apply_final_payout(state)
        assert final_state.ai_points == 8
        assert final_state.player_points == 5


class TestWinnerDetermination:
    """Test Requirement: Winner determination"""

    def test_ai_wins_when_ai_has_more_points(self):
        """AI wins when AI has more points after bank payout"""
        state = GameState(10, 5, 15, 0, True)
        winner = determine_winner(state)
        assert winner == 'AI'

    def test_player_wins_when_player_has_more_points(self):
        """Player wins when player has more points after bank payout"""
        state = GameState(10, 20, 15, 0, True)
        winner = determine_winner(state)
        assert winner == 'Player'

    def test_tie_when_equal_points(self):
        """Tie when both players have equal points after bank payout"""
        state = GameState(10, 15, 15, 0, True)
        winner = determine_winner(state)
        assert winner == 'Tie'

    def test_winner_with_bank_payout_to_ai(self):
        """Winner determination includes bank payout"""
        state = GameState(10, 10, 8, 5, is_player_turn=True)
        # AI gets bank: 8 + 5 = 13, Player: 10
        winner = determine_winner(state)
        assert winner == 'AI'

    def test_winner_with_bank_payout_to_player(self):
        """Winner determination includes bank payout"""
        state = GameState(10, 10, 8, 5, is_player_turn=False)
        # Player gets bank: 10 + 5 = 15, AI: 8
        winner = determine_winner(state)
        assert winner == 'Player'


class TestFullGameScenario:
    """Test complete game scenarios end-to-end"""

    def test_simple_game_sequence(self):
        """Test a simple game from start to finish"""
        # Start with 72
        state = GameState(72, 0, 0, 0, is_player_turn=True)

        # Player divides by 2 -> 36
        state = apply_move(state, 2)
        assert state.current_number == 36
        assert state.player_points == 0  # Opponent (AI) gets 2
        assert state.ai_points == 2
        assert state.is_player_turn == False
        assert is_terminal_state(state) == False

        # AI divides by 3 -> 12
        state = apply_move(state, 3)
        assert state.current_number == 12
        assert state.player_points == 0
        assert state.ai_points == 5  # AI gets 3
        assert state.is_player_turn == True
        assert is_terminal_state(state) == False

        # Player divides by 2 -> 6
        # Game ends here (6 <= 10)
        state = apply_move(state, 2)
        assert state.current_number == 6
        assert state.player_points == 0
        assert state.ai_points == 7  # AI gets 2 (opponent)
        assert is_terminal_state(state) == True

        # Determine winner - Player made last move (now AI's turn)
        winner = determine_winner(state)
        assert winner == 'AI'

    def test_game_with_bank_accumulation(self):
        """Test game where bank accumulates and gets paid out"""
        # Start with 60
        state = GameState(60, 0, 0, 0, is_player_turn=True)

        # Player divides by 2 -> 30 (ends in 0, bank gets 1)
        state = apply_move(state, 2)
        assert state.current_number == 30
        assert state.ai_points == 2  # Opponent gets 2
        assert state.bank_points == 1

        # AI divides by 2 -> 15 (ends in 5, bank gets 1)
        state = apply_move(state, 2)
        assert state.current_number == 15
        assert state.player_points == 2  # Opponent gets 2
        assert state.bank_points == 2

        # Player divides by 3 -> 5 (ends in 5, bank gets 1)
        state = apply_move(state, 3)
        assert state.current_number == 5
        assert state.player_points == 5  # Gets 3
        assert state.bank_points == 3
        assert is_terminal_state(state) == True

        # Player made last move (now AI's turn), so Player gets bank
        final_state = apply_final_payout(state)
        assert final_state.player_points == 8  # 5 + 3
        assert final_state.ai_points == 2


class TestAIIntegration:
    """Test AI integration with game rules"""

    def test_ai_returns_valid_move(self):
        """AI should return a legal move"""
        state = GameState(18, 0, 0, 0, is_player_turn=False)
        move, metrics = find_best_move_alpha_beta(state, depth=3)

        legal_moves = get_legal_moves(state)
        assert move in legal_moves

    def test_ai_metrics_tracking(self):
        """AI should track metrics"""
        state = GameState(18, 0, 0, 0, is_player_turn=False)
        move, metrics = find_best_move_alpha_beta(state, depth=3)

        assert metrics.nodes_generated > 0
        assert metrics.nodes_evaluated > 0
        assert metrics.elapsed_ms >= 0
        assert metrics.best_move == move
        assert metrics.best_score is not None

    def test_game_tree_building(self):
        """Game tree should build correctly"""
        state = GameState(18, 0, 0, 0, is_player_turn=False)
        root = build_game_tree(state, max_depth=2)

        assert root.state.current_number == 18
        assert root.depth == 0
        assert len(root.children) > 0

        # Check children are valid
        for move, child in root.children.items():
            assert move in [2, 3]
            assert child.depth == 1
            assert child.state.current_number == 18 // move

    def test_ai_handles_terminal_state(self):
        """AI should handle near-terminal states correctly"""
        state = GameState(12, 5, 8, 2, is_player_turn=False)
        move, metrics = find_best_move_alpha_beta(state, depth=5)

        # Should return a valid move
        assert move in get_legal_moves(state)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

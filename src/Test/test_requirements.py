"""
End-to-end tests verifying all requirements from requirements.md

Tests cover:
1. Initial number generation (1000-2000, divisible by 6)
2. Player selection and turn management
3. Move validation (divide by 2 or 3 only if whole number, always for -5 and -7)
4. Scoring rules:
   - Divide by 2: opponent gets 2 points
   - Divide by 3: current player gets 3 points
   - Subtract 5: 1 point to bank
   - Subtract 7: 1 point to opponent
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
        """Numbers should be in range [1000, 2000]"""
        numbers = generate_starting_numbers()
        for num in numbers:
            assert 1000 <= num <= 2000

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
        state = create_initial_state(1200, player_starts=True)
        assert state.current_number == 1200
        assert state.player_points == 0
        assert state.ai_points == 0
        assert state.bank_points == 0
        assert state.is_player_turn == True

    def test_create_initial_state_ai_starts(self):
        """Initial state should correctly set AI as first"""
        state = create_initial_state(1200, player_starts=False)
        assert state.is_player_turn == False


class TestMoveValidation:
    """Test Requirement: Move validation"""

    def test_valid_move_divisible_by_2(self):
        assert is_valid_move(12, 2) == True

    def test_valid_move_divisible_by_3(self):
        assert is_valid_move(12, 3) == True

    def test_invalid_move_not_divisible_by_2(self):
        assert is_valid_move(11, 2) == False

    def test_invalid_move_not_divisible_by_3(self):
        assert is_valid_move(10, 3) == False
        
    def test_valid_move_subtract_5_and_7(self):
        assert is_valid_move(11, -5) == True
        assert is_valid_move(10, -7) == True

    def test_get_legal_moves_both_valid(self):
        state = GameState(18, 0, 0, 0, True)
        moves = get_legal_moves(state)
        assert 2 in moves
        assert 3 in moves
        assert -5 in moves
        assert -7 in moves
        assert len(moves) == 4

    def test_get_legal_moves_only_2_valid(self):
        state = GameState(16, 0, 0, 0, True)
        moves = get_legal_moves(state)
        assert set(moves) == {2, -5, -7}

    def test_get_legal_moves_none_valid(self):
        state = GameState(11, 0, 0, 0, True)
        moves = get_legal_moves(state)
        assert set(moves) == {-5, -7}


class TestScoringRules:
    """Test Requirement: Scoring rules"""

    def test_divide_by_2_opponent_gets_2_points_player_turn(self):
        state = GameState(100, 5, 3, 0, is_player_turn=True)
        new_state = apply_move(state, 2)
        assert new_state.player_points == 5  
        assert new_state.ai_points == 5      
        
    def test_divide_by_3_current_player_gets_3_points_player_turn(self):
        state = GameState(99, 5, 3, 0, is_player_turn=True)
        new_state = apply_move(state, 3)
        assert new_state.player_points == 8  
        assert new_state.ai_points == 3      

    def test_subtract_5_bank_gets_1_point(self):
        state = GameState(60, 5, 5, 0, True)
        new_state = apply_move(state, -5)
        assert new_state.bank_points == 1
        assert new_state.player_points == 5
        assert new_state.ai_points == 5

    def test_subtract_7_opponent_gets_1_point(self):
        state = GameState(30, 5, 5, 5, True) # Player turn
        new_state = apply_move(state, -7)
        assert new_state.bank_points == 5
        assert new_state.player_points == 5
        assert new_state.ai_points == 6 # AI gets 1
        
        state2 = GameState(30, 5, 5, 5, False) # AI turn
        new_state2 = apply_move(state2, -7)
        assert new_state2.player_points == 6 # Player gets 1
        assert new_state2.ai_points == 5

    def test_turn_switches_after_move(self):
        state = GameState(100, 0, 0, 0, is_player_turn=True)
        new_state = apply_move(state, -5)
        assert new_state.is_player_turn == False


class TestTerminalConditions:
    """Test Requirement: Game ends when number <= 10"""

    def test_terminal_when_number_equals_10(self):
        state = GameState(10, 10, 15, 5, True)
        assert is_terminal_state(state) == True

    def test_terminal_when_number_less_than_10(self):
        state = GameState(5, 10, 15, 5, True)
        assert is_terminal_state(state) == True

    def test_not_terminal_when_number_greater_than_10(self):
        state = GameState(11, 10, 15, 5, True)
        assert is_terminal_state(state) == False


class TestBankPayout:
    """Test Requirement: Final player gets bank points"""

    def test_bank_payout_to_ai_when_ai_made_last_move(self):
        state = GameState(10, 5, 8, 10, is_player_turn=True)
        final_state = apply_final_payout(state)
        assert final_state.ai_points == 18     
        assert final_state.player_points == 5
        assert final_state.bank_points == 0

    def test_bank_payout_to_player_when_player_made_last_move(self):
        state = GameState(10, 5, 8, 10, is_player_turn=False)
        final_state = apply_final_payout(state)
        assert final_state.player_points == 15  
        assert final_state.ai_points == 8
        assert final_state.bank_points == 0


class TestWinnerDetermination:
    """Test Requirement: Winner determination"""

    def test_ai_wins_when_ai_has_more_points(self):
        state = GameState(10, 5, 15, 0, True)
        assert determine_winner(state) == 'AI'

    def test_player_wins_when_player_has_more_points(self):
        state = GameState(10, 20, 15, 0, True)
        assert determine_winner(state) == 'Player'

    def test_tie_when_equal_points(self):
        state = GameState(10, 15, 15, 0, True)
        assert determine_winner(state) == 'Tie'


class TestFullGameScenario:
    """Test complete game scenarios end-to-end"""

    def test_simple_game_sequence(self):
        # Start with 20
        state = GameState(20, 0, 0, 0, is_player_turn=True)

        # Player subtracts 5 -> 15 (bank gets 1)
        state = apply_move(state, -5)
        assert state.current_number == 15
        assert state.bank_points == 1
        assert state.is_player_turn == False
        assert is_terminal_state(state) == False

        # AI subtracts 7 -> 8 (player gets 1)
        state = apply_move(state, -7)
        assert state.current_number == 8
        assert state.player_points == 1
        assert state.is_player_turn == True
        assert is_terminal_state(state) == True

        # Determine winner - AI made the last move (now Player's turn)
        # Final payout: AI gets the 1 bank point
        winner = determine_winner(state)
        # AI has 1 point, Player has 1 point. Tie!
        assert winner == 'Tie'


class TestAIIntegration:
    """Test AI integration with game rules"""

    def test_ai_returns_valid_move(self):
        state = GameState(18, 0, 0, 0, is_player_turn=False)
        move, metrics = find_best_move_alpha_beta(state, depth=3)
        legal_moves = get_legal_moves(state)
        assert move in legal_moves

    def test_ai_metrics_tracking(self):
        state = GameState(18, 0, 0, 0, is_player_turn=False)
        move, metrics = find_best_move_alpha_beta(state, depth=3)
        assert metrics.nodes_generated > 0
        assert metrics.elapsed_ms >= 0

    def test_game_tree_building(self):
        state = GameState(18, 0, 0, 0, is_player_turn=False)
        root = build_game_tree(state, max_depth=2)
        assert root.depth == 0
        
        # Valid moves for 18 are 2, 3, -5, -7
        for move, child in root.children.items():
            assert move in [2, 3, -5, -7]
            assert child.depth == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

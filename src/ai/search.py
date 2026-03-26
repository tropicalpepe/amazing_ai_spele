import time
from typing import Optional
from src.data.data import GameState, GameTreeNode
from src.logic.logic import get_legal_moves, apply_move, is_terminal_state
from src.ai.heuristics import evaluate_terminal_state, evaluate_heuristic
from src.ai.metrics import AIMetrics


# ===== Tree Building Functions =====

def create_node(state: GameState, depth: int, metrics: Optional[AIMetrics] = None) -> GameTreeNode:
    """Creates a new game tree node and tracks metrics"""
    if metrics:
        metrics.nodes_generated += 1

    return GameTreeNode(
        state=state,
        depth=depth,
        children={},
        is_terminal=is_terminal_state(state)
    )


def expand_node(node: GameTreeNode, metrics: Optional[AIMetrics] = None) -> None:
    """Expands a node by creating all child nodes for legal moves"""
    if node.is_terminal:
        return

    legal_moves = get_legal_moves(node.state)
    for move in legal_moves:
        new_state = apply_move(node.state, move)
        child_node = create_node(new_state, node.depth + 1, metrics)
        node.children[move] = child_node


def build_game_tree(initial_state: GameState, max_depth: int, metrics: Optional[AIMetrics] = None) -> GameTreeNode:
    """
    Builds a game tree up to max_depth.

    Args:
        initial_state: Starting game state
        max_depth: Maximum depth to build
        metrics: Optional metrics tracker

    Returns:
        Root node of the generated tree
    """
    root = create_node(initial_state, 0, metrics)

    def build_recursive(node: GameTreeNode):
        if node.depth >= max_depth or node.is_terminal:
            return

        expand_node(node, metrics)
        for child in node.children.values():
            build_recursive(child)

    build_recursive(root)
    return root


# ===== Alpha-Beta Search =====

def alpha_beta_search(
    node: GameTreeNode,
    depth: int,
    alpha: float,
    beta: float,
    is_maximizing: bool,
    metrics: Optional[AIMetrics] = None,
    start_time: float = 0.0,
    timeout: float = 10.0
) -> float:
    if start_time > 0 and (time.time() - start_time > timeout):
        raise TimeoutError(f"AI algoritms tika apturēts: pārsniegts {timeout}s limits. Lūdzu samaziniet dziļumu!")
    """
    Alpha-beta pruning search on game tree nodes.

    Args:
        node: Current tree node
        depth: Remaining search depth
        alpha: Best value for maximizer
        beta: Best value for minimizer
        is_maximizing: True if maximizing player's turn
        metrics: Optional metrics tracker

    Returns:
        Evaluation score from current node
    """
    # Base cases
    if depth == 0 or node.is_terminal:
        if node.is_terminal:
            node.evaluation = evaluate_terminal_state(node.state)
        else:
            node.evaluation = evaluate_heuristic(node.state)

        if metrics:
            metrics.nodes_evaluated += 1

        return node.evaluation

    # Expand if needed
    if not node.children:
        expand_node(node, metrics)

    if not node.children:  # No legal moves
        node.evaluation = evaluate_terminal_state(node.state)
        if metrics:
            metrics.nodes_evaluated += 1
        return node.evaluation

    if is_maximizing:
        max_eval = float('-inf')
        for move, child in node.children.items():
            curr_eval = alpha_beta_search(child, depth - 1, alpha, beta, False, metrics, start_time, timeout)
            if curr_eval > max_eval:
                max_eval = curr_eval
                node.best_move = move
            alpha = max(alpha, curr_eval)
            if beta <= alpha:
                if metrics:
                    metrics.pruned_branches += 1
                break
        node.evaluation = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for move, child in node.children.items():
            curr_eval = alpha_beta_search(child, depth - 1, alpha, beta, True, metrics, start_time, timeout)
            if curr_eval < min_eval:
                min_eval = curr_eval
                node.best_move = move
            beta = min(beta, curr_eval)
            if beta <= alpha:
                if metrics:
                    metrics.pruned_branches += 1
                break
        node.evaluation = min_eval
        return min_eval


# ===== Minimax Search =====

def minimax_search(
    node: GameTreeNode,
    depth: int,
    is_maximizing: bool,
    metrics: Optional[AIMetrics] = None,
    start_time: float = 0.0,
    timeout: float = 10.0
) -> float:
    if start_time > 0 and (time.time() - start_time > timeout):
        raise TimeoutError(f"AI algoritms tika apturēts: pārsniegts {timeout}s limits. Lūdzu samaziniet dziļumu!")
    """
    Minimax search on game tree nodes (exhaustive evaluation without pruning).

    Args:
        node: Current tree node
        depth: Remaining search depth
        is_maximizing: True if maximizing player's turn
        metrics: Optional metrics tracker

    Returns:
        Evaluation score from current node
    """
    # Base cases
    if depth == 0 or node.is_terminal:
        if node.is_terminal:
            node.evaluation = evaluate_terminal_state(node.state)
        else:
            node.evaluation = evaluate_heuristic(node.state)

        if metrics:
            metrics.nodes_evaluated += 1

        return node.evaluation

    # Expand if needed
    if not node.children:
        expand_node(node, metrics)

    if not node.children:  # No legal moves
        node.evaluation = evaluate_terminal_state(node.state)
        if metrics:
            metrics.nodes_evaluated += 1
        return node.evaluation

    if is_maximizing:
        max_eval = float('-inf')
        for move, child in node.children.items():
            curr_eval = minimax_search(child, depth - 1, False, metrics, start_time, timeout)
            if curr_eval > max_eval:
                max_eval = curr_eval
                node.best_move = move
        node.evaluation = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for move, child in node.children.items():
            curr_eval = minimax_search(child, depth - 1, True, metrics, start_time, timeout)
            if curr_eval < min_eval:
                min_eval = curr_eval
                node.best_move = move
        node.evaluation = min_eval
        return min_eval


# ===== Best Move Selector =====

def find_best_move_alpha_beta(state: GameState, depth: int, timeout: float = 10.0) -> tuple[int, AIMetrics]:
    """
    Finds the best move using alpha-beta pruning.

    Args:
        state: Current game state
        depth: Search depth limit

    Returns:
        Tuple of (best_move, metrics)
    """
    metrics = AIMetrics()
    start_time = time.time()

    # Create root node
    root = create_node(state, 0, metrics)

    # Determine if AI is maximizing (AI's turn means minimizer just moved)
    is_maximizing = not state.is_player_turn

    # Run alpha-beta search
    score = alpha_beta_search(
        root,
        depth,
        float('-inf'),
        float('inf'),
        is_maximizing,
        metrics,
        start_time,
        timeout
    )

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    metrics.elapsed_ms = elapsed_time * 1000
    metrics.best_score = score
    metrics.best_move = root.best_move

    return root.best_move, metrics


def find_best_move_minimax(state: GameState, depth: int, timeout: float = 10.0) -> tuple[int, AIMetrics]:
    """
    Finds the best move using minimax.

    Args:
        state: Current game state
        depth: Search depth limit

    Returns:
        Tuple of (best_move, metrics)
    """
    metrics = AIMetrics()
    start_time = time.time()

    # Create root node
    root = create_node(state, 0, metrics)

    # Determine if AI is maximizing (AI's turn means minimizer just moved)
    is_maximizing = not state.is_player_turn

    # Run minimax search
    score = minimax_search(
        root,
        depth,
        is_maximizing,
        metrics,
        start_time,
        timeout
    )

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    metrics.elapsed_ms = elapsed_time * 1000
    metrics.best_score = score
    metrics.best_move = root.best_move

    return root.best_move, metrics


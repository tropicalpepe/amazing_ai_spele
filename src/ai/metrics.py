from dataclasses import dataclass
from typing import Optional


@dataclass
class AIMetrics:
    """Tracks metrics for AI search algorithms"""
    nodes_generated: int = 0
    nodes_evaluated: int = 0
    pruned_branches: int = 0
    elapsed_ms: float = 0.0
    best_move: Optional[int] = None
    best_score: Optional[float] = None

    def reset(self):
        """Resets all counters"""
        self.nodes_generated = 0
        self.nodes_evaluated = 0
        self.pruned_branches = 0
        self.elapsed_ms = 0.0
        self.best_move = None
        self.best_score = None

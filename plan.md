# AI Game Tree and Alpha-Beta Implementation Plan

## Goal

Implement a proper game tree structure and an Alpha-Beta Pruning algorithm that:

- builds and stores the generated part of the game tree
- traverses the tree using legal game moves
- evaluates terminal and non-terminal states correctly
- uses a custom heuristic for depth-limited search
- returns the best move for the AI
- tracks metrics required for experiments

---

# 1. Main Design Goals

## 1.1 Requirements this plan addresses

This implementation must satisfy these assignment needs:

- proper data structure for generated game tree storage
- tree generation up to a depth limit
- custom heuristic evaluation function
- Alpha-Beta Pruning search
- support for metrics:
    - nodes generated
    - nodes evaluated
    - move decision time

## 1.2 High-level architecture

The implementation should be split into these responsibilities:

- **Data structures**
    - game state
    - game tree node
    - AI metrics/result objects

- **Rule helpers**
    - legal move generation
    - move application
    - terminal state detection
    - final payout handling

- **Tree helpers**
    - node creation
    - child expansion
    - tree generation to depth

- **Evaluation helpers**
    - terminal evaluation
    - custom heuristic evaluation

- **Search**
    - alpha-beta recursive traversal
    - best move selection wrapper

---

# 2. Step-by-Step Implementation Plan

## Step 1 - Finalize the core state model

### Objective
Make sure one game state structure is used consistently everywhere.

### Tasks
- Define a stable `GameState`
- Ensure it contains all information needed for search:
    - current number
    - player points
    - AI points
    - bank points
    - whose turn it is
- Decide whether terminal status is:
    - stored in state, or
    - computed by helper function

### Recommendation
Prefer computing terminal status with a helper rather than storing it unless every state update guarantees correctness.

### Deliverable
A reliable state object that can be safely passed through the game tree and search.

---

## Step 2 - Create the game tree node structure

### Objective
Represent the generated search tree using a proper data structure.

### Tasks
Create a `GameTreeNode` that stores:

- `state`
- `depth`
- `children`
- optional future-friendly fields such as:
    - `evaluation`
    - `best_move`
    - `is_terminal`

### Child storage
Use a mapping from move to child node, for example:

- move `2` -> child node
- move `3` -> child node

### Why this matters
This satisfies the assignment requirement that the generated tree is stored using classes/objects instead of loose variables.

### Deliverable
A reusable node type for minimax and alpha-beta traversal.

---

## Step 3 - Create helper functions for move generation and rule handling

### Objective
Centralize all rule-related logic so the search algorithm does not duplicate game rules.

### Required helpers

#### 3.1 `get_legal_moves(state)`
Returns all legal divisors from the current state.

Expected outputs:
- `[]`
- `[2]`
- `[3]`
- `[2, 3]`

#### 3.2 `apply_move(state, divisor)`
Returns a new state after:
- dividing the number
- updating scores
- updating bank if needed
- switching turns

#### 3.3 `is_terminal_state(state)`
Checks whether the game is over.

Primary condition:
- current number is `<= 10`

#### 3.4 `apply_final_payout(state)`
If the game is terminal:
- award the bank to the player who made the final move
- clear bank points

#### 3.5 `determine_winner(state)`
Returns:
- AI win
- human win
- tie

### Deliverable
A complete set of pure helper functions used by both tree generation and search.

---

## Step 4 - Add tree expansion logic

### Objective
Generate child nodes dynamically from a node's state.

### Tasks
Implement a helper such as:

- `expand_node(node)`

This helper should:
1. read the node's state
2. compute legal moves
3. create a child state for each legal move
4. create child nodes
5. store them in `node.children`

### Notes
- do not create children for invalid moves
- do not expand terminal nodes
- every created child counts as a generated node for metrics

### Deliverable
A function that transforms one node into its next search layer.

---

## Step 5 - Implement full tree generation to depth limit

### Objective
Generate the game tree up to a chosen search depth.

### Tasks
Implement a recursive or iterative helper such as:

- `build_game_tree(initial_state, max_depth)`

Suggested behavior:
1. create root node
2. if node is terminal or depth limit reached, stop
3. otherwise expand node
4. recursively build children until cutoff

### Important rule
Tree generation must be dynamic and based on the actual rules, not hardcoded states.

### Deliverable
A root node with generated descendants up to the selected depth.

---

## Step 6 - Define evaluation strategy

### Objective
Separate exact terminal evaluation from heuristic evaluation.

### 6.1 Terminal evaluation
Create a helper like:

- `evaluate_terminal_state(state)`

Behavior:
- apply final payout if needed
- compute final score from AI perspective

Suggested convention:
- positive value = favorable for AI
- negative value = favorable for human
- zero = tie

### 6.2 Heuristic evaluation
Create a helper like:

- `evaluate_heuristic(state)`

This is used when:
- depth limit is reached
- the state is not terminal

### Deliverable
Two clearly separated evaluation methods:
- exact evaluation for real end states
- custom heuristic for non-terminal cutoff states

---

## Step 7 - Design the custom heuristic

### Objective
Create a heuristic stronger than simple score difference.

### Minimum starting heuristic
Start with:

- current score difference

### Recommended heuristic factors

#### A. Score difference
Main component:
- `ai_points - player_points`

#### B. Bank value
Higher bank can strongly affect near-end positions.

#### C. Turn advantage
If it is AI's turn, that may deserve a small bonus.

#### D. Mobility
Count how many legal moves are available in the current state.

#### E. Distance to endgame
If the number is closer to `10`, the position may be tactically sharper.

### Example heuristic structure
Not final code, just planning logic:
python heuristic_score = ### Recommendation
Start simple:
1. score difference
2. bank value
3. turn bonus

Then extend only if testing shows weak decisions.

### Deliverable
A documented custom heuristic with explainable weighting choices.

---

## Step 8 - Implement alpha-beta traversal over the game tree

### Objective
Search the tree recursively and prune branches that cannot affect the final decision.

### Core idea
At each node:
- if AI turn -> maximize
- if human turn -> minimize

Track:
- `alpha` = best guaranteed value for maximizer
- `beta` = best guaranteed value for minimizer

Prune when:
- `beta <= alpha`

### Recursive alpha-beta plan

#### Input
The recursive search should receive:
- current node
- remaining depth
- alpha
- beta
- whether this is maximizing or minimizing

#### Base cases
Stop and evaluate when:
- node is terminal
- depth limit is reached
- node has no children / no legal moves

#### Recursive case
- expand children if not already expanded
- recursively evaluate children
- update alpha/beta
- prune when cutoff condition is met

### Deliverable
A recursive alpha-beta function that works on tree nodes, not only raw values.

---

## Step 9 - Add a root-level best move selector

### Objective
Turn the recursive search into an actual AI move decision.

### Tasks
Create a wrapper such as:

- `find_best_move_with_alpha_beta(state, depth)`

Behavior:
1. create root node from current state
2. generate or lazily expand children
3. evaluate each child using alpha-beta
4. track the best move and best score
5. return the chosen divisor and metrics

### Return format
Prefer returning a result object containing:
- chosen move
- score
- nodes generated
- nodes evaluated
- elapsed time

### Deliverable
A clean AI API usable by UI and experiments.

---

## Step 10 - Add metrics tracking

### Objective
Support the required experiments.

### Required counters

#### 10.1 Nodes generated
Increment whenever a new tree node is created.

#### 10.2 Nodes evaluated
Increment whenever a leaf is evaluated by:
- terminal evaluation, or
- heuristic evaluation

#### 10.3 Time per move
Measure total duration of one AI decision.

### Suggested structure
Create an `AIMetrics` or `SearchStats` object.

Possible fields:
- `nodes_generated`
- `nodes_evaluated`
- `pruned_branches`
- `elapsed_ms`

### Deliverable
Metrics attached to each AI move result.

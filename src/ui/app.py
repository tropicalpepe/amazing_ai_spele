import streamlit as st
from src.logic.game_controller import GameController
# --------- page setup ---------
st.set_page_config(page_title="AI Spēle", layout="wide")

# --------- state initialization ---------
if "controller" not in st.session_state:
    # controller holds entire game logic; keep it in session state
    st.session_state.controller = GameController()

controller: GameController = st.session_state.controller

# cache the generated starting numbers so they don't change on every rerun
if "numbers" not in st.session_state:
    st.session_state.numbers = controller.generate_starting_numbers()

# Store selected AI algorithm
if "algorithm" not in st.session_state:
    st.session_state.algorithm = "Alpha-Beta"

# Store selected search depth
if "depth" not in st.session_state:
    st.session_state.depth = 15

# Store the last AI move for the side panel
if "last_ai_move" not in st.session_state:
    st.session_state.last_ai_move = None

# Store AI metrics/statistics from the last move
if "last_ai_metrics" not in st.session_state:
    st.session_state.last_ai_metrics = None

# Store move history shown in the history panel
if "game_history" not in st.session_state:
    st.session_state.game_history = []
# --------- UI ---------

# --------- helper functions ---------
# Reset controller and all UI-related session data
def restart_game():
    st.session_state.controller = GameController()
    st.session_state.numbers = st.session_state.controller.generate_starting_numbers()
    st.session_state.last_ai_move = None
    st.session_state.last_ai_metrics = None
    st.session_state.game_history = []
    st.rerun()

 # --------- start screen ---------
if controller.state is None:
    st.title("Dalīšanas Spēle")
    st.subheader("Jauna spēle")

    left, right = st.columns([2, 1])

    with left:
         # --------- start number selection ---------
        selected = st.selectbox(
            "Izvēlies sākuma skaitli",
            st.session_state.numbers
        )
        # --------- first player selection ---------
        player_first = st.radio(
            "Kurš izdara pirmo gājienu?",
            ["Cilvēks", "AI"],
            horizontal=True
        ) == "Cilvēks"

        # --------- algorithm selection ---------
        algorithm = st.radio(
            "AI algoritms",
            ["Minimax", "Alpha-Beta"],
            index=1,
            horizontal=True
        )

         # --------- depth selection ---------
        depth = st.slider(
            "Meklēšanas dziļums",
            min_value=3,
            max_value=20,
            value=15,
            step=1
        )

        st.session_state.algorithm = algorithm
        st.session_state.depth = depth

        col1, col2 = st.columns(2)

        with col1:
             # --------- start game button ---------
            if st.button("Sākt spēli", use_container_width=True):
                controller.start_game(selected, player_first)
                st.session_state.game_history.append(
                    f"Spēle sākta ar skaitli {selected}. Pirmais iet: {'Cilvēks' if player_first else 'AI'}."
                )
                st.rerun()

        with col2:
             # --------- regenerate numbers button ---------
            if st.button("Ģenerēt jaunus 5 skaitļus", use_container_width=True):
                st.session_state.numbers = controller.generate_starting_numbers()
                st.rerun()

    with right:
        # --------- start screen info panel ---------
        st.info(
            f"""
**Izvēlētais algoritms:** {st.session_state.algorithm}

**Dziļums:** {st.session_state.depth}

**Sākuma skaitļi:**  
{", ".join(str(x) for x in st.session_state.numbers)}
"""
        )
else:
    # --------- game screen ---------
    summary = controller.get_game_summary()

    st.title("Dalīšanas Spēle")
    st.subheader("Spēles stāvoklis")

    # --------- top stats row ---------
    top1, top2, top3, top4 = st.columns(4)
    top1.metric("Pašreizējais skaitlis", summary["current_number"])
    top2.metric("Cilvēka punkti", summary["player_points"])
    top3.metric("AI punkti", summary["ai_points"])
    top4.metric("Banka", summary["bank_points"])

    # --------- game info row ---------
    info1, info2, info3 = st.columns(3)
    with info1:
        st.write("**Algoritms:**", st.session_state.algorithm)
    with info2:
        st.write("**Dziļums:**", st.session_state.depth)
    with info3:
        st.write(
            "**Tagad gājiens:**",
            "Cilvēks" if summary["is_player_turn"] else "AI"
        )

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        # --------- game over screen ---------
        if summary["is_game_over"]:
            st.success("Spēle beigusies")
            st.write(f"**Uzvarētājs:** {summary.get('winner', '---')}")

            if summary["player_points"] > summary["ai_points"]:
                st.balloons()
                
            if st.button("Sākt jaunu spēli", use_container_width=True):
                restart_game()

        else:
            # --------- active turn area ---------
            if summary["is_player_turn"]:
                # --------- human turn screen ---------
                legal = summary["legal_moves"]
                st.write("**Tavas pieejamās darbības:**")

                cols = st.columns(2)
                # Show divide by 2 button only if legal
                if 2 in legal:
                    with cols[0]:
                        if st.button("Dalīt ar 2", use_container_width=True):
                            try:
                                before = summary["current_number"]
                                controller.make_move(2)
                                after = controller.state.current_number
                                st.session_state.game_history.append(
                                    f"Cilvēks: {before} ÷ 2 = {after}"
                                )
                            except (ValueError, RuntimeError) as e:
                                st.error(str(e))
                            st.rerun()
                # Show divide by 3 button only if legal
                if 3 in legal:
                    with cols[1]:
                        if st.button("Dalīt ar 3", use_container_width=True):
                            try:
                                before = summary["current_number"]
                                controller.make_move(3)
                                after = controller.state.current_number
                                st.session_state.game_history.append(
                                    f"Cilvēks: {before} ÷ 3 = {after}"
                                )
                            except (ValueError, RuntimeError) as e:
                                st.error(str(e))
                            st.rerun()

            else:
                # --------- AI turn screen ---------
                st.warning("Dators domā...")

                try:
                    before = summary["current_number"]

                    
                    move, metrics, game_ended = controller.make_ai_move(
                        depth=st.session_state.depth
                    )

                    after = controller.state.current_number
                    st.session_state.last_ai_move = move
                    st.session_state.last_ai_metrics = metrics
                    st.session_state.game_history.append(
                        f"AI: {before} ÷ {move} = {after}"
                    )

                except TypeError:

                    move, metrics, game_ended = controller.make_ai_move()
                    after = controller.state.current_number
                    st.session_state.last_ai_move = move
                    st.session_state.last_ai_metrics = metrics
                    st.session_state.game_history.append(
                        f"AI: {before} ÷ {move} = {after}"
                    )

                except RuntimeError as e:
                    st.error(str(e))

                st.rerun()

        st.divider()

        # --------- bottom action buttons ---------
        # Restart game or clear history
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Restartēt spēli", use_container_width=True):
                restart_game()

        with col_b:
            if st.button("Notīrīt vēsturi", use_container_width=True):
                st.session_state.game_history = []
                st.rerun()

    with right:
        # --------- right side panel ---------
        # Shows AI information and move history
        st.markdown("### AI informācija")

        if st.session_state.last_ai_move is not None:
            st.write(f"**Pēdējais AI gājiens:** {st.session_state.last_ai_move}")

        metrics = st.session_state.last_ai_metrics
        if metrics is not None:
            if hasattr(metrics, "nodes_generated"):
                st.write(f"**Ģenerētie mezgli:** {metrics.nodes_generated}")
            if hasattr(metrics, "nodes_evaluated"):
                st.write(f"**Novērtētie mezgli:** {metrics.nodes_evaluated}")
            if hasattr(metrics, "elapsed_ms"):
                st.write(f"**Laiks:** {metrics.elapsed_ms:.2f} ms")
            if hasattr(metrics, "pruned_branches"):
                st.write(f"**Nogrieztie zari:** {metrics.pruned_branches}")
        
        # --------- move history panel ---------
        # Shows the last 12 moves, newest first
        st.markdown("### Gājienu vēsture")
        if st.session_state.game_history:
            for item in reversed(st.session_state.game_history[-12:]):
                st.write("- ", item)
        else:
            st.write("Vēsture vēl nav.")   
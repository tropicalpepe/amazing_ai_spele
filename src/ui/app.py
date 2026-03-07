import streamlit as st
from src.logic.game_controller import GameController

st.set_page_config(page_title="AI Spēle")

# --------- state initialization ---------
if "controller" not in st.session_state:
    # controller holds entire game logic; keep it in session state
    st.session_state.controller = GameController()

controller: GameController = st.session_state.controller

# cache the generated starting numbers so they don't change on every rerun
if "numbers" not in st.session_state:
    st.session_state.numbers = controller.generate_starting_numbers()

# --------- UI ---------
st.title("Dalīšanas Spēle")

# helper to restart the UI and controller state

def restart_game():
    st.session_state.controller = GameController()
    st.session_state.numbers = st.session_state.controller.generate_starting_numbers()
    st.experimental_rerun()

# main rendering logic
if controller.state is None:
    # game has not started yet
    st.subheader("Izvēlies sākuma skaitli")

    selected = st.selectbox("5 ģenerētie skaitļi:", st.session_state.numbers)
    player_first = st.checkbox("Es eju pirmais")

    if st.button("Sākt spēli"):
        controller.start_game(selected, player_first)
        st.experimental_rerun()

else:
    summary = controller.get_game_summary()
    st.subheader("Spēles stāvoklis")

    st.write("Pašreizējais skaitlis:", summary["current_number"])
    st.write("Cilvēka punkti:", summary["player_points"])
    st.write("AI punkti:", summary["ai_points"])
    st.write("Banka:", summary["bank_points"])

    if summary["is_game_over"]:
        st.success("Spēle beigusies!")
        st.write(f"Uzvarētājs: {summary.get('winner', '---')}")
        if st.button("Restartēt"):
            restart_game()

    else:
        if summary["is_player_turn"]:
            legal = summary["legal_moves"]
            st.write(f"Legalās darbības: {legal}")

            cols = st.columns(len(legal))
            for i, move in enumerate(legal):
                with cols[i]:
                    if st.button(f"Dalīt ar {move}", key=f"move{move}"):
                        try:
                            controller.make_move(move)
                        except (ValueError, RuntimeError) as e:
                            st.error(str(e))
                        st.experimental_rerun()
        else:
            # AI's turn - perform the move automatically once
            try:
                move, metrics, game_ended = controller.make_ai_move()
                st.write(f"AI izvēlējās: {move}")
                st.write(f"(novērtēts {metrics.nodes_evaluated} mezgli, {metrics.elapsed_ms:.0f}ms)")
            except RuntimeError as e:
                # should not happen unless something is wrong
                st.error(str(e))
            st.experimental_rerun()

    if st.button("Restartēt"):
        st.session_state.current = None
        st.session_state.numbers = generate_start_numbers()
        st.rerun()

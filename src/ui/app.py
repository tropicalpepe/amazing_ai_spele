import streamlit as st
import random

st.set_page_config(page_title="AI Spēle")

# --------- Fake sākuma skaitļi (kamēr nav loģikas) ---------
def generate_start_numbers():
    nums = []
    while len(nums) < 5:
        n = random.randint(10000, 20000)
        if n % 6 == 0:
            nums.append(n)
    return nums

if "numbers" not in st.session_state:
    st.session_state.numbers = generate_start_numbers()

if "current" not in st.session_state:
    st.session_state.current = None

if "player_points" not in st.session_state:
    st.session_state.player_points = 0

if "ai_points" not in st.session_state:
    st.session_state.ai_points = 0

if "bank" not in st.session_state:
    st.session_state.bank = 0

# --------- UI ---------
st.title("Dalīšanas Spēle")

if st.session_state.current is None:

    st.subheader("Izvēlies sākuma skaitli")

    selected = st.selectbox("5 ģenerētie skaitļi:", st.session_state.numbers)

    if st.button("Sākt spēli"):
        st.session_state.current = selected
        st.session_state.player_points = 0
        st.session_state.ai_points = 0
        st.session_state.bank = 0
        st.rerun()

else:
    st.subheader("Spēles stāvoklis")

    st.write("Pašreizējais skaitlis:", st.session_state.current)
    st.write("Cilvēka punkti:", st.session_state.player_points)
    st.write("AI punkti:", st.session_state.ai_points)
    st.write("Banka:", st.session_state.bank)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Dalīt ar 2"):
            if st.session_state.current % 2 == 0:
                st.session_state.current //= 2
            else:
                st.error("Nevar dalīt ar 2!")

    with col2:
        if st.button("Dalīt ar 3"):
            if st.session_state.current % 3 == 0:
                st.session_state.current //= 3
            else:
                st.error("Nevar dalīt ar 3!")

    if st.button("Restartēt"):
        st.session_state.current = None
        st.session_state.numbers = generate_start_numbers()
        st.rerun()
import streamlit as st

from frontend.landing import show_landing
from frontend.portfolio_init import show_portfolio_init
from frontend.leaderboard import show_leaderboard
from frontend.sidebar import show_sidebar

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Capital Street | Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Session state initialization
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "players" not in st.session_state:
    st.session_state.players = {}

if "market_sim_active" not in st.session_state:
    st.session_state.market_sim_active = False

if "sim_phase" not in st.session_state:
    st.session_state.sim_phase = "selection"

# Persistent Sidebar
show_sidebar()

# -----------------------------
# Simple router
# -----------------------------
if st.session_state.page == "landing":
    show_landing()

elif st.session_state.page == "portfolio_init":
    show_portfolio_init()

elif st.session_state.page == "leaderboard":
    show_leaderboard()

else:
    # Safety fallback
    st.session_state.page = "landing"
    show_landing()

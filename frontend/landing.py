import streamlit as st
from backend.personas import PERSONAS
from .styles import load_styles
import re
import base64

def show_landing():
    # Inject Styles
    st.markdown(load_styles(), unsafe_allow_html=True)

    # Header Section
    st.markdown(
        """
        <div class="landing-header">
            <div class="glow-header" style="justify-content: center; font-size: 2.5rem;">
                CAPITAL STREET TERMINAL
            </div>
            <p class="landing-subtitle">
                ACCESS SYSTEM: ESTABLISH INVESTOR IDENTITY TO BEGIN SELECTION
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Init session state
    if "selected_personas" not in st.session_state:
        st.session_state.selected_personas = set()

    cols = st.columns(4)

    for i, persona in enumerate(PERSONAS):
        with cols[i]:
            # Extract persona info
            is_selected = persona['id'] in st.session_state.selected_personas
            
            # Persona Card
            st.markdown(
                f"""
                <div class="persona-card" style="border-width: {'3px' if is_selected else '1px'}; opacity: {1 if is_selected else 0.8}">
                    <div class="persona-img-box">
                        <img src="data:image/png;base64,{get_base64_of_bin_file(persona['image'])}">
                    </div>
                    <div class="persona-info">
                        <div class="persona-name-text">{persona['display_name'].split('“')[0]}</div>
                        <div class="persona-details-text">
                            {persona['one_liner'].split('·')[0]}<br>
                            <span style="color: #00CCFF; font-weight: 600;">{persona['one_liner'].split('·')[1]}</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

            # Select Button
            btn_label = "PROFILE ACTIVE" if is_selected else "SELECT PROFILE"
            if st.button(btn_label, key=f"btn_{persona['id']}", use_container_width=True):
                toggle_selection(persona['id'])

            # Name Input
            st.text_input(
                "IDENTITY VERIFICATION",
                key=f"player_name_{persona['id']}",
                placeholder="PROFILING NAME...",
                disabled=not is_selected,
                label_visibility="collapsed"
            )

    # Bottom Action
    st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)
    
    can_continue = True
    for pid in st.session_state.selected_personas:
        if not st.session_state.get(f"player_name_{pid}", "").strip():
            can_continue = False
            break

    _, mid_col, _ = st.columns([1, 1, 1])
    with mid_col:
        st.markdown('<div class="init-button-box">', unsafe_allow_html=True)
        if st.button(
            "INITIALIZE TERMINAL SESSION",
            disabled=(len(st.session_state.selected_personas) == 0 or not can_continue),
            use_container_width=True
        ):
            from backend.portfolio_engine import recommended_portfolio
            from backend.investor_profiles import INVESTOR_PROFILES
            
            players = {}
            for pid in st.session_state.selected_personas:
                persona = next(p for p in PERSONAS if p["id"] == pid)
                player_name = st.session_state[f"player_name_{pid}"].strip()
                
                # Fetch initial recommendation
                profile = INVESTOR_PROFILES[pid]
                rec = recommended_portfolio(profile)
                
                players[pid] = {
                    "player_name": player_name,
                    "persona_id": pid,
                    "persona": persona,
                    "capital": 10_00_000,
                    "current_weights": rec["weights"],
                    "metrics": rec["results"],
                    "rebalanced": False,
                    "frontier": rec["frontier"],
                    "mu": rec["mu"]
                }
            st.session_state.players = players
            st.session_state.page = "portfolio_init"
            # Reset Simulation State for new session
            st.session_state.current_round = 1
            st.session_state.market_sim_active = False
            st.session_state.sim_phase = "selection"
            if "round_history" in st.session_state: del st.session_state.round_history
            if "current_wealth" in st.session_state: del st.session_state.current_wealth
            if "psych_logs" in st.session_state: del st.session_state.psych_logs
            if "results_saved" in st.session_state: del st.session_state.results_saved
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def toggle_selection(pid):
    if pid in st.session_state.selected_personas:
        st.session_state.selected_personas.remove(pid)
    else:
        st.session_state.selected_personas.add(pid)
    st.rerun()


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

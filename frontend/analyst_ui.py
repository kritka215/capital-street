import streamlit as st
import time
from backend.analyst_engine import FinancialAnalyst, get_quick_questions

# Minimalist SVG Icons
ICONS = {
    "chart": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M18 9l-6 6-4-4-4 4"/></svg>',
    "info": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>',
    "brain": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.5 2A1.5 1.5 0 0 1 11 3.5v1A1.5 1.5 0 0 1 9.5 6H9A1.5 1.5 0 0 1 7.5 4.5v-1A1.5 1.5 0 0 1 9 2h.5z"/><path d="M14.5 2A1.5 1.5 0 0 1 16 3.5v1a1.5 1.5 0 0 1-1.5 1.5H14a1.5 1.5 0 0 1-1.5-1.5v-1A1.5 1.5 0 0 1 14 2h.5z"/><path d="M10 14h.01"/><path d="M14 14h.01"/><path d="M12 18h.01"/><path d="M12 15h.01"/><path d="M12 21h.01"/></svg>',
    "history": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="10"/></svg>'
}

def show_analyst_chat():
    if "analyst_open" not in st.session_state:
        st.session_state.analyst_open = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "bot", "content": "CS-ANALYST ONLINE. Initializing state-aware diagnostic tools..."}]

    # FAB (Institutional Squared Design)
    fab_html = """
    <div class="analyst-fab">
        <span style="font-family: inherit; font-weight: 800; letter-spacing: 1px;">⌬</span>
    </div>
    """
    st.markdown(fab_html, unsafe_allow_html=True)
    
    # Internal trigger with better positioning (hidden native button)
    _, _, col_trigger = st.columns([0.8, 0.1, 0.1])
    with col_trigger:
        if st.button("⌬", key="fab_internal_trigger", help="Toggle Terminal Analyst"):
            st.session_state.analyst_open = not st.session_state.analyst_open
            st.rerun()

    if st.session_state.analyst_open:
        # Analyst Sidebar Container
        st.markdown('<div class="analyst-sidebar">', unsafe_allow_html=True)
        
        # Header Section
        st.markdown('<div class="chat-header">', unsafe_allow_html=True)
        st.markdown('<div class="chat-title">NODE-01 // ANALYST TERMINAL</div>', unsafe_allow_html=True)
        if st.button("X", key="close_chat", help="Terminate Session"):
            st.session_state.analyst_open = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Message Stream
        st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            if msg["role"] == "bot":
                st.markdown(f'<div class="message-bot">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-user">{msg["content"]}</div>', unsafe_allow_html=True)
        
        # Optional Thinking Animation (only if last message was user)
        if st.session_state.chat_history[-1]["role"] == "user":
            st.markdown('<div class="message-bot">ANALYZING DATA STREAM<span class="terminal-cursor"></span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Bottom Dock (Quick Actions + Input)
        st.markdown('<div class="bottom-dock">', unsafe_allow_html=True)
        
        active_event = st.session_state.get("selected_event", None)
        quick_qs = get_quick_questions(active_event)
        
        st.markdown('<div class="quick-actions-grid">', unsafe_allow_html=True)
        for q in quick_qs:
            icon_key = "brain" if "strategy" in q.lower() or "advice" in q.lower() else \
                       "history" if "history" in q.lower() or "recovery" in q.lower() else \
                       "chart" if "effect" in q.lower() or "portfolio" in q.lower() or "cvar" in q.lower() else "info"
            
            # Using st.markdown + st.button hack for ghost appearance with icons
            st.markdown(f'<div style="margin-bottom: 5px;">{ICONS[icon_key]} <span style="font-size:0.7rem; color:#00E5FF; text-transform:uppercase; letter-spacing:1px; font-family:inherit;">{q}</span></div>', unsafe_allow_html=True)
            if st.button(f"EXECUTE: {q}", key=f"quick_{q}", help=f"Request data on {q}"):
                process_query(q)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Analysis Input
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        user_input = st.text_input("EXECUTE QUERY", placeholder="TYPE COMMAND...", key="analyst_input", label_visibility="collapsed")
        if user_input:
            process_query(user_input)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Terminal Disclaimer
        st.markdown('<div class="chat-disclaimer">SECURE CONNECTION // EDUCATIONAL SIMULATION ONLY // NON-ADVISORY NODE</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # End Sidebar
        st.markdown('</div>', unsafe_allow_html=True) # End Container

def process_query(query):
    # Log user message
    st.session_state.chat_history.append({"role": "user", "content": query})
    
    # State-Aware Params
    active_event = st.session_state.get("selected_event", None)
    round_num = st.session_state.get("current_round", 1)
    players = st.session_state.get("players", {})
    first_pid = list(players.keys())[0] if players else None
    persona_data = players.get(first_pid, None) if first_pid else None
    wealth = st.session_state.get("current_wealth", {}).get(first_pid, 1000000)
    
    brain = FinancialAnalyst(
        current_event=active_event,
        persona=persona_data,
        round_num=round_num,
        total_value=wealth
    )
    
    # Immediate response for terminal feel
    response = brain.get_context_advice(query)
    st.session_state.chat_history.append({"role": "bot", "content": response})

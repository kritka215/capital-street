import streamlit as st
from .styles import load_styles
from backend.leaderboard_service import load_leaderboard

def show_leaderboard():
    st.markdown(load_styles(), unsafe_allow_html=True)
    
    # Header logic (Minimalist)
    st.markdown('<div class="glow-header">GLOBAL LEADERBOARD | ♜ WALL OF FAME</div>', unsafe_allow_html=True)
    
    data = load_leaderboard()
    
    if not data:
        st.markdown("""
        <div style="text-align: center; padding: 100px; opacity: 0.3;">
            <div style="font-size: 3rem;">⌬</div>
            <p style="font-size: 0.9rem; letter-spacing: 2px;">NO HISTORICAL DATA DETECTED</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)
        
        for idx, entry in enumerate(data):
            rank = idx + 1
            wealth = entry.get("wealth", 0)
            
            st.markdown(f"""
            <div class="leader-row">
                <div style="display: flex; align-items: center;">
                    <div class="rank-badge">{rank}</div>
                    <div>
                        <div style="font-weight: 800; color: white; font-size: 1.1rem; letter-spacing: 1px;">{entry['name'].upper()}</div>
                        <div style="font-size: 0.7rem; color: var(--neon-cyan); text-transform: uppercase;">STRATEGY: {entry['strategy']}</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.2rem; font-weight: 900; color: #FFF;">₹{wealth:,.0f}</div>
                    <div style="font-size: 0.65rem; color: #AAA;">PEAK WEALTH</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    if st.button("RETURN TO DASHBOARD", use_container_width=True):
        st.session_state.page = "landing"
        st.rerun()

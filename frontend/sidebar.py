import streamlit as st

def show_sidebar():
    if "sidebar_expanded" not in st.session_state:
        st.session_state.sidebar_expanded = True
    
    # Inject dynamic width for sidebar
    sidebar_width = "260px" if st.session_state.sidebar_expanded else "80px"
    st.markdown(f"""
        <style>
        [data-testid="stSidebar"] {{
            width: {sidebar_width} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
            padding: 1rem 0.5rem !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        # Toggle button
        toggle_label = "CLOSE" if st.session_state.sidebar_expanded else "OPEN"
        if st.button(toggle_label, key="sidebar_toggle"):
            st.session_state.sidebar_expanded = not st.session_state.sidebar_expanded
            st.rerun()

        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        
        # Professional Navigation Matrix
        nav_items = [
            {"label": "DASHBOARD", "icon": "⌘", "page": "landing", "key": "nav_home"},
            {"label": "STRATEGY TERMINAL", "icon": "◈", "page": "portfolio_init", "key": "nav_analysis"},
            {"label": "AGILE REBALANCE", "icon": "⌬", "page": "portfolio_init", "key": "nav_rebal"},
            {"label": "MARKET STRESS TEST", "icon": "⊞", "page": "market_events", "key": "nav_events"},
            {"label": "LEADERBOARD", "icon": "♜", "page": "leaderboard", "key": "nav_leader"},
        ]
        
        for item in nav_items:
            # Combined minimalist representation
            btn_label = f"{item['icon']} {item['label']}" if st.session_state.sidebar_expanded else item['icon']
            
            # Identify active state
            is_active = False
            if item['label'] == "MARKET STRESS TEST" and st.session_state.get("market_sim_active"):
                is_active = True
            elif item['page'] == st.session_state.page and not st.session_state.get("market_sim_active"):
                is_active = True

            # Use st.markdown to inject class for active state if needed
            # Streamlit buttons don't easily accept classes, so we rely on session state logic in the component
            # to render a slightly different style or we use the CSS classes we added.
            
            if st.button(btn_label, key=item['key'], help=item['label']):
                if item['label'] == "MARKET STRESS TEST":
                    st.session_state.page = "portfolio_init"
                    st.session_state.market_sim_active = True
                    st.session_state.sim_phase = "selection"
                else:
                    st.session_state.page = item['page']
                    st.session_state.market_sim_active = False
                
                if item['page'] in ["portfolio_init"]:
                    if not st.session_state.players:
                        st.info("⚠️ Initialize a portfolio first.")
                        st.session_state.page = "landing"
                st.rerun()
            
            if is_active:
                st.markdown(f"""
                    <style>
                    div.stButton > button[key="{item['key']}"] {{
                        background: #FFFFFF !important;
                        color: #000000 !important;
                        font-weight: 900 !important;
                    }}
                    </style>
                """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top: auto; padding-bottom: 20px;"></div>', unsafe_allow_html=True)
        security_label = "SECURE" if st.session_state.sidebar_expanded else "S"
        st.button(security_label, key="nav_settings")

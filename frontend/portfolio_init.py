import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
import base64
import os

from backend.portfolio_engine import evaluate_portfolio, ASSET_NAMES
from backend.leaderboard_service import save_to_leaderboard
from .styles import load_styles

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None

def get_event_image(event):
    # Map event IDs to their corresponding local filenames
    # Filenames are exactly as listed in the assets folder
    image_map = {
        "gfc": "GFC .png",
        "rate_shock": "Interest rate shock.png", 
        "inflation_shock": "Inflation shock.png",
        "liquidity_shock": "Domestic Liquidity shock.png",
        "credit_crisis": "Shadow Banking crisis.png",
        "currency_flight": "Currency Flight Crisis.png",
        "bubble_burst": "Asset Bubble Burst.png",
        "taper_tantrum_2": "New Taper Tantrum.png",
        "commodity_shock": "Oil and Commodity shock.png",
        "pandemic": "black swan pandemic.png",
        "war_shock": "Geopolitical war shock.png",
        "cyber_attack": "Cyber Attack.png",
        "natural_disaster": "Natural Disaster.png",
        "political_instability": "Political Instability.png"
    }

    if event['id'] in image_map:
        local_filename = image_map[event['id']]
        local_path = os.path.join("assets", local_filename)
        if os.path.exists(local_path):
             img_b64 = get_base64_image(local_path)
             if img_b64:
                 return f"data:image/png;base64,{img_b64}"
    
    # Fallback/Default if local file missing
    if event['id'] in ['commodity_shock', 'pandemic', 'war_shock', 'cyber_attack', 'natural_disaster', 'political_instability']:
         return "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=400&auto=format&fit=crop" 
    
    return "https://images.unsplash.com/photo-1611974714658-94578160918a?q=80&w=400&auto=format&fit=crop"

def show_portfolio_init():
    st.markdown(load_styles(), unsafe_allow_html=True)
    
    players = st.session_state.players
    player_ids = list(players.keys())
    
    if "current_round" not in st.session_state: st.session_state.current_round = 1
    if "round_history" not in st.session_state: st.session_state.round_history = {pid: [] for pid in player_ids}
    if "current_wealth" not in st.session_state: st.session_state.current_wealth = {pid: 1000000 for pid in player_ids}
    if "psych_logs" not in st.session_state: st.session_state.psych_logs = {pid: [] for pid in player_ids}
    if "market_sim_active" not in st.session_state: st.session_state.market_sim_active = False
    if "sim_phase" not in st.session_state: st.session_state.sim_phase = "selection"
    
    BASE_INITIAL_CAPITAL = 1000000

    st.markdown(f'<div class="glow-header" style="font-size: 1.2rem; margin-bottom: 30px;">STRATEGY TERMINAL | ROUND {min(3, st.session_state.current_round)} OF 3</div>', unsafe_allow_html=True)

    ASSET_COLORS = {"Equity": "#003399", "Debt": "#00CCFF", "Gold": "#FFD700", "Silver": "#C0C0C0", "Oil": "#444444", "Cash": "#001A33"}

    # --- FINAL P&L SUMMARY & PSYCHOLOGY ---
    if st.session_state.current_round > 3:
        if "results_saved" not in st.session_state:
            for pid in player_ids: save_to_leaderboard(players[pid]['player_name'], st.session_state.current_wealth[pid], players[pid]['persona']['id'])
            st.session_state.results_saved = True

        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
        st.markdown('<div class="glow-header" style="justify-content: center; font-size: 2.2rem; margin-bottom: 0;">FINANCIAL CHAMPIONSHIP SUMMARY</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: var(--neon-cyan); letter-spacing: 4px; font-size: 0.8rem; margin-bottom: 40px;">TOTAL DEPOT PERFORMANCE AUDIT</div>', unsafe_allow_html=True)
        
        st.markdown('<table class="statement-table"><tr><th>PERSONA</th><th>ROUND 1 P&L</th><th>ROUND 2 P&L</th><th>ROUND 3 P&L</th><th>FINAL WEALTH</th><th>TOTAL %</th></tr>', unsafe_allow_html=True)
        for pid in player_ids:
            p = players[pid]; logs = st.session_state.round_history[pid]; fw = st.session_state.current_wealth[pid]; tp = ((fw / BASE_INITIAL_CAPITAL) - 1) * 100
            p_cells = "".join([f'<td style="color:{"#00FF64" if l>=0 else "#FF0032"};">₹{l:,.0f}</td>' for l in logs[:3]] + ['<td>-</td>' for _ in range(3-len(logs))])
            st.markdown(f'<tr class="statement-row"><td>{p["player_name"].upper()}</td>{p_cells}<td>₹{fw:,.0f}</td><td style="color:{"#00FF64" if tp>=0 else "#FF0032"};">{tp:+.1f}%</td></tr>', unsafe_allow_html=True)
        st.markdown('</table>', unsafe_allow_html=True)

        # PSYCHOLOGY SECTION
        st.markdown('<div class="glow-header" style="margin-top: 60px; font-size: 1.5rem;">INVESTOR PSYCHOLOGY ANALYSIS</div>', unsafe_allow_html=True)
        psych_cols = st.columns(len(player_ids))
        for i, pid in enumerate(player_ids):
            with psych_cols[i]:
                p_logs = st.session_state.psych_logs[pid]
                badges = []
                reactive_count = sum(1 for l in p_logs if l["type"] == "reactive")
                hunter_count = sum(1 for l in p_logs if l["type"] == "hunter")
                balanced_count = sum(1 for l in p_logs if l["type"] == "balanced")
                
                if reactive_count > 0: badges.append('<span class="psych-badge badge-reactive">REACTIVE</span>')
                if hunter_count > 1: badges.append('<span class="psych-badge badge-hunter">VALUE HUNTER</span>')
                if balanced_count > 1: badges.append('<span class="psych-badge badge-balanced">BALANCED STRATEGIST</span>')
                if not badges: badges.append('<span class="psych-badge" style="border:1px solid #666; color:#666;">STEADY OBSERVER</span>')

                stability = 100 - (reactive_count * 20) + (balanced_count * 5)
                stability = max(50, min(98, stability))

                txt = "You successfully avoided Herd Mentality" if reactive_count == 0 else f"You displayed Loss Aversion in {reactive_count} round(s)"
                if hunter_count > 0: txt += " and spotted undervalued opportunities."

                st.markdown(f"""
                <div class="psych-card">
                    <div style="font-weight: 800; color: white; margin-bottom: 15px;">{players[pid]['player_name'].upper()}</div>
                    <div>{' '.join(badges)}</div>
                    <p style="font-size: 0.82rem; color: #AAA; line-height: 1.4;">{txt}</p>
                    <div class="psych-metric-box">
                        <div class="psych-metric-label">EMOTIONAL STABILITY</div>
                        <div class="psych-metric-val">{stability}%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div style="margin-top: 60px; display: flex; justify-content: center;">', unsafe_allow_html=True)
        if st.button("EXIT SIMULATION & RESET TERMINAL", key="final_exit_btn"): st.session_state.clear(); st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True); return

    if not st.session_state.market_sim_active:
        st.markdown('<div class="terminal-grid">', unsafe_allow_html=True)
        grid_cols = st.columns(4)
        for i in range(4):
            with grid_cols[i]:
                if i < len(player_ids):
                    pid = player_ids[i]; player = players[pid]; locked = player.get("locked", False)
                    st.markdown('<div class="terminal-column">', unsafe_allow_html=True)
                    st.markdown(f'<div class="column-header"><div style="font-size: 1.1rem; font-weight: 800; color: #FFF;">{player["player_name"].upper()}</div><div style="font-size: 0.65rem; color: var(--neon-cyan); letter-spacing: 2px;">{player["persona"]["id"].upper()} NODE</div></div>', unsafe_allow_html=True)
                    st.markdown('<div class="slot-title">I. STRATEGY PROFILE</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="profile-box"><div style="font-size: 0.82rem; color: #AAA; line-height: 1.5;">{player.get("logic", "Standard market allocation.")}</div></div>', unsafe_allow_html=True)
                    st.markdown('<div class="slot-title">II. TARGET ALLOCATION</div>', unsafe_allow_html=True)
                    cw = []
                    for a in ASSET_NAMES:
                        v = st.slider(a, 0, 100, int(player["current_weights"][ASSET_NAMES.index(a)]*100), key=f"i_sl_{pid}_{a}", disabled=locked); cw.append(v)
                    sum_cw = sum(cw) if sum(cw) > 0 else 1; nw = [v/sum_cw for v in cw]; fig = go.Figure(data=[go.Pie(labels=ASSET_NAMES, values=nw, hole=.75, marker=dict(colors=[ASSET_COLORS[a] for a in ASSET_NAMES]), textinfo='none')])
                    fig.update_layout(margin=dict(t=5, b=5, l=5, r=5), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=180); st.plotly_chart(fig, key=f"i_p_{pid}", use_container_width=True, config={'displayModeBar': False})
                    if st.button("LOCKED / READY" if locked else "FINALIZE ALLOCATION", key=f"i_l_{pid}"):
                        if not locked: st.session_state.players[pid]["current_weights"] = np.array(nw); st.session_state.players[pid]["metrics"] = evaluate_portfolio(np.array(nw), player["mu"]); st.session_state.players[pid]["locked"] = True; st.rerun()
                    st.markdown(f'<div class="mini-metric-row"><div class="mini-metric"><div class="mini-label">NET WEALTH</div><div class="mini-val">₹{st.session_state.current_wealth[pid]:,.0f}</div></div><div class="mini-metric"><div class="mini-label">EXP RET</div><div class="mini-val">{player["metrics"]["expected_return"]*100:.1f}%</div></div></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button(f"READY: PROCEED TO ROUND {st.session_state.current_round} SIMULATION", key="p_sim", use_container_width=True): st.session_state.market_sim_active = True; st.session_state.sim_phase = "selection"; st.rerun()
    else:
        from backend.market_events import MARKET_EVENTS
        t_items = ["NIFTY 50: 22,120.45", "SENSEX: 72,852.17", "RBI MPC: 6.5%", "Forex: $616Bn", "Brent: $84"]
        th = "".join([f'<span class="ticker-item">{t}</span>' for t in t_items])
        st.markdown(f'<div class="ticker-container"><div class="ticker-content">{th} {th}</div></div>', unsafe_allow_html=True)
        if st.session_state.sim_phase == "selection":
            st.markdown(f'<div class="glow-header" style="margin-top: 20px; font-size: 1.5rem; letter-spacing: 5px;">TACTICAL TERMINAL | PHASE: STRESS TEST</div>', unsafe_allow_html=True)
            
            # SECTION 1: SYSTEMIC SHOCKS
            st.markdown("<div style='margin: 30px 0 15px 0; font-family: Roboto Mono; font-weight: 800; color: #00CCFF; letter-spacing: 2px;'>SYSTEMIC SHOCKS [INSTITUTIONAL GRADE]</div>", unsafe_allow_html=True)
            
            systemic_ids = ['gfc', 'rate_shock', 'inflation_shock', 'liquidity_shock', 'credit_crisis', 'currency_flight', 'bubble_burst', 'taper_tantrum_2']
            systemic_events = [e for e in MARKET_EVENTS if e['id'] in systemic_ids]
            
            # Compact 4-column grid
            for i in range(0, len(systemic_events), 4):
                cols = st.columns(4)
                for j in range(4):
                    if i + j < len(systemic_events):
                        e = systemic_events[i + j]
                        with cols[j]:
                            st.markdown(f'''
                                <div class="event-card-tactical-blue">
                                    <div class="tactical-img-container">
                                        <img src="{get_event_image(e)}" alt="{e['title']}">
                                        <div class="tactical-title-overlay">{e["title"]}</div>
                                    </div>
                                </div>
                            ''', unsafe_allow_html=True)
                            if st.button("SELECT", key=f"sel_{e['id']}", use_container_width=True):
                                st.session_state.selected_event = e
                                st.session_state.sim_phase = "live"
                                st.session_state.sim_start_time = time.time()
                                for p in st.session_state.players:
                                    st.session_state.players[p]["sim_locked"] = False
                                    st.session_state.players[p]["start_sim_weights"] = st.session_state.players[p]["current_weights"].copy()
                                st.rerun()
                            st.markdown(f"""
                                <style>
                                div.stButton > button[key="sel_{e['id']}"] {{
                                    background: transparent !important;
                                    color: #00CCFF !important;
                                    border: 1px solid #00CCFF !important;
                                    border-radius: 2px !important;
                                    font-size: 0.65rem !important;
                                    padding: 4px !important;
                                    min-height: 25px !important;
                                    margin-top: -10px !important;
                                }}
                                </style>
                            """, unsafe_allow_html=True)
            
            st.markdown('<div class="muted-divider"></div>', unsafe_allow_html=True)

            # SECTION 2: MOST DANGEROUS EVENTS
            st.markdown("<div style='margin: 15px 0 15px 0; font-family: Roboto Mono; font-weight: 800; color: #FF3131; letter-spacing: 2px;'>MOST DANGEROUS EVENTS [CRITICAL ALERT]</div>", unsafe_allow_html=True)
            
            danger_ids = ['commodity_shock', 'pandemic', 'war_shock', 'cyber_attack', 'natural_disaster', 'political_instability']
            danger_events = [e for e in MARKET_EVENTS if e['id'] in danger_ids]
            
            # Compact 4-column grid for consistency
            for i in range(0, len(danger_events), 4):
                cols = st.columns(4)
                for j in range(4):
                    if i + j < len(danger_events):
                        e = danger_events[i + j]
                        with cols[j]:
                            st.markdown(f'''
                                <div class="event-card-tactical-red">
                                    <div class="tactical-img-container">
                                        <img src="{get_event_image(e)}" alt="{e['title']}">
                                        <div class="tactical-title-overlay">{e["title"]}</div>
                                    </div>
                                </div>
                            ''', unsafe_allow_html=True)
                            if st.button("SELECT", key=f"sel_{e['id']}", use_container_width=True):
                                st.session_state.selected_event = e
                                st.session_state.sim_phase = "live"
                                st.session_state.sim_start_time = time.time()
                                for p in st.session_state.players:
                                    st.session_state.players[p]["sim_locked"] = False
                                    st.session_state.players[p]["start_sim_weights"] = st.session_state.players[p]["current_weights"].copy()
                                st.rerun()
                            st.markdown(f"""
                                <style>
                                div.stButton > button[key="sel_{e['id']}"] {{
                                    background: transparent !important;
                                    color: #FF3131 !important;
                                    border: 1px solid #FF3131 !important;
                                    border-radius: 2px !important;
                                    font-size: 0.65rem !important;
                                    padding: 4px !important;
                                    min-height: 25px !important;
                                    margin-top: -10px !important;
                                }}
                                </style>
                            """, unsafe_allow_html=True)
            
            # Back Button at Bottom as requested
            st.markdown('<div style="margin-top: 40px; text-align: center;">', unsafe_allow_html=True)
            if st.button("← RETURN TO STRATEGY TERMINAL", key="back_to_analysis_bot"):
                st.session_state.market_sim_active = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        elif st.session_state.sim_phase in ["live", "results", "recovery"]:
            e = st.session_state.selected_event; l_col, r_col = st.columns([3, 1])
            with l_col:
                st.markdown(f'<div class="glow-header">{st.session_state.sim_phase.upper()} | ROUND {st.session_state.current_round}</div>', unsafe_allow_html=True)
                sim_cols = st.columns(4)
                for i in range(4):
                    with sim_cols[i]:
                        if i < len(player_ids):
                            pid = player_ids[i]; player = players[pid]; sl = player.get("sim_locked", False); cw = st.session_state.current_wealth[pid]
                            st.markdown('<div class="terminal-column">', unsafe_allow_html=True)
                            st.markdown(f'<div class="column-header" style="height: 60px; margin-bottom: 20px;"><div style="font-size: 0.9rem; font-weight: 800; color: #FFF;">{player["player_name"].upper()}</div></div>', unsafe_allow_html=True)
                            if st.session_state.sim_phase == "live":
                                rw = []
                                for a in ASSET_NAMES: v = st.slider(a, 0, 100, int(player["current_weights"][ASSET_NAMES.index(a)]*100), key=f"s_{pid}_{a}", disabled=sl); rw.append(v)
                                s_sum = sum(rw) if sum(rw) > 0 else 1; nr = [v/s_sum for v in rw]; fig = go.Figure(data=[go.Pie(labels=ASSET_NAMES, values=nr, hole=.75, marker=dict(colors=[ASSET_COLORS[a] for a in ASSET_NAMES]), textinfo='none')])
                                fig.update_layout(margin=dict(t=5, b=5, l=5, r=5), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=160); st.plotly_chart(fig, key=f"l_{pid}", use_container_width=True, config={'displayModeBar': False})
                                if st.button("LOCKED" if sl else "FINALISE", key=f"lck_{pid}"):
                                    if not sl: st.session_state.players[pid]["current_weights"] = np.array(nr); st.session_state.players[pid]["sim_locked"] = True; st.rerun()
                            if st.session_state.sim_phase in ["results", "recovery"]:
                                imp = {k: (1 + e["impact"][k]) * (1 + e["stabilization"].get(k, 0)) - 1 for k in e["impact"]} if st.session_state.sim_phase == "recovery" else e["impact"]
                                pv = [player["current_weights"][idx] * cw * (1 + imp.get(a, 0)) for idx, a in enumerate(ASSET_NAMES)]; tp = sum(pv); pl = tp - cw
                                st.markdown(f'<div class="post-event-label">{"RECOVERY" if st.session_state.sim_phase == "recovery" else "SHOCK"} ALLOCATION</div>', unsafe_allow_html=True)
                                fig = go.Figure(data=[go.Pie(labels=ASSET_NAMES, values=pv, hole=.75, marker=dict(colors=[ASSET_COLORS[a] for a in ASSET_NAMES]), textinfo='none')])
                                fig.update_layout(margin=dict(t=5, b=5, l=5, r=5), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=160); st.plotly_chart(fig, key=f"p_{pid}", use_container_width=True, config={'displayModeBar': False})
                                st.markdown(f'<div class="value-box-main"><div class="val-label">NEW WEALTH</div><div class="val-amount">₹{tp:,.0f}</div><div style="font-size:0.7rem; color:{"#00FF64" if pl>=0 else "#FF0032"}; font-weight:800; margin-top:5px;">₹{pl:,.0f} P&L</div></div>', unsafe_allow_html=True)
                                if st.session_state.sim_phase == "recovery" and len(st.session_state.round_history[pid]) < st.session_state.current_round:
                                    # LOG BEHAVIOR
                                    orig_w = player["start_sim_weights"]; final_w = player["current_weights"]
                                    for a_idx, asset in enumerate(ASSET_NAMES):
                                        impact_val = e["impact"].get(asset, 0)
                                        if impact_val <= -0.15: # Asset is crashing
                                            if final_w[a_idx] < orig_w[a_idx] - 0.20: st.session_state.psych_logs[pid].append({"type": "reactive", "round": st.session_state.current_round})
                                            elif final_w[a_idx] > orig_w[a_idx] + 0.05: st.session_state.psych_logs[pid].append({"type": "hunter", "round": st.session_state.current_round})
                                    if sum(1 for w in final_w if w >= 0.10) >= 4: st.session_state.psych_logs[pid].append({"type": "balanced", "round": st.session_state.current_round})
                                    st.session_state.round_history[pid].append(pl); st.session_state.current_wealth[pid] = tp; st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)
            with r_col:
                st.markdown('<div class="intel-panel">', unsafe_allow_html=True)
                st.markdown(f'<div class="slot-title" style="color:var(--neon-cyan);">EVENT INTEL</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:1.1rem; font-weight:800; color:white; margin:15px 0;">{e["title"]}</div>', unsafe_allow_html=True)
                txt = e["description"] if st.session_state.sim_phase != "recovery" else e["recovery"]
                st.markdown(f'<div style="font-size:14px; color:#BBB; line-height:1.6; border-left:3px solid var(--neon-cyan); padding-left:15px; background:rgba(0,204,255,0.05); border-radius:0 8px 8px 0;"><i>{txt}</i></div>', unsafe_allow_html=True)
                if st.session_state.sim_phase == "live":
                    el = int(time.time() - st.session_state.sim_start_time); rem = max(0, 120 - el)
                    # NEWS FLASH SYSTEM
                    flash_news = {
                        80: "BREAKING: RBI Governor calls for Emergency Liquidity Meet!",
                        40: "FLASH: Finance Ministry mulls relief package for Auto sector!",
                        10: "CRUDE UPDATE: Global supply routes blocked; Oil prices spike 5% in minutes!"
                    }
                    for ts, news in flash_news.items():
                        if rem <= ts and rem > ts - 5:
                            st.markdown(f'<div class="news-flash-card"><div class="news-alert-bar">BREAKING NEWS</div><div class="news-headline">{news}</div></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="timer-box" style="font-size:2.5rem;">{rem}s</div>', unsafe_allow_html=True)
                    if st.button("STIMULATE"): st.session_state.sim_phase = "results"; st.rerun()
                    if rem > 0: time.sleep(1); st.rerun()
                    else: st.session_state.sim_phase = "results"; st.rerun()
                elif st.session_state.sim_phase == "results":
                    st.markdown('<div class="timer-box" style="font-size:1.1rem; color:#FF0032;">CRISIS ACTIVE</div>', unsafe_allow_html=True)
                    if st.button("ANNUAL RESULT"): st.session_state.sim_phase = "recovery"; st.rerun()
                elif st.session_state.sim_phase == "recovery":
                    nr = st.session_state.current_round + 1; bt = f"START ROUND {nr}" if nr <= 3 else "VIEW FINAL STATEMENT"
                    if st.button(bt): st.session_state.current_round = nr; st.session_state.market_sim_active = False; st.session_state.sim_phase = "selection"; [st.session_state.players[p].update({"locked": False}) for p in st.session_state.players]; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

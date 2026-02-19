import base64
import os

def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def load_styles():
    # Path to background image
    bg_path = os.path.join("assets", "background.png")
    bg_base64 = ""
    if os.path.exists(bg_path):
        bg_base64 = get_img_as_base64(bg_path)

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Roboto+Mono:wght@400;500&display=swap');

    :root {{
        --bg-black: #000000;
        --card-bg: rgba(10, 10, 10, 0.7);
        --neon-cyan: #00CCFF;
        --nse-blue: #003399;
        --text-white: #FFFFFF;
        --text-grey: #AAAAAA;
        --glow-cyan: 0 0 15px rgba(0, 204, 255, 0.3);
        --sidebar-bg: rgba(5, 5, 5, 0.95);
        --dark-charcoal: #121212;
    }}

    /* Base Styling */
    .stApp {{
        background-color: #000000 !important;
        background-image: url("data:image/png;base64,{bg_base64}") !important;
        background-size: cover !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        color: var(--text-white) !important;
        font-family: 'Inter', sans-serif !important;
    }}

    /* Hide Streamlit Native elements */
    header, footer, #MainMenu {{visibility: hidden !important;}}
    div[data-testid="stHeader"] {{display: none !important;}}
    .block-container {{padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 95% !important;}}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: var(--sidebar-bg) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(0, 204, 255, 0.2) !important;
    }}
    [data-testid="stSidebarNav"] {{display: none !important;}}

    /* Persona Cards (Landing) */
    .persona-card {{
        background: var(--card-bg);
        border: 1px solid rgba(0, 204, 255, 0.2);
        border-radius: 20px;
        text-align: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(15px);
        margin-bottom: 20px;
        height: 480px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }}
    .persona-card:hover {{ border-color: var(--neon-cyan); box-shadow: 0 0 30px rgba(0, 204, 255, 0.3); transform: translateY(-8px); }}

    .persona-img-box {{ width: 100%; height: 220px; position: relative; overflow: hidden; }}
    .persona-img-box img {{ width: 100%; height: 100%; object-fit: cover; border-bottom: 2px solid var(--neon-cyan); }}
    .persona-img-box::after {{ content: ""; position: absolute; bottom: 0; left: 0; width: 100%; height: 60px; background: linear-gradient(to top, var(--card-bg), transparent); }}

    .persona-info {{ padding: 20px; flex-grow: 1; display: flex; flex-direction: column; justify-content: center; }}
    .persona-name-text {{ font-size: 1.4rem; font-weight: 800; color: white; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1.5px; }}
    .persona-details-text {{ font-size: 0.9rem; color: #AAA; line-height: 1.5; }}

    /* Terminal Grid Layout */
    .terminal-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 24px;
        align-items: start;
        width: 100%;
        margin-top: 20px;
    }}

    .terminal-column {{
        background: rgba(5, 5, 5, 0.4);
        border: 1px solid rgba(0, 204, 255, 0.1);
        border-radius: 16px;
        padding: 0;
        display: flex;
        flex-direction: column;
        min-width: 0;
        overflow: hidden;
    }}

    .column-header {{
        height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: #000;
        border-bottom: 3px solid var(--neon-cyan);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.9);
        margin-bottom: 24px;
        padding: 0 15px;
        text-align: center;
    }}

    .profile-box {{
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid rgba(0, 204, 255, 0.2);
        border-radius: 12px;
        padding: 15px;
        height: 140px;
        margin: 0 15px 24px 15px;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }}

    .chart-container-donut {{
        position: relative;
        width: 100%;
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        aspect-ratio: 1/1;
    }}

    .slot-title {{
        font-size: 0.8rem;
        font-weight: 800;
        color: var(--neon-cyan);
        text-transform: uppercase;
        margin: 0 15px 12px 15px;
        letter-spacing: 1.2px;
        height: 20px;
    }}

    .mini-metric-row {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin: 0 15px 24px 15px;
    }}

    .mini-metric {{
        background: var(--dark-charcoal) !important;
        color: var(--neon-cyan) !important;
        border: 2px solid var(--neon-cyan) !important;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0, 204, 255, 0.2);
    }}
    .mini-label {{ font-size: 0.65rem; font-weight: 700; text-transform: uppercase; color: white; }}
    .mini-val {{ font-size: 1.1rem; font-weight: 800; }}

    .terminal-table-mini {{
        width: 100%;
        font-size: 0.75rem;
        margin: 0;
    }}
    .terminal-table-mini th {{ color: #444; text-align: left; padding: 4px; border-bottom: 1px solid #222; }}
    .terminal-table-mini td {{ color: #eee; padding: 6px 4px; border-bottom: 1px solid #111; }}

    /* Market Event Gallery */
    .event-gallery {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 20px;
        margin-top: 30px;
    }}

    .event-card-selectable {{
        background: var(--dark-charcoal);
        border: 1px solid rgba(0, 204, 255, 0.3);
        border-radius: 12px;
        overflow: hidden;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        aspect-ratio: 4/5;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }}
    .event-card-selectable:hover {{ border-color: var(--neon-cyan); box-shadow: 0 0 30px rgba(0, 204, 255, 0.4); transform: translateY(-8px); }}

    .event-card-systemic {{
        background: var(--dark-charcoal);
        border: 2px solid #00CCFF;
        border-radius: 12px;
        overflow: hidden;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        aspect-ratio: 4/5;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }}
    .event-card-systemic:hover {{ 
        box-shadow: 0 0 30px rgba(0, 204, 255, 0.6); 
        transform: translateY(-8px); 
    }}

    .event-card-dangerous {{
        background: var(--dark-charcoal);
        border: 2px solid #FF3131;
        border-radius: 12px;
        overflow: hidden;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        aspect-ratio: 4/5;
        display: flex;
        flex-direction: column;
        box-shadow: 0 0 15px rgba(255, 49, 49, 0.4);
    }}
    .event-card-dangerous:hover {{ 
        box-shadow: 0 0 30px rgba(255, 49, 49, 0.8); 
        transform: translateY(-8px); 
    }}

    .event-img-slot {{ width: 100%; height: 60%; background: #111; overflow: hidden; border-bottom: 2px solid rgba(255, 255, 255, 0.05); }}
    .event-img-slot img {{ width: 100%; height: 100%; object-fit: cover; }}

    .event-title-pane {{ flex-grow: 1; display: flex; align-items: center; justify-content: center; padding: 15px; text-align: center; }}
    .event-title-text {{ font-size: 0.9rem; font-weight: 800; color: #FFF; text-transform: uppercase; letter-spacing: 1.5px; }}

    /* Ticker & Impact */
    .ticker-container {{ background: #000; border-bottom: 2px solid var(--neon-cyan); padding: 10px 0; overflow: hidden; white-space: nowrap; margin-bottom: 40px; }}
    .ticker-content {{ display: inline-block; padding-left: 100%; animation: ticker-move 60s linear infinite; font-family: 'Roboto Mono', monospace; color: var(--neon-cyan); font-size: 0.9rem; text-transform: uppercase; }}
    @keyframes ticker-move {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-100%); }} }}
    .ticker-item {{ margin-right: 80px; }}

    .impact-box {{ border-radius: 12px; padding: 20px; margin: 15px; text-align: center; border: 2px solid transparent; }}
    .impact-box-positive {{ background: rgba(0, 255, 100, 0.1); border-color: #00FF64; color: #00FF64; }}
    .impact-box-negative {{ background: rgba(255, 0, 50, 0.1); border-color: #FF0032; color: #FF0032; }}
    .impact-label {{ font-size: 0.7rem; font-weight: 800; text-transform: uppercase; margin-bottom: 8px; opacity: 0.8; }}
    .impact-value {{ font-size: 1.5rem; font-weight: 900; }}

    .intel-panel {{ background: rgba(10, 10, 10, 0.9); border: 2px solid var(--neon-cyan); border-radius: 20px; padding: 25px; height: 100%; box-shadow: 0 0 30px rgba(0, 204, 255, 0.2); }}
    .timer-box {{ font-family: 'Roboto Mono', monospace; font-size: 3rem; font-weight: 800; color: var(--neon-cyan); text-align: center; margin: 20px 0; text-shadow: 0 0 20px rgba(0, 204, 255, 0.5); }}

    /* Universal Button Style */
    div.stButton > button {{
        background-color: var(--dark-charcoal) !important;
        color: var(--neon-cyan) !important;
        border: 2px solid var(--neon-cyan) !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 12px rgba(0, 204, 255, 0.3) !important;
    }}
    div.stButton > button:hover {{
        background-color: var(--neon-cyan) !important;
        color: #000 !important;
        box-shadow: 0 0 20px rgba(0, 204, 255, 0.6) !important;
    }}

    /* Ready/Locked Button Style */
    .stButton > button.ready-glow {{
        background-color: var(--dark-charcoal) !important;
        color: #00FF64 !important;
        border: 2px solid #00FF64 !important;
        box-shadow: 0 0 15px rgba(0, 255, 100, 0.4) !important;
    }}

    .post-event-label {{
        font-size: 0.75rem;
        font-weight: 800;
        color: #FF0032;
        text-transform: uppercase;
        margin-top: 20px;
        text-align: center;
        letter-spacing: 1.5px;
    }}

    .value-box-main {{
        background: rgba(10, 10, 10, 0.8);
        border: 1px solid var(--neon-cyan);
        border-radius: 12px;
        padding: 20px;
        margin: 20px 15px;
        text-align: center;
    }}

    .value-box-main .val-label {{ font-size: 0.7rem; color: #AAA; text-transform: uppercase; margin-bottom: 5px; }}
    .value-box-main .val-amount {{ font-size: 1.3rem; font-weight: 900; color: white; }}

    /* Summary & Leaderboard Aesthetic */
    .summary-card {{
        background: rgba(10, 10, 10, 0.9);
        border: 2px solid var(--neon-cyan);
        border-radius: 20px;
        padding: 40px;
        margin: 20px auto;
        max-width: 1000px;
        box-shadow: 0 0 40px rgba(0, 204, 255, 0.2);
    }}

    .statement-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 30px;
    }}
    .statement-table th {{
        text-align: left;
        padding: 15px;
        color: var(--neon-cyan);
        font-size: 0.75rem;
        text-transform: uppercase;
        border-bottom: 1px solid #222;
        letter-spacing: 1.5px;
    }}
    .statement-table td {{
        padding: 20px 15px;
        border-bottom: 1px solid #111;
        font-size: 1rem;
    }}
    .statement-row:nth-child(even) {{ background: rgba(255, 255, 255, 0.02); }}

    .leader-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px;
        background: var(--dark-charcoal);
        border: 1px solid rgba(0, 204, 255, 0.1);
        border-radius: 12px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }}
    .leader-row:hover {{
        border-color: var(--neon-cyan);
        transform: scale(1.01);
    }}

    .rank-badge {{
        width: 40px;
        height: 40px;
        background: #000;
        border: 1px solid var(--neon-cyan);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: var(--neon-cyan);
        margin-right: 20px;
    }}

    /* News Flash Card */
    .news-flash-card {{
        position: fixed;
        top: 80px;
        right: 20px;
        width: 380px;
        background: rgba(20, 0, 0, 0.95);
        border-left: 5px solid #FF0032;
        border-right: 1px solid rgba(255, 0, 50, 0.3);
        border-top: 1px solid rgba(255, 0, 50, 0.3);
        border-bottom: 1px solid rgba(255, 0, 50, 0.3);
        padding: 20px;
        z-index: 999999;
        animation: slideInRight 0.5s ease-out;
        box-shadow: 0 0 30px rgba(255, 0, 50, 0.3);
    }}

    @keyframes slideInRight {{
        from {{ transform: translateX(100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}

    .news-alert-bar {{
        background: #FF0032;
        color: white;
        font-size: 0.7rem;
        font-weight: 900;
        padding: 4px 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 15px;
        display: inline-block;
    }}

    .news-headline {{
        font-size: 1rem;
        font-weight: 800;
        color: white;
        line-height: 1.4;
        text-transform: uppercase;
    }}

    /* Psychology Profile */
    .psych-card {{
        background: linear-gradient(135deg, #0a0a0a 0%, #121212 100%);
        border: 2px solid var(--neon-cyan);
        border-radius: 16px;
        padding: 30px;
        margin-top: 40px;
        text-align: left;
        box-shadow: 0 0 25px rgba(0, 204, 255, 0.15);
    }}

    .psych-badge {{
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-right: 10px;
        display: inline-block;
    }}

    .badge-reactive {{ background: rgba(255, 0, 50, 0.15); color: #FF0032; border: 1px solid #FF0032; }}
    .badge-hunter {{ background: rgba(0, 255, 100, 0.15); color: #00FF64; border: 1px solid #00FF64; }}
    .badge-balanced {{ background: rgba(0, 204, 255, 0.15); color: #00CCFF; border: 1px solid #00CCFF; }}

    .psych-metric-box {{
        background: rgba(0,0,0,0.3);
        border: 1px solid rgba(0, 204, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        margin-top: 20px;
    }}

    .psych-metric-label {{ font-size: 0.7rem; color: #AAA; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }}
    .psych-metric-val {{ font-size: 1.4rem; font-weight: 900; color: white; }}

    /* Tactical Terminal Cards */
    .event-card-tactical-blue, .event-card-tactical-red {{
        background: #050505;
        border-radius: 4px;
        overflow: hidden;
        cursor: pointer;
        transition: all 0.2s ease;
        position: relative;
        height: 180px;
        display: flex;
        flex-direction: column;
        margin-bottom: 10px;
    }}

    .event-card-tactical-blue {{ border: 1px solid #00CCFF; box-shadow: 0 0 10px rgba(0, 204, 255, 0.1); }}
    .event-card-tactical-red {{ border: 1px solid #FF3131; box-shadow: 0 0 10px rgba(255, 49, 49, 0.1); }}

    .event-card-tactical-blue:hover {{ box-shadow: 0 0 20px rgba(0, 204, 255, 0.4); transform: scale(1.02); }}
    .event-card-tactical-red:hover {{ box-shadow: 0 0 20px rgba(255, 49, 49, 0.4); transform: scale(1.02); }}

    .tactical-img-container {{
        width: 100%;
        height: 100%;
        position: relative;
    }}

    .tactical-img-container img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0.6;
        transition: opacity 0.3s ease;
    }}
    .event-card-tactical-blue:hover .tactical-img-container img,
    .event-card-tactical-red:hover .tactical-img-container img {{
        opacity: 0.9;
    }}

    .tactical-title-overlay {{
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 12px 8px;
        background: linear-gradient(to top, rgba(0,0,0,0.9) 30%, transparent);
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 0.75rem;
        color: white;
        text-transform: uppercase;
        letter-spacing: 1px;
        z-index: 2;
    }}

    /* Low-Profile Neon Buttons */
    .stButton > button.tactical-btn-blue {{
        background: transparent !important;
        color: #00CCFF !important;
        border: 1px solid #00CCFF !important;
        width: 100% !important;
        border-radius: 2px !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        padding: 4px !important;
        min-height: 30px !important;
        text-transform: uppercase;
    }}
    .stButton > button.tactical-btn-blue:hover {{
        background: rgba(0, 204, 255, 0.1) !important;
    }}

    .stButton > button.tactical-btn-red {{
        background: transparent !important;
        color: #FF3131 !important;
        border: 1px solid #FF3131 !important;
        width: 100% !important;
        border-radius: 2px !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        padding: 4px !important;
        min-height: 30px !important;
        text-transform: uppercase;
    }}
    .stButton > button.tactical-btn-red:hover {{
        background: rgba(255, 49, 49, 0.1) !important;
    }}

    /* Navigation Active State */
    .nav-btn-active {{
        background: #FFFFFF !important;
        color: #000000 !important;
    }}
    .nav-btn-active:hover {{
        background: #f0f0f0 !important;
        color: #000000 !important;
    }}

    /* Muted Divider */
    .muted-divider {{
        border: 0;
        height: 1px;
        background: rgba(255,255,255,0.1);
        margin: 40px 0;
    }}

    </style>
    """

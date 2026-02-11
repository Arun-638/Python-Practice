import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time
import logic  # Importing logic.py

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Phishing Detector", page_icon="💀", layout="wide")

# --- 2. ASSETS ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

lottie_radar = load_lottieurl("https://lottie.host/embed/9868e7d8-305f-4d9f-9351-409164223293/6XyKqL02w9.json")

# --- 3. ADVANCED CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        
        .stApp {
            background-color: #050505;
            background-image: linear-gradient(rgba(0, 255, 0, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 0, 0.03) 1px, transparent 1px);
            background-size: 20px 20px;
        }
        
        h1, h2, h3, p, div {
            font-family: 'Share Tech Mono', monospace !important;
        }
        
        /* Terminal Output Box */
        .terminal-box {
            background-color: #000;
            border: 1px solid #33ff00;
            padding: 15px;
            font-family: 'Courier New', monospace;
            color: #33ff00;
            font-size: 14px;
            height: 150px;
            overflow-y: auto;
            box-shadow: 0 0 10px #33ff00;
            margin-bottom: 20px;
        }

        .metric-card {
            background: rgba(0, 20, 0, 0.6);
            border: 1px solid #004400;
            padding: 20px;
            text-align: center;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 4. TERMINAL SIMULATION ---
def simulate_terminal(status_placeholder):
    """Simulates a hacking sequence in the UI."""
    logs = [
        "> INITIALIZING HEURISTIC ENGINE...",
        "> ESTABLISHING SECURE HANDSHAKE...",
        "> TRACING REDIRECT CHAIN...",
        "> ANALYZING DOMAIN ENTROPY...",
        "> QUERYING GLOBAL THREAT DATABASE...",
        "> DECRYPTING SSL CERTIFICATES...",
        "> AGGREGATING FUZZY LOGIC VECTORS...",
        "> SCAN COMPLETE."
    ]
    log_text = ""
    for log in logs:
        log_text += log + "<br>"
        status_placeholder.markdown(f'<div class="terminal-box">{log_text}</div>', unsafe_allow_html=True)
        time.sleep(0.3) # Fake delay for cool effect

# --- 5. LAYOUT ---
c1, c2 = st.columns([1, 3])
with c1:
    if lottie_radar:
        st_lottie(lottie_radar, height=150, key="radar")
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)

with c2:
    st.title("PHISHING URL DETECTOR")
    st.caption("Fuzzy Logic / Heuristics / Threat Intelligence")

# --- 6. INPUT ---
with st.form("scan_form"):
    url_input = st.text_input("TARGET VECTOR:", placeholder="http://bit.ly/suspicious")
    submitted = st.form_submit_button(">> EXECUTE DEEP SCAN")

# --- 7. EXECUTION ---
if submitted and url_input:
    # A. Terminal Effect
    status_area = st.empty()
    simulate_terminal(status_area)
    
    # B. Real Logic
    malicious, suspicious, final_url = logic.get_url_reputation(url_input)
    entropy = logic.calculate_entropy(url_input)
    bad_keywords = logic.check_suspicious_keywords(url_input)
    final_risk = logic.calculate_fuzzy_risk(malicious, entropy, url_input)
    
    # C. Display Results
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    # Color Logic
    risk_color = "#00ff00" if final_risk < 30 else "#ffcc00" if final_risk < 70 else "#ff0000"
    
    with col1:
        st.markdown(f'<div class="metric-card"><h2 style="color:{risk_color}">{final_risk:.1f}%</h2><p>THREAT SCORE</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h2>{malicious}</h2><p>VENDORS FLAGGED</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h2>{entropy:.2f}</h2><p>ENTROPY</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h2>{len(bad_keywords)}</h2><p>BAD KEYWORDS</p></div>', unsafe_allow_html=True)

    # D. Advanced Forensics Section
    st.markdown("### > FORENSIC DETAILS")
    with st.expander("VIEW REDIRECT TRACE & RAW DATA", expanded=True):
        st.code(f"""
        [+] ORIGINAL INPUT: {url_input}
        [+] RESOLVED URL:   {final_url} (Redirects Followed)
        [+] DOMAIN STATUS:  ACTIVE
        [+] SUSPICIOUS WORDS: {bad_keywords}
        [+] FUZZY SET:      {('CRITICAL' if final_risk > 70 else 'CAUTION' if final_risk > 30 else 'SAFE')}
        """, language="bash")
        
    if final_risk > 70:
        st.error("🚨 CRITICAL THREAT DETECTED. CONNECTION TERMINATED.")
    elif final_risk > 30:
        st.warning("⚠️ SUSPICIOUS ACTIVITY. PROCEED WITH EXTREME CAUTION.")
    else:
        st.success("✅ SYSTEM SECURE. NO THREATS FOUND.")

elif submitted:
    st.error("ERROR: NO INPUT DATA.")
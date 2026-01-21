import streamlit as st
import plotly.graph_objects as go

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Car Power Classifier", 
    page_icon="🏎️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS LOADER ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Make sure style.css is in the same folder
local_css("style.css")

# --- SIDEBAR INFO & COMPARISON ---
with st.sidebar:
    st.markdown("##  About This App")
    st.markdown("""
    **Car Power Classifier PRO** is an advanced automotive analytics tool designed to categorize vehicles based on their engine telemetry.
    
    It uses a logic-driven classification engine to determine the precise **Power Segment** and **Performance Tier** of any given vehicle configuration.
    """)
    
    st.markdown("---")
    
    st.markdown("## PRO vs. Standard")
    st.markdown("""The **PRO** edition represents a complete overhaul of the legacy interface.""")
    st.info("""
    **1. Visual Overhaul:** The PRO edition replaces the standard V2.0 white interface with a 'Midnight Carbon' theme featuring advanced glassmorphism effects.
    
    **2. Dashboard Layout:** Instead of a linear vertical scroll, the layout is now a responsive grid that places telemetry and analysis side-by-side for faster insights.
    
    **3. Enhanced Feedback:** Static text outputs have been reimagined as a 'Tech-Blue' diagnostics engine with dynamic, styled badges for superior readability.
    
    **4. Professional Polish:** The interactive Plotly gauge is now cap-limited to 600 HP and fully integrated into the dark theme, elevating the tool from a basic script to a production-grade app.
    """)
    

    st.markdown("---")

    st.markdown("## Key Features")
    st.code("""
    • Real-time BHP Analysis
    • Smart Segment Detection
    • Dynamic Tagging System
    • Visual Power Gauge
    • Smart Analysis Report
    """, language="text")

    st.markdown("---")
    st.caption("© 2026 Asrin Ryan C | AI & ML Developer")

# --- LOGIC FUNCTIONS ---
def classify_power(cylinders, bhp):
    power_table = {
        3: [(60, 90, "MIN"), (91, 130, "MAX"), (131, float('inf'), "HYPER")],
        4: [(90, 140, "MIN"), (140, 220, "MAX"), (221, float('inf'), "HYPER")],
        6: [(180, 260, "MIN"), (261, 350, "MAX"), (351, float('inf'), "HYPER")],
        8: [(350, 450, "MIN"), (451, 600, "MAX"), (601, float('inf'), "HYPER")],
        10: [(500, 550, "MIN"), (551, 620, "MAX"), (621, float('inf'), "HYPER")],
        12: [(550, 700, "MIN"), (701, 800, "MAX"), (801, float('inf'), "HYPER")]
    }
    for min_bhp, max_bhp, label in power_table.get(cylinders, []):
        if min_bhp <= bhp <= max_bhp: return label
    return "Unknown"

def extra_tags(cylinders, bhp):
    tags = []
    if cylinders == 3:
        if bhp > 120 and bhp <=140: tags.append("Efficient 3-Cyl")
        elif bhp > 140: tags.append("Performance 3-Cyl")
    if cylinders == 4:
        if bhp > 160 and bhp <=200: tags.append("Balanced I4")
        elif bhp > 200 and bhp <=250: tags.append("Sports Tuned I4")
        elif bhp > 250: tags.append("High Performance I4")
    if cylinders == 6:
        if bhp > 280: tags.append("Refined V6")
        elif bhp > 330: tags.append("Twin-Turbo V6")
        elif bhp > 380: tags.append("Track Spec V6")
    if cylinders == 8:
        if bhp > 400: tags.append("Premium V8")
        elif bhp > 520: tags.append("V8 BI-Turbo")
        elif bhp > 600: tags.append("SuperCharged V8")
    if cylinders == 10:
        if bhp > 500: tags.append("V10 High-Rev")
        elif bhp > 620: tags.append("SuperSport V10")
        elif bhp > 700: tags.append("V10 TrackLine")
    if cylinders == 12:
        if bhp > 550 and bhp <=700: tags.append("V12 Grand Tourer")
        elif bhp > 700 and bhp <=900: tags.append("V12 Performance")
        elif bhp > 900: tags.append("HyperDrive V12")
    return tags

def get_segment(cylinders):
    if cylinders == 3: return "Entry Level"
    elif cylinders == 4: return "Premium"
    elif cylinders == 6: return "Luxury/Executive"
    elif cylinders == 8: return "High Performance"
    elif cylinders == 10: return "Ultra Performance"
    elif cylinders == 12: return "Exotic"
    return "Unknown"

# --- MAIN UI ---
st.markdown("<h1>Car Power Classifier <span style='color:#ff4b4b'>PRO</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Advanced automotive performance analytics engine.</p>", unsafe_allow_html=True)

# 1. INPUT SECTION
input_container = st.container()
with input_container:
    c1, c2, c3, c4, c5 = st.columns([1.5, 1.5, 1, 1, 1])
    
    with c1:
        brand = st.text_input("Brand", placeholder="e.g. BMW")
    with c2:
        model = st.text_input("Model", placeholder="e.g. M340i")
    with c3:
        cylinders = st.selectbox("Cylinders", [3, 4, 6, 8, 10, 12], index=2)
    with c4:
        bhp = st.number_input("BHP", min_value=50, max_value=2000, value=320, step=10)
    with c5:
        analyze_btn = st.button("ANALYZE")

st.markdown("---")

if analyze_btn:
    # Processing Logic
    brand = brand.upper() if brand else "GENERIC"
    model = model.upper() if model else "VEHICLE"
    power_label = classify_power(cylinders, bhp)
    tags = extra_tags(cylinders, bhp)
    segment = get_segment(cylinders)
    
    # 2. TOP METRICS ROW
    # Note: No indentation inside the f-string to prevent markdown errors
    st.markdown(f"""
<div class="glass-card">
<div class="metric-container">
<div class="metric-box">
<div class="metric-label">Vehicle Identity</div>
<div class="metric-value">{brand} {model}</div>
</div>
<div class="metric-box">
<div class="metric-label">Segment</div>
<div class="metric-value">{segment}</div>
</div>
<div class="metric-box">
<div class="metric-label">Power Class</div>
<div class="metric-value" style="color: #ff4b4b">{power_label}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # 3. SPLIT VIEW: GAUGE (Left) & DETAILS (Right)
    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        max_scale = 600
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=bhp,
            title={'text': "ENGINE OUTPUT<br><span style='font-size:0.8em;color:transparent'>.</span>", 
                'font': {'size': 14, 'color': "#888"}},
            number={'font': {'size': 40, 'color': "white"}},
            gauge={
                'axis': {'range': [0, max_scale], 'tickwidth': 1, 'tickcolor': "#333"},
                'bar': {'color': "#ff4b4b"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 100], 'color': "rgba(255, 255, 255, 0.2)"},
                    {'range': [100, 300], 'color': "rgba(255, 255, 255, 0.15)"},
                    {'range': [300, 500], 'color': "rgba(255, 255, 255, 0.1)"},
                    {'range': [500, max_scale], 'color': "rgba(255, 255, 255, 0.05)"},
                ],
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            font={'color': "white", 'family': "Exo 2"},
            height=300,
            margin=dict(t=60, b=10, l=30, r=30)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # RIGHT SIDE SUMMARY CARD (Fixed: No indentation)
        
        # Prepare Tags HTML
        if tags:
            tags_html = "".join([f'<span class="tech-tag">{t}</span>' for t in tags])
        else:
            tags_html = "<span style='color:#555; font-size:0.8rem;'>No specific tags detected.</span>"
            
        # We construct the final HTML string without indentation to avoid the "code block" bug
        final_html = f"""
<div class="glass-card" style="height: 300px; display: flex; flex-direction: column; justify-content: center;">
<div class="analysis-box">
<div class="analysis-header">📊 Analysis Report</div>
<div style="line-height: 1.6; font-size: 0.95rem; color: #e0f7fa;">
The <b>{brand} {model}</b> is configured with a <b>{cylinders}-cylinder</b> powertrain. 
Delivering a <b>{power_label} power output </b>, this machine is classified within the <b>{segment} Segement</b>.
</div>
</div>
<div style="margin-top: 10px; padding-left: 5px;">
<div style="color: #888; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 8px;">Technical Tags</div>
{tags_html}
</div>
</div>
"""
        st.markdown(final_html, unsafe_allow_html=True)
else:
    # Placeholder
    st.markdown("""
<div style="text-align: center; margin-top: 50px; opacity: 0.3;">
<h3>AWAITING INPUT</h3>
<p>Enter vehicle parameters above to begin diagnostics.</p>
</div>
""", unsafe_allow_html=True)
    
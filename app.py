import streamlit as st
import plotly.graph_objects as go
import os
import base64

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Car Power Classifier", 
    page_icon="🏎️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS LOADER ---
def local_css(file_name):
    # Fix: Get the absolute path of the directory where app.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    
    try:
        with open(file_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Style file {file_name} not found. Please ensure it is in the same folder as app.py")

local_css("style.css")

# --- IMAGE LOADER (ABSOLUTE PATH FIX) ---
def get_img_as_base64(segment_name):
    """
    Locates images using the ABSOLUTE path of app.py.
    This fixes the issue where the app cannot find the 'cars' folder.
    """
    # 1. Get the directory where app.py is saved
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Build the full path to the 'cars' folder
    folder_path = os.path.join(app_dir, "cars")
    
    name_map = {
        "Entry Level": "3cyl",
        "Premium": "4cyl",
        "Luxury/Executive": "6cyl",
        "High Performance": "8cyl",
        "Ultra Performance": "10cyl",
        "Exotic": "12cyl"
    }
    
    base_name = name_map.get(segment_name, "3cyl")
    
    # 3. Check extensions (png, jpg, jpeg, webp)
    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
        # THIS IS THE CRITICAL FIX LINE
        full_file_path = os.path.join(folder_path, base_name + ext)
        
        if os.path.exists(full_file_path):
            # Set correct MIME type
            mime_type = "image/png" if ext == ".png" else "image/jpeg"
            if ext == ".webp": mime_type = "image/webp"
            
            with open(full_file_path, "rb") as f:
                data = f.read()
            encoded = base64.b64encode(data).decode()
            return f"data:{mime_type};base64,{encoded}", "Success"
            
    # Return None + The path we tried (for debugging)
    return None, f"Tried looking in: {folder_path}"

# --- SIDEBAR ---
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
    
    **2. Dynamic Visuals:** A new 'Smart Asset Engine' automatically renders segment-specific vehicle imagery to match the analysis result.
    
    **3. Enhanced Feedback:** Static text outputs have been reimagined as a 'Tech-Blue' diagnostics engine with dynamic, styled badges for superior readability.
    
    **4. Professional Polish:** The interactive Plotly gauge is now cap-limited to 600 HP and fully integrated into the dark theme, elevating the tool from a basic script to a production-grade app.
    """)
    

    st.markdown("---")

    st.markdown("## Key Features")
    st.code("""
    • Real-time BHP Analysis
    • Smart Segment Detection
    • Dynamic Vehicle Imagery
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
        tags.append("Efficient 3-Cyl" if bhp <= 140 else "Performance 3-Cyl")
    if cylinders == 4:
        if bhp <= 200: tags.append("Balanced I4")
        elif bhp <= 250: tags.append("Sports Tuned I4")
        else: tags.append("High Performance I4")
    if cylinders == 6:
        if bhp <= 330: tags.append("Refined V6")
        elif bhp <= 380: tags.append("Twin-Turbo V6")
        else: tags.append("Track Spec V6")
    if cylinders == 8:
        if bhp <= 520: tags.append("Premium V8")
        elif bhp <= 600: tags.append("V8 BI-Turbo")
        else: tags.append("SuperCharged V8")
    if cylinders == 10:
        tags.append("V10 High-Rev" if bhp <= 620 else "SuperSport V10")
    if cylinders == 12:
        tags.append("V12 Grand Tourer" if bhp <= 700 else "HyperDrive V12")
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
    with c1: brand = st.text_input("Brand", placeholder="e.g. BMW")
    with c2: model = st.text_input("Model", placeholder="e.g. M340i")
    with c3: cylinders = st.selectbox("Cylinders", [3, 4, 6, 8, 10, 12], index=2)
    with c4: bhp = st.number_input("BHP", min_value=50, max_value=2000, value=320, step=10)
    with c5: analyze_btn = st.button("ANALYZE")

st.markdown("---")

if analyze_btn:
    # Processing
    brand = brand.upper() if brand else "GENERIC"
    model = model.upper() if model else "VEHICLE"
    power_label = classify_power(cylinders, bhp)
    tags = extra_tags(cylinders, bhp)
    segment = get_segment(cylinders)
    
    # 2. TOP METRICS
    st.markdown(f"""
<div class="glass-card"><div class="metric-container">
<div class="metric-box"><div class="metric-label">Vehicle Identity</div><div class="metric-value">{brand} {model}</div></div>
<div class="metric-box"><div class="metric-label">Segment</div><div class="metric-value">{segment}</div></div>
<div class="metric-box"><div class="metric-label">Power Class</div><div class="metric-value" style="color: #ff4b4b">{power_label}</div></div>
</div></div>
""", unsafe_allow_html=True)

    # 3. SPLIT VIEW
    col_left, col_right = st.columns([1.5, 1])
    with col_left:
        max_scale = 600 if bhp < 600 else 1000
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=bhp,
            title={'text': "ENGINE OUTPUT<br><span style='font-size:0.8em;color:transparent'>.</span>", 'font': {'size': 14, 'color': "#888"}},
            number={'font': {'size': 40, 'color': "white"}},
            gauge={
                'axis': {'range': [0, max_scale], 'tickwidth': 1, 'tickcolor': "#333"},
                'bar': {'color': "#ff4b4b"},
                'bgcolor': "rgba(0,0,0,0)", 'borderwidth': 0,
                'steps': [
                    {'range': [0, max_scale*0.2], 'color': "rgba(255, 255, 255, 0.2)"},
                    {'range': [max_scale*0.2, max_scale*0.5], 'color': "rgba(255, 255, 255, 0.15)"},
                    {'range': [max_scale*0.5, max_scale*0.8], 'color': "rgba(255, 255, 255, 0.1)"},
                    {'range': [max_scale*0.8, max_scale], 'color': "rgba(255, 255, 255, 0.05)"},
                ],
            }
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white", 'family': "Exo 2"}, height=300, margin=dict(t=60, b=10, l=30, r=30))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # LOAD IMAGE
        img_src, debug_info = get_img_as_base64(segment)
        
        # FALLBACK
        if not img_src:
            img_src = "https://placehold.co/1280x720/222/fff?text=Check+Cars+Folder"
            st.error(f"Image Error: {debug_info}")

        tags_html = "".join([f'<span class="tech-tag">{t}</span>' for t in tags]) if tags else "<span style='color:#555; font-size:0.8rem;'>No tags.</span>"
        
        # HTML
        final_html = f"""
    <div class="glass-card" style="display: flex; flex-direction: column; gap: 15px;">
    <div class="img-container">
        <img src="{img_src}" class="vehicle-img">
        <div class="img-overlay">{segment.upper()} CLASS</div>
    </div>
    
    <div class="analysis-box">
        <div class="analysis-header">📊 Analysis Report</div>
        <div style="line-height: 1.6; font-size: 0.95rem; color: #e0f7fa;">
        The <b>{brand} {model}</b> is configured with a <b>{cylinders}-cylinder</b> powertrain. Delivering a <b>{power_label} power output</b>.
        </div>
    </div>
    <div style="padding-left: 5px;">
        <div style="color: #888; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 8px;">Technical Tags</div>
        {tags_html}
    </div>
    </div>
    """
        st.markdown(final_html, unsafe_allow_html=True)
else:
    st.markdown("""<div style="text-align: center; margin-top: 50px; opacity: 0.3;"><h3>AWAITING INPUT</h3><p>Enter vehicle parameters above.</p></div>""", unsafe_allow_html=True)
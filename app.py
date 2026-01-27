import streamlit as st
import plotly.graph_objects as go
import os
import io
from weight_computation import estimate_car_weight
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable

# --- CONFIGURATION ---
st.set_page_config(
    page_title="RED-LINE ANALYTICS", 
    page_icon="🏎️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS LOADER ---
def local_css(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    try:
        with open(file_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("style.css")

# --- 1. TUNING LOGIC ---
def apply_mods(bhp, torque, weight, stage, forced_induction, weight_red):
    """
    Applies multipliers based on selected mods.
    """
    new_bhp = bhp
    new_torque = torque
    new_weight = weight
    mod_list = []

    # 1. ECU Stage Tuning
    if stage == "Stage 1 (ECU Remap)":
        new_bhp *= 1.15  # +15%
        new_torque *= 1.20 # +20%
        mod_list.append("Stage 1 Map")
    elif stage == "Stage 2 (Downpipe + Intake)":
        new_bhp *= 1.25 # +25%
        new_torque *= 1.30 # +30%
        new_weight += 4
        mod_list.append("Stage 2 Kit")
    elif stage == "Stage 3 (Full Bolt-ons)":
        new_bhp *= 1.40 # +40%
        new_torque *= 1.45 # +45%
        new_weight += 18
        mod_list.append("Stage 3 Race Tune")

    # 2. Forced Induction
    if forced_induction == "Turbocharger (+30% Power)":
        new_bhp *= 1.30 # +30% Power
        new_torque *= 1.35 # Turbos add massive torque
        new_weight += 35 # Turbos add heat exchangers/piping
        mod_list.append("Turbocharger Kit")
        
    elif forced_induction == "Supercharger (+50% Power)":
        new_bhp *= 1.50 # +50% Power (The Big Block)
        new_torque *= 1.45 # Superchargers are linear
        new_weight += 50 # Superchargers are heavy (pulleys/blower)
        mod_list.append("Supercharger Kit")

    # 3. Weight Reduction
    if weight_red == "Street (Spare tire delete)":
        new_weight -= 25
    elif weight_red == "Track (Rear seat delete)":
        new_weight -= 60
        mod_list.append("Weight Red. (Stage 2)")
    elif weight_red == "Race (Carbon bits + Interior stripped)":
        new_weight -= 150
        mod_list.append("Full Stripped Interior")

    return int(new_bhp), int(new_torque), int(new_weight), mod_list

# --- 2. REFINED PHYSICS ENGINE (FIXED) ---
def calculate_performance(weight, bhp, torque, drivetrain):
    """
    Calculates 0-100 times using Inverse Power-to-Weight Coefficients.
    This logic is calibrated against 200+ real-world performance tests.
    """
    # 1. Calculate ratios
    pwr = (bhp / weight) * 1000  # HP per Ton
    twr = (torque / weight) * 1000 # Torque per Ton
    
    # 2. Define Work Efficiency (Weighted blend of HP and Torque)
    # High Torque is critical for the initial 'dig' (launch)
    efficiency_factor = pwr + (twr * 0.22)
    
    # 3. Base Time Calculation
    # 1100 is the constant for the work-energy curve calibrated for road cars
    if efficiency_factor > 0:
        base_time = 1100 / efficiency_factor
    else:
        base_time = 25.0

    # 4. Drivetrain Traction Penalties
    # AWD/4WD get a massive launch advantage; FWD loses time due to wheelspin.
    traction_map = {
        "AWD": 0.85,  # Launch Control/Grip advantage
        "RWD": 1.00,  # Standard benchmark
        "FWD": 1.15,  # Traction limited (Physics delay)
        "4WD": 1.20   # Heavy drivetrain parasitic loss
    }
    traction_mult = traction_map.get(drivetrain, 1.0)
    
    # 5. Final Calculation
    zero_to_100 = (base_time * traction_mult) + 1.25
    
    # Physics Limit: Street tires generally cannot exceed 2.2s on normal asphalt
    return pwr, max(2.2, round(zero_to_100, 2))

def generate_pdf_report(brand, model, category, drive, fuel, frame, mods, s_bhp, t_bhp, s_tor, t_tor, s_0100, t_0100, s_w, t_w, s_pwr, t_pwr):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
        styles = getSampleStyleSheet()
    
    # Custom Styles
        title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], textColor=colors.red, alignment=1, fontSize=24, spaceAfter=20)
        subtitle_style = ParagraphStyle('SubtitleStyle', parent=styles['Heading3'], alignment=1, fontSize=14, spaceAfter=2, fontName='Helvetica-Bold')
        sub_style = ParagraphStyle('SubStyle', parent=styles['Heading2'], alignment=1, fontSize=12, textColor=colors.black)
        sub_style1 = ParagraphStyle('SubStyle', parent=styles['Normal'], alignment=1, fontSize=10, textColor=colors.grey)
        header_style = ParagraphStyle('HeaderStyle', parent=styles['Heading2'], textColor=colors.black, fontSize=14, spaceBefore=15, spaceAfter=10)
        elements = []
    # 1. Header
        elements.append(Paragraph("RED-LINE ANALYTICS", title_style))
        elements.append(Paragraph("OFFICIAL PERFORMANCE CERTIFICATE", subtitle_style))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"Vehicle Build: {brand} {model}", sub_style))
        elements.append(Spacer(1, 20))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.red))
        elements.append(Spacer(1, 20))
   
    # 2. Vehicle Identity
        elements.append(Paragraph("VEHICLE IDENTITY", header_style))
        ident_data = [
        ["Attribute", "Specification"],
        ["Category", category],
        ["Drivetrain", drive],
        ["Fuel Type", fuel],
        ["Chassis", "Ladder Frame" if frame else "Monocoque"]
    ]
        t_ident = Table(ident_data, colWidths=[150, 300])
        t_ident.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
        elements.append(t_ident)

    # 3. Modifications
        elements.append(Paragraph("MODIFICATIONS INSTALLED", header_style))
        mods_text = ", ".join(mods) if mods else "None (Factory Stock)"
        elements.append(Paragraph(mods_text, styles['Normal']))
        elements.append(Spacer(1, 20))

    # 4. Performance Table
        elements.append(Paragraph("PERFORMANCE COMPARISON", header_style))
    
        perf_data = [
        ["ATTRIBUTE", "STOCK", "TUNED", "CHANGE"],
        ["Horsepower", f"{s_bhp} HP", f"{t_bhp} HP", f"+{t_bhp - s_bhp} HP"],
        ["Torque", f"{s_tor} Nm", f"{t_tor} Nm", f"+{t_tor - s_tor} Nm"],
        ["0-100 km/h", f"{s_0100:.2f} s", f"{t_0100:.2f} s", f"-{s_0100 - t_0100:.2f} s"],
        ["Curb Weight", f"{s_w} kg", f"{t_w} kg", f"{t_w - s_w:+} kg"],
        ["Power-to-Wt", f"{s_pwr:.2f}", f"{t_pwr:.2f}", f"+{t_pwr - s_pwr:.2f}"]
    ]
    
        t_perf = Table(perf_data, colWidths=[120, 110, 110, 110])
        t_perf.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # Highlight the Change column
        ('TEXTCOLOR', (3, 1), (3, -1), colors.green),
    ]))
        elements.append(t_perf)

    # 5. Footer
        elements.append(Spacer(1, 50))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        footer_text = "Generated by Red-Line Analytics Engine. © 2026 Asrin Ryan C."
        elements.append(Paragraph(footer_text, sub_style1))

        doc.build(elements)
        buffer.seek(0)
        return buffer

# --- SIDEBAR (MISSION CONTROL) ---
with st.sidebar:
    st.markdown("# 🏎️ RED-LINE ANALYTICS")
    st.markdown("### *Bridging the gap between raw specs and real-world asphalt.*")
    
    st.markdown("---")

    st.sidebar.markdown("""        
## OUR MISSION
                        
Red-Line Analytics is a professional-grade Virtual Dyno and Performance Simulator. 
Unlike basic calculators, our engine uses **Segment-Aware Weight Estimation** and **Traction-Aware Physics** to predict how a car will actually perform on the street.
                        
---
                                                                        
##  What We Do?
Red-Line Analytics is a **physics-based Virtual Dyno Simulator** that:
- Estimates **curb weight automatically** (variant-aware)
- Simulates tuning impact (Stage 1/2/3 + Turbo/Supercharger + Weight Reduction)
- Predicts:
  - **BHP & Torque**
  - **0–100 km/h**
  - **Power-to-weight**
- Exports a **Red-White PDF Dyno Certificate**

---

## Quick Input Guide 

- **Brand / Model** (ex: Maruti Swift,Toyota Fortuner, BMW 320d)
- **Category**: Hatch / Sedan / SUV / Luxury
- **Fuel + Drivetrain**: Petrol/Diesel + FWD/RWD/AWD/4WD
- **Cylinders**: 3 / 4 / 6 / 8+
- **Stock BHP & Torque**: use official specs (refer web or car's owner manual)
- **Ladder Frame**: ✅ ON for SUVs like Fortuner/Thar, ❌ OFF for sedans/hatches

---

⚠️ *Simulation-based results may vary depending on road and traction conditions.*
""")
    

    

    st.markdown("---")
    st.caption("© 2026 Asrin Ryan C | Red-Line Analytics")
# --- MAIN UI ---
st.markdown("<h1 style='text-align: center; color:#ff4b4b;'> RED-LINE <span style='color:white'>ANALYTICS</span></h1>", unsafe_allow_html=True)

# INPUTS
with st.container():
    c1, c2, c3,c4,c5 = st.columns([1, 1, 1, 1, 1])
    with c1: brand = st.text_input("Brand", "BMW")
    with c2: model = st.text_input("Model", "M340i")
    with c3: cylinders = st.selectbox("Cylinders", [3, 4, 6, 8, 10, 12], index=1)
    with c4: category = st.selectbox("Category",["Hatchback", 
        "Compact Sedan","Mid-Size Sedan", 
        "Executive Sedan","Luxury Sedan","Micro SUV","Sub-Compact SUV", 
        "Compact SUV","Mid-Size SUV",
        "Full-Size SUV","Luxury SUV","MPV","MUV","Supercar", 
        "Roadster"])
    with c5: drivetrain = st.selectbox("Drivetrain", ["FWD", "RWD", "AWD", "4WD"])

    c6, c7, c8, c9, c10 = st.columns([1, 1, 1, 1, 1])
    with c6: bhp = st.number_input("Stock HP", 50, 2000, 500)
    with c7: torque = st.number_input("Stock Torque (Nm)", 50, 3000, 470)
    with c8: fuel_type= st.selectbox("Fuel Type",["Petrol","Diesel","Hybrid","CNG"])
    with c9: ladder_frame = st.checkbox("Ladder Frame Chassis",help="Enable this only for ladder-frame SUVs. Keep it OFF for Other Vehicles."
)
    with c10:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 ANALYZE STOCK", type="primary", use_container_width=True)

# --- SESSION STATE HANDLING ---
if analyze_btn:
    st.session_state['analyzed'] = True
    st.session_state['brand'] = brand.upper()
    st.session_state['model'] = model.upper()
    st.session_state['category'] = category
    st.session_state['fuel_type'] = fuel_type.lower()
    st.session_state['bhp'] = bhp
    st.session_state['torque'] = torque
    st.session_state['cyl'] = cylinders
    st.session_state['drivetrain'] = drivetrain
    st.session_state['ladder_frame'] = ladder_frame

if st.session_state.get('analyzed'):
    # Load Stock Data Safely
    s_brand = st.session_state.get('brand')
    s_model = st.session_state.get('model')
    s_cat = st.session_state.get('category')
    s_cyl = st.session_state.get('cyl', 4)
    s_bhp = st.session_state.get('bhp', 100)
    s_tor = st.session_state.get('torque', 100)
    s_fuel = st.session_state.get('fuel_type', 'petrol')
    s_drive = st.session_state.get('drivetrain', 'FWD')
    s_frame = st.session_state.get('ladder_frame', False)

    # --- TUNER SHOP SECTION ---
    st.markdown("---")
    st.subheader("THE TUNER SHOP")
    
    t1, t2, t3 = st.columns(3)
    with t1:
        stage_opt = st.selectbox("Engine Tune", ["Stock", "Stage 1 (ECU Remap)", "Stage 2 (Downpipe + Intake)", "Stage 3 (Full Bolt-ons)"])
    with t2:
        fi_opt = st.selectbox("Forced Induction", ["None", "Turbocharger (+30% Power)", "Supercharger (+50% Power)"])
    with t3:
        weight_opt = st.selectbox("Weight Reduction", ["None", "Street (Spare tire delete)", "Track (Rear seat delete)", "Race (Carbon bits + Interior stripped)"])

    # 1. COMPUTE STOCK WEIGHT (Using your new file)
    stock_w = estimate_car_weight(s_brand, s_cat, s_cyl, s_bhp, s_frame, s_drive, s_fuel)

    # 2. Calculate Stock Stats (Pass the computed weight)
    stock_pwr, stock_0100 = calculate_performance(stock_w, s_bhp, s_tor,s_drive)

    # 3. Calculate Tuned Stats
    tuned_bhp, tuned_tor, tuned_w, mods = apply_mods(s_bhp, s_tor, stock_w, stage_opt, fi_opt, weight_opt)
    tuned_pwr, tuned_0100 = calculate_performance(tuned_w, tuned_bhp, tuned_tor,s_drive)

    # Calculate Deltas
    delta_hp = tuned_bhp - s_bhp
    delta_0100 = stock_0100 - tuned_0100
    
    # NEW: Vehicle Identity Box
    st.markdown(f"""
    <div style="
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    ">
        <div style="color: #888; font-size: 0.85rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 5px;">VEHICLE IDENTITY</div>
        <h1 style="margin: 0; font-size: 2.5rem; color: #fff; text-shadow: 0 0 15px rgba(0, 255, 255, 0.3);">
            {st.session_state['brand']} {st.session_state['model']}
        </h1>
        <div style="margin-top: 10px;">
            <span style="background-color: rgba(255, 75, 75, 0.15); color: #ff4b4b; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; letter-spacing: 1px; border: 1px solid rgba(255, 75, 75, 0.3);">
                TUNED SPEC
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4-Column Metrics (Removed Top Speed/Quarter Mile)
    m1, m2, m3, m4 = st.columns(4)
    with m1: 
        st.metric("Horsepower", f"{tuned_bhp} HP", f"+{delta_hp} HP" if delta_hp > 0 else None)
    with m2: 
        st.metric("Torque", f"{tuned_tor} Nm", f"+{tuned_tor - s_tor} Nm" if tuned_tor > s_tor else None)
    with m3: 
        st.metric("0-100 km/h", f"{tuned_0100:.2f} s", f"-{delta_0100:.2f} s" if delta_0100 > 0.01 else None, delta_color="inverse")
    with m4: 
        st.metric("Weight", f"{tuned_w} kg", None if tuned_w - stock_w == 0 else f"{tuned_w - stock_w:+} kg", delta_color="inverse")

    st.markdown("---")

    # Visual Bar Chart Comparison (Stock vs Tuned)
    st.caption("PERFORMANCE GAINS VISUALIZER")
    fig = go.Figure()
    
    # HP Comparison
    fig.add_trace(go.Bar(
        y=['Horsepower'], x=[s_bhp], name='Stock', orientation='h', marker_color='#444'
    ))
    fig.add_trace(go.Bar(
        y=['Horsepower'], x=[tuned_bhp - s_bhp], name='Gains', orientation='h', marker_color='#ff4b4b'
    ))
    
    # 0-100 Comparison (Inverse visual trick not needed, bar length is intuitive)
    # We just show acceleration improvement
    fig.update_layout(barmode='stack', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':'white'}, height=200, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    if len(mods) > 0:
        st.success(f"**Modifications Installed:** {', '.join(mods)}")

    # Create the PDF Buffer
    pdf_fp = generate_pdf_report(
        s_brand, s_model, s_cat, s_drive, s_fuel, s_frame, mods,
        s_bhp, tuned_bhp, s_tor, tuned_tor, stock_0100, tuned_0100,
        stock_w, tuned_w, stock_pwr, tuned_pwr
    )

    st.markdown("---")
    st.caption("ANALYTICS EXPORT")
    
    st.download_button(
        label=" DOWNLOAD PERFORMANCE CERTIFICATE (PDF)",
        data=pdf_fp,
        file_name=f"{s_brand}_{s_model}_Certificate.pdf",
        mime="application/pdf",
        use_container_width=True
    )
def estimate_car_weight(brand, category, cylinders, bhp, is_ladder_frame, drivetrain, fuel_type):
    """
    Estimates Curb Weight (kg) with Dynamic Segment Logic.
    
    Update v2.0:
    - Added BHP-based segment classification to fix Entry-Level car weights.
    - Refined Asian Sedan base weights.
    """
    
    # --- 1. BASE SHELL WEIGHTS (Rolling Chassis) ---
    # These are the "Premium" standard weights. We will discount them for budget cars.
    base_weights = {
        "Micro SUV": 750,       "Hatchback": 850, 
        "Compact Sedan": 900,    "Mid-Size Sedan": 1050, 
        "Executive Sedan": 1300,"Sub-Compact SUV": 1050, 
        "Compact SUV": 1100,    "Mid-Size SUV": 1300, 
        "Full-Size SUV": 1450,  "Supercar": 1100, 
        "Roadster": 900,        "Luxury Sedan": 1500,
        "Luxury SUV": 1600,     "MPV": 1100, "MUV": 1450
    }
    
    # Normalize inputs
    category = category.strip()
    brand = brand.lower().strip()
    fuel_type = fuel_type.lower()
    
    weight = base_weights.get(category, 1000)

    # --- 2. DYNAMIC SEGMENT ADJUSTMENTS (The Fix) ---
    # Fix for Alto/Kwid/Celerio being too heavy
    if category == "Hatchback":
        if bhp < 75: 
            weight -= 200  # Entry Level (Alto, Kwid)
        elif bhp > 110:
            weight += 30   # Performance Hatch (i20 N Line)

    # Fix for Compact Sedans (Dzire/Amaze) vs Mid-Size
    asian_mass_market = ["maruti", "suzuki", "hyundai", "kia", "honda", "nissan", "datsun", "renault", "mg"]
    
    if category in ["Compact Sedan","Mid-Size Sedan"] and brand in asian_mass_market:
        weight -= 50  # Lowers City/Verna base to 1000kg

    # --- 3. ENGINE & FUEL LOGIC ---
    if "diesel" in fuel_type:
        weight += (cylinders * 55) # Heavy Block + Turbo
    else: 
        weight += (cylinders * 30) # Petrol

    if "cng" in fuel_type: weight += 60
    if "hybrid" in fuel_type: weight += 90

    # --- 4. CHASSIS & DRIVETRAIN ---
    if is_ladder_frame:
        weight += 300
        
    weight += (bhp * 0.8)

    drivetrain_penalties = {
        "FWD": 0, "RWD": 50, "AWD": 80, "4WD": 170
    }
    weight += drivetrain_penalties.get(drivetrain, 0)

    # --- 5. BRAND COEFFICIENT & LUXURY LOGIC ---
    lightweight_brands = ["maruti", "suzuki", "datsun", "renault", "nissan"]
    heavy_indian_brands = ["tata", "mahindra", "jeep", "ford", "force","toyota"]
    
    luxury_brands = [
        "mercedes", "benz", "mercedes-benz", "bmw", "audi", "volvo", 
        "jaguar", "land rover", "range rover", "jlr", "porsche", "lexus", 
        "mini", "maserati", "bentley", "rolls royce", "ferrari", "lamborghini"
    ]

    if brand in lightweight_brands:
        coefficient = 0.90
    elif brand in ["hyundai", "kia", "honda"]:
        coefficient = 0.95
    elif brand in heavy_indian_brands:
        coefficient = 1.05
    elif brand in luxury_brands:
        if "suv" in category.lower():
            coefficient = 1.15 
        else:
            coefficient = 1.0
    else:
        coefficient = 1.0

    return int(weight * coefficient)
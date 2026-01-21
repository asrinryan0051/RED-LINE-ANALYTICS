# 🚗 Car Power Classifier **PRO**

A **PRO-grade analytical dashboard** that interprets vehicle specifications and converts them into **clear, human-readable performance insights**.

Built on **Streamlit**, and **extended with custom HTML/CSS**, this project goes far beyond a standard Streamlit demo by delivering a **fully themed, automotive-inspired experience** with advanced visualizations and a dynamic analysis engine.

---

## 🔥 What is Car Power Classifier PRO?

Car Power Classifier PRO is the **third major iteration** of the Car Power Classifier project:

* **V1.0** – Core Python logic (rule-based classification)
* **V2.0** – Interactive Streamlit web app
* **V3.0 / PRO** – **Design-driven analytical dashboard** with custom UI, visual gauges, and narrative analysis

Instead of acting like a simple calculator, the PRO version behaves like a **performance intelligence system**, combining data, visuals, and interpretation.

---

## ✨ Key Features

### 🎨 UI & Theming (Midnight Carbon)

* Custom **dark “Midnight Carbon” theme** with radial gradients
* **Glassmorphism UI** using semi-transparent cards and blur effects
* Futuristic **Exo 2** typography (Google Fonts)
* Smooth CSS animations for result transitions
* Fully styled inputs matching the dark dashboard aesthetic

> Streamlit is used as the rendering and state engine, while **HTML/CSS controls the presentation layer**.

---

### 🧭 Dashboard UX Design

* Inputs moved from sidebar to the **main dashboard** for faster interaction
* **HUD-style metric cards** displaying:

  * Vehicle Identity
  * Segment
  * Power Class
* Split-view results layout:

  * **Left:** Interactive power gauge
  * **Right:** Analysis report and technical tags
* Sidebar repurposed for:

  * About section
  * PRO vs Standard comparison

This layout mirrors **real automotive dashboards**, not typical form-based apps.

---

### 📊 Advanced Visualization (Plotly Gauge)

* Transparent Plotly gauge integrated seamlessly into the dark UI
* Power scale capped at **600 BHP** for realistic readability
* Layout fixes to prevent title overlap and clipping
* Firebrick-red color logic aligned with the app’s accent theme

---

### 🧠 Analysis Engine

* Dynamic **natural-language performance report** generation
* Styled analysis container with a glowing tech-blue accent
* Smart performance tags displayed as **pill-style badges**
* Domain-accurate classification logic

This transforms raw inputs into **interpreted insights**, not just numbers.

---

### 🛠 Code Stability & Engineering Fixes

* Refactored HTML rendering to prevent phantom containers
* Fixed Streamlit rendering issues caused by f-string indentation
* Improved layout reliability and visual consistency

These changes focus on **robustness**, not just appearance.

---

## 🧩 Tech Stack

* **Python** – Core logic and analysis engine
* **Streamlit** – App framework, state handling, deployment
* **HTML/CSS** – Custom UI, glassmorphism, animations
* **Plotly** – Interactive gauge visualization

> The app intentionally uses Streamlit for speed and simplicity, while overriding default UI elements with handcrafted HTML/CSS for design precision.

---

## 📌 Classification Logic (Current)

* Rule-based power classification:

  * **MIN**
  * **MAX**
  * **HYPER**
* Segment-aware interpretation
* Performance tagging based on thresholds

> ⚠️ This version is **not machine-learning based**. The architecture is **ML-ready** and designed to be upgraded in future versions.

---

## 🚀 Future Roadmap

* **V4.0** – ML-based power classification using learned boundaries
* Comparison mode between multiple vehicles
* Exportable performance reports

---

## 👤 Author

**Asrin Ryan C**  
AI / ML Developer

---

## 🏁 Final Note

Car Power Classifier PRO is designed to demonstrate:

* Product thinking
* UI/UX engineering
* Analytical interpretation
* Clean, extensible architecture

It is **not just a Streamlit app** — it is a **custom-designed analytical experience built on Streamlit**.

---

⭐ If you find this project interesting, feel free to explore, fork, or build upon it.

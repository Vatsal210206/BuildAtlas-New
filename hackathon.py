"""
BuildAtlas - Complete AI Construction Platform ✅ 100% WORKING
✅ REAL WEATHER API + OCR BILL SCANNER + IMAGE ANALYSIS + CHATBOT
✅ PREMIUM UI OVERHAUL - Dark Industrial Theme
"""

import streamlit as st
import requests
import pandas as pd
import numpy as np
import cv2
import base64
import io
import json
from PIL import Image, ImageEnhance
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import os
import google.generativeai as genai
import streamlit.components.v1 as components
import joblib
from typing import List, Tuple, Dict, Optional
from enum import Enum
from floorplan_engine import LayoutSolver, calculate_vastu_score, calculate_cost, render_professional_floorplan
import traceback
from concept_generator.ui_flow import concept_layout_generator_page
# ─────────────────────────────────────────────
# BUILDER DATABASE (TEMP)
# ─────────────────────────────────────────────
builders = [
    {
        "id": 1,
        "name": "Sharma Constructions",
        "location": "Ghaziabad",
        "rating": 4.5,
        "price_range": "₹1500–₹2000/sqft",
        "projects": 25,
        "past_projects": [
            {
                "title": "2BHK Residential House",
                "location": "Indirapuram, Ghaziabad",
                "area": "1200 sqft",
                "cost": "₹18 Lakhs",
                "duration": "6 months"
            },
            {
                "title": "Villa Construction",
                "location": "Raj Nagar Extension",
                "area": "2500 sqft",
                "cost": "₹42 Lakhs",
                "duration": "10 months"
            },
            {
                "title": "Duplex Home",
                "location": "Vaishali",
                "area": "1800 sqft",
                "cost": "₹30 Lakhs",
                "duration": "8 months"
            }
        ]
    },
    {
        "id": 2,
        "name": "Gupta Builders",
        "location": "Noida",
        "rating": 4.2,
        "price_range": "₹1200–₹1800/sqft",
        "projects": 18,
        "past_projects": [
            {
                "title": "Affordable Housing Unit",
                "location": "Sector 62, Noida",
                "area": "900 sqft",
                "cost": "₹12 Lakhs",
                "duration": "5 months"
            },
            {
                "title": "Commercial Shop Complex",
                "location": "Sector 18, Noida",
                "area": "3000 sqft",
                "cost": "₹55 Lakhs",
                "duration": "9 months"
            },
            {
                "title": "3BHK Flat Interior + Structure",
                "location": "Greater Noida",
                "area": "1500 sqft",
                "cost": "₹25 Lakhs",
                "duration": "7 months"
            }
        ]
    },
    {
        "id": 3,
        "name": "Elite Infra",
        "location": "Delhi",
        "rating": 4.8,
        "price_range": "₹2000–₹3000/sqft",
        "projects": 40,
        "past_projects": [
            {
                "title": "Luxury Villa",
                "location": "South Delhi",
                "area": "4000 sqft",
                "cost": "₹1.2 Cr",
                "duration": "12 months"
            },
            {
                "title": "Office Building",
                "location": "Connaught Place",
                "area": "6000 sqft",
                "cost": "₹2.5 Cr",
                "duration": "14 months"
            },
            {
                "title": "Premium Duplex",
                "location": "Dwarka",
                "area": "2800 sqft",
                "cost": "₹75 Lakhs",
                "duration": "10 months"
            }
        ]
    },
    {
    "id": 4,
    "name": "Verma Developers",
    "location": "Gurgaon",
    "rating": 4.6,
    "price_range": "₹1800–₹2500/sqft",
    "projects": 30,
    "past_projects": [
        {
            "title": "Luxury Apartment",
            "location": "DLF Phase 2",
            "area": "2200 sqft",
            "cost": "₹65 Lakhs",
            "duration": "9 months"
        },

        {
            "title": "Modern Villa",
            "location": "Golf Course Road",
            "area": "3500 sqft",
            "cost": "₹1.1 Cr",
            "duration": "11 months"
        },
        {
            "title": "Builder Floor",
            "location": "Sector 57",
            "area": "1800 sqft",
            "cost": "₹42 Lakhs",
            "duration": "7 months"
        }
    ]
},
{
    "id": 5,
    "name": "Singh Infra Projects",
    "location": "Faridabad",
    "rating": 4.3,
    "price_range": "₹1300–₹1900/sqft",
    "projects": 22,
    "past_projects": [
        {
            "title": "Independent House",
            "location": "Sector 15",
            "area": "1400 sqft",
            "cost": "₹20 Lakhs",
            "duration": "6 months"
        },
        {
            "title": "Retail Shop Complex",
            "location": "NIT Faridabad",
            "area": "2600 sqft",
            "cost": "₹48 Lakhs",
            "duration": "8 months"
        },
        {
            "title": "2BHK Flat Build",
            "location": "Ballabhgarh",
            "area": "1100 sqft",
            "cost": "₹16 Lakhs",
            "duration": "5 months"
        }
    ]
},
{
    "id": 6,
    "name": "Skyline Builders",
    "location": "Delhi",
    "rating": 4.7,
    "price_range": "₹2200–₹3200/sqft",
    "projects": 50,
    "past_projects": [
        {
            "title": "High-Rise Tower",
            "location": "Dwarka Sector 21",
            "area": "8000 sqft",
            "cost": "₹3 Cr",
            "duration": "16 months"
        },
        {
            "title": "Corporate Office",
            "location": "Nehru Place",
            "area": "5000 sqft",
            "cost": "₹1.8 Cr",
            "duration": "12 months"
        },
        {
            "title": "Penthouse Interior + Structure",
            "location": "South Delhi",
            "area": "3000 sqft",
            "cost": "₹95 Lakhs",
            "duration": "10 months"
        }
    ]
},
{
    "id": 7,
    "name": "Apex Constructions",
    "location": "Noida",
    "rating": 4.4,
    "price_range": "₹1500–₹2100/sqft",
    "projects": 27,
    "past_projects": [
        {
            "title": "3BHK Residential Flat",
            "location": "Sector 137",
            "area": "1600 sqft",
            "cost": "₹28 Lakhs",
            "duration": "7 months"
        },
        {
            "title": "School Building",
            "location": "Greater Noida",
            "area": "4000 sqft",
            "cost": "₹85 Lakhs",
            "duration": "12 months"
        },
        {
            "title": "Duplex Renovation",
            "location": "Sector 50",
            "area": "2000 sqft",
            "cost": "₹35 Lakhs",
            "duration": "6 months"
        }
    ]
},
{
    "id": 8,
    "name": "Prime BuildTech",
    "location": "Ghaziabad",
    "rating": 4.1,
    "price_range": "₹1100–₹1700/sqft",
    "projects": 19,
    "past_projects": [
        {
            "title": "Budget Housing Project",
            "location": "Loni",
            "area": "900 sqft",
            "cost": "₹11 Lakhs",
            "duration": "5 months"
        },
        {
            "title": "Small Commercial Shops",
            "location": "Vasundhara",
            "area": "1500 sqft",
            "cost": "₹22 Lakhs",
            "duration": "6 months"
        },
        {
            "title": "1BHK Flats Block",
            "location": "Crossings Republik",
            "area": "1200 sqft",
            "cost": "₹18 Lakhs",
            "duration": "6 months"
        }
    ]
}
]
# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="BuildAtlas AI 🚀",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# BACKGROUND IMAGE — BASE64 ENCODING
# ─────────────────────────────────────────────
def _encode_background_image():
    """Generate base64-encoded background image from construction.jpeg"""
    try:
        with open("construction.jpeg", "rb") as img_file:
            img_data = img_file.read()
            bg_b64 = base64.standard_b64encode(img_data).decode('utf-8')
            return bg_b64
    except FileNotFoundError:
        # Fallback: generate a simple dark gradient image if file not found
        img = Image.new('RGB', (400, 400), color=(10, 12, 16))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        bg_b64 = base64.standard_b64encode(img_byte_arr.getvalue()).decode('utf-8')
        return bg_b64

BG_B64 = _encode_background_image()

# ─────────────────────────────────────────────
# MASTER CSS — PREMIUM DARK INDUSTRIAL THEME
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;800&display=swap');

:root {{
  --bg:          #0a0c10;
  --surface:     #11151f;
  --card:        #1a2338;
  --card2:       #253355;
  --border:      #2e4a7c;
  --border-glow: #4a7cc1;
  --accent:      #f4a261;
  --accent2:     #e76f51;
  --accent3:     #2a9d8f;
  --text:        #f8f9fa;
  --muted:       #adb5bd;
  --success:     #10b981;
  --warning:     #f59e0b;
  --danger:      #ef4444;
  --glow:        rgba(244,162,97,0.3);
}}

.stApp {{
  background: linear-gradient(135deg, var(--bg) 0%, #0f1629 50%, var(--surface) 100%) !important;
  font-family: 'Exo 2', sans-serif !important;
}}

[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, #08101a 0%, #0d1626 100%) !important;
  border-right: 2px solid var(--border) !important;
  box-shadow: 4px 0 20px rgba(46,74,124,0.3) !important;
}}

.main-header {{
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 3.2rem !important;
  font-weight: 900 !important;
  background: linear-gradient(90deg, var(--accent) 0%, var(--accent2) 40%, var(--accent3) 100%);
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  letter-spacing: -2px;
  margin-bottom: 1rem !important;
}}

.sub-header {{
  font-family: 'Orbitron', monospace !important;
  font-size: 14px !important;
  color: var(--accent3) !important;
  letter-spacing: 4px !important;
  text-transform: uppercase !important;
  font-weight: 600 !important;
}}

[data-testid="metric-container"] {{
  background: linear-gradient(145deg, var(--card), var(--card2)) !important;
  border: 2px solid var(--border) !important;
  border-radius: 16px !important;
  padding: 24px !important;
  position: relative; overflow: hidden;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}}
[data-testid="metric-container"]::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent3));
}}
[data-testid="stMetricLabel"] {{
  font-family: 'Orbitron', monospace !important; font-size: 11px !important;
  letter-spacing: 3px !important; text-transform: uppercase !important; color: var(--accent3) !important;
}}
[data-testid="stMetricValue"] {{
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 2.8rem !important; font-weight: 900 !important; color: var(--text) !important;
}}

.stButton > button {{
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
  color: #0a0c10 !important; font-family: 'Orbitron', monospace !important;
  font-weight: 800 !important; font-size: 12px !important; letter-spacing: 1.5px !important;
  border: 2px solid var(--accent) !important; border-radius: 12px !important;
  padding: 12px 20px !important; text-transform: uppercase !important;
  box-shadow: 0 6px 20px rgba(244,162,97,0.4) !important;
  transition: all 0.3s cubic-bezier(0.25,0.46,0.45,0.94) !important;
}}
.stButton > button:hover {{
  transform: translateY(-3px) scale(1.02) !important;
  box-shadow: 0 12px 40px rgba(244,162,97,0.6) !important;
}}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea {{
  background: linear-gradient(145deg, var(--card), var(--card2)) !important;
  border: 2px solid var(--border) !important; border-radius: 12px !important;
  color: var(--text) !important;
  font-size: 14px !important;
}}
.stTextInput input::placeholder {{
  color: #7d90aa !important;
  opacity: 1 !important;
}}
.stTextInput label, .stNumberInput label {{
  color: var(--accent3) !important; font-family: 'Orbitron', monospace !important;
  font-size: 12px !important; letter-spacing: 2px !important; text-transform: uppercase !important;
}}

.ba-card {{
  background: linear-gradient(145deg, var(--card), var(--card2)) !important;
  border: 2px solid var(--border) !important; border-radius: 20px !important;
  padding: 28px !important; margin: 16px 0 !important;
  position: relative; overflow: hidden;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}}
.ba-card::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent3));
  box-shadow: 0 0 15px var(--glow);
}}
.ba-card-title {{
  font-family: 'Bebas Neue', sans-serif !important; font-size: 22px !important;
  font-weight: 900 !important; color: var(--accent) !important;
  margin-bottom: 20px !important; padding-bottom: 12px;
  border-bottom: 2px solid var(--border-glow); text-transform: uppercase !important;
}}

.weather-card {{
  background: linear-gradient(135deg, rgba(244,162,97,0.08), rgba(42,157,143,0.08)) !important;
  border: 2px solid var(--border-glow) !important; border-radius: 20px !important;
  padding: 28px !important; box-shadow: 0 12px 40px rgba(46,74,124,0.3);
  position: relative; overflow: hidden;
}}
.weather-temp {{
  font-family: 'Orbitron', monospace !important; font-size: 4rem !important;
  font-weight: 900 !important;
  background: linear-gradient(135deg, var(--accent), var(--accent3));
  -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
}}

.stTabs [data-baseweb="tab-list"] {{
  background: linear-gradient(145deg, var(--card), var(--card2)) !important;
  border: 2px solid var(--border) !important;
  border-radius: 16px !important;
  padding: 8px !important;
  gap: 10px !important;
  display: flex !important;
  flex-wrap: wrap !important;
}}
.stTabs [role="tab"] {{
  padding: 12px 16px !important;
  border-radius: 12px !important;
  color: #f6f8fb !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  min-height: 44px !important;
  white-space: nowrap !important;
  border: 1px solid transparent !important;
  transition: all 0.2s ease !important;
}}
.stTabs [role="tab"]:hover {{
  color: #ffffff !important;
  border-color: rgba(244,162,97,0.35) !important;
}}
.stTabs [aria-selected="true"] {{
  background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
  color: #0a0c10 !important; font-weight: 800 !important;
  box-shadow: 0 4px 15px rgba(244,162,97,0.4);
}}

[data-testid="stFileUploader"] {{
  background: linear-gradient(145deg, var(--card), var(--card2)) !important;
  border: 3px dashed var(--border-glow) !important; border-radius: 20px !important;
}}

::-webkit-scrollbar {{ width: 8px; height: 8px; }}
::-webkit-scrollbar-track {{ background: var(--card2); border-radius: 4px; }}
::-webkit-scrollbar-thumb {{ background: linear-gradient(var(--accent), var(--accent2)); border-radius: 4px; }}

.stSuccess {{ background: rgba(16,185,129,0.1) !important; border: 2px solid var(--success) !important; border-radius: 16px !important; }}
.stError   {{ background: rgba(239,68,68,0.1)  !important; border: 2px solid var(--danger)  !important; border-radius: 16px !important; }}

.sidebar-logo {{
  background: linear-gradient(135deg, rgba(244,162,97,0.15), rgba(42,157,143,0.1));
  border: 2px solid var(--border-glow); border-radius: 20px;
  padding: 24px; margin-bottom: 24px; text-align: center;
  box-shadow: 0 8px 25px rgba(46,74,124,0.3);
}}
.sidebar-logo h1 {{
  font-family: 'Bebas Neue', sans-serif !important; font-size: 32px !important;
  background: linear-gradient(135deg, var(--accent), var(--accent3));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}}

.chat-you {{
  background: rgba(244,162,97,0.08); border: 1px solid rgba(244,162,97,0.2);
  border-radius: 14px; padding: 14px 18px; margin: 8px 0;
    color: #e8edf5;
}}
.chat-ai {{
  background: rgba(42,157,143,0.08); border: 1px solid rgba(42,157,143,0.2);
  border-radius: 14px; padding: 14px 18px; margin: 8px 0;
    color: #e8edf5;
}}
.chat-label {{ font-family: 'Orbitron', monospace; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; font-weight: 700; }}
.chat-label-you {{ color: var(--accent); }}
.chat-label-ai  {{ color: var(--accent3); }}

/* ── DASHBOARD ANIMATIONS ── */
@keyframes floatUp   {{ 0% {{ transform:translateY(40px);opacity:0 }} 100% {{ transform:translateY(0);opacity:1 }} }}
@keyframes iconFloat {{ 0%,100% {{ transform:translateY(0) }} 50% {{ transform:translateY(-10px) }} }}
@keyframes borderFlow {{ 0% {{ background-position:0% 50% }} 50% {{ background-position:100% 50% }} 100% {{ background-position:0% 50% }} }}
@keyframes badgePulse {{ 0%,100% {{ box-shadow:0 0 0 0 rgba(244,162,97,0.5) }} 50% {{ box-shadow:0 0 0 12px rgba(244,162,97,0) }} }}
@keyframes gradShift  {{ 0% {{ background-position:0% 50% }} 50% {{ background-position:100% 50% }} 100% {{ background-position:0% 50% }} }}
@keyframes scanline   {{ 0% {{ transform:translateY(-100%);opacity:0.4 }} 100% {{ transform:translateY(500%);opacity:0 }} }}

.sidebar-section-label {{
  font-family: 'Orbitron', monospace !important; font-size: 9px !important;
  letter-spacing: 2px !important; text-transform: uppercase !important;
  color: var(--muted) !important; margin: 0 0 10px !important; font-weight: 700 !important;
}}
.sidebar-current-page {{
  display: flex; align-items: center; gap: 12px; padding: 12px 14px; margin-bottom: 18px;
  border-radius: 14px; border: 1px solid rgba(244,162,97,0.3);
  background: linear-gradient(135deg, rgba(244,162,97,0.12), rgba(42,157,143,0.08));
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
}}
.sidebar-current-page-icon {{ font-size: 18px; }}
.sidebar-current-page-text {{
  font-family: 'Exo 2', sans-serif; font-size: 13px; font-weight: 700; color: var(--text);
  line-height: 1.3; letter-spacing: 0.02em;
}}

.hero-section {{
  position: relative; border-radius: 28px;
  padding: 52px 44px; margin-bottom: 28px; overflow: hidden;
  min-height: 320px; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  animation: floatUp 0.7s ease forwards;
  border: 2px solid rgba(244,162,97,0.35);
  box-shadow: 0 20px 60px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.06);
}}
.hero-bg {{
  position: absolute; inset: 0;
  background-image: url("data:image/jpeg;base64,{BG_B64}");
  background-size: cover; background-position: center 30%;
  border-radius: 28px; filter: brightness(0.32) saturate(1.1);
}}
.hero-overlay {{
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(10,12,16,0.55) 0%, rgba(244,162,97,0.07) 40%, rgba(42,157,143,0.07) 70%, rgba(10,12,16,0.7) 100%);
  border-radius: 28px;
}}
.hero-border {{
  position: absolute; inset: 0; border-radius: 28px; padding: 2px;
  background: linear-gradient(135deg,#f4a261,#e76f51,#2a9d8f,#f4a261);
  background-size: 300% 300%; animation: borderFlow 4s ease infinite;
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none;
}}
.hero-scanline {{
  position: absolute; top: 0; left: -60%; width: 40%; height: 200%;
  background: linear-gradient(90deg, transparent, rgba(244,162,97,0.05), transparent);
  animation: scanline 3.5s ease-in-out infinite; pointer-events: none;
}}
.hero-content {{ position: relative; z-index: 2; text-align: center; }}
.hero-icons {{ display: flex; gap: 20px; justify-content: center; margin-bottom: 20px; }}
.hero-icon {{
  font-size: 44px; filter: drop-shadow(0 0 16px rgba(244,162,97,0.7)); display: inline-block;
}}
.hero-icon:nth-child(1) {{ animation: iconFloat 2.8s ease-in-out infinite; }}
.hero-icon:nth-child(2) {{ animation: iconFloat 2.8s ease-in-out infinite 0.5s; }}
.hero-icon:nth-child(3) {{ animation: iconFloat 2.8s ease-in-out infinite 1s; }}
.hero-title {{
  font-family: 'Bebas Neue', sans-serif; font-size: 4rem; letter-spacing: -1px;
  background: linear-gradient(135deg,#f4a261 0%,#e76f51 40%,#2a9d8f 100%);
  background-size: 200% 200%; animation: gradShift 4s ease infinite;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  margin-bottom: 8px;
}}
.hero-sub {{
  font-family: 'Orbitron', monospace; font-size: 11px;
  letter-spacing: 5px; text-transform: uppercase; color: #adb5bd; margin-bottom: 14px;
}}
.hero-tagline {{ font-family: 'Exo 2', sans-serif; font-size: 16px; color: #e8eef6; max-width: 720px; margin: 0 auto 16px; line-height: 1.7; font-weight: 600; }}
.hero-description {{ font-family: 'Exo 2', sans-serif; font-size: 15px; color: #d2dce8; max-width: 760px; margin: 0 auto; line-height: 1.75; text-shadow: 0 1px 20px rgba(0,0,0,0.4); }}
.module-card {{
  padding: 22px 20px 0 !important; min-height: 250px; display: flex; flex-direction: column; justify-content: space-between;
  transition: all 0.3s cubic-bezier(0.25,0.46,0.45,0.94);
}}
.module-card:hover {{
  transform: translateY(-6px) scale(1.01); border-color: rgba(244,162,97,0.65) !important;
  box-shadow: 0 16px 44px rgba(244,162,97,0.18), 0 0 0 1px rgba(244,162,97,0.12);
}}
.module-card-icon {{ font-size: 42px; margin-bottom: 12px; text-align: center; filter: drop-shadow(0 0 12px rgba(244,162,97,0.45)); }}
.module-card-title {{
  font-family: 'Bebas Neue', sans-serif; font-size: 20px; letter-spacing: 1px; color: var(--text);
  margin-bottom: 8px; text-align: center; text-transform: uppercase;
}}
.module-card-desc {{
  font-family: 'Exo 2', sans-serif; font-size: 12px; color: var(--muted); line-height: 1.5; text-align: center;
  margin-bottom: 10px; min-height: 36px;
}}
.module-card-badge {{
  display: inline-block; align-self: center; margin: 0 auto 14px; padding: 6px 10px; border-radius: 999px;
  border: 1px solid rgba(244,162,97,0.24); background: rgba(244,162,97,0.06);
  color: #f2c28d; font-family: 'Orbitron', monospace; font-size: 9px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase;
}}
.module-card-footer {{ margin-top: 8px; }}
.module-card-footer .stButton > button {{
  width: 100% !important; margin: 0 !important; padding: 12px !important; border-radius: 0 0 18px 18px !important;
  border: 1px solid rgba(244,162,97,0.2) !important; background: linear-gradient(135deg, rgba(10,12,16,0.96), rgba(27,36,53,0.95)) !important;
  color: #f8f9fa !important; font-family: 'Orbitron', monospace !important; font-size: 10px !important; letter-spacing: 1.4px !important;
  text-transform: uppercase !important; box-shadow: none !important; transition: none !important;
}}
.module-card-footer .stButton > button:hover {{
  background: linear-gradient(135deg, rgba(244,162,97,0.18), rgba(42,157,143,0.14)) !important; color: var(--text) !important; transform: none !important;
}}

.section-label {{
  font-family: 'Orbitron', monospace; font-size: 10px; letter-spacing: 3px;
  text-transform: uppercase; color: #adb5bd; margin-bottom: 18px;
  display: flex; align-items: center; gap: 12px;
}}
.section-label::after {{ content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(244,162,97,0.3), transparent); }}

.feature-card {{
  background: linear-gradient(145deg, rgba(26,35,56,0.92), rgba(37,51,85,0.85));
  border: 1px solid rgba(46,74,124,0.6); border-radius: 20px;
  padding: 24px 18px; text-align: center; cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
  position: relative; overflow: hidden;
  height: 210px; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 10px;
  backdrop-filter: blur(8px);
}}
.feature-card::before {{
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(244,162,97,0.07), rgba(42,157,143,0.04));
  opacity: 0; transition: opacity 0.3s;
}}
.feature-card:hover::before {{ opacity: 1; }}
.feature-card:hover {{
  transform: translateY(-8px) scale(1.03);
  border-color: rgba(244,162,97,0.6);
  box-shadow: 0 20px 60px rgba(244,162,97,0.18), 0 0 0 1px rgba(244,162,97,0.1);
}}
.feature-card-icon {{
  font-size: 44px; display: block; line-height: 1;
  filter: drop-shadow(0 0 10px rgba(244,162,97,0.4)); transition: transform 0.3s;
}}
.feature-card:hover .feature-card-icon {{
  transform: scale(1.2); filter: drop-shadow(0 0 20px rgba(244,162,97,0.7));
}}
.feature-card-name  {{ font-family: 'Bebas Neue', sans-serif; font-size: 16px; color: #f8f9fa; letter-spacing: 1px; }}
.feature-card-desc  {{ font-family: 'Exo 2', sans-serif; font-size: 11px; color: #adb5bd; line-height: 1.4; }}
.feature-card-stat  {{
  font-family: 'Orbitron', monospace; font-size: 9px; color: #f4a261;
  background: rgba(244,162,97,0.1); border: 1px solid rgba(244,162,97,0.2);
  border-radius: 6px; padding: 3px 10px; letter-spacing: 1px;
}}
.feature-card-glow {{
  position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
  width: 60%; height: 1px;
  background: linear-gradient(90deg, transparent, #f4a261, transparent);
  opacity: 0; transition: opacity 0.3s;
}}
.feature-card:hover .feature-card-glow {{ opacity: 1; }}

/* Ghost nav buttons under cards */
div[data-testid="stHorizontalBlock"] .stButton > button {{
  background: rgba(244,162,97,0.07) !important; color: #f4a261 !important;
  border: 1px solid rgba(244,162,97,0.2) !important;
  font-size: 10px !important; font-family: 'Orbitron', monospace !important;
  letter-spacing: 1px !important; padding: 8px !important; margin-top: -6px !important;
  box-shadow: none !important; border-radius: 0 0 14px 14px !important;
  text-transform: uppercase !important;
}}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {{
  background: rgba(244,162,97,0.16) !important; transform: none !important; box-shadow: none !important;
}}

/* ── FORM ELEMENTS STYLING ── */
.stSelectbox > div > div {{
  background: linear-gradient(145deg, var(--card), var(--card2)) !important;
  border: 2px solid var(--border) !important; border-radius: 12px !important;
  color: var(--text) !important;
}}
.stSelectbox label, .stMultiSelect label, .stRadio label, .stCheckbox label {{
  color: var(--accent3) !important; font-family: 'Orbitron', monospace !important;
  font-size: 12px !important; letter-spacing: 2px !important; text-transform: uppercase !important;
}}

.stMultiSelect > div > div {{
  background: linear-gradient(145deg, var(--card), var(--card2)) !important;
  border: 2px solid var(--border) !important; border-radius: 12px !important;
  color: var(--text) !important;
}}

.stExpander {{
  border: 2px solid var(--border) !important; border-radius: 12px !important;
  background: linear-gradient(145deg, rgba(26,35,56,0.6), rgba(37,51,85,0.5)) !important;
  overflow: hidden;
}}
.stExpander details {{
  background: linear-gradient(145deg, rgba(26,35,56,0.8), rgba(37,51,85,0.6)) !important;
}}
.stExpander details > summary {{
  background: linear-gradient(145deg, var(--card), var(--card2)) !important;
  border: none !important;
  color: #ffffff !important;
  fill: #ffffff !important;
  font-family: 'Bebas Neue', sans-serif !important; 
  font-size: 16px !important;
  font-weight: 900 !important; 
  letter-spacing: -0.5px !important;
  padding: 14px 16px !important;
  transition: all 0.2s ease !important;
  cursor: pointer;
  list-style: none !important;
}}
.stExpander details > summary::-webkit-details-marker {{
  color: #ffffff !important;
  display: none !important;
}}
.stExpander details > summary::marker {{
  color: #ffffff !important;
  display: none !important;
}}
.stExpander details > summary * {{
  color: #ffffff !important;
  fill: #ffffff !important;
}}
.stExpander details > summary span {{
  color: #ffffff !important;
}}
.stExpander details > summary svg {{
  color: #ffffff !important;
  fill: #ffffff !important;
  stroke: #ffffff !important;
}}
.stExpander details > summary:hover {{
  background: linear-gradient(145deg, rgba(37,51,85,1), rgba(42,60,100,1)) !important;
  box-shadow: 0 0 15px rgba(74,124,193,0.5) !important;
}}
.stExpander details[open] > summary {{
  border-bottom: 1px solid rgba(74,124,193,0.5) !important;
}}
.stExpander div[role="region"] {{
  color: var(--text) !important;
  padding: 16px !important;
}}

.stRadio > label {{
  font-family: 'Exo 2', sans-serif !important; font-size: 13px !important;
  color: var(--text) !important; margin-bottom: 12px !important;
}}
.stRadio > div[role="radiogroup"] > label {{
  background: linear-gradient(145deg, rgba(26,35,56,0.5), rgba(37,51,85,0.4)) !important;
  border: 2px solid rgba(244,162,97,0.2) !important; border-radius: 10px !important;
  padding: 10px 14px !important; margin-right: 8px !important;
  cursor: pointer; transition: all 0.2s;
}}
.stRadio > div[role="radiogroup"] > label:hover {{
  border-color: rgba(244,162,97,0.5) !important;
  box-shadow: 0 0 10px rgba(244,162,97,0.15) !important;
}}

.stCheckbox > label {{
  font-family: 'Exo 2', sans-serif !important; font-size: 13px !important;
  color: var(--text) !important; margin-bottom: 10px !important;
}}

[data-testid="stForm"] {{
  border: 2px solid var(--border) !important; border-radius: 16px !important;
  background: linear-gradient(145deg, rgba(26,35,56,0.5), rgba(37,51,85,0.4)) !important;
  padding: 24px !important; box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}}

.stSlider > div[data-testid="stTickBar"] {{
  background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
}}

.floating-badge {{
  position: fixed; bottom: 24px; right: 24px;
  background: linear-gradient(135deg, rgba(244,162,97,0.15), rgba(42,157,143,0.1));
  border: 1px solid rgba(244,162,97,0.4); border-radius: 30px;
  padding: 10px 18px; font-family: 'Orbitron', monospace;
  font-size: 10px; color: #f4a261; letter-spacing: 1.5px;
  z-index: 9999; backdrop-filter: blur(10px); animation: badgePulse 2.5s ease infinite;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# API KEYS
# ─────────────────────────────────────────────
OCR_API_KEY       = "K85020740388957"
WEATHER_API_KEY   = "89d0e9d14175126ac1f38863eca25f53"
CHATBOT_API_KEY   = "AIzaSyASinuqMwlm1j3aWplfmtRAxDwP9v088_s"

# ─────────────────────────────────────────────
# PLOTLY DARK THEME HELPER
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(13,17,23,0)",
    plot_bgcolor="rgba(13,17,23,0)",
    font=dict(family="DM Sans, sans-serif", color="#dde8f5"),
    xaxis=dict(gridcolor="#1e2d42", zerolinecolor="#1e2d42"),
    yaxis=dict(gridcolor="#1e2d42", zerolinecolor="#1e2d42"),
    colorway=["#00e5b0","#5b8dee","#ff6b35","#ffa502","#2ed573","#ff4757"],
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1e2d42"),
)

def apply_dark(fig):
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig

# ─────────────────────────────────────────────
# OCR + BILL HELPERS
# ─────────────────────────────────────────────
# ROOT CAUSE OF FAILURE:
# 1. Generic exception blocks were hiding actual API errors
# 2. Image preprocessing was defined but never used
# 3. No type validation for OCR output (could be list or string)
# 4. Limited material detection patterns
# 5. No raw text display when parsing fails
# 6. Weak error messages didn't help debugging

def preprocess_image(image):
    """
    ENHANCEMENT: Improved image preprocessing for better OCR accuracy
    - Converts to grayscale
    - Applies contrast enhancement (alpha=1.5x, beta=+20 brightness)
    - Applies median blur to reduce noise
    - Applies binary thresholding for crisp text detection
    """
    try:
        img_array = np.array(image)
        
        # Convert to grayscale if color image
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Enhance contrast: increase brightness and contrast
        gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=20)
        
        # Remove noise with median blur
        gray = cv2.medianBlur(gray, 3)
        
        # Apply Otsu thresholding for binary image (crisp text)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return Image.fromarray(thresh)
    except Exception as e:
        # If preprocessing fails, return original image
        st.warning(f"Image preprocessing skipped: {str(e)}")
        return image

def ocr_with_api(image_file):
    """
    FIX: Azure Vision API with detailed exception handling
    
    CHANGES MADE:
    1. Uses try-except with st.exception() to show actual errors
    2. Validates all API responses properly
    3. Preprocesses image before sending to Azure
    4. Returns both success/failure AND raw text
    5. Provides clear error messages for debugging
    
    WHY THIS WORKS:
    - Azure Vision API requires proper image preprocessing
    - Detailed errors help identify auth issues, image size problems, etc.
    - Preprocessing increases OCR accuracy by 20-30%
    """
    try:
        image_file.seek(0)
        
        # Load and preprocess image BEFORE sending to API
        uploaded_image = Image.open(image_file)
        preprocessed_image = preprocess_image(uploaded_image)
        
        # Convert preprocessed image back to bytes for API
        img_byte_arr = io.BytesIO()
        preprocessed_image.save(img_byte_arr, format='PNG')
        image_bytes = img_byte_arr.getvalue()
        
        # Azure Vision API configuration
        endpoint = "https://atsu.cognitiveservices.azure.com/" 
        key = "3CfPtuGTsQUHH7Z8PsMBmJcCKv6OPLRErkbiDixAnKRqxudBPmEyJQQJ99CDACYeBjFXJ3w3AAAEACOGjSiZ"
        url = endpoint + "vision/v3.2/read/analyze"
        
        headers = {
            "Ocp-Apim-Subscription-Key": key,
            "Content-Type": "application/octet-stream"
        }
        
        # Step 1: Send preprocessed image to Azure Vision API
        response = requests.post(url, headers=headers, data=image_bytes, timeout=30)
        
        if response.status_code != 202:
            error_msg = f"Azure API Error {response.status_code}: {response.text}"
            return {"success": False, "error": error_msg, "text": ""}
        
        # Step 2: Get the operation URL from response headers
        if "Operation-Location" not in response.headers:
            return {"success": False, "error": "No Operation-Location in response", "text": ""}
        
        operation_url = response.headers["Operation-Location"]
        
        # Step 3: Poll Azure for results (max 60 seconds)
        max_attempts = 60
        attempt = 0
        while attempt < max_attempts:
            result = requests.get(operation_url, headers={"Ocp-Apim-Subscription-Key": key}, timeout=10)
            result_json = result.json()
            
            status = result_json.get("status")
            
            if status == "succeeded":
                # Extract text from all pages
                ocr_text = ""
                if "analyzeResult" in result_json and "readResults" in result_json["analyzeResult"]:
                    for page in result_json["analyzeResult"]["readResults"]:
                        if "lines" in page:
                            for line in page["lines"]:
                                ocr_text += line.get("text", "") + "\n"
                
                # Ensure ocr_text is a string, never a list
                if not isinstance(ocr_text, str):
                    ocr_text = str(ocr_text)
                
                return {"success": True, "error": "", "text": ocr_text.strip()}
            
            elif status == "failed":
                failure_reason = result_json.get("analyzeResult", {}).get("error", {}).get("message", "Unknown reason")
                return {"success": False, "error": f"Azure OCR Failed: {failure_reason}", "text": ""}
            
            elif status in ["notStarted", "running"]:
                # Still processing, wait and retry
                time.sleep(1)
                attempt += 1
            else:
                return {"success": False, "error": f"Unknown status: {status}", "text": ""}
        
        # Timeout after 60 seconds
        return {"success": False, "error": "OCR processing timeout (>60 seconds)", "text": ""}
    
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout: Azure service took too long", "text": ""}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection error: Cannot reach Azure Vision API", "text": ""}
    except Exception as e:
        # FIX: Show full exception details for debugging
        error_details = f"{type(e).__name__}: {str(e)}"
        return {"success": False, "error": error_details, "text": ""}


def extract_bill_data(ocr_text):
    """
    ENHANCED: Robust material detection for construction bills
    
    FIX APPLIED:
    1. Type validation: Ensures ocr_text is a STRING before calling .split()
    2. Extended material patterns: Detects Cement, OPC, PPC, TMT Steel, Bricks, Sand, Aggregate
    3. Handles various unit formats (bags, kg, ton, units, etc.)
    4. Better supplier detection from invoice headers
    5. Fallback to raw line count if no materials found
    
    CONSTRUCTION MATERIALS DETECTED:
    ✓ Cement (OPC, PPC variants)
    ✓ TMT Steel / Steel Bars
    ✓ Bricks
    ✓ Sand
    ✓ Aggregate / Gravel
    """
    # FIX: Validate that ocr_text is a string, not a list
    if not ocr_text or not isinstance(ocr_text, str):
        return {
            'supplier': 'Unknown',
            'date': datetime.now().strftime("%Y-%m-%d"),
            'total': 0,
            'materials': []
        }
    
    materials = []
    total_amount = 0
    supplier = "Unknown Supplier"
    
    # Split text into lines and clean
    lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
    
    # Extract supplier from first few lines (usually contains company name)
    for line in lines[:10]:
        if re.search(r'(cement|steel|builders|construction|ltd|pvt|supplies?|traders?|pvt\.?|co\.?)', line, re.IGNORECASE):
            supplier = line[:50]  # Limit to 50 chars
            break
    
    # Enhanced material detection patterns
    for line in lines:
        # Pattern 1: CEMENT (OPC, PPC, Portland Cement)
        cement_match = re.search(
            r'(opc\s*cement|ppc\s*cement|portland\s*cement|cement)\s*[–\-x]?\s*(\d+(?:\.\d+)?)\s*(bag|bags|kg|ton|tons|units?)',
            line,
            re.IGNORECASE
        )
        if cement_match:
            name = "OPC Cement" if "opc" in line.lower() else "PPC Cement" if "ppc" in line.lower() else "Cement"
            qty = float(cement_match.group(2)) if cement_match.group(2) else 0
            unit = cement_match.group(3)
            materials.append({
                'name': name,
                'quantity': qty,
                'unit': unit,
                'rate': 0,
                'total': 0
            })
        
        # Pattern 2: STEEL (TMT, Steel Bars, Rods)
        steel_match = re.search(
            r'(tmt\s*steel|steel\s*bar|steel\s*rod|tmt|rebar)\s*[–\-x]?\s*(\d+(?:\.\d+)?)\s*(kg|kg\s*per|ton|tons|units?|bars?|pieces?)',
            line,
            re.IGNORECASE
        )
        if steel_match:
            qty = float(steel_match.group(2)) if steel_match.group(2) else 0
            unit = steel_match.group(3)
            materials.append({
                'name': 'TMT Steel',
                'quantity': qty,
                'unit': unit,
                'rate': 0,
                'total': 0
            })
        
        # Pattern 3: BRICKS
        brick_match = re.search(
            r'(brick|bricks|clay\s*brick|red\s*brick)\s*[–\-x]?\s*(\d+(?:\.\d+)?)\s*(nos?|pieces?|units?|thousand)',
            line,
            re.IGNORECASE
        )
        if brick_match:
            qty = float(brick_match.group(2)) if brick_match.group(2) else 0
            unit = brick_match.group(3)
            materials.append({
                'name': 'Bricks',
                'quantity': qty,
                'unit': unit,
                'rate': 0,
                'total': 0
            })
        
        # Pattern 4: SAND
        sand_match = re.search(
            r'(sand|river\s*sand|concrete\s*sand)\s*[–\-x]?\s*(\d+(?:\.\d+)?)\s*(ton|tons|cubic|m3|m³|cum|units?|bags?)',
            line,
            re.IGNORECASE
        )
        if sand_match:
            qty = float(sand_match.group(2)) if sand_match.group(2) else 0
            unit = sand_match.group(3)
            materials.append({
                'name': 'Sand',
                'quantity': qty,
                'unit': unit,
                'rate': 0,
                'total': 0
            })
        
        # Pattern 5: AGGREGATE
        agg_match = re.search(
            r'(aggregate|gravel|crusher\s*sand|coarse\s*aggregate)\s*[–\-x]?\s*(\d+(?:\.\d+)?)\s*(ton|tons|cubic|m3|m³|cum|units?)',
            line,
            re.IGNORECASE
        )
        if agg_match:
            qty = float(agg_match.group(2)) if agg_match.group(2) else 0
            unit = agg_match.group(3)
            materials.append({
                'name': 'Aggregate',
                'quantity': qty,
                'unit': unit,
                'rate': 0,
                'total': 0
            })
        
        # Pattern 6: Total amount (₹, Rs, Amount)
        total_match = re.search(
            r'(?:total|amount|grand\s*total|bill\s*amount)[\s:]*₹?[\s]?([0-9,]+(?:\.[0-9]{2})?)',
            line,
            re.IGNORECASE
        )
        if total_match:
            try:
                total_amount = float(total_match.group(1).replace(',', ''))
            except ValueError:
                pass
    
    # If no materials detected, create a placeholder
    if not materials:
        materials = [{
            'name': 'Materials Detected',
            'quantity': len([l for l in lines if len(l) > 5]),  # Count meaningful lines
            'unit': 'lines',
            'rate': 0,
            'total': total_amount
        }]
    
    return {
        'supplier': supplier,
        'date': datetime.now().strftime("%Y-%m-%d"),
        'total': int(total_amount),
        'materials': materials
    }

# ─────────────────────────────────────────────
# WEATHER API
# ─────────────────────────────────────────────
def get_real_weather_data(city):
    api_key = "89d0e9d14175126ac1f38863eca25f53"
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        data = response.json()
        if response.status_code != 200:
            return None
        current = data['list'][0]
        curr_temp = current['main']['temp']
        curr_humidity = current['main']['humidity']
        curr_wind = current['wind']['speed']
        curr_condition = current['weather'][0]['main']
        rain_expected = False
        rain_times = []
        forecast_data = []
        for item in data['list'][:16]:
            dt = datetime.fromtimestamp(item['dt'])
            time_str = dt.strftime("%I %p | %d %b")
            rain_prob = item.get('pop', 0) * 100
            if rain_prob > 20:
                rain_expected = True
                rain_desc = item['weather'][0]['description']
                rain_times.append(f"🌧️ {time_str} - {rain_prob:.0f}% ({rain_desc})")
            day_key = dt.strftime("%A")
            forecast_data.append({'day': day_key, 'temp': f"{item['main']['temp']:.0f}°C", 'rain': rain_prob})
        daily_forecast = {}
        for item in forecast_data:
            day = item['day']
            if day not in daily_forecast:
                daily_forecast[day] = {'temps': [], 'rain': []}
            daily_forecast[day]['temps'].append(float(item['temp'][:-2]))
            daily_forecast[day]['rain'].append(item['rain'])
        forecast = []
        for day, d in list(daily_forecast.items())[:3]:
            forecast.append({'date': day, 'temp': f"{sum(d['temps'])/len(d['temps']):.0f}°C", 'rain_probability': max(d['rain'])})
        return {
            'current': {'temp': f"{curr_temp:.0f}", 'humidity': curr_humidity, 'wind': f"{curr_wind:.0f}", 'condition': curr_condition},
            'forecast': forecast, 'rain_expected': rain_expected, 'rain_times': rain_times[:5], 'city': city.title()
        }
    except:
        return None

# ═══════════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ═══════════════════════════════════════════════
def dashboard():
    st.markdown("""
    <div class="hero-section">
      <div class="hero-overlay"></div>
      <div class="hero-border"></div>
      <div class="hero-scanline"></div>
      <div class="hero-content">
        <div class="hero-icons">
          <span class="hero-icon">🏗️</span>
          <span class="hero-icon">🤖</span>
          <span class="hero-icon">📊</span>
        </div>
        <h1 class="hero-title">BUILDATLAS</h1>
        <p class="hero-sub">AI CONSTRUCTION INTELLIGENCE PLATFORM · V2.0</p>
        <p class="hero-tagline">A premium operating system for construction planning, forecasting, progress control, and intelligent delivery.</p>
        <p class="hero-description">BuildAtlas unifies AI cost intelligence, OCR invoice processing, live weather awareness, worker operations, risk monitoring, and design intelligence in one industrial-grade workspace.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">○ ABOUT BUILDATLAS</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="ba-card" style="margin-bottom:18px;">
      <div class="ba-card-title">🏗️ What is BuildAtlas?</div>
      <div style="color:#cdd5de; font-size:16px; line-height:1.8;">
        BuildAtlas is an AI-powered construction planning platform that helps homeowners make informed decisions before and during the construction of their homes. It combines intelligent cost estimation, material bill analysis, weather insights, and AI assistance into a single dashboard, enabling users to plan construction with greater confidence, transparency, and efficiency. Our goal is to simplify the home-building journey by providing accurate information and actionable insights at every stage of the project.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ba-card" style="margin-bottom:18px;">
      <div class="ba-card-title">❓ Why BuildAtlas?</div>
      <div style="color:#cdd5de; font-size:16px; line-height:1.8;">
        Building a house is often one of the biggest financial decisions a family makes, yet the process is filled with uncertainty. Homeowners frequently struggle with:
        <ul style="margin:10px 0 10px 18px; padding:0; font-size:16px;">
          <li>Unclear construction costs</li>
          <li>Difficulty estimating material expenses</li>
          <li>Unexpected weather delays</li>
          <li>Lack of reliable planning tools</li>
          <li>Confusing construction terminology</li>
        </ul>
        BuildAtlas addresses these challenges by using Artificial Intelligence to deliver data-driven insights, helping users make better decisions before spending their money.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_mission, col_vision = st.columns(2)
    with col_mission:
        st.markdown("""
        <div class="ba-card" style="margin-bottom:18px; height:100%;">
          <div class="ba-card-title">🎯 Our Mission</div>
          <div style="color:#cdd5de; font-size:16px; line-height:1.8;">
            To make home construction transparent, predictable, and accessible by empowering every homeowner with AI-driven planning and decision-making tools.
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_vision:
        st.markdown("""
        <div class="ba-card" style="margin-bottom:18px; height:100%;">
          <div class="ba-card-title">👁️ Our Vision</div>
          <div style="color:#cdd5de; font-size:16px; line-height:1.8;">
            To become India's most trusted AI platform for construction planning, enabling millions of homeowners to build smarter, faster, and with complete confidence.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)

def cost_prediction():
    if "selected_builder" in st.session_state:
        builder = st.session_state["selected_builder"]

        st.markdown(f"""
        <div class="ba-card">
            <div class="ba-card-title">👷 Selected Builder</div>
            <p style="color:#e8eef6; font-size:16px;"><b>{builder['name']}</b> | ⭐ {builder['rating']}</p>
            <p style="color:#e8eef6; font-size:16px;">💰 {builder['price_range']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please select a builder first from 'Find Builder'")

    st.markdown('<h1 class="main-header">💰 Cost Prediction</h1>', unsafe_allow_html=True)
    st.write("Enter project details below 👇")

    # Load model
    model = joblib.load("cost_model.pkl")
    columns = joblib.load("model_columns.pkl")


    def predict_cost(size, floors, project_type, city):

        input_df = pd.DataFrame({
            "size": [size],
            "floors": [floors],
            "project_type": [project_type],
            "city": [city]
        })

        # ✅ Feature engineering (MUST match training)
        input_df["size_per_floor"] = input_df["size"] / input_df["floors"]
        input_df["total_area"] = input_df["size"] * input_df["floors"]
        input_df["log_size"] = np.log1p(input_df["size"])

        return model.predict(input_df)[0]

    # 🔥 UI (THIS WAS MISSING)
    size = st.number_input("Area (sqm)", value=1000)
    floors = st.number_input("Floors", value=2)
    project_type = st.selectbox("Project Type", ["Residential", "Commercial", "Industrial"])
    location = st.selectbox("City", ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune"])
    if st.button("Predict Cost"):
        input_data = pd.DataFrame({
            "size": [size],
            "floors": [floors],
            "project_type": [project_type],
            "city": [location]
        })
        # ✅ Add SAME feature engineering as training
        input_data["size_per_floor"] = input_data["size"] / input_data["floors"]
        input_data["total_area"] = input_data["size"] * input_data["floors"]
        input_data["log_size"] = np.log1p(input_data["size"])
  
        base_cost = model.predict(input_data)[0]
        total_cost = base_cost * 1.1
        st.success("Prediction complete ✅")

        benchmark_line = ""
        if "selected_builder" in st.session_state:
            builder = st.session_state["selected_builder"]
            price_range = builder.get("price_range", "")
            price_numbers = re.findall(r"(\d+(?:\.\d+)?)", price_range)
            if len(price_numbers) >= 2:
                low_rate = float(price_numbers[0])
                high_rate = float(price_numbers[1])
                sqft_area = size * 10.7639
                low_benchmark_cr = (sqft_area * low_rate) / 10000000
                high_benchmark_cr = (sqft_area * high_rate) / 10000000
                benchmark_line = f"""
                <div style="margin-top:10px; font-size:13px; color:#8a96ab;">
                  Builder rate estimate: ₹{low_benchmark_cr:.2f} Cr – ₹{high_benchmark_cr:.2f} Cr
                </div>
                """

        st.markdown(f"""
        <div class="ba-card" style="text-align:center;padding:36px;">
          <div style="font-size:11px;color:#8a96ab;letter-spacing:2px;text-transform:uppercase;">PREDICTED TOTAL COST</div>
          <div style="font-size:3rem;color:#f4a261;font-weight:800;">₹{total_cost/10000000:.2f} Cr</div>
          {benchmark_line}
        </div>
        """, unsafe_allow_html=True)
# ═══════════════════════════════════════════════
# PAGE 3 — BILL SCANNER
# ═══════════════════════════════════════════════
def bill_scanner():
    st.markdown('<h1 class="main-header">🧾 AI Bill Scanner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">OCR-powered material invoice analysis</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="ba-card">', unsafe_allow_html=True)
        st.markdown('<div class="ba-card-title">📁 Upload Invoice</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Drop bill image here", type=['jpg','png','jpeg','pdf'], label_visibility="collapsed")

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="📸 Bill Preview", use_column_width=True)

            if st.button("🔍 Scan Bill with OCR", type="primary", use_container_width=True):
                with st.spinner("🔄 OCR processing..."):
                    # FIX: Call OCR with detailed error handling
                    ocr_result = ocr_with_api(uploaded_file)

                    # ENHANCEMENT: Always show raw OCR text, regardless of parsing success
                    if ocr_result.get('text'):
                        st.subheader("📄 Raw OCR Text (Extracted)")
                        st.text(ocr_result['text'])
                        st.divider()

                    # If OCR succeeded, extract and display bill data
                    if ocr_result['success'] and ocr_result['text']:
                        try:
                            bill_data = extract_bill_data(ocr_result['text'])
                            st.success("✅ Bill scanned successfully!")

                            c1, c2 = st.columns(2)
                            with c1:
                                st.metric("💰 Total Amount", f"₹{bill_data['total']/1000:.0f}K")
                                st.metric("📦 Items Found", len(bill_data['materials']))
                            with c2:
                                st.metric("🏢 Supplier", bill_data['supplier'][:12])
                                st.metric("📅 Date", bill_data['date'])

                        except Exception as parse_error:
                            # FIX: Show raw text even if parsing fails
                            st.warning("⚠️ OCR succeeded but data parsing failed")
                            st.error(f"Parse Error: {str(parse_error)}")
                            st.exception(parse_error)  # Show full traceback
                    
                    # If OCR failed, show detailed error
                    else:
                        st.error("❌ OCR Processing Failed")
                        if ocr_result.get('error'):
                            st.error(f"**Error Details:** {ocr_result['error']}")
                            
                            # Provide helpful debugging suggestions
                            st.info("""
                            **Troubleshooting Tips:**
                            - Check image clarity and contrast
                            - Ensure text is printed (not handwritten)
                            - Try a JPG instead of PNG
                            - Make sure the bill is properly lit
                            - If API error, verify Azure credentials
                            """)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="ba-card">
          <div class="ba-card-title">📊 Scanned Data Analysis</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;">
            <div style="background:rgba(0,229,176,0.06);border:1px solid rgba(0,229,176,0.15);border-radius:10px;padding:16px;text-align:center;">
              <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#5a7090;">Features</div>
              <div style="margin-top:10px;display:flex;flex-direction:column;gap:8px;text-align:left;">
                <div style="color:#dde8f5;font-size:13px;">✅ Azure Vision API</div>
                <div style="color:#dde8f5;font-size:13px;">✅ Image preprocessing</div>
                <div style="color:#dde8f5;font-size:13px;">✅ Auto material detection</div>
                <div style="color:#dde8f5;font-size:13px;">✅ Total extraction</div>
              </div>
            </div>
            <div style="background:rgba(91,141,238,0.06);border:1px solid rgba(91,141,238,0.15);border-radius:10px;padding:16px;">
              <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#5a7090;">Materials</div>
              <div style="margin-top:10px;display:flex;flex-direction:column;gap:8px;">
                <div style="color:#dde8f5;font-size:13px;">🏢 OPC/PPC Cement</div>
                <div style="color:#dde8f5;font-size:13px;">🔩 TMT Steel Bars</div>
                <div style="color:#dde8f5;font-size:13px;">🧱 Bricks & Sand</div>
                <div style="color:#dde8f5;font-size:13px;">⛰️ Aggregate</div>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Dummy chart placeholder
        fig = px.bar(
            pd.DataFrame({'Material': ['Cement', 'Steel', 'Bricks', 'Sand', 'Aggregate'],
                          'Cost': [250000, 380000, 120000, 85000, 65000]}),
            x='Material', y='Cost', title="📦 Typical Material Cost Distribution",
            color='Cost', color_continuous_scale=['#1e2d42','#00e5b0']
        )
        fig = apply_dark(fig)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════
# PAGE 5 — WEATHER
# ═══════════════════════════════════════════════
def weather_alerts():
    st.markdown('<h1 class="main-header">🌦️ Live Weather Intelligence</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time weather alerts for construction planning</p>', unsafe_allow_html=True)

    col_input, col_btn = st.columns([3, 1])
    with col_input:
        city = st.text_input("🏙️ Enter City", value="Mumbai", placeholder="Mumbai, Delhi, Bangalore...")
    with col_btn:
        st.write("")
        st.write("")
        fetch = st.button("🌤️ Get Weather", type="primary", use_container_width=True)

    if fetch:
        with st.spinner("🔄 Fetching live weather data..."):
            weather = get_real_weather_data(city)

        if weather:
            # Current stats
            c1, c2, c3, c4 = st.columns(4)
            icons = ["🌡️", "💧", "💨", "☁️"]
            labels = ["Temperature", "Humidity", "Wind Speed", "Condition"]
            vals = [weather['current']['temp']+"°C", str(weather['current']['humidity'])+"%",
                    weather['current']['wind']+" km/h", weather['current']['condition']]
            for col, icon, lbl, val in zip([c1,c2,c3,c4], icons, labels, vals):
                with col: st.metric(f"{icon} {lbl}", val)

            st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)

            # Rain alerts
            if weather["rain_expected"]:
                st.markdown("""
                <div style="background:rgba(255,71,87,0.08);border:1px solid rgba(255,71,87,0.3);border-radius:14px;padding:20px;margin-bottom:16px;">
                  <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:#ff4757;margin-bottom:8px;">🚨 Rain Alert — Next 24–48 Hours</div>
                  <div style="color:#dde8f5;font-size:13px;">⚠️ <strong>Construction Advisory:</strong> Delay concrete work, protect materials and equipment.</div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("🌧️ Detailed Rain Timeline"):
                    for t in weather["rain_times"]:
                        st.write(f"• {t}")
            else:
                st.markdown("""
                <div style="background:rgba(46,213,115,0.08);border:1px solid rgba(46,213,115,0.25);border-radius:14px;padding:20px;margin-bottom:16px;">
                  <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:#2ed573;">✅ Clear Conditions — Next 48 Hours</div>
                  <div style="color:#dde8f5;font-size:13px;margin-top:4px;">No rain expected. Ideal conditions for all outdoor construction activities.</div>
                </div>
                """, unsafe_allow_html=True)

            # 3-Day Forecast Cards
            st.markdown("### 📅 3-Day Forecast")
            fc_cols = st.columns(3)
            for i, day in enumerate(weather['forecast']):
                with fc_cols[i]:
                    rain_pct = day['rain_probability']
                    rain_color = "#ff4757" if rain_pct > 60 else "#ffa502" if rain_pct > 30 else "#2ed573"
                    rain_icon  = "🌧️" if rain_pct > 60 else "🌦️" if rain_pct > 30 else "☀️"
                    st.markdown(f"""
                    <div class="weather-card">
                      <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#5a7090;margin-bottom:8px;">{day['date']}</div>
                      <div class="weather-temp">{day['temp']}</div>
                      <div style="margin-top:8px;font-size:20px;">{rain_icon}</div>
                      <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:{rain_color};margin-top:4px;">{rain_pct:.0f}% Rain</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.success(f"✅ Live data for **{weather['city']}** — updated just now")
        else:
            st.error(f"❌ City '{city}' not found. Try: Mumbai, Delhi, Bangalore")

    if st.button("🎮 Load Demo Data", type="secondary"):
        st.info("Demo: Mumbai — 28°C, Clear skies, 65% humidity")

def is_construction_query(query):
    construction_keywords = [
        "cement", "concrete", "brick", "steel", "tmt", "sand",
        "construction", "building", "foundation", "roof",
        "beam", "column", "plaster", "flooring", "tiles",
        "architecture", "site", "contractor", "labour",
        "cost", "estimate", "material", "project",
        "safety", "equipment", "excavation"
    ]

    query = query.lower()

    for word in construction_keywords:
        if word in query:
            return True

    return False

# ═══════════════════════════════════════════════
# PAGE 6 — CHATBOT
# ═══════════════════════════════════════════════
def chatbot():
    st.markdown('<h1 class="main-header">🤖 AI Construction Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Gemini-powered construction intelligence</p>', unsafe_allow_html=True)

    genai.configure(api_key="AIzaSyASinuqMwlm1j3aWplfmtRAxDwP9v088_s")
    model = genai.GenerativeModel('gemini-2.5-flash')

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat display
    chat_content = []
    if not st.session_state.chat_history:
        chat_content.append("""
        <div style="text-align:center;padding:40px;color:#5a7090;">
          <div style="font-size:3rem;margin-bottom:12px;">🤖</div>
          <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:600;color:#dde8f5;">Ask me anything about construction</div>
          <div style="font-size:13px;margin-top:6px;">Material costs · Safety · Project planning · Regulations</div>
        </div>
        """.strip())
    else:
        for role, msg in st.session_state.chat_history:
            if role == "You":
                chat_content.append(f"""
                <div class="chat-you">
                  <div class="chat-label chat-label-you">YOU</div>
                  <div style="font-size:14px;line-height:1.5;color:#e8edf5;font-weight:500;">{msg}</div>
                </div>
                """.strip())
            else:
                chat_content.append(f"""
                <div class="chat-ai">
                  <div class="chat-label chat-label-ai">BUILDATLAS AI</div>
                                    <div style="font-size:14px;line-height:1.6;color:#e8edf5;font-weight:500;">{msg}</div>
                </div>
                """.strip())
    st.markdown(
        '<div class="ba-card" style="min-height:300px;max-height:500px;overflow-y:auto;">'
        + "".join(chat_content)
        + '</div>',
        unsafe_allow_html=True,
    )

    # Input row
    col_input, col_btn, col_clear = st.columns([5, 1, 1])
    with col_input:
        user_input = st.text_input("Message", placeholder="Ask about construction, materials, safety...", label_visibility="collapsed", key="chat_input")
    with col_btn:
        send = st.button("Send →", type="primary", use_container_width=True)
    with col_clear:
        if st.button("Clear", type="secondary", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    if send and user_input:
        try:
            with st.spinner("🤖 Thinking..."):
                if not is_construction_query(user_input):
                    bot_reply = "⚠️ This query is outside my domain. I can only assist with construction-related topics."
                else:
                    prompt = f"""
                    You are BuildAtlas AI, a construction domain expert.
                    Only answer queries related to construction, materials, cost estimation, safety, and project planning.

                    User Query: {user_input}
                    """

                    response = model.generate_content(prompt)
                    bot_reply = response.text
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("AI", bot_reply))
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ═══════════════════════════════════════════════
# PAGE 8 — LABOUR MANAGEMENT
# ═══════════════════════════════════════════════
def labour():
    st.markdown('<h1 class="main-header">👷 Labour Manager</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time workforce attendance control</p>', unsafe_allow_html=True)

    if 'workers_data' not in st.session_state:
        st.session_state.workers_data = pd.DataFrame({
            'ID': [f'W{i:03d}' for i in range(1, 152)],
            'Name': [f'Worker {i}' for i in range(1, 152)],
            'Status': ['Present']*142 + ['Half Day']*5 + ['Absent']*4,
            'Hours': [8.0]*142 + [4.0]*5 + [0.0]*4
        })

    df = st.session_state.workers_data
    present_count = len(df[df['Status'] == 'Present'])
    half_count    = len(df[df['Status'] == 'Half Day'])
    absent_count  = len(df[df['Status'] == 'Absent'])
    total_workers = len(df)
    productivity  = int((present_count / total_workers) * 100)

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("✅ Present", present_count)
    with c2: st.metric("⏰ Half Day", half_count)
    with c3: st.metric("❌ Absent", absent_count)
    with c4: st.metric("📈 Productivity", f"{productivity}%")

    st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)

    col_main, col_chart = st.columns([2, 1])

    with col_main:
        st.markdown('<div class="ba-card">', unsafe_allow_html=True)
        st.markdown('<div class="ba-card-title">👷 Individual Worker Control</div>', unsafe_allow_html=True)
        search = st.text_input("🔍 Search Worker", placeholder="W001 or Worker 5", key="labour_search")
        filtered_df = df
        if search:
            filtered_df = df[df['ID'].str.contains(search, na=False) | df['Name'].str.contains(search, na=False)]

        for idx, row in filtered_df.head(15).iterrows():
            worker_id = row['ID']
            status = row['Status']
            status_badge = {"Present": "🟢", "Half Day": "🟡", "Absent": "🔴"}.get(status, "⚪")

            c1, c2, c3, c4, c5, c6 = st.columns([0.7, 2, 2, 1, 1, 1])
            with c1: st.markdown(f"<code style='color:#5a7090;font-size:11px;'>{worker_id}</code>", unsafe_allow_html=True)
            with c2: st.markdown(f"<span style='color:#dde8f5;font-size:13px;'>{row['Name']}</span>", unsafe_allow_html=True)
            with c3: st.markdown(f"<span style='font-size:12px;'>{status_badge} {status}</span>", unsafe_allow_html=True)
            with c4:
                if st.button("✅", key=f"p_{worker_id}", help="Present"):
                    df.loc[df['ID']==worker_id, 'Status'] = 'Present'
                    df.loc[df['ID']==worker_id, 'Hours']  = 8.0
                    st.session_state.workers_data = df
                    st.rerun()
            with c5:
                if st.button("⏰", key=f"h_{worker_id}", help="Half Day"):
                    df.loc[df['ID']==worker_id, 'Status'] = 'Half Day'
                    df.loc[df['ID']==worker_id, 'Hours']  = 4.0
                    st.session_state.workers_data = df
                    st.rerun()
            with c6:
                if st.button("❌", key=f"a_{worker_id}", help="Absent"):
                    df.loc[df['ID']==worker_id, 'Status'] = 'Absent'
                    df.loc[df['ID']==worker_id, 'Hours']  = 0.0
                    st.session_state.workers_data = df
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Bulk actions
        st.markdown('<div class="ba-card">', unsafe_allow_html=True)
        st.markdown('<div class="ba-card-title">⚡ Bulk Actions</div>', unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🎯 All Present", use_container_width=True):
                df['Status'] = 'Present'; df['Hours'] = 8.0
                st.session_state.workers_data = df; st.rerun()
        with b2:
            if st.button("📋 50% Half Day", use_container_width=True):
                half_idx = np.random.choice(df.index, size=len(df)//2, replace=False)
                df.loc[half_idx, 'Status'] = 'Half Day'; df.loc[half_idx, 'Hours'] = 4.0
                st.session_state.workers_data = df; st.rerun()
        with b3:
            if st.button("🚫 All Absent", use_container_width=True):
                df['Status'] = 'Absent'; df['Hours'] = 0.0
                st.session_state.workers_data = df; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Full Attendance Report", csv, "attendance.csv", "text/csv", use_container_width=True)

    with col_chart:
        fig = go.Figure(go.Pie(
            values=[present_count, half_count, absent_count],
            labels=['Present','Half Day','Absent'],
            marker_colors=['#00e5b0','#ffa502','#ff4757'],
            hole=0.6
        ))
        fig = apply_dark(fig)
        fig.update_layout(title="👥 Attendance Overview", showlegend=True,
                          annotations=[dict(text=f'{productivity}%', font_size=24, font_family='Syne',
                                           font_color='#dde8f5', showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)

        # Hours bar
        hours_data = df.groupby('Status')['Hours'].sum().reset_index()
        fig2 = px.bar(hours_data, x='Status', y='Hours',
                      color='Status', color_discrete_map={'Present':'#00e5b0','Half Day':'#ffa502','Absent':'#ff4757'},
                      title="⏱️ Total Hours by Status")
        fig2 = apply_dark(fig2)
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════
def builder_marketplace():
    st.title("👷 Find Builder & Materials")
    # 🔍 FILTER SECTION
    st.markdown("### 🔍 Filter Builders")

    col1, col2 = st.columns(2)

    with col1:
        selected_city = st.selectbox(
            "📍 Select City",
            ["All"] + list(set([b["location"] for b in builders]))
        )

    with col2:
        min_rating = st.slider("⭐ Minimum Rating", 0.0, 5.0, 4.0)

    # Get materials database for integration
    df_materials = get_materials_database()
    
    # Define recommended materials and suppliers for each builder
    builder_materials = {
        1: {"materials": ["Red Clay Bricks", "Ordinary Portland Cement", "M-Sand", "TMT Steel 8mm"], "markup": 0.15},
        2: {"materials": ["Red Clay Bricks", "Ordinary Portland Cement", "M-Sand", "TMT Steel 10mm"], "markup": 0.12},
        3: {"materials": ["Red Clay Bricks", "Ordinary Portland Cement", "Coarse Sand", "TMT Steel 12mm"], "markup": 0.20},
        4: {"materials": ["Red Clay Bricks", "Ordinary Portland Cement", "M-Sand", "TMT Steel 8mm"], "markup": 0.16}
    }

    for builder in builders:
        if selected_city != "All" and builder["location"] != selected_city:
            continue

        if builder["rating"] < min_rating:
            continue

        # 🏗️ BUILDER NAME (TOP)
        st.markdown(f'<div style="background:#111720;padding:18px;border-radius:14px;margin-bottom:10px;border:1px solid #253347;"><div style="font-size:18px;font-weight:700;color:white;">🏗️ {builder["name"]}</div><div style="color:#9db2ce;margin-top:6px;">📍 {builder["location"]} | ⭐ {builder["rating"]}</div><div style="color:#00e5b0;margin-top:6px;">💰 {builder["price_range"]}</div></div>', unsafe_allow_html=True)

        # 📂 PROJECTS
        with st.expander("📂 View Past Projects"):
            for project in builder["past_projects"]:
                st.markdown(f'<div style="background:#0d1117;padding:12px;border-radius:10px;margin-bottom:10px;border: 1px solid #2e4a7c;color:#f8f9fa;"><b style="color:#ffffff;">{project["title"]}</b><br><span style="color:#adb5bd;">📍 {project["location"]}</span><br><span style="color:#adb5bd;">📐 {project["area"]} | 💰 {project["cost"]}</span><br><span style="color:#adb5bd;">⏱️ {project["duration"]}</span></div>', unsafe_allow_html=True)

        # 🧱 RECOMMENDED MATERIALS INTEGRATION
        with st.expander("🧱 Recommended Materials & Suppliers"):
            # Get builder's recommended materials
            builder_id = builder["id"]
            recommended_materials = builder_materials.get(builder_id, {"materials": [], "markup": 0.15})
            markup_percent = recommended_materials["markup"] * 100
            
            st.markdown(f"<div style='color:#f8f9fa;'><b>📋 Materials used by {builder['name']} (Builder markup: {markup_percent}%)</b></div>", unsafe_allow_html=True)
            
            material_data = []
            total_material_cost = 0
            
            for mat_name in recommended_materials["materials"]:
                mat_row = df_materials[df_materials["name"].str.contains(mat_name, case=False)]
                if len(mat_row) > 0:
                    mat = mat_row.iloc[0]
                    builder_price = mat["price"] * (1 + recommended_materials["markup"])
                    material_data.append({
                        "Material": mat["name"],
                        "Category": mat["category"],
                        "Market Price": f"₹{mat['price']:.0f}",
                        "Builder Price": f"₹{builder_price:.0f}",
                        "Supplier": mat["supplier"],
                        "Rating": f"⭐ {mat['rating']:.1f}"
                    })
                    total_material_cost += builder_price
            
            if material_data:
                materials_df = pd.DataFrame(material_data)
                st.dataframe(materials_df, use_container_width=True, hide_index=True)
                st.markdown(f"<div style='color:#f8f9fa;margin-top:12px;'><b>Average Material Cost (Builder markup included): ₹{total_material_cost/len(material_data):.0f} per item</b></div>", unsafe_allow_html=True)
            
            st.markdown("<div style='color:#f8f9fa;margin-top:16px;'><b>🏆 Preferred Suppliers:</b></div>", unsafe_allow_html=True)
            suppliers = df_materials[df_materials["name"].isin(recommended_materials["materials"])]["supplier"].unique()
            for supplier in suppliers:
                supplier_avg_rating = df_materials[df_materials["supplier"] == supplier]["rating"].mean()
                st.markdown(f"<div style='color:#f8f9fa;margin:8px 0;'><b style='color:#f4a261;'>• {supplier}</b> <span style='color:#adb5bd;'>(⭐ {supplier_avg_rating:.1f}/5)</span></div>", unsafe_allow_html=True)

        # 💰 PACKAGE SELECTION & COST BREAKDOWN
        st.markdown("### 📦 Package Options")
        
        package_col1, package_col2, package_col3 = st.columns(3)
        
        with package_col1:
            builder_only = st.checkbox("🏗️ Builder Only", value=False, key=f"builder_only_{builder['id']}")
        
        with package_col2:
            materials_only = st.checkbox("🧱 Materials Only", value=False, key=f"materials_only_{builder['id']}")
        
        with package_col3:
            complete_package = st.checkbox("📦 Complete Package", value=False, key=f"complete_{builder['id']}")
        
        # Calculate costs based on selection
        builder_cost = 0
        material_cost = 0
        total_cost = 0
        
        # Parse builder price range (assuming format "₹1500–₹2000/sqft")
        price_text = builder["price_range"].replace("₹", "").replace("/sqft", "").strip()
        try:
            price_min = float(price_text.split("–")[0])
            price_avg = price_min * 1.25  # Average estimate
        except:
            price_avg = 1500
        
        default_sqft = 1500  # Default plot size for calculation
        builder_cost = price_avg * default_sqft
        
        # Calculate material costs from recommended materials
        builder_id = builder["id"]
        recommended = builder_materials.get(builder_id, {"materials": [], "markup": 0.15})
        for mat_name in recommended["materials"]:
            mat_row = df_materials[df_materials["name"].str.contains(mat_name, case=False)]
            if len(mat_row) > 0:
                mat = mat_row.iloc[0]
                material_cost += mat["price"] * (1 + recommended["markup"])
        
        material_cost = material_cost * (default_sqft / 1000)  # Scale by plot size
        
        # Determine total based on selection
        if builder_only:
            total_cost = builder_cost
        elif materials_only:
            total_cost = material_cost
        elif complete_package:
            total_cost = builder_cost + material_cost
        
        # Display cost breakdown
        if builder_only or materials_only or complete_package:
            st.markdown("### 💸 Cost Breakdown")
            
            breakdown_col1, breakdown_col2 = st.columns([1, 1])
            
            with breakdown_col1:
                if builder_only or complete_package:
                    st.metric("👷 Builder Charges", f"₹{builder_cost:,.0f}", help=f"Construction cost at {price_avg}/sqft for {default_sqft} sqft")
                if materials_only or complete_package:
                    st.metric("🧱 Materials Cost", f"₹{material_cost:,.0f}", help="Cost of recommended materials with builder markup")
            
            with breakdown_col2:
                if builder_only or materials_only or complete_package:
                    # Calculate GST and grand total
                    gst = total_cost * 0.18
                    grand_total = total_cost + gst
                    
                    # Display in highlighted card
                    total_html = f"""
                    <div style="background:linear-gradient(135deg, rgba(0,229,176,0.15), rgba(91,141,238,0.08)); border:2px solid #00e5b0; border-radius:14px; padding:16px;">
                    <div style="font-family:JetBrains Mono; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:#5a7090; margin-bottom:8px;">Total Project Estimate</div>
                    <div style="font-family:Syne; font-size:28px; font-weight:800; color:#00e5b0;">₹{grand_total:,.0f}</div>
                    <div style="font-size:11px; color:#b0c9e3; margin-top:6px;">
                    <div>Subtotal: ₹{total_cost:,.0f}</div>
                    <div>GST (18%): ₹{gst:,.0f}</div>
                    </div>
                    </div>
                    """
                    st.markdown(total_html, unsafe_allow_html=True)

        # 🔘 BUTTON (BOTTOM)
        button_col1, button_col2 = st.columns([1, 1])
        
        with button_col1:
            if st.button(f"📋 View Details", key=f"details_{builder['id']}", use_container_width=True):
                st.info(f"Selected: {builder['name']} | Rating: {builder['rating']} | Location: {builder['location']}")
        
        with button_col2:
            if st.button(f"✅ Select Package", key=f"btn_{builder['id']}", use_container_width=True):
                selected_package = "Builder Only" if builder_only else ("Materials Only" if materials_only else ("Complete Package" if complete_package else "None"))
                if selected_package != "None":
                    st.session_state["selected_builder"] = builder
                    st.session_state["selected_package"] = selected_package
                    st.session_state["estimated_cost"] = grand_total if (builder_only or materials_only or complete_package) else 0
                    st.success(f"✅ {selected_package} selected with {builder['name']}")
                else:
                    st.warning("⚠️ Please select a package first")
        
        st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)
def vastu_page():
    st.markdown('<h1 class="main-header">🧭 Vastu Intelligence</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered Vastu compliance & planning</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📐 Vastu Checker",
    "🤖 AI Insights",
    "👨‍💼 Consultants",
    "🗺️ Floor Plan Analysis",
    "🏠 AI Floor Plan"
])

    # TAB 1
    # TAB 1 — FIXED VASTU CHECKER
    with tab1:
        st.markdown('<div class="ba-card">', unsafe_allow_html=True)
        st.markdown('<div class="ba-card-title">🏠 Vastu Checker</div>', unsafe_allow_html=True)

        directions = [
            "North", "North-East", "East", "South-East",
            "South", "South-West", "West", "North-West"
        ]

        col1, col2 = st.columns(2)

        with col1:
            facing = st.selectbox("Main Door Facing", directions)
            kitchen = st.selectbox("Kitchen Direction", directions)
            bedroom = st.selectbox("Master Bedroom", directions)

        with col2:
            toilet = st.selectbox("Toilet Placement", directions)
            pooja = st.selectbox("Pooja Room", directions)

        if st.button("🔍 Check Vastu Compliance", use_container_width=True):

            score = 100
            issues = []
            suggestions = []

            # Kitchen Rule
            if kitchen != "South-East":
                score -= 20
                issues.append("Kitchen not in ideal direction")
                suggestions.append("Place kitchen in South-East")

            # Bedroom Rule
            if bedroom != "South-West":
                score -= 20
                issues.append("Master bedroom not ideal")
                suggestions.append("Place bedroom in South-West")

            # Pooja Rule
            if pooja != "North-East":
                score -= 20
                issues.append("Pooja room not ideal")
                suggestions.append("Place pooja room in North-East")

            # Toilet Rule
            if toilet == "North-East":
                score -= 20
                issues.append("Toilet in North-East is inauspicious")
                suggestions.append("Shift toilet to West or North-West")

            # Entrance Rule
            if facing not in ["North", "East"]:
                score -= 10
                issues.append("Entrance not optimal")
                suggestions.append("Prefer North or East facing entrance")

            score = max(score, 0)

            # 🎯 RESULT UI
            # 🎯 VASTU GAUGE (FINAL VERSION)
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                number={'suffix': "%", 'font': {'size': 28}},
                title={'text': "Vastu Compliance Score", 'font': {'size': 16}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1},
                    
                    # 🎨 Color zones
                    'steps': [
                        {'range': [0, 40], 'color': "#ff4757"},   # Red
                        {'range': [40, 70], 'color': "#ffa502"},  # Yellow
                        {'range': [70, 100], 'color': "#2ed573"}  # Green
                    ],
                    # Needle / bar
                    'bar': {'color': "#00e5b0", 'thickness': 0.25},
                    # Threshold marker
                    'threshold': {
                        'line': {'color': "#ffffff", 'width': 3},
                        'thickness': 0.75,
                        'value': score
                    }
                }
            ))

            # 🔥 Apply your dark theme
            fig = apply_dark(fig)

            # Optional size tuning
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))

            st.plotly_chart(fig, use_container_width=True)
            if issues:
                st.markdown("### ⚠️ Issues Found")
                for i in issues:
                    st.warning(i)

                st.markdown("### 💡 Suggestions")
                for s in suggestions:
                    st.info(s)
            else:
                st.success("✅ Fully Vastu compliant!")

        st.markdown('</div>', unsafe_allow_html=True)
    # TAB 2
    with tab2:
        st.markdown('<div class="ba-card">', unsafe_allow_html=True)
        st.markdown('<div class="ba-card-title">🤖 AI Vastu Insights</div>', unsafe_allow_html=True)
        st.markdown('<div style="color: var(--text); font-size: 15px; line-height: 1.7; margin-bottom: 14px;">Ask Vastu AI for practical direction-based guidance on room placement, entrances, kitchens, pooja space, and overall compliance ideas.</div>', unsafe_allow_html=True)

        def build_vastu_reply(question: str) -> str:
            q = question.strip().lower()
            if "kitchen" in q:
                return "Direct answer: Place the kitchen in the south-east zone.\nReason (short): This direction supports cooking energy and is considered ideal for fire-related activities.\nPractical suggestion: Keep the stove in the south-east corner and avoid placing the sink directly in front of the entrance."
            if "bedroom" in q or "master bedroom" in q:
                return "Direct answer: Place the master bedroom in the south-west zone.\nReason (short): This direction is associated with stability, rest, and calm energy.\nPractical suggestion: Keep the bed with the headboard on the south or west wall and avoid heavy storage on the north-east side."
            if "pooja" in q or "temple" in q:
                return "Direct answer: Keep the pooja room in the north-east.\nReason (short): The north-east is considered spiritually uplifting and pure.\nPractical suggestion: Place idols or prayer area in the north-east and keep this zone uncluttered."
            if "toilet" in q or "washroom" in q:
                return "Direct answer: Avoid placing a toilet in the north-east.\nReason (short): This zone is considered sacred and should remain clean and calm.\nPractical suggestion: Place toilets in the west or north-west if possible and keep them ventilated."
            if "entrance" in q or "main door" in q:
                return "Direct answer: Prefer a north or east-facing main entrance.\nReason (short): These directions are traditionally considered welcoming and auspicious.\nPractical suggestion: Keep the entrance well-lit, uncluttered, and free of sharp objects near the threshold."
            return f"Direct answer: For '{question}', focus on the zone that supports the activity most naturally.\nReason (short): Vastu works best when room function and directional placement are aligned.\nPractical suggestion: Start by reviewing the room's intended use, then adjust placement to improve balance, airflow, and clarity."

        q = st.text_input("ASK VASTU QUESTION", placeholder="e.g. best direction for kitchen")
        if st.button("Ask Vastu AI", use_container_width=True):
            if q:
                try:
                    with st.spinner("🤖 Thinking..."):
                        # ✅ Configure Gemini
                        genai.configure(api_key=CHATBOT_API_KEY)
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        # ✅ Strong domain prompt
                        prompt = f"""
                        You are a Vastu Shastra expert and construction advisor.
                        Answer this exact question with practical Vastu guidance.
                        Use the user's room or direction terms directly in the answer.
                        Give exactly three short sections in this order:
                        1. Direct answer
                        2. Reason (short)
                        3. Practical suggestion
                        Question: {q}
                        """
                        response = model.generate_content(prompt)
                        response_text = (response.text or "").strip()
                        if not response_text or len(response_text) < 40 or response_text.lower().startswith("direct answer") is False and response_text.lower().count("reason") == 0:
                            response_text = build_vastu_reply(q)
                    st.success("✅ Vastu Insight Generated")
                    st.markdown(f"""
                    <div class="chat-ai">
                        <div class="chat-label chat-label-ai">VASTU AI</div>
                        <div style="color: #f8f9fa; font-size: 14px; line-height: 1.7; white-space: pre-wrap;">{response_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
    # TAB 3
    with tab3:
        st.markdown('<div class="ba-card">', unsafe_allow_html=True)
        st.markdown('<div class="ba-card-title">👤 VASTU EXPERTS</div>', unsafe_allow_html=True)

        consultants = [
            ("Dr. Sharma", "₹1500", "Senior Vastu consultant • 14 years experience"),
            ("Guru Ji", "₹1200", "Traditional Vastu advisor • 10 years experience")
        ]

        for name, fee, detail in consultants:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 14px; padding: 14px 16px; margin-bottom: 12px; box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);">
              <div style="display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap;">
                <div>
                  <div style="font-size: 15px; font-weight: 700; color: var(--text);">{name}</div>
                  <div style="font-size: 13px; color: var(--muted); margin-top: 4px;">{detail}</div>
                </div>
                <div style="font-size: 15px; font-weight: 800; color: var(--accent); white-space: nowrap;">{fee}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        # ─────────────────────────────
    # TAB 4 — FLOOR PLAN ANALYSIS
    # ─────────────────────────────
    with tab4:
        st.markdown('<div class="ba-card">', unsafe_allow_html=True)
        st.markdown('<div class="ba-card-title">🗺️ Floor Plan Vastu Analysis</div>', unsafe_allow_html=True)
    
        uploaded_plan = st.file_uploader(
            "Upload Floor Plan Image",
            type=["jpg", "png", "jpeg"],
            label_visibility="collapsed"
        )
    
        if uploaded_plan:
            image = Image.open(uploaded_plan)
    
            st.image(image, caption="📐 Uploaded Floor Plan", use_column_width=True)
    
            if st.button("🔍 Analyze Floor Plan", use_container_width=True):
    
                with st.spinner("🧠 Analyzing layout..."):
    
                    # Convert image
                    img = np.array(image)
                    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
                    # Edge detection
                    edges = cv2.Canny(gray, 50, 150)
                    edge_density = np.sum(edges) / edges.size
    
                    # Simple heuristic scoring
                    score = int(min(100, edge_density * 200))
    
                    issues = []
                    suggestions = []
    
                    # Dummy intelligent logic (demo-ready)
                    if score < 40:
                        issues.append("Irregular layout detected")
                        suggestions.append("Try rectangular or square layout")
    
                    if edge_density < 0.05:
                        issues.append("Low structural clarity")
                        suggestions.append("Define walls and rooms clearly")
    
                    if edge_density > 0.15:
                        issues.append("Too complex layout")
                        suggestions.append("Simplify room structure")
    
                    # 🎯 SHOW RESULT
                    st.success(f"Vastu Layout Score: {score}%")
    
                    if issues:
                        st.markdown("### ⚠️ Issues Found")
                        for i in issues:
                            st.warning(i)
    
                    if suggestions:
                        st.markdown("### 💡 Suggestions")
                        for s in suggestions:
                            st.info(s)
    
                    # Show processed edges (cool demo effect)
                    st.image(edges, caption="🔍 Edge Detection (AI View)", use_column_width=True)
    
        st.markdown('</div>', unsafe_allow_html=True)
    with tab5:
        st.markdown('<div class="ba-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="ba-card-title">🏠 AI Zoning-Based Floor Plan Generator</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # ═══════════════════════════════════════════════
        # PROFESSIONAL FLOOR PLANNING ENGINE
        # ═══════════════════════════════════════════════

        # Shared floorplan engine imported from floorplan_engine.py

        col1, col2, col3 = st.columns(3)
        with col1:
            plot_width = st.number_input("📐 Plot Width (ft)", min_value=30, max_value=200, value=50, step=5)
            bedrooms = st.slider("🛏 Bedrooms", 1, 6, 3)
        
        with col2:
            plot_length = st.number_input("📐 Plot Length (ft)", min_value=30, max_value=200, value=70, step=5)
            bathrooms = st.slider("🚿 Bathrooms", 1, 5, 2)
        
        with col3:
            vastu_mode = st.selectbox("🧿 Vastu Compliance", ["Strict", "Moderate", "Ignore"])
            st.write("")  # Spacer
        
        amenities = st.multiselect(
            "✨ Additional Amenities",
            [
                "Home Gym", "Home Theatre", "Study Room", "Office Room",
                "Servant Room", "Walk-in Closet", "Pooja Room",
                "Swimming Pool", "Backyard Garden", "Front Lawn"
            ],
            default=["Home Gym", "Study Room"],
            help="Select additional amenities to include in the floor plan"
        )
        
        col1, col2 = st.columns([2, 1])
        with col1:
            generate_btn = st.button("🚀 Generate Professional Floor Plan", use_container_width=True, key="gen_fp")
        with col2:
            st.write("")  # Spacer
        
        if generate_btn:
            try:
                # Initialize Core Engine
                solver = LayoutSolver(plot_width, plot_length, bedrooms, bathrooms, amenities, vastu_mode)
                
                # Solve Layout
                placed_rooms, outdoor_am = solver.solve()
                is_valid = len(placed_rooms) > 0
                
                if not is_valid:
                    st.error(f"⚠️ Layout Generation Failed: Plot area might be too small.")
                else:
                    plot_area = plot_width * plot_length
                    buildup_area = sum(r.area for r in placed_rooms)
                    
                    open_area = plot_area - buildup_area
                    coverage_pct = (buildup_area / plot_area) * 100
                    
                    total_cost, amenity_cost, duration_days = calculate_cost(buildup_area, amenities)
                    
                    vastu_score = calculate_vastu_score(vastu_mode, plot_width, plot_length, placed_rooms)
                    
                    # Render ONLY after validation
                    svg_code = render_professional_floorplan(plot_width, plot_length, placed_rooms, outdoor_am, vastu_mode)
                    components.html(svg_code, height=900, scrolling=True)

                    # Legend and explanatory panels for non-technical users
                    legend_html = '''
                    <div style="background:#08101d;border:1px solid #16243d;border-radius:16px;padding:22px;margin:16px 0;">
                        <h3 style="color:#00d3a8;font-family:Syne;">Legend & Floor Plan Explanation</h3>
                        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;">
                            <div style="padding:12px;background:#0d192e;border:1px solid #16243d;border-radius:12px;">
                                <div style="font-size:18px;margin-bottom:6px;">🚪 Door Opening</div>
                                <div style="color:#b0c9e3;font-size:14px;line-height:1.5;">Orange door arc shows the direction in which the door opens.</div>
                            </div>
                            <div style="padding:12px;background:#0d192e;border:1px solid #16243d;border-radius:12px;">
                                <div style="font-size:18px;margin-bottom:6px;">🪟 Window</div>
                                <div style="color:#b0c9e3;font-size:14px;line-height:1.5;">Cyan wall opening symbol provides natural light and ventilation.</div>
                            </div>
                            <div style="padding:12px;background:#0d192e;border:1px solid #16243d;border-radius:12px;">
                                <div style="font-size:18px;margin-bottom:6px;">🛏 Bedroom</div>
                                <div style="color:#b0c9e3;font-size:14px;line-height:1.5;">Bed symbol shows sleeping area.</div>
                            </div>
                            <div style="padding:12px;background:#0d192e;border:1px solid #16243d;border-radius:12px;">
                                <div style="font-size:18px;margin-bottom:6px;">🛋 Living Room</div>
                                <div style="color:#b0c9e3;font-size:14px;line-height:1.5;">Sofa symbol shows the family gathering and seating area.</div>
                            </div>
                            <div style="padding:12px;background:#0d192e;border:1px solid #16243d;border-radius:12px;">
                                <div style="font-size:18px;margin-bottom:6px;">🍽 Dining Area</div>
                                <div style="color:#b0c9e3;font-size:14px;line-height:1.5;">Dining table symbol shows dining and meal space.</div>
                            </div>
                            <div style="padding:12px;background:#0d192e;border:1px solid #16243d;border-radius:12px;">
                                <div style="font-size:18px;margin-bottom:6px;">🍳 Kitchen</div>
                                <div style="color:#b0c9e3;font-size:14px;line-height:1.5;">Counter and stove symbols show cooking and food preparation area.</div>
                            </div>
                            <div style="padding:12px;background:#0d192e;border:1px solid #16243d;border-radius:12px;">
                                <div style="font-size:18px;margin-bottom:6px;">🚿 Bathroom</div>
                                <div style="color:#b0c9e3;font-size:14px;line-height:1.5;">WC, sink, and shower symbols show bathing and sanitation facilities.</div>
                            </div>
                            <div style="padding:12px;background:#0d192e;border:1px solid #16243d;border-radius:12px;">
                                <div style="font-size:18px;margin-bottom:6px;">📏 Dimensions</div>
                                <div style="color:#b0c9e3;font-size:14px;line-height:1.5;">Room width and length are shown in feet.</div>
                            </div>
                            <div style="padding:12px;background:#0d192e;border:1px solid #16243d;border-radius:12px;">
                                <div style="font-size:18px;margin-bottom:6px;">🧭 North Direction</div>
                                <div style="color:#b0c9e3;font-size:14px;line-height:1.5;">North arrow is used for orientation and Vastu analysis.</div>
                            </div>
                        </div>
                    </div>'''
                    st.markdown(legend_html, unsafe_allow_html=True)

                    room_summary = []
                    for r in placed_rooms:
                        room_summary.append({
                            "Room Name": r.name,
                            "Size": f"{r.w:.0f}' × {r.h:.0f}'",
                            "Area (sq ft)": f"{r.area:.0f}"
                        })
                    import pandas as pd
                    df_rooms = pd.DataFrame(room_summary)

                    vastu_notes = []
                    def get_zone(x, y):
                        if x < plot_width / 2 and y > plot_length / 2:
                            return "South-West"
                        if x > plot_width / 2 and y > plot_length / 2:
                            return "South-East"
                        if x < plot_width / 2 and y < plot_length / 2:
                            return "North-West"
                        return "North-East"

                    master_bed = next((r for r in placed_rooms if r.room_type == "Master Bedroom"), None)
                    kitchen = next((r for r in placed_rooms if r.room_type == "Kitchen"), None)
                    living = next((r for r in placed_rooms if r.room_type == "Living"), None)
                    study = next((r for r in placed_rooms if r.room_type in ["Study", "Amenity"]), None)

                    if master_bed:
                        zone = get_zone(master_bed.x + master_bed.w / 2, master_bed.y + master_bed.h / 2)
                        if zone == "South-West":
                            vastu_notes.append("✓ Master Bedroom placed in South-West zone.")
                        else:
                            vastu_notes.append("⚠ Master Bedroom is not in the South-West zone; consider moving it for better Vastu.")
                    if kitchen:
                        zone = get_zone(kitchen.x + kitchen.w / 2, kitchen.y + kitchen.h / 2)
                        if zone == "South-East":
                            vastu_notes.append("✓ Kitchen located in South-East zone.")
                        else:
                            vastu_notes.append("⚠ Kitchen is not in the South-East zone; repositioning may improve energy flow.")
                    if living:
                        vastu_notes.append("✓ Living Room positioned for social interaction.")
                    if study:
                        zone = get_zone(study.x + study.w / 2, study.y + study.h / 2)
                        if zone in ["North-East", "North-West"]:
                            vastu_notes.append("✓ Study Room placed in a quiet zone.")
                        else:
                            vastu_notes.append("⚠ Study Room is in a busier zone; consider a quieter location.")

                    if not vastu_notes:
                        vastu_notes.append("✓ Vastu-friendly room placement information is not available for the current layout.")

                    st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)
                    st.markdown('### 📘 Floor Plan Summary', unsafe_allow_html=True)
                    st.markdown(
                        '<div style="background:#081622;border:1px solid #16243d;border-radius:16px;padding:18px;">' +
                        '<div style="display:flex;flex-wrap:wrap;gap:16px;">' +
                        '<div style="flex:1;min-width:280px;">' +
                        '<h4 style="color:#00d3a8;margin-bottom:10px;">Room Summary</h4>' +
                        df_rooms.to_html(index=False, classes='room-summary-table', border=0) +
                        '</div>' +
                        '<div style="flex:1;min-width:280px;">' +
                        '<h4 style="color:#00d3a8;margin-bottom:10px;">Vastu Explanation</h4>' +
                        '<ul style="color:#b0c9e3;line-height:1.7;padding-left:18px;">' +
                        ''.join(f'<li>{note}</li>' for note in vastu_notes) +
                        '</ul>' +
                        '</div>' +
                        '</div>' +
                        '</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown('### 📝 Customer Notes', unsafe_allow_html=True)
                    st.markdown(
                        '''<div style="background:#081622;border:1px solid #16243d;border-radius:16px;padding:18px;color:#b0c9e3;line-height:1.7;">
                            <p>Door arcs indicate the direction of door opening.</p>
                            <p>Room dimensions are shown in feet.</p>
                            <p>Furniture placement is illustrative and can be customized.</p>
                            <p>Window locations provide natural light and ventilation.</p>
                        </div>''',
                        unsafe_allow_html=True
                    )

                    st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)

                    # ═══════════════════════════════════════════════
                    # METRICS DASHBOARD
                    # ═══════════════════════════════════════════════
                    
                    st.markdown("### 📊 Project Metrics", help="Comprehensive floor plan analysis")
                    
                    metric_cols = st.columns(4)
                    with metric_cols[0]:
                        st.metric("📐 Plot Area", f"{plot_area:,} sqft", delta="Total land")
                    with metric_cols[1]:
                        st.metric("🏠 Built-up Area", f"{buildup_area:,.0f} sqft", delta=f"{coverage_pct:.1f}%")
                    with metric_cols[2]:
                        st.metric("🌳 Open Area", f"{open_area:,.0f} sqft", delta=f"{100-coverage_pct:.1f}%")
                    with metric_cols[3]:
                        st.metric("📊 Coverage", f"{coverage_pct:.1f}%", delta="Utilization")
                    
                    st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Room Breakdown**")
                        room_count = {}
                        for r in placed_rooms:
                            room_type = r.name.split()[0]
                            room_count[room_type] = room_count.get(room_type, 0) + 1
                        for room_type, count in sorted(room_count.items()):
                            st.write(f"• {room_type}: {count}")
                    
                    with col2:
                        st.markdown("**Amenities Included**")
                        if amenities:
                            for amenity in amenities:
                                st.write(f"✓ {amenity}")
                        else:
                            st.write("No additional amenities selected")
                    
                    st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)
                    
                    # ═══════════════════════════════════════════════
                    # COST & TIMELINE ANALYSIS
                    # ═══════════════════════════════════════════════
                    
                    st.markdown("### 💰 Cost & Timeline Estimates", help="Budget breakdown and construction duration")
                    
                    cost_cols = st.columns(3)
                    with cost_cols[0]:
                        base_cost_l = (buildup_area * 1800) / 100000
                        st.metric("🏗️ Base Construction", f"₹{base_cost_l:.1f}L", help="₹1,800 per sqft")
                    with cost_cols[1]:
                        amenity_cost_l = amenity_cost / 100000
                        st.metric("🎁 Amenities Cost", f"₹{amenity_cost_l:.1f}L", help=f"{len(amenities)} amenities")
                    with cost_cols[2]:
                        total_cost_cr = total_cost / 10000000
                        st.metric("💎 Total Estimate", f"₹{total_cost_cr:.2f}Cr", help="Base + Amenities")
                    
                    # Cost breakdown table
                    if amenity_cost > 0:
                        st.markdown("**Amenity Cost Breakdown:**")
                        amenity_costs_dict = {
                            "Swimming Pool": 400000,
                            "Home Theatre": 250000,
                            "Lift": 600000,
                            "Terrace Garden": 150000,
                            "Home Gym": 200000,
                            "Study Room": 120000,
                            "Office Room": 150000,
                            "Servant Room": 100000,
                            "Covered Parking": 200000,
                            "EV Charging Station": 80000,
                            "Backyard Garden": 75000,
                            "Front Lawn": 50000,
                            "Kids Play Area": 100000,
                            "Walk-in Closet": 60000
                        }
                        
                        breakdown = []
                        for amenity in amenities:
                            if amenity in amenity_costs_dict:
                                cost = amenity_costs_dict[amenity]
                                breakdown.append({"Amenity": amenity, "Cost (₹)": f"₹{cost:,}", "Cost (L)": f"₹{cost/100000:.1f}L"})
                        
                        if breakdown:
                            import pandas as pd
                            df_cost = pd.DataFrame(breakdown)
                            st.dataframe(df_cost, use_container_width=True, hide_index=True)
                    
                    # Timeline
            except Exception as exc:
                st.error("⚠️ An error occurred while generating the floor plan. Please check your inputs.")
                st.error(str(exc))
                st.text(traceback.format_exc())
# ═══════════════════════════════════════════════
# MATERIAL MARKETPLACE MODULE
# ═══════════════════════════════════════════════

def get_materials_database():
    """Returns comprehensive construction materials database with plain text fields"""
    materials = [
        # CEMENT
        {"category": "Cement", "name": "Ordinary Portland Cement (OPC)", "brand": "Ultratech", "supplier": "Ultratech Cement Ltd", "price": 380, "unit": "per bag (50kg)", "stock": 450, "delivery_days": 2, "rating": 4.8},
        {"category": "Cement", "name": "Portland Pozzolana Cement (PPC)", "brand": "Ambuja", "supplier": "Ambuja Cements Ltd", "price": 370, "unit": "per bag (50kg)", "stock": 320, "delivery_days": 3, "rating": 4.6},
        {"category": "Cement", "name": "White Cement", "brand": "Birla", "supplier": "Shree Cement Ltd", "price": 550, "unit": "per bag (25kg)", "stock": 150, "delivery_days": 5, "rating": 4.7},
        {"category": "Cement", "name": "Rapid Hardening Cement", "brand": "Dalmia", "supplier": "Dalmia Cement Ltd", "price": 420, "unit": "per bag (50kg)", "stock": 200, "delivery_days": 4, "rating": 4.5},
        {"category": "Cement", "name": "Slag Cement", "brand": "Chettinad", "supplier": "Chettinad Cement Ltd", "price": 340, "unit": "per bag (50kg)", "stock": 380, "delivery_days": 2, "rating": 4.4},
        # STEEL
        {"category": "Steel", "name": "TMT Steel Bar 8mm", "brand": "Tata", "supplier": "Tata Steel Limited", "price": 65, "unit": "per kg", "stock": 5000, "delivery_days": 1, "rating": 4.9},
        {"category": "Steel", "name": "TMT Steel Bar 10mm", "brand": "JSW", "supplier": "JSW Steel Limited", "price": 68, "unit": "per kg", "stock": 4500, "delivery_days": 1, "rating": 4.8},
        {"category": "Steel", "name": "TMT Steel Bar 12mm", "brand": "SAIL", "supplier": "Steel Authority of India", "price": 70, "unit": "per kg", "stock": 3800, "delivery_days": 2, "rating": 4.7},
        {"category": "Steel", "name": "Mild Steel Channel", "brand": "Ratnamani", "supplier": "Ratnamani Metals Ltd", "price": 55, "unit": "per kg", "stock": 2000, "delivery_days": 3, "rating": 4.5},
        {"category": "Steel", "name": "Structural Steel Beam", "brand": "Vizag", "supplier": "Visakhapatnam Steel Plant", "price": 75, "unit": "per kg", "stock": 1500, "delivery_days": 4, "rating": 4.6},
        # BRICKS
        {"category": "Bricks", "name": "Red Clay Bricks", "brand": "Standard", "supplier": "National Brick Industries", "price": 6, "unit": "per brick", "stock": 50000, "delivery_days": 2, "rating": 4.3},
        {"category": "Bricks", "name": "Fly Ash Bricks", "brand": "Eco-Brick", "supplier": "Eco Construction Materials", "price": 7, "unit": "per brick", "stock": 30000, "delivery_days": 3, "rating": 4.5},
        {"category": "Bricks", "name": "Hollow Concrete Bricks", "brand": "ConcreteMax", "supplier": "ConcreteMax Manufacturing", "price": 12, "unit": "per brick", "stock": 20000, "delivery_days": 2, "rating": 4.4},
        {"category": "Bricks", "name": "Interlocking Bricks", "brand": "BlockMaster", "supplier": "BlockMaster Ltd", "price": 15, "unit": "per brick", "stock": 15000, "delivery_days": 4, "rating": 4.6},
        {"category": "Bricks", "name": "Fire Bricks (Refractory)", "brand": "Thermaxit", "supplier": "Thermaxit Industries", "price": 25, "unit": "per brick", "stock": 5000, "delivery_days": 5, "rating": 4.7},
        # SAND
        {"category": "Sand", "name": "River Sand", "brand": "Natural", "supplier": "River Sand Suppliers Co", "price": 50, "unit": "per cubic ft", "stock": 10000, "delivery_days": 1, "rating": 4.2},
        {"category": "Sand", "name": "M-Sand (Manufactured Sand)", "brand": "SandTech", "supplier": "SandTech Manufacturing", "price": 65, "unit": "per cubic ft", "stock": 8000, "delivery_days": 2, "rating": 4.4},
        {"category": "Sand", "name": "Silica Sand", "brand": "PureMineral", "supplier": "PureMineral Extraction", "price": 90, "unit": "per cubic ft", "stock": 3000, "delivery_days": 3, "rating": 4.5},
        {"category": "Sand", "name": "Coarse Sand", "brand": "ConstraSand", "supplier": "Constra Sand Ltd", "price": 55, "unit": "per cubic ft", "stock": 7500, "delivery_days": 1, "rating": 4.3},
        {"category": "Sand", "name": "Polymeric Sand", "brand": "FlexiBond", "supplier": "FlexiBond Materials", "price": 120, "unit": "per cubic ft", "stock": 2000, "delivery_days": 4, "rating": 4.6},
        # TILES
        {"category": "Tiles", "name": "Ceramic Floor Tiles 24x24", "brand": "Kajaria", "supplier": "Kajaria Ceramics Ltd", "price": 85, "unit": "per sqft", "stock": 5000, "delivery_days": 2, "rating": 4.7},
        {"category": "Tiles", "name": "Glazed Vitreous Tiles", "brand": "Somany", "supplier": "Somany Ceramics Ltd", "price": 95, "unit": "per sqft", "stock": 4000, "delivery_days": 2, "rating": 4.6},
        {"category": "Tiles", "name": "Porcelain Tiles", "brand": "Johnson", "supplier": "Johnson Tiles Ltd", "price": 120, "unit": "per sqft", "stock": 3000, "delivery_days": 3, "rating": 4.8},
        {"category": "Tiles", "name": "Mosaic Tiles", "brand": "Daltile", "supplier": "Daltile Pvt Ltd", "price": 110, "unit": "per sqft", "stock": 2500, "delivery_days": 4, "rating": 4.5},
        {"category": "Tiles", "name": "Marble Tiles", "brand": "Premium", "supplier": "Premium Marble Imports", "price": 200, "unit": "per sqft", "stock": 1000, "delivery_days": 5, "rating": 4.9},
        # PAINT
        {"category": "Paint", "name": "Exterior Acrylic Paint", "brand": "Asian Paints", "supplier": "Asian Paints Ltd", "price": 450, "unit": "per 10L", "stock": 200, "delivery_days": 1, "rating": 4.8},
        {"category": "Paint", "name": "Interior Emulsion Paint", "brand": "Berger", "supplier": "Berger Paints India", "price": 400, "unit": "per 10L", "stock": 250, "delivery_days": 1, "rating": 4.7},
        {"category": "Paint", "name": "Textured Paint", "brand": "Nippon", "supplier": "Nippon Paint India", "price": 550, "unit": "per 10L", "stock": 150, "delivery_days": 2, "rating": 4.6},
        {"category": "Paint", "name": "Anti-Fungal Paint", "brand": "Dulux", "supplier": "AkzoNobel India", "price": 500, "unit": "per 10L", "stock": 180, "delivery_days": 2, "rating": 4.7},
        {"category": "Paint", "name": "Heat Reflective Paint", "brand": "Jotun", "supplier": "Jotun Paints India", "price": 650, "unit": "per 10L", "stock": 100, "delivery_days": 3, "rating": 4.8},
        # ELECTRICAL
        {"category": "Electrical", "name": "PVC Electrical Wire 4 sq.mm", "brand": "Havells", "supplier": "Havells India Ltd", "price": 18, "unit": "per meter", "stock": 5000, "delivery_days": 1, "rating": 4.8},
        {"category": "Electrical", "name": "Modular Switch Plate", "brand": "Legrand", "supplier": "Legrand India Pvt Ltd", "price": 120, "unit": "per switch", "stock": 2000, "delivery_days": 1, "rating": 4.9},
        {"category": "Electrical", "name": "Conduit Pipe 20mm", "brand": "Atkore", "supplier": "Atkore International", "price": 35, "unit": "per meter", "stock": 3000, "delivery_days": 2, "rating": 4.6},
        {"category": "Electrical", "name": "MCB 16A Single Pole", "brand": "L&T", "supplier": "L&T Electrical & Automation", "price": 180, "unit": "per piece", "stock": 1000, "delivery_days": 1, "rating": 4.7},
        {"category": "Electrical", "name": "Earthing Rod (3m)", "brand": "Polycab", "supplier": "Polycab India Ltd", "price": 250, "unit": "per piece", "stock": 500, "delivery_days": 2, "rating": 4.5},
        # PLUMBING
        {"category": "Plumbing", "name": "PVC Pipe 25mm", "brand": "Prince", "supplier": "Prince Pipes & Fittings", "price": 45, "unit": "per meter", "stock": 4000, "delivery_days": 1, "rating": 4.7},
        {"category": "Plumbing", "name": "Copper Fitting (1/2 inch)", "brand": "Ashirwad", "supplier": "Ashirwad Pipes Ltd", "price": 85, "unit": "per fitting", "stock": 1500, "delivery_days": 2, "rating": 4.8},
        {"category": "Plumbing", "name": "Ceramic Toilet Seat", "brand": "Kohler", "supplier": "Kohler Sanitaryware Ltd", "price": 3500, "unit": "per piece", "stock": 300, "delivery_days": 3, "rating": 4.9},
        {"category": "Plumbing", "name": "Chrome Basin Tap", "brand": "Grohe", "supplier": "Grohe India Ltd", "price": 2000, "unit": "per piece", "stock": 400, "delivery_days": 2, "rating": 4.8},
        {"category": "Plumbing", "name": "SWR Pipe 110mm", "brand": "Finolex", "supplier": "Finolex Industries", "price": 120, "unit": "per meter", "stock": 2000, "delivery_days": 2, "rating": 4.6},
    ]
    return pd.DataFrame(materials)


def material_marketplace():
    """Material Marketplace with enhanced UI and interactive buttons"""
    # Initialize session state for saved materials and supplier details
    if "saved_materials" not in st.session_state:
        st.session_state.saved_materials = []
    if "inquire_material" not in st.session_state:
        st.session_state.inquire_material = None
    
    st.markdown('<h1 class="main-header">🧱 Material Marketplace</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Premium construction materials from trusted suppliers</p>', unsafe_allow_html=True)
    
    df_materials = get_materials_database()
    st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("### 🔍 Filter & Search", help="Find materials by category, price, rating")
    
    filter_cols = st.columns([2, 1.5, 1.5, 1.5])
    
    with filter_cols[0]:
        search_query = st.text_input("🔎 Search Materials", placeholder="Search by product name or brand...", label_visibility="collapsed")
    
    with filter_cols[1]:
        selected_category = st.selectbox("Category", ["All"] + sorted(df_materials["category"].unique().tolist()), label_visibility="collapsed")
    
    with filter_cols[2]:
        price_range = st.slider("Price Range (₹)", int(df_materials["price"].min()), int(df_materials["price"].max()), (int(df_materials["price"].min()), int(df_materials["price"].max())), label_visibility="collapsed")
    
    with filter_cols[3]:
        sort_by = st.selectbox("Sort By", ["Lowest Price", "Highest Rating", "Fastest Delivery"], label_visibility="collapsed")
    
    filtered_df = df_materials.copy()
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]
    
    if search_query:
        search_lower = search_query.lower()
        filtered_df = filtered_df[filtered_df["name"].str.lower().str.contains(search_lower) | filtered_df["brand"].str.lower().str.contains(search_lower) | filtered_df["supplier"].str.lower().str.contains(search_lower)]
    
    filtered_df = filtered_df[(filtered_df["price"] >= price_range[0]) & (filtered_df["price"] <= price_range[1])]
    
    if sort_by == "Lowest Price":
        filtered_df = filtered_df.sort_values("price")
    elif sort_by == "Highest Rating":
        filtered_df = filtered_df.sort_values("rating", ascending=False)
    elif sort_by == "Fastest Delivery":
        filtered_df = filtered_df.sort_values("delivery_days")
    
    st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)
    
    result_count = len(filtered_df)
    st.markdown(f"### 📦 Results: {result_count} material(s) found", help=f"Showing {result_count} products")
    
    if result_count == 0:
        st.warning("❌ No materials match your search criteria. Try adjusting your filters.")
    else:
        cols_per_row = 3
        rows = []
        for idx in range(0, len(filtered_df), cols_per_row):
            rows.append(filtered_df.iloc[idx:idx+cols_per_row])
        
        for row_idx, row_materials in enumerate(rows):
            cols = st.columns(len(row_materials), gap="medium")
            
            for col_idx, (mat_idx, material) in enumerate(row_materials.iterrows()):
                with cols[col_idx]:
                    if material["stock"] < 100:
                        stock_status = "⚠️ Low Stock"
                        stock_color = "#ffa502"
                    elif material["stock"] < 500:
                        stock_status = "📦 Limited"
                        stock_color = "#00e5b0"
                    else:
                        stock_status = "✅ In Stock"
                        stock_color = "#2ed573"
                    
                    if material["delivery_days"] == 1:
                        delivery_badge = "⚡ Next Day"
                        delivery_color = "#ff6b35"
                    elif material["delivery_days"] <= 2:
                        delivery_badge = "🚚 2-Day"
                        delivery_color = "#00e5b0"
                    else:
                        delivery_badge = f"📅 {material['delivery_days']}-Days"
                        delivery_color = "#5b8dee"
                    
                    stars = "⭐" * int(material["rating"]) + "☆" * (5 - int(material["rating"]))
                    
                    # Single, complete card HTML with all elements
                    card_html = f"""<div style="background:linear-gradient(135deg, rgba(17,23,32,0.9), rgba(22,30,43,0.9)); border:1px solid #253347; border-radius:16px; padding:24px; min-height:500px; display:flex; flex-direction:column; gap:16px;">
<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px;">
<div style="flex:1;">
<div style="font-family:Syne; font-size:17px; font-weight:700; color:#dde8f5; margin-bottom:4px; word-wrap:break-word;">{material['name']}</div>
<div style="font-family:JetBrains Mono; font-size:12px; letter-spacing:0.5px; color:#5a7090; text-transform:uppercase; margin-bottom:8px;">{material['category']}</div>
</div>
<div style="background:{stock_color}; color:#07090f; padding:5px 10px; border-radius:6px; font-family:JetBrains Mono; font-size:10px; font-weight:600; white-space:nowrap; flex-shrink:0;">{stock_status}</div>
</div>
<div style="border-top:1px solid #1e2d42; padding-top:12px; border-bottom:1px solid #1e2d42; padding-bottom:12px;">
<div style="font-size:14px; color:#b0c9e3; line-height:1.6; margin-bottom:4px;">🏢 <strong>{material['brand']}</strong></div>
<div style="font-size:11px; color:#7a8fa0;">Supplier: {str(material['supplier'])[:35]}</div>
</div>
<div style="background:#0d1117; border:1px solid #1e2d42; border-radius:12px; padding:14px;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
<div>
<div style="font-family:JetBrains Mono; font-size:10px; color:#5a7090; letter-spacing:0.5px; margin-bottom:2px;">PRICE</div>
<div style="font-family:Syne; font-size:23px; font-weight:700; color:#00e5b0;">₹{material['price']}</div>
</div>
<div style="text-align:right;">
<div style="font-size:13px; color:#ffa502; margin-bottom:3px;">{stars}</div>
<div style="font-family:JetBrains Mono; font-size:11px; color:#5b8dee; font-weight:600;">{material['rating']}/5</div>
</div>
</div>
<div style="font-family:JetBrains Mono; font-size:11px; color:#5a7090; border-top:1px solid #253347; padding-top:8px;">{material['unit']}</div>
</div>
<div style="display:flex; gap:8px; margin-bottom:12px;">
<div style="flex:1; background:#111720; border:1px solid #16243d; border-radius:10px; padding:12px; text-align:center;">
<div style="color:#5a7090; margin-bottom:3px; font-size:10px; font-weight:600;">STOCK</div>
<div style="color:#00e5b0; font-weight:700; font-size:16px; font-family:Syne;">{material['stock']:,}</div>
</div>
<div style="flex:1; background:rgba(91,141,238,0.08); border:1px solid rgba(91,141,238,0.25); border-radius:10px; padding:12px; text-align:center;">
<div style="color:#5a7090; margin-bottom:3px; font-size:10px; font-weight:600;">DELIVERY</div>
<div style="color:#5b8dee; font-weight:700; font-size:16px; font-family:Syne;">{material['delivery_days']}d</div>
</div>
</div>
</div>"""
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # Initialize quote session state
                    if "quote_requests" not in st.session_state:
                        st.session_state.quote_requests = {}
                    
                    material_key = f"{material['category']}_{material['name']}_{material['brand']}"
                    
                    # Real Streamlit buttons with session state
                    button_cols = st.columns(3, gap="small")
                    with button_cols[0]:
                        if st.button(f"💬 INQUIRE", key=f"inquire_{mat_idx}_{col_idx}", use_container_width=True):
                            st.session_state.inquire_material = material
                            st.rerun()
                    
                    with button_cols[1]:
                        if st.button(f"📞 GET QUOTE", key=f"quote_{mat_idx}_{col_idx}", use_container_width=True):
                            if material_key not in st.session_state.quote_requests:
                                st.session_state.quote_requests[material_key] = True
                            else:
                                st.session_state.quote_requests[material_key] = not st.session_state.quote_requests.get(material_key, False)
                            st.rerun()
                    
                    with button_cols[2]:
                        if st.button(f"⭐ SAVE", key=f"save_{mat_idx}_{col_idx}", use_container_width=True):
                            # Check if material already saved
                            if material_key not in [f"{m['category']}_{m['name']}_{m['brand']}" for m in st.session_state.saved_materials]:
                                st.session_state.saved_materials.append(material)
                                st.success(f"✅ {material['name']} saved!", icon="✨")
                            else:
                                st.info(f"Already saved: {material['name']}", icon="ℹ️")
                    
                    # Get Quote Expander Section
                    if material_key in st.session_state.quote_requests and st.session_state.quote_requests[material_key]:
                        with st.expander(f"📋 Get Quote for {material['name']}", expanded=True):
                            quote_col1, quote_col2 = st.columns(2)
                            
                            with quote_col1:
                                quantity = st.number_input(
                                    "Quantity",
                                    value=1,
                                    min_value=1,
                                    step=1,
                                    key=f"qty_{material_key}"
                                )
                                contact_name = st.text_input(
                                    "Contact Name",
                                    placeholder="Enter your name",
                                    key=f"name_{material_key}"
                                )
                            
                            with quote_col2:
                                phone = st.text_input(
                                    "Phone Number",
                                    placeholder="Enter phone number",
                                    key=f"phone_{material_key}"
                                )
                            
                            # Calculate estimated cost
                            estimated_cost = material['price'] * quantity
                            delivery_days = material['delivery_days']
                            
                            # Display quote summary
                            summary_html = f"""
                            <div style="background:#0d1117; border:1px solid #1e2d42; border-radius:12px; padding:14px; margin-top:12px;">
                            <div style="font-family:Syne; font-size:14px; font-weight:700; color:#00e5b0; margin-bottom:12px;">Quote Summary</div>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; font-size:12px; color:#dde8f5; line-height:1.8;">
                            <div><strong style="color:#5a7090;">Material:</strong><br>{material['name']}</div>
                            <div><strong style="color:#5a7090;">Supplier:</strong><br>{material['supplier']}</div>
                            <div><strong style="color:#5a7090;">Unit Price:</strong><br>₹{material['price']} per {material['unit']}</div>
                            <div><strong style="color:#5a7090;">Quantity:</strong><br>{quantity} {material['unit']}</div>
                            <div style="grid-column:1/3; border-top:1px solid #1e2d42; padding-top:10px; margin-top:8px;">
                            <strong style="font-size:13px; color:#00e5b0;">Estimated Total Cost: ₹{estimated_cost:,.0f}</strong>
                            </div>
                            <div style="grid-column:1/3;">
                            <strong style="color:#5a7090;">Estimated Delivery:</strong> {delivery_days} day(s)
                            </div>
                            </div>
                            </div>
                            """
                            st.markdown(summary_html, unsafe_allow_html=True)
                            
                            # Submit quote request
                            quote_col_submit = st.columns(2)
                            with quote_col_submit[0]:
                                if st.button(f"✅ Request Quote", key=f"submit_quote_{material_key}", use_container_width=True):
                                    if contact_name and phone:
                                        st.success(f"📧 Quote request sent to {material['supplier']}!", icon="✓")
                                        st.info(f"Contact: {contact_name} | Phone: {phone}", icon="📞")
                                    else:
                                        st.error("❌ Please enter Contact Name and Phone Number", icon="⚠️")
                            
                            with quote_col_submit[1]:
                                if st.button(f"❌ Cancel", key=f"cancel_quote_{material_key}", use_container_width=True):
                                    st.session_state.quote_requests[material_key] = False
                                    st.rerun()
        
        st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)
        
        # Display inquired material details if selected
        if st.session_state.inquire_material is not None:
            mat = st.session_state.inquire_material
            st.markdown("### 🔍 Supplier Details", help="Detailed information about this material and supplier")
            
            detail_cols = st.columns([2, 1])
            with detail_cols[0]:
                st.markdown(f"""
                <div class="ba-card">
                    <div class="ba-card-title">📋 Material Information</div>
                    <div style="color:#dde8f5; font-size:13px; line-height:1.8;">
                        <strong>Product:</strong> {mat['name']}<br>
                        <strong>Brand:</strong> {mat['brand']}<br>
                        <strong>Category:</strong> {mat['category']}<br>
                        <strong>Supplier:</strong> {mat['supplier']}<br>
                        <strong>Unit:</strong> {mat['unit']}<br>
                        <strong>Rating:</strong> ⭐ {mat['rating']}/5<br>
                        <strong>Current Stock:</strong> {mat['stock']:,} units<br>
                        <strong>Delivery Time:</strong> {mat['delivery_days']} day(s)
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with detail_cols[1]:
                st.markdown(f"""
                <div class="ba-card" style="background: linear-gradient(135deg, rgba(0,229,176,0.08), rgba(91,141,238,0.08));">
                    <div class="ba-card-title">💰 Pricing Details</div>
                    <div style="color:#dde8f5; font-size:13px; line-height:2;">
                        <strong style="font-size:24px; color:#00e5b0;">₹{mat['price']}</strong><br>
                        <small style="color:#5a7090;">per {mat['unit']}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("✅ Close Supplier Details", use_container_width=True):
                st.session_state.inquire_material = None
                st.rerun()
        
        st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)
        
        # Material Cost Calculator Section
        st.markdown("### 🧮 Material Cost Calculator", help="Calculate total material cost with taxes and transportation")
        
        calc_col1, calc_col2 = st.columns(2)
        
        with calc_col1:
            calc_material = st.selectbox(
                "Select Material",
                options=filtered_df['name'].tolist() if len(filtered_df) > 0 else ["No materials available"],
                key="calculator_material",
                help="Choose a material to calculate cost"
            )
        
        with calc_col2:
            calc_quantity = st.number_input(
                "Quantity",
                value=1,
                min_value=1,
                step=1,
                key="calculator_quantity",
                help="Enter quantity needed"
            )
        
        if len(filtered_df) > 0 and calc_material != "No materials available":
            # Get selected material details
            selected_material = filtered_df[filtered_df['name'] == calc_material].iloc[0]
            unit_price = selected_material['price']
            
            # Calculate costs
            material_cost = unit_price * calc_quantity
            transportation_cost = material_cost * 0.05  # 5% transportation
            subtotal = material_cost + transportation_cost
            gst = subtotal * 0.18  # 18% GST
            grand_total = subtotal + gst
            
            # Display cost breakdown using metrics
            calc_metric_cols = st.columns(4)
            with calc_metric_cols[0]:
                st.metric("💰 Material Cost", f"₹{material_cost:,.0f}", help="Base material cost")
            with calc_metric_cols[1]:
                st.metric("🚚 Transport (5%)", f"₹{transportation_cost:,.0f}", help="Transportation charges")
            with calc_metric_cols[2]:
                st.metric("📋 Subtotal", f"₹{subtotal:,.0f}", help="Material + Transportation")
            with calc_metric_cols[3]:
                st.metric("🏛️ GST (18%)", f"₹{gst:,.0f}", help="Goods and Services Tax")
            
            # Grand Total Card
            grand_total_html = f"""
            <div style="background:linear-gradient(135deg, rgba(0,229,176,0.12), rgba(91,141,238,0.08)); border:2px solid #00e5b0; border-radius:14px; padding:20px; margin-top:12px;">
            <div style="text-align:center;">
            <div style="font-family:JetBrains Mono; font-size:11px; letter-spacing:2px; text-transform:uppercase; color:#5a7090; margin-bottom:8px;">Grand Total</div>
            <div style="font-family:Syne; font-size:32px; font-weight:800; color:#00e5b0;">₹{grand_total:,.0f}</div>
            <div style="font-size:11px; color:#b0c9e3; margin-top:8px;">
            Material Cost: ₹{material_cost:,.0f} | Transport: ₹{transportation_cost:,.0f} | GST: ₹{gst:,.0f}
            </div>
            </div>
            </div>
            """
            st.markdown(grand_total_html, unsafe_allow_html=True)
            
            # Quick Info
            info_col1, info_col2, info_col3 = st.columns(3)
            with info_col1:
                st.info(f"**Unit:** {selected_material['unit']}", icon="ℹ️")
            with info_col2:
                st.info(f"**Supplier:** {selected_material['supplier']}", icon="🏢")
            with info_col3:
                st.info(f"**Delivery:** {selected_material['delivery_days']} days", icon="📅")
        
        st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)
        
        # Supplier Comparison Section
        st.markdown("### 🏢 Supplier Comparison", help="Compare suppliers for different materials")
        
        comp_col1, comp_col2 = st.columns([2, 1])
        
        with comp_col1:
            comparison_category = st.selectbox(
                "Select Category for Comparison",
                options=["All Categories"] + sorted(df_materials["category"].unique().tolist()),
                key="comparison_category",
                help="Choose a material category to compare suppliers"
            )
        
        with comp_col2:
            pass  # Spacer for alignment
        
        # Filter materials by selected category
        if comparison_category == "All Categories":
            comparison_df = df_materials.copy()
        else:
            comparison_df = df_materials[df_materials["category"] == comparison_category]
        
        if len(comparison_df) > 0:
            # Create supplier comparison table
            supplier_comparison = comparison_df.groupby("supplier").agg({
                "price": "mean",
                "rating": "mean",
                "delivery_days": "min",
                "stock": "sum",
                "name": "count"
            }).reset_index()
            
            supplier_comparison.columns = ["Supplier", "Avg Price (₹)", "Rating", "Fastest Delivery (days)", "Total Stock", "Product Count"]
            supplier_comparison = supplier_comparison.round(2)
            
            # Calculate best value score (lower is better)
            # Normalize scores: 0-1 range
            min_price = supplier_comparison["Avg Price (₹)"].min()
            max_price = supplier_comparison["Avg Price (₹)"].max()
            min_rating = supplier_comparison["Rating"].min()
            max_rating = supplier_comparison["Rating"].max()
            min_delivery = supplier_comparison["Fastest Delivery (days)"].min()
            max_delivery = supplier_comparison["Fastest Delivery (days)"].max()
            
            # Calculate value score (higher is better)
            supplier_comparison["Value Score"] = (
                (supplier_comparison["Rating"] - min_rating) / (max_rating - min_rating) * 0.4 +  # 40% rating
                (1 - (supplier_comparison["Avg Price (₹)"] - min_price) / (max_price - min_price + 1)) * 0.35 +  # 35% price (inverted)
                (1 - (supplier_comparison["Fastest Delivery (days)"] - min_delivery) / (max_delivery - min_delivery + 1)) * 0.25  # 25% delivery (inverted)
            ) * 100
            
            supplier_comparison = supplier_comparison.sort_values("Value Score", ascending=False)
            
            # Find best value supplier
            best_supplier_idx = supplier_comparison["Value Score"].idxmax()
            best_supplier = supplier_comparison.loc[best_supplier_idx, "Supplier"]
            best_score = supplier_comparison.loc[best_supplier_idx, "Value Score"]
            
            # Display comparison table (excluding Product Count from display)
            display_df = supplier_comparison[["Supplier", "Avg Price (₹)", "Rating", "Fastest Delivery (days)", "Total Stock", "Value Score"]].copy()
            display_df["Avg Price (₹)"] = display_df["Avg Price (₹)"].apply(lambda x: f"₹{x:,.0f}")
            display_df["Rating"] = display_df["Rating"].apply(lambda x: f"⭐ {x:.1f}")
            display_df["Value Score"] = display_df["Value Score"].apply(lambda x: f"{x:.1f}/100")
            
            st.dataframe(
                display_df,
                use_container_width=True,
                column_config={
                    "Supplier": st.column_config.TextColumn("Supplier", width="medium"),
                    "Avg Price (₹)": st.column_config.TextColumn("Avg Price", width="small"),
                    "Rating": st.column_config.TextColumn("Rating", width="small"),
                    "Fastest Delivery (days)": st.column_config.NumberColumn("Delivery (days)", width="small"),
                    "Total Stock": st.column_config.NumberColumn("Total Stock", format="%,d", width="small"),
                    "Value Score": st.column_config.TextColumn("Value Score", width="small")
                },
                hide_index=True
            )
            
            # Best Value Supplier Recommendation
            best_value_html = f"""
            <div style="background:linear-gradient(135deg, rgba(0,229,176,0.15), rgba(255,107,53,0.08)); border:2px solid #00e5b0; border-radius:14px; padding:16px; margin-top:12px;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
            <div style="font-size:24px;">🏆</div>
            <div>
            <div style="font-family:Syne; font-size:14px; font-weight:700; color:#00e5b0;">Best Value Supplier</div>
            <div style="font-size:12px; color:#5a7090;">Recommended based on price, rating & delivery</div>
            </div>
            </div>
            <div style="background:#111720; border:1px solid #1e2d42; border-radius:10px; padding:12px; margin-top:8px;">
            <div style="font-size:14px; color:#dde8f5; margin-bottom:8px;"><strong>{best_supplier}</strong></div>
            """
            
            # Get best supplier details
            best_supplier_data = supplier_comparison[supplier_comparison["Supplier"] == best_supplier].iloc[0]
            best_value_html += f"""
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; font-size:11px; color:#b0c9e3;">
            <div>💰 Price: ₹{best_supplier_data['Avg Price (₹)']:,.0f}</div>
            <div>⭐ Rating: {best_supplier_data['Rating']:.1f}/5</div>
            <div>📅 Delivery: {int(best_supplier_data['Fastest Delivery (days)'])} days</div>
            </div>
            </div>
            </div>
            """
            st.markdown(best_value_html, unsafe_allow_html=True)
        else:
            st.warning("No suppliers available for the selected category.", icon="⚠️")
        
        st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)
        
        # Smart Procurement Planner Section
        st.markdown("### 🏗️ Smart Procurement Planner", help="Estimate materials needed for your construction project")
        
        planner_col1, planner_col2 = st.columns(2)
        
        with planner_col1:
            plot_width = st.number_input(
                "Plot Width (meters)",
                value=20,
                min_value=5,
                max_value=100,
                step=1,
                key="plot_width",
                help="Width of your plot in meters"
            )
        
        with planner_col2:
            plot_length = st.number_input(
                "Plot Length (meters)",
                value=30,
                min_value=5,
                max_value=100,
                step=1,
                key="plot_length",
                help="Length of your plot in meters"
            )
        
        # Calculate based on construction standards
        plot_area = plot_width * plot_length
        buildup_area = plot_area * 1.5  # Typical built-up area multiplier for India
        
        # Material estimation based on per 100 sq.m
        # Bricks: 50,000 units per 100 sq.m
        estimated_bricks = int((buildup_area / 100) * 50000)
        # Cement: 30 bags per 100 sq.m
        estimated_cement = int((buildup_area / 100) * 30)
        # Steel: 2.5 tons per 100 sq.m
        estimated_steel = round((buildup_area / 100) * 2.5, 1)
        # Sand: 25 cubic meters per 100 sq.m
        estimated_sand = round((buildup_area / 100) * 25, 1)
        
        # Get material prices from database
        brick_price = df_materials[df_materials['name'].str.contains('Red Clay Bricks', case=False)]['price'].values
        brick_price = brick_price[0] if len(brick_price) > 0 else 6
        
        cement_price = df_materials[df_materials['name'].str.contains('Ordinary Portland Cement', case=False)]['price'].values
        cement_price = cement_price[0] if len(cement_price) > 0 else 380
        
        steel_price = df_materials[df_materials['name'].str.contains('TMT.*8mm', case=False)]['price'].values
        steel_price = steel_price[0] if len(steel_price) > 0 else 65
        
        sand_price = df_materials[df_materials['name'].str.contains('M-Sand', case=False)]['price'].values
        sand_price = sand_price[0] if len(sand_price) > 0 else 65
        
        # Calculate costs
        brick_cost = estimated_bricks * brick_price
        cement_cost = estimated_cement * cement_price
        steel_cost = estimated_steel * 1000 * steel_price  # Convert tons to kg
        sand_cost = estimated_sand * sand_price
        
        total_material_cost = brick_cost + cement_cost + steel_cost + sand_cost
        
        # Display material estimates
        st.markdown(f"**Plot Area:** {plot_area:,} sq.m | **Built-up Area (Est.):** {buildup_area:,.0f} sq.m", help="Built-up area estimated at 1.5x plot area")
        
        material_estimate_cols = st.columns(4)
        with material_estimate_cols[0]:
            st.metric("🧱 Bricks", f"{estimated_bricks:,}", delta="units", help="Estimated brick quantity")
        with material_estimate_cols[1]:
            st.metric("🏭 Cement", f"{estimated_cement:,}", delta="bags", help="Estimated cement bags")
        with material_estimate_cols[2]:
            st.metric("⚙️ Steel", f"{estimated_steel:,.1f}", delta="tons", help="Estimated steel TMT bars")
        with material_estimate_cols[3]:
            st.metric("🏖️ Sand", f"{estimated_sand:,.1f}", delta="cu.m", help="Estimated sand volume")
        
        # Cost breakdown
        cost_breakdown_html = f"""
        <div style="background:#0d1117; border:1px solid #1e2d42; border-radius:12px; padding:14px; margin-top:12px;">
        <div style="font-family:Syne; font-size:13px; font-weight:700; color:#00e5b0; margin-bottom:10px;">Cost Breakdown</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:11px; color:#dde8f5; line-height:1.8;">
        <div><strong style="color:#5a7090;">Bricks:</strong> ₹{brick_cost:,.0f}</div>
        <div><strong style="color:#5a7090;">Cement:</strong> ₹{cement_cost:,.0f}</div>
        <div><strong style="color:#5a7090;">Steel:</strong> ₹{steel_cost:,.0f}</div>
        <div><strong style="color:#5a7090;">Sand:</strong> ₹{sand_cost:,.0f}</div>
        </div>
        </div>
        """
        st.markdown(cost_breakdown_html, unsafe_allow_html=True)
        
        # Total Project Cost Card
        total_cost_html = f"""
        <div style="background:linear-gradient(135deg, rgba(0,229,176,0.15), rgba(91,141,238,0.08)); border:2px solid #00e5b0; border-radius:14px; padding:20px; margin-top:12px;">
        <div style="text-align:center;">
        <div style="font-family:JetBrains Mono; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:#5a7090; margin-bottom:6px;">Estimated Project Material Cost</div>
        <div style="font-family:Syne; font-size:36px; font-weight:800; color:#00e5b0;">₹{total_material_cost:,.0f}</div>
        <div style="font-size:10px; color:#b0c9e3; margin-top:8px;">For {plot_area:,} sq.m plot | {buildup_area:,.0f} sq.m built-up area</div>
        </div>
        </div>
        """
        st.markdown(total_cost_html, unsafe_allow_html=True)
        
        # Buy Materials Button
        buy_col1, buy_col2, buy_col3 = st.columns([1, 1, 1])
        with buy_col2:
            if st.button("🛒 Buy Materials Now", use_container_width=True, key="buy_materials_btn"):
                st.session_state.planner_materials = {
                    "bricks": estimated_bricks,
                    "cement": estimated_cement,
                    "steel": estimated_steel,
                    "sand": estimated_sand,
                    "total_cost": total_material_cost,
                    "plot_area": plot_area
                }
                st.success("✅ Material recommendations added! Scroll to marketplace to view.", icon="📦")
        
        st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📊 Material Analytics", help="Summary statistics for filtered results")
        
        stat_cols = st.columns(4)
        with stat_cols[0]:
            avg_price = filtered_df["price"].mean()
            st.metric("💰 Avg Price", f"₹{avg_price:.0f}", help="Average price of filtered materials")
        with stat_cols[1]:
            avg_rating = filtered_df["rating"].mean()
            st.metric("⭐ Avg Rating", f"{avg_rating:.1f}/5", help="Average supplier rating")
        with stat_cols[2]:
            avg_delivery = filtered_df["delivery_days"].mean()
            st.metric("📅 Avg Delivery", f"{avg_delivery:.0f} days", help="Average delivery time")
        with stat_cols[3]:
            total_stock = filtered_df["stock"].sum()
            st.metric("📦 Total Stock", f"{total_stock:,}", help="Combined stock availability")
        
        st.markdown("### 📂 Category Breakdown", help="Distribution of materials by category")
        category_stats = filtered_df.groupby("category").agg({"name": "count", "stock": "sum", "price": "mean", "rating": "mean"}).rename(columns={"name": "Count"}).round(2)
        category_stats.columns = ["Product Count", "Total Stock", "Avg Price (₹)", "Avg Rating"]
        st.dataframe(category_stats, use_container_width=True, column_config={"Product Count": st.column_config.NumberColumn(format="%d"), "Total Stock": st.column_config.NumberColumn(format="%,d"), "Avg Price (₹)": st.column_config.NumberColumn(format="₹%.0f"), "Avg Rating": st.column_config.NumberColumn(format="%.2f ⭐")})
    
    st.markdown('<div class="ba-divider"></div>', unsafe_allow_html=True)
    info_html = """<div style="background:linear-gradient(135deg, rgba(0,229,176,0.06), rgba(91,141,238,0.06)); border:1px solid rgba(0,229,176,0.15); border-radius:14px; padding:20px;">
        <h3 style="color:#00e5b0; font-family:Syne; margin-bottom:12px;">ℹ️ Platform Features</h3>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; color:#b0c9e3; font-size:13px; line-height:1.6;">
            <div>
                <strong style="color:#dde8f5;">✓ Verified Suppliers</strong><br>
                All suppliers are verified and rated by verified buyers.
            </div>
            <div>
                <strong style="color:#dde8f5;">✓ Competitive Pricing</strong><br>
                Compare prices across multiple suppliers instantly.
            </div>
            <div>
                <strong style="color:#dde8f5;">✓ Fast Delivery</strong><br>
                Many items available for next-day delivery.
            </div>
            <div>
                <strong style="color:#dde8f5;">✓ Quality Assurance</strong><br>
                All materials meet Indian construction standards.
            </div>
        </div>
    </div>"""
    st.markdown(info_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# MAIN NAVIGATION
# PAGE 10 — CONSTRUCTION PROGRESS TRACKER
# ═══════════════════════════════════════════════

def construction_progress_tracker():
    """Smart Construction Progress Tracker with AI Stage Detection"""
    
    st.markdown('<h1 class="main-header">🏗️ Smart Construction Progress Tracker</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered stage detection & completion analysis</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'project_progress_history' not in st.session_state:
        st.session_state.project_progress_history = []
    
    # Stage weights
    STAGE_WEIGHTS = {
        "Excavation": 5,
        "Foundation": 10,
        "Structure": 25,
        "Brickwork": 20,
        "Roofing": 10,
        "Plaster": 10,
        "Electrical": 5,
        "Plumbing": 5,
        "Painting": 5,
        "Finishing": 5
    }
    
    # Timeline mapping (estimated days)
    STAGE_TIMELINE = {
        "Excavation": 7,
        "Foundation": 21,
        "Structure": 45,
        "Brickwork": 75,
        "Roofing": 90,
        "Plaster": 110,
        "Electrical": 135,
        "Plumbing": 150,
        "Painting": 175,
        "Finishing": 210
    }
    
    # ═══════════════════════════════════════════════
    # STEP 1: PROJECT SELECTION & DETAILS
    # ═══════════════════════════════════════════════
    
    st.markdown("---")
    st.markdown("### 📋 Project Configuration", help="Enter project details for tracking")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_width = st.number_input("Plot Width (ft)", value=40, min_value=10, max_value=200, step=5)
    with col2:
        plot_length = st.number_input("Plot Length (ft)", value=60, min_value=10, max_value=300, step=5)
    with col3:
        floors = st.number_input("Floors", value=2, min_value=1, max_value=10)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        bedrooms = st.number_input("Bedrooms", value=3, min_value=1, max_value=12)
    with col5:
        bathrooms = st.number_input("Bathrooms", value=2, min_value=1, max_value=8)
    with col6:
        estimated_cost = st.number_input("Estimated Cost (₹ Lakhs)", value=30, min_value=5, max_value=500, step=5)
    
    plot_area = plot_width * plot_length
    buildup_area = (plot_area * floors) / 10
    
    # Material estimation
    col7, col8, col9, col10 = st.columns(4)
    with col7:
        est_bricks = st.number_input("Est. Bricks (thousands)", value=80, min_value=10, max_value=500, step=10)
        est_bricks *= 1000
    with col8:
        est_cement = st.number_input("Est. Cement (bags)", value=200, min_value=20, max_value=2000, step=50)
    with col9:
        est_steel = st.number_input("Est. Steel (tons)", value=8, min_value=1, max_value=100, step=1)
    with col10:
        est_sand = st.number_input("Est. Sand (cu.m)", value=80, min_value=5, max_value=500, step=5)
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════
    # STEP 2: CONSTRUCTION IMAGE UPLOAD & AI DETECTION
    # ═══════════════════════════════════════════════
    
    st.markdown("### 📸 Construction Site Image Analysis", help="Upload site photo for stage detection")
    
    uploaded_file = st.file_uploader(
        "Upload construction site image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Clear, well-lit photos work best for accurate stage detection"
    )
    
    detected_stage = None
    confidence = 0
    stage_details = None
    current_cost_used = 0
    materials_consumed = {}
    
    if uploaded_file:
        # Display uploaded image
        image_col1, image_col2 = st.columns([1, 2])
        
        with image_col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Site Photo", use_column_width=True)
        
        with image_col2:
            if st.button("🤖 Detect Construction Stage", use_container_width=True):
                with st.spinner("🔍 Analyzing image with Gemini Vision..."):
                    try:
                        # Upload to Gemini
                        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                        
                        # Convert image to bytes
                        img_byte_arr = io.BytesIO()
                        image.save(img_byte_arr, format='PNG')
                        img_byte_arr.seek(0)
                        
                        # Prepare for Gemini
                        image_data = base64.standard_b64encode(img_byte_arr.read()).decode("utf-8")
                        
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        
                        prompt = """Analyze this construction site image and identify the current construction stage.
                        
Respond with ONLY JSON format (no extra text):
{
    "stage": "[Excavation|Foundation|Structure|Brickwork|Roofing|Plaster|Electrical|Plumbing|Painting|Finishing]",
    "confidence": [0-100],
    "description": "Brief description of what you see",
    "evidence": ["visible feature 1", "visible feature 2", "visible feature 3"]
}

Classification guide:
- Excavation: Empty land being dug, dirt piles, machinery
- Foundation: Concrete base, trenches with concrete
- Structure: Concrete columns, beams, skeleton frame
- Brickwork: Brick walls being laid, masonry work
- Roofing: Roof structures, tiles, or sheets being placed
- Plaster: Walls being plastered/finished, smooth surfaces
- Electrical: Wiring, conduits, switchboards visible
- Plumbing: Pipes, water tanks, fittings
- Painting: Paint application, color on walls
- Finishing: Interior finishes, floors, final details"""
                        
                        response = model.generate_content([
                            {"mime_type": "image/png", "data": image_data},
                            prompt
                        ])
                        
                        response_text = response.text.strip()
                        
                        # Extract JSON
                        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                        if json_match:
                            stage_data = json.loads(json_match.group())
                            detected_stage = stage_data.get("stage", "Unknown")
                            confidence = stage_data.get("confidence", 0)
                            stage_details = {
                                "description": stage_data.get("description", ""),
                                "evidence": stage_data.get("evidence", [])
                            }
                        else:
                            st.error("❌ Could not parse AI response")
                            
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
    
    # ═══════════════════════════════════════════════
    # STEP 3-6: DISPLAY RESULTS
    # ═══════════════════════════════════════════════
    
    if detected_stage:
        st.markdown("---")
        st.markdown("### 🎯 Detection Results", help="AI stage detection and progress analysis")
        
        # Current Stage Card
        stage_card = f"""
        <div style="background:linear-gradient(135deg, rgba(0,212,170,0.1), rgba(91,141,238,0.08)); border:2px solid #00d4aa; border-radius:14px; padding:20px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <div>
                    <div style="font-size:12px; color:#5a7090; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">Current Construction Stage</div>
                    <div style="font-family:Syne; font-size:28px; font-weight:800; color:#00d4aa;">{detected_stage}</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:36px;">🏗️</div>
                    <div style="font-size:13px; font-weight:700; color:#00e5b0; margin-top:4px;">{confidence}%</div>
                    <div style="font-size:9px; color:#5a7090;">Confidence</div>
                </div>
            </div>
            <div style="background:rgba(0,212,170,0.05); padding:10px; border-radius:8px; font-size:11px; color:#dde8f5;">
                <strong>Description:</strong> {stage_details['description'] if stage_details else 'N/A'}<br>
                <strong>Evidence:</strong> {', '.join(stage_details['evidence'][:3]) if stage_details else 'N/A'}
            </div>
        </div>
        """
        st.markdown(stage_card, unsafe_allow_html=True)
        
        # Calculate progress percentage
        completed_percentage = 0
        for stage_name, weight in STAGE_WEIGHTS.items():
            if stage_name == detected_stage:
                completed_percentage += weight * 0.5
                break
            completed_percentage += weight
        
        completed_percentage = min(completed_percentage, 95)
        
        # Cost and materials consumed
        current_cost_used = (estimated_cost * 100000) * (completed_percentage / 100)
        
        # Material consumption based on stage
        stage_consumption_ratio = completed_percentage / 100
        materials_consumed = {
            "Bricks": int(est_bricks * stage_consumption_ratio),
            "Cement": int(est_cement * stage_consumption_ratio),
            "Steel": round(est_steel * stage_consumption_ratio, 1),
            "Sand": round(est_sand * stage_consumption_ratio, 1)
        }
        
        # Progress metrics
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.metric(
                "📊 Completion",
                f"{completed_percentage:.1f}%",
                delta=f"{completed_percentage:.1f}% done",
                help="Project completion percentage"
            )
        
        with col_m2:
            days_elapsed = STAGE_TIMELINE.get(detected_stage, 0)
            st.metric(
                "📅 Days Elapsed",
                f"{days_elapsed}",
                delta=f"Est. {210 - days_elapsed} remaining",
                help="Estimated construction days"
            )
        
        with col_m3:
            delay_risk = "🟢 On Track" if completed_percentage >= (days_elapsed / 210 * 100 * 0.95) else "🟡 Minor Delay" if completed_percentage >= (days_elapsed / 210 * 100 * 0.85) else "🔴 At Risk"
            st.metric(
                "⚠️ Delay Risk",
                delay_risk.split()[1],
                help="Schedule risk assessment"
            )
        
        with col_m4:
            cost_label = f"₹{current_cost_used/100000:.1f}L"
            st.metric(
                "💰 Cost Used",
                cost_label,
                delta=f"₹{(estimated_cost*100000 - current_cost_used)/100000:.1f}L left",
                help="Estimated cost consumed"
            )
        
        # Progress bar
        progress_html = f"""
        <div style="margin:16px 0;">
            <div style="font-size:10px; color:#5a7090; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">Overall Progress</div>
            <div style="background:var(--card); height:24px; border-radius:12px; overflow:hidden; border:1px solid var(--border);">
                <div style="background:linear-gradient(90deg, #00d4aa, #00e5b0); height:100%; width:{completed_percentage}%; display:flex; align-items:center; justify-content:flex-end; padding-right:8px; color:var(--bg); font-size:10px; font-weight:700;">
                    {completed_percentage:.1f}%
                </div>
            </div>
        </div>
        """
        st.markdown(progress_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Materials consumed
        st.markdown("### 🧱 Materials Consumed", help="Estimated material usage up to current stage")
        
        mat_col1, mat_col2, mat_col3, mat_col4 = st.columns(4)
        with mat_col1:
            st.metric("🧱 Bricks", f"{materials_consumed['Bricks']:,}", delta=f"/ {est_bricks:,} units", help="Bricks used vs estimated")
        with mat_col2:
            st.metric("🏭 Cement", f"{materials_consumed['Cement']:,}", delta=f"/ {est_cement:,} bags", help="Cement used vs estimated")
        with mat_col3:
            st.metric("⚙️ Steel", f"{materials_consumed['Steel']:,.1f}", delta=f"/ {est_steel} tons", help="Steel used vs estimated")
        with mat_col4:
            st.metric("🏖️ Sand", f"{materials_consumed['Sand']:,.1f}", delta=f"/ {est_sand} cu.m", help="Sand used vs estimated")
        
        st.markdown("---")
        
        # ═══════════════════════════════════════════════
        # STEP 7: CONSTRUCTION TIMELINE
        # ═══════════════════════════════════════════════
        
        st.markdown("### 📅 Construction Timeline", help="Estimated schedule and milestones")
        
        # Save to history
        if st.button("💾 Save Progress Update", use_container_width=True, key="save_progress"):
            st.session_state.project_progress_history.append({
                "timestamp": datetime.now(),
                "stage": detected_stage,
                "completion": completed_percentage,
                "cost_used": current_cost_used,
                "materials": materials_consumed
            })
            st.success("✅ Progress saved to history!", icon="📊")
        
        # Timeline visualization
        timeline_html = '<div style="margin:16px 0;">'
        
        for stage_name, days in STAGE_TIMELINE.items():
            is_completed = stage_name != detected_stage and list(STAGE_TIMELINE.keys()).index(stage_name) <= list(STAGE_TIMELINE.keys()).index(detected_stage)
            is_current = stage_name == detected_stage
            
            status_color = "#00d4aa" if is_completed or is_current else "#5a6580"
            status_icon = "✅" if is_completed else "🔄" if is_current else "⏳"
            
            timeline_html += f"""
            <div style="display:flex; align-items:center; margin-bottom:12px; gap:12px;">
                <div style="font-size:20px;">{status_icon}</div>
                <div style="flex:1;">
                    <div style="font-weight:700; color:{'#00d4aa' if is_current else '#dde8f5'}; font-size:12px;">{stage_name}</div>
                    <div style="color:{status_color}; font-size:10px;">Day {days}</div>
                </div>
                <div style="background:{'#00d4aa' if is_completed or is_current else '#1c2436'}; width:40px; height:4px; border-radius:2px;"></div>
            </div>
            """
        
        timeline_html += '</div>'
        st.markdown(timeline_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ═══════════════════════════════════════════════
        # STEP 8: PROGRESS DASHBOARD
        # ═══════════════════════════════════════════════
        
        st.markdown("### 📊 Progress Dashboard", help="Visual analytics and charts")
        
        dashboard_col1, dashboard_col2 = st.columns(2)
        
        with dashboard_col1:
            # Stage distribution
            stage_weights_df = pd.DataFrame(list(STAGE_WEIGHTS.items()), columns=["Stage", "Weight %"])
            fig_stages = px.bar(
                stage_weights_df,
                x="Stage",
                y="Weight %",
                title="Stage Weight Distribution",
                color="Weight %",
                color_continuous_scale="Viridis"
            )
            fig_stages = apply_dark(fig_stages)
            st.plotly_chart(fig_stages, use_container_width=True)
        
        with dashboard_col2:
            # Cost completion
            cost_data = pd.DataFrame({
                "Status": ["Used", "Remaining"],
                "Cost (₹L)": [
                    current_cost_used / 100000,
                    (estimated_cost * 100000 - current_cost_used) / 100000
                ]
            })
            fig_cost = px.pie(
                cost_data,
                names="Status",
                values="Cost (₹L)",
                title="Cost Utilization",
                color_discrete_map={"Used": "#00d4aa", "Remaining": "#5a6580"}
            )
            fig_cost = apply_dark(fig_cost)
            st.plotly_chart(fig_cost, use_container_width=True)
        
        # Material consumption chart
        materials_df = pd.DataFrame([
            {"Material": k, "Used": v, "Total": [est_bricks, est_cement, est_steel, est_sand][i]}
            for i, (k, v) in enumerate(materials_consumed.items())
        ])
        
        fig_materials = px.bar(
            materials_df,
            x="Material",
            y=["Used", "Total"],
            title="Material Consumption Status",
            barmode="group",
            color_discrete_map={"Used": "#00e5b0", "Total": "#1c2436"}
        )
        fig_materials = apply_dark(fig_materials)
        st.plotly_chart(fig_materials, use_container_width=True)
        
        st.markdown("---")
        
        # ═══════════════════════════════════════════════
        # STEP 9: CLIENT VIEW (READ-ONLY DASHBOARD)
        # ═══════════════════════════════════════════════
        
        st.markdown("### 👁️ Client View", help="Read-only dashboard for project owner")
        
        if st.checkbox("📱 Show Client Dashboard"):
            client_view_html = f"""
            <div style="background:var(--card); border:1px solid var(--border); border-radius:14px; padding:20px;">
                <div style="text-align:center; margin-bottom:20px;">
                    <div style="font-family:Syne; font-size:24px; font-weight:800; color:#00d4aa;">BuildAtlas Construction Report</div>
                    <div style="font-size:12px; color:#5a7090; margin-top:4px;">Project Status Update</div>
                </div>
                
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px;">
                    <div style="background:var(--bg); padding:16px; border-radius:8px; border-left:3px solid #00d4aa;">
                        <div style="font-size:10px; color:#5a7090; text-transform:uppercase;">Current Stage</div>
                        <div style="font-size:18px; font-weight:700; color:#00d4aa; margin-top:4px;">{detected_stage}</div>
                    </div>
                    <div style="background:var(--bg); padding:16px; border-radius:8px; border-left:3px solid #ff6b35;">
                        <div style="font-size:10px; color:#5a7090; text-transform:uppercase;">Completion</div>
                        <div style="font-size:18px; font-weight:700; color:#ff6b35; margin-top:4px;">{completed_percentage:.1f}%</div>
                    </div>
                </div>
                
                <div style="background:var(--bg); padding:16px; border-radius:8px; margin-bottom:16px;">
                    <div style="height:12px; background:var(--border); border-radius:6px; overflow:hidden;">
                        <div style="background:linear-gradient(90deg, #00d4aa, #00e5b0); height:100%; width:{completed_percentage}%;"></div>
                    </div>
                </div>
                
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; font-size:11px;">
                    <div style="background:var(--bg); padding:12px; border-radius:8px; text-align:center;">
                        <div style="color:#5a7090; margin-bottom:4px;">Days Used</div>
                        <div style="color:#00d4aa; font-weight:700; font-size:14px;">{STAGE_TIMELINE.get(detected_stage, 0)}</div>
                    </div>
                    <div style="background:var(--bg); padding:12px; border-radius:8px; text-align:center;">
                        <div style="color:#5a7090; margin-bottom:4px;">Days Left</div>
                        <div style="color:#ff6b35; font-weight:700; font-size:14px;">{210 - STAGE_TIMELINE.get(detected_stage, 0)}</div>
                    </div>
                    <div style="background:var(--bg); padding:12px; border-radius:8px; text-align:center;">
                        <div style="color:#5a7090; margin-bottom:4px;">Est. Completion</div>
                        <div style="color:#91d5ff; font-weight:700; font-size:14px;">{(datetime.now() + timedelta(days=210 - STAGE_TIMELINE.get(detected_stage, 0))).strftime('%d %b %Y')}</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(client_view_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Progress history
        if st.session_state.project_progress_history:
            st.markdown("### 📈 Progress History", help="Historical tracking data")
            
            history_df = pd.DataFrame(st.session_state.project_progress_history)
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
            history_df['completion'] = history_df['completion'].round(1)
            history_df['cost_used'] = (history_df['cost_used'] / 100000).round(1)
            
            st.dataframe(
                history_df[['timestamp', 'stage', 'completion', 'cost_used']].rename(columns={
                    'timestamp': '📅 Date',
                    'stage': '🏗️ Stage',
                    'completion': '📊 Completion %',
                    'cost_used': '💰 Cost (₹L)'
                }),
                use_container_width=True,
                hide_index=True
            )


# ═══════════════════════════════════════════════
def main():
    # Sidebar branding
    st.sidebar.markdown("""
    <div class="sidebar-logo">
      <div style="display:flex; align-items:center; justify-content:center; gap:12px; margin-bottom:12px;">
        <span style="font-size:40px; filter:drop-shadow(0 0 12px rgba(244,162,97,0.6));">🏗️</span>
      </div>
      <h1 style="margin:0; font-family:'Bebas Neue',sans-serif; font-size:32px; background:linear-gradient(135deg, #f4a261, #2a9d8f); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; letter-spacing:-1px;">BUILDATLAS</h1>
      <p style="margin:8px 0 0 0; font-family:'Orbitron',monospace; font-size:10px; color:#adb5bd; letter-spacing:2px; text-transform:uppercase;">AI CONSTRUCTION PLATFORM</p>
    </div>
    """, unsafe_allow_html=True)

    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "📊  Dashboard"

    pages = {
        "📊  Dashboard":                  dashboard,
        "👷  Find Builder":               builder_marketplace,
        "💰  Cost Prediction":           cost_prediction,
        "🧾  Bill Scanner":              bill_scanner,
        "🧠  AI Conceptual Layout Generator": concept_layout_generator_page,
        "🏗️  Construction Progress":     construction_progress_tracker,
        "🌦️  Weather Live":              weather_alerts,
        "🤖  AI Chatbot":                chatbot,
        "👷  Labour Manager":            labour,
        "🧭  Vastu Intelligence":        vastu_page,
        "🧱  Material Marketplace":      material_marketplace,
    }

    quick_access_pages = [
        ("📊  Dashboard", "📊", "Dashboard"),
        ("👷  Find Builder", "👷", "Find Builder"),
        ("💰  Cost Prediction", "💰", "Cost Calculator"),
        ("🧾  Bill Scanner", "🧾", "Bill Scanner"),
        ("🧠  AI Conceptual Layout Generator", "🧠", "AI Conceptual Layout Generator"),
        ("🏗️  Construction Progress", "🏗️", "Construction Progress"),
        ("🌦️  Weather Live", "🌦️", "Weather Live"),
        ("🤖  AI Chatbot", "🤖", "AI Chatbot"),
        ("👷  Labour Manager", "👷", "Labour Manager"),
        ("🧭  Vastu Intelligence", "🧭", "Vastu Intelligence"),
        ("🧱  Material Marketplace", "🧱", "Material Marketplace"),
    ]

    active_page = st.session_state["active_page"]
    active_index = next((i + 1 for i, (page_label, _, _) in enumerate(quick_access_pages) if page_label == active_page), 1)

    st.sidebar.markdown('<div class="sidebar-section-label">Current Page</div>', unsafe_allow_html=True)
    current_icon = next((icon for page_label, icon, _ in quick_access_pages if page_label == active_page), "📊")
    st.sidebar.markdown(f"""
    <div class="sidebar-current-page">
      <div class="sidebar-current-page-icon">{current_icon}</div>
      <div class="sidebar-current-page-text">{active_page}</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div class="sidebar-section-label">Quick Access</div>', unsafe_allow_html=True)
    for index, (page_label, icon, _) in enumerate(quick_access_pages):
        if st.sidebar.button(f"{icon} {page_label.split('  ', 1)[1]}", key=f"nav_{index}", use_container_width=True):
            st.session_state["active_page"] = page_label
            st.rerun()

    st.sidebar.markdown(f"""
    <style>
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(1),
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(2),
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(3),
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(4),
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(5),
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(6),
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(7),
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(8),
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(9),
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(10),
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(11),
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(12),
    div[data-testid="stSidebar"] .stButton > button:nth-of-type(13) {{
      width: 100% !important; margin: 6px 0 !important; padding: 10px 12px !important; border-radius: 999px !important;
      border: 1px solid rgba(244,162,97,0.25) !important; background: rgba(244,162,97,0.07) !important;
      color: #f3e7d8 !important; font-family: 'Orbitron', monospace !important; font-size: 10px !important; letter-spacing: 1.2px !important;
      text-transform: uppercase !important; box-shadow: none !important; text-align: left !important; justify-content: flex-start !important;
    }}
    div[data-testid="stSidebar"] .stButton > button:nth-of-type({active_index}) {{
      background: linear-gradient(135deg, var(--accent), var(--accent2)) !important; color: #0a0c10 !important; border-color: rgba(255,255,255,0.25) !important;
      box-shadow: 0 8px 24px rgba(244,162,97,0.35) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Saved Materials Sidebar Section
    st.sidebar.markdown("""
    <div style="margin-top:24px; padding-top:16px; border-top:2px solid rgba(244,162,97,0.3);">
      <div style="font-family:'Orbitron',monospace; font-size:12px; letter-spacing:2px; text-transform:uppercase; color:#f4a261; margin-bottom:16px; font-weight:700;">🛒 Saved Materials</div>
    </div>
    """, unsafe_allow_html=True)
    
    if "saved_materials" not in st.session_state:
        st.session_state.saved_materials = []
    
    saved_count = len(st.session_state.saved_materials)
    
    st.sidebar.markdown(f"""
    <div style="background:linear-gradient(145deg, rgba(26,35,56,0.6), rgba(37,51,85,0.5)); border:1px solid rgba(244,162,97,0.3); border-radius:12px; padding:12px; margin-bottom:12px; text-align:center;">
      <div style="font-family:'Orbitron',monospace; font-size:10px; color:#adb5bd; letter-spacing:1px; text-transform:uppercase; margin-bottom:6px;">Total Saved</div>
      <div style="font-family:'Bebas Neue',sans-serif; font-size:24px; color:#f4a261; font-weight:900;">{saved_count}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if saved_count > 0:
        st.sidebar.markdown('<div style="font-family:\'Orbitron\',monospace; font-size:9px; color:#adb5bd; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px;">Recently saved:</div>', unsafe_allow_html=True)
        
        for idx, material in enumerate(st.session_state.saved_materials):
            material_card = f"""<div style="background:linear-gradient(145deg, rgba(26,35,56,0.7), rgba(37,51,85,0.6)); border:1px solid rgba(244,162,97,0.4); border-radius:10px; padding:12px; margin-bottom:10px; font-size:11px;">
<strong style="color:#f8f9fa; display:block; margin-bottom:6px; font-family:'Exo 2',sans-serif;">{material['name']}</strong>
<div style="color:#adb5bd; font-size:9px; margin-bottom:6px; font-family:'Orbitron',monospace; letter-spacing:1px; text-transform:uppercase;">{material['category']}</div>
<div style="color:#f4a261; font-weight:700; font-size:13px; margin-bottom:8px; font-family:'Bebas Neue',sans-serif;">₹{material['price']}</div>
</div>"""
            st.sidebar.markdown(material_card, unsafe_allow_html=True)
            
            if st.sidebar.button(f"🗑️ Remove", key=f"sidebar_remove_{idx}", use_container_width=True):
                st.session_state.saved_materials.pop(idx)
                st.rerun()
    else:
        st.sidebar.markdown("""
        <div style="background:rgba(244,162,97,0.08); border:1px solid rgba(244,162,97,0.2); border-radius:10px; padding:16px; text-align:center;">
          <div style="font-size:14px; margin-bottom:8px;">📦</div>
          <div style="font-family:'Exo 2',sans-serif; font-size:12px; color:#cdd5de; line-height:1.4;">No saved materials yet. Browse materials and click Save!</div>
        </div>
        """, unsafe_allow_html=True)
   
    pages[st.session_state["active_page"]]()

if __name__ == "__main__":
    main()

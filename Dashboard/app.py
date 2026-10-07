import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import base64
import math
import requests
import time

st.set_page_config(
    page_title="Smart EV Motor Protection System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "https://smart-ev-motor-protection.onrender.com/data"

try:
    response = requests.get(API_URL, timeout=5)
    data = response.json() if response.status_code == 200 else None
except Exception:
    data = None

temperature = float(data.get("temperature", 0.0)) if data else 0.0
current = float(data.get("current", 0.0)) if data else 0.0
voltage = float(data.get("voltage", 0.0)) if data else 0.0
fan_on = bool(data.get("fan", False)) if data else False
system_on = bool(data.get("system", False)) if data else False
system_status = str(data.get("status", "NOT CONNECTED")) if data else "NOT CONNECTED"
speed = max(0.0, min(float(data.get("speed", 0.0)) if data else 0.0, 100.0))
battery_health = data.get("battery_health") if data else None

odo = 1256
range_km = 78
now = datetime.now(ZoneInfo("Asia/Kolkata"))
current_time = now.strftime("%I:%M %p")

status_upper = system_status.upper()
if "ACCIDENT" in status_upper:
    status_label = "ACCIDENT DETECTED"
    status_color = "#62D62F"
elif any(x in status_upper for x in ("CRITICAL", "WARNING", "LOAD RISING")):
    status_label = status_upper
    status_color = "#FF4747"
elif data is None:
    status_label = "NOT CONNECTED"
    status_color = "#FF4747"
else:
    status_label = "NORMAL"
    status_color = "#62D62F"

ready = bool(data) and system_on and "ACCIDENT" not in status_upper and "CRITICAL" not in status_upper
ready_label = "READY" if ready else "NOT READY"
ready_color = "#62D62F" if ready else "#FF4747"
drive_mode = "D" if system_on else "P"

def svg_data(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

def icon_svg(kind, color):
    if kind == "temp":
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><g fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M32 10a8 8 0 0 0-8 8v22a13 13 0 1 0 16 0V18a8 8 0 0 0-8-8z"/><path d="M32 29v17"/><circle cx="32" cy="49" r="6" fill="{color}" stroke="none"/><path d="M45 17h5M45 25h5M45 33h5"/></g></svg>'''
    elif kind == "bolt":
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path d="M36 5 13 36h16l-4 23 26-34H34z" fill="{color}"/></svg>'''
    elif kind == "fan":
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><g fill="{color}"><circle cx="32" cy="32" r="7"/><path d="M31 25C18 25 12 18 15 11c3-7 13-7 18 0 4 7 1 12-2 14z"/><path d="M39 31c7-11 15-12 20-7 5 5 1 14-7 16-8 2-12-3-13-6z"/><path d="M35 39c11 6 12 14 7 19-5 5-14 1-16-7-2-8 3-12 6-12z"/><path d="M25 35c-6 11-14 12-19 7-5-5-1-14 7-16 8-2 12 3 12 9z"/></g></svg>'''
    elif kind == "battery":
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><g fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"><rect x="13" y="10" width="38" height="48" rx="5"/><path d="M25 5h14"/><path d="M32 20 24 34h7l-2 10 11-15h-7z" fill="{color}" stroke="none"/></g></svg>'''
    elif kind == "shield":
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path d="M32 6 53 14v16c0 14-8 23-21 29C19 53 11 44 11 30V14z" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/><path d="m22 32 7 7 14-15" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
    elif kind == "light":
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><g fill="none" stroke="{color}" stroke-width="3.5" stroke-linecap="round"><path d="M13 25h17c10 0 17 6 17 14s-7 14-17 14H13z"/><path d="M13 30H5M13 37H3M13 44H5"/><path d="M31 25v28"/></g></svg>'''
    else:
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path d="M32 6 57 54H7z" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/><path d="M32 22v17" stroke="{color}" stroke-width="5" stroke-linecap="round"/><circle cx="32" cy="46" r="3" fill="{color}"/></svg>'''
    return svg_data(svg)

def gauge_svg(value):
    cx, cy, radius = 260, 245, 178
    start = 220
    end = -40
    sweep = start - end
    arc_len = math.pi * radius * sweep / 180.0

    def point(deg, r=radius):
        a = math.radians(deg)
        return cx + r * math.cos(a), cy - r * math.sin(a)

    def path_for(v1, v2):
        p1 = point(start - sweep * v1 / 100)
        p2 = point(start - sweep * v2 / 100)
        large = 1 if abs(v2 - v1) > 50 else 0
        return f"M {p1[0]:.1f} {p1[1]:.1f} A {radius} {radius} 0 {large} 1 {p2[0]:.1f} {p2[1]:.1f}"

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 500" width="100%" height="100%">',
        '<defs>',
        '<filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        '<linearGradient id="green" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#63D62E"/><stop offset="1" stop-color="#59D52A"/></linearGradient>',
        '</defs>',
        f'<path d="{path_for(0,100)}" fill="none" stroke="#253440" stroke-width="30" stroke-linecap="butt"/>',
        f'<path d="{path_for(0,40)}" fill="none" stroke="url(#green)" stroke-width="30" stroke-linecap="butt"/>',
        f'<path d="{path_for(40,55)}" fill="none" stroke="#1679E7" stroke-width="30" stroke-linecap="butt"/>'
    ]

    for v in range(0, 101, 5):
        deg = start - sweep * v / 100
        r1 = 160 if v % 10 == 0 else 166
        r2 = 184
        x1, y1 = point(deg, r1)
        x2, y2 = point(deg, r2)
        w = 3.5 if v % 10 == 0 else 2
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#F4F6F8" stroke-width="{w}"/>')

    for v in (0, 50, 100):
        deg = start - sweep * v / 100
        x, y = point(deg, 145)
        parts.append(f'<text x="{x:.1f}" y="{y+7:.1f}" text-anchor="middle" fill="#F4F6F8" font-family="Arial" font-size="20" font-weight="500">{v}</text>')

    needle_deg = start - sweep * value / 100
    nx, ny = point(needle_deg, 170)
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" filter="url(#glow)"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="#FFFFFF"/>')
    parts.append(f'<text x="{cx}" y="275" text-anchor="middle" fill="#F7F8FA" font-family="Arial" font-size="72" font-weight="700">{value:.0f}</text>')
    parts.append(f'<text x="{cx}" y="313" text-anchor="middle" fill="#F7F8FA" font-family="Arial" font-size="25">km/h</text>')
    parts.append(f'<text x="{cx}" y="383" text-anchor="middle" fill="#63D62E" font-family="Arial" font-size="48" font-weight="700">{drive_mode}</text>')
    parts.append('<line x1="125" y1="386" x2="205" y2="386" stroke="#20313D" stroke-width="2"/>')
    parts.append('<line x1="315" y1="386" x2="395" y2="386" stroke="#20313D" stroke-width="2"/>')
    parts.append('</svg>')
    return svg_data("".join(parts))

temp_icon = icon_svg("temp", "#1484FF")
bolt_icon = icon_svg("bolt", "#FFC400")
fan_icon = icon_svg("fan", "#63D62E")
battery_icon = icon_svg("battery", "#1484FF")
shield_icon = icon_svg("shield", "#63D62E")
light_icon = icon_svg("light", "#63D62E")
warning_icon = icon_svg("warning", "#FFC400")
gauge_image = gauge_svg(speed)

temp_pct = max(0.0, min(temperature / 120.0, 1.0))
current_pct = max(0.0, min(current / 30.0, 1.0))
temp_marker = temp_pct * 100
current_marker = current_pct * 100

st.markdown(
    f"""
<style>
html,body,[data-testid="stAppViewContainer"] {{
    background:#020B10 !important;
}}
[data-testid="stHeader"],[data-testid="stToolbar"],footer {{
    display:none !important;
}}
.main .block-container {{
    max-width:1500px !important;
    padding:0.8rem 2.4rem 0.4rem !important;
}}
.stApp {{
    background:
        radial-gradient(circle at 15% 30%,rgba(0,90,160,.10),transparent 28%),
        radial-gradient(circle at 85% 30%,rgba(0,90,160,.08),transparent 28%),
        #020B10;
}}
.dashboard {{
    color:#F5F7F9;
    font-family:Arial,Helvetica,sans-serif;
}}
.top {{
    display:grid;
    grid-template-columns:1fr 1fr 1fr;
    align-items:center;
    height:72px;
    border-bottom:1px solid rgba(160,185,205,.28);
}}
.brand {{
    font-size:31px;
    font-weight:700;
    letter-spacing:.2px;
}}
.brand .ev {{color:#63D62E;font-weight:800;}}
.brand .system {{color:#F3F5F7;}}
.clock {{
    text-align:center;
    font-size:25px;
    font-weight:700;
}}
.ready {{
    text-align:right;
    color:{ready_color};
    font-size:27px;
    font-weight:700;
}}
.main-grid {{
    display:grid;
    grid-template-columns:28% 44% 28%;
    align-items:center;
    gap:0;
    padding:12px 0 4px;
}}
.left-stack,.right-stack {{
    display:flex;
    flex-direction:column;
    gap:10px;
}}
.card {{
    min-height:145px;
    border:1px solid rgba(130,160,182,.28);
    border-radius:15px;
    background:linear-gradient(145deg,rgba(12,24,34,.92),rgba(2,10,15,.97));
    box-shadow:inset 0 0 18px rgba(80,140,180,.025),0 4px 16px rgba(0,0,0,.22);
    padding:17px 22px 14px;
}}
.card-title {{
    display:flex;
    align-items:center;
    gap:16px;
    font-size:22px;
    font-weight:700;
    color:#F1F4F7;
    line-height:1;
}}
.icon {{
    width:55px;
    height:55px;
    object-fit:contain;
    flex:none;
}}
.card-value {{
    margin:7px 0 10px 72px;
    font-size:43px;
    font-weight:700;
    line-height:1;
}}
.blue {{color:#1484FF;}}
.yellow {{color:#FFC400;}}
.green {{color:#63D62E;}}
.red {{color:#FF4747;}}
.unit {{
    color:#E9EDF0;
    font-size:23px;
    font-weight:400;
}}
.gradient-bar {{
    height:11px;
    border-radius:8px;
    background:linear-gradient(90deg,#62D62E 0%,#62D62E {temp_marker if temp_marker > 0 else 0:.1f}%,#F1D328 {max(temp_marker-5,0):.1f}%,#F1D328 {min(temp_marker+5,100):.1f}%,#EE4540 100%);
}}
.current-bar {{
    height:11px;
    border-radius:8px;
    background:linear-gradient(90deg,#62D62E 0%,#62D62E {current_marker if current_marker > 0 else 0:.1f}%,#F1D328 {max(current_marker-5,0):.1f}%,#F1D328 {min(current_marker+5,100):.1f}%,#EE4540 100%);
}}
.scale {{
    display:flex;
    justify-content:space-between;
    margin-top:7px;
    font-size:17px;
    color:#F0F2F4;
}}
.center {{
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:510px;
}}
.gauge {{
    width:100%;
    max-width:540px;
    height:auto;
}}
.fan-card {{
    min-height:125px;
}}
.fan-title-row {{
    display:flex;
    align-items:center;
    gap:16px;
}}
.fan-value {{
    margin:8px 0 0 73px;
    font-size:43px;
    font-weight:700;
}}
.auto {{
    margin-left:73px;
    margin-top:7px;
    font-size:17px;
    color:#F0F2F4;
}}
.small-card {{
    min-height:92px;
    padding-top:14px;
    padding-bottom:10px;
}}
.small-card .card-title {{
    font-size:20px;
}}
.small-card .icon {{
    width:48px;
    height:48px;
}}
.small-value {{
    margin:2px 0 0 73px;
    font-size:38px;
    font-weight:700;
}}
.status-value {{
    margin:4px 0 0 73px;
    font-size:27px;
    font-weight:700;
    white-space:nowrap;
}}
.bottom {{
    display:grid;
    grid-template-columns:12% 38% 38% 12%;
    align-items:center;
    min-height:73px;
    border-top:1px solid rgba(160,185,205,.30);
    border-bottom:1px solid rgba(160,185,205,.18);
}}
.bottom-item {{
    height:55px;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:18px;
    border-right:1px solid rgba(160,185,205,.23);
}}
.bottom-label {{
    font-size:21px;
    color:#AEB7BF;
    font-weight:500;
}}
.bottom-value {{
    font-size:28px;
    color:#F3F5F7;
    font-weight:700;
}}
.light-icon,.warning-icon {{
    width:40px;
    height:40px;
}}
.health {{
    color:#63D62E;
}}
.caption {{
    text-align:right;
    color:#6E7B85;
    font-size:11px;
    margin-top:3px;
}}
@media(max-width:1000px) {{
    .main-grid {{grid-template-columns:1fr;}}
    .center {{order:-1;min-height:auto;}}
    .top {{grid-template-columns:1fr;height:auto;padding:10px 0;gap:5px;}}
    .clock,.ready {{text-align:center;}}
    .bottom {{grid-template-columns:1fr 1fr;}}
    .bottom-item {{border-bottom:1px solid rgba(160,185,205,.15);}}
}}
</style>

<div class="dashboard">
    <div class="top">
        <div class="brand"><span class="ev">EV</span> <span class="system">SYSTEM</span></div>
        <div class="clock">{current_time}</div>
        <div class="ready">{ready_label}</div>
    </div>

    <div class="main-grid">
        <div class="left-stack">
            <div class="card">
                <div class="card-title">
                    <img class="icon" src="{temp_icon}">
                    <span>TEMP</span>
                </div>
                <div class="card-value blue">{temperature:.0f} <span class="unit">°C</span></div>
                <div class="gradient-bar"></div>
                <div class="scale"><span>0</span><span>60</span><span>120</span></div>
            </div>

            <div class="card">
                <div class="card-title">
                    <img class="icon" src="{bolt_icon}">
                    <span>CURRENT</span>
                </div>
                <div class="card-value yellow">{current:.1f} <span class="unit">A</span></div>
                <div class="current-bar"></div>
                <div class="scale"><span>0</span><span>15</span><span>30</span></div>
            </div>
        </div>

        <div class="center">
            <img class="gauge" src="{gauge_image}">
        </div>

        <div class="right-stack">
            <div class="card fan-card">
                <div class="fan-title-row">
                    <img class="icon" src="{fan_icon}">
                    <span class="card-title">FAN</span>
                </div>
                <div class="fan-value {'green' if fan_on else ''}">{'ON' if fan_on else 'OFF'}</div>
                <div class="auto">AUTO MODE</div>
            </div>

            <div class="card small-card">
                <div class="card-title">
                    <img class="icon" src="{battery_icon}">
                    <span>VOLTAGE</span>
                </div>
                <div class="small-value blue">{voltage:.1f} <span class="unit">V</span></div>
            </div>

            <div class="card small-card">
                <div class="card-title">
                    <img class="icon" src="{shield_icon}">
                    <span>STATUS</span>
                </div>
                <div class="status-value" style="color:{status_color}">{status_label}</div>
            </div>
        </div>
    </div>

    <div class="bottom">
        <div class="bottom-item">
            <img class="light-icon" src="{light_icon}">
        </div>
        <div class="bottom-item">
            <span class="bottom-label">ODO</span>
            <span class="bottom-value">{odo} <span style="font-size:20px">km</span></span>
        </div>
        <div class="bottom-item">
            <span class="bottom-label">RANGE</span>
            <span class="bottom-value">{range_km} <span style="font-size:20px">km</span></span>
        </div>
        <div class="bottom-item" style="border-right:none">
            <img class="warning-icon" src="{warning_icon}">
        </div>
    </div>

    <div class="caption">Last updated: {now.strftime("%d-%m-%Y")} {current_time}</div>
</div>
""",
    unsafe_allow_html=True
)

time.sleep(0.7)
st.rerun()

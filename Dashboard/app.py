import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from zoneinfo import ZoneInfo
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
speed = float(data.get("speed", 0.0)) if data else 0.0
speed = max(0.0, min(speed, 100.0))
battery_health = data.get("battery_health") if data else None

odo = 1256
range_km = 78
now = datetime.now(ZoneInfo("Asia/Kolkata"))
current_time = now.strftime("%I:%M %p")
current_date = now.strftime("%d-%m-%Y")

status_upper = system_status.upper()
if "ACCIDENT" in status_upper:
    status_label = "ACCIDENT DETECTED"
    status_color = "#FF4D4D"
elif any(x in status_upper for x in ("CRITICAL", "WARNING", "LOAD RISING")):
    status_label = status_upper
    status_color = "#FF4D4D"
elif data is None:
    status_label = "NOT CONNECTED"
    status_color = "#FF4D4D"
else:
    status_label = "NORMAL"
    status_color = "#55D72D"

ready = bool(data) and system_on and "ACCIDENT" not in status_upper and "CRITICAL" not in status_upper
ready_label = "READY" if ready else "NOT READY"
ready_color = "#55D72D" if ready else "#FF4D4D"
drive_mode = "D" if system_on else "P"

def clamp(value, low, high):
    return max(low, min(value, high))

def gauge_figure(value):
    start_angle = 210
    end_angle = -30

    def angle(v):
        return start_angle + clamp(v, 0, 100) / 100 * (end_angle - start_angle)

    def xy(radius, degrees):
        radians = math.radians(degrees)
        return radius * math.cos(radians), radius * math.sin(radians)

    def arc(start, end, color):
        outer = 1.0
        inner = 0.76
        points = []
        for i in range(61):
            a = start + (end - start) * i / 60
            points.append(xy(outer, a))
        for i in range(60, -1, -1):
            a = start + (end - start) * i / 60
            points.append(xy(inner, a))
        return go.Scatter(
            x=[p[0] for p in points],
            y=[p[1] for p in points],
            mode="lines",
            fill="toself",
            fillcolor=color,
            line={"color": color, "width": 0},
            hoverinfo="skip",
            showlegend=False
        )

    fig = go.Figure()
    fig.add_trace(arc(angle(0), angle(40), "#55D72D"))
    fig.add_trace(arc(angle(40), angle(55), "#1678E8"))
    fig.add_trace(arc(angle(55), angle(100), "#263442"))

    for value in range(0, 101, 5):
        a = angle(value)
        outer, inner = (1.17, 1.02) if value % 10 == 0 else (1.14, 1.05)
        x1, y1 = xy(outer, a)
        x2, y2 = xy(inner, a)
        fig.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode="lines",
            line={"color": "#F4F7FA", "width": 5 if value % 10 == 0 else 3},
            hoverinfo="skip",
            showlegend=False
        ))

    for value in (0, 50, 100):
        x, y = xy(1.31, angle(value))
        fig.add_annotation(
            x=x, y=y, text=str(value), showarrow=False,
            font={"size": 20, "color": "#F4F7FA"}
        )

    a = angle(speed)
    x1, y1 = xy(1.0, a)
    x2, y2 = xy(0.72, a)
    fig.add_trace(go.Scatter(
        x=[x1, x2],
        y=[y1, y2],
        mode="lines",
        line={"color": "#FFFFFF", "width": 7},
        hoverinfo="skip",
        showlegend=False
    ))

    fig.add_annotation(
        x=0, y=0.03, text=f"{speed:.0f}", showarrow=False,
        font={"size": 72, "color": "#FFFFFF", "family": "Arial Black"}
    )
    fig.add_annotation(
        x=0, y=-0.24, text="km/h", showarrow=False,
        font={"size": 24, "color": "#FFFFFF"}
    )
    fig.add_annotation(
        x=0, y=-0.52, text=drive_mode, showarrow=False,
        font={"size": 42, "color": "#55D72D", "family": "Arial Black"}
    )

    fig.update_layout(
        height=500,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis={"visible": False, "range": [-1.45, 1.45], "fixedrange": True},
        yaxis={
            "visible": False,
            "range": [-1.45, 1.45],
            "fixedrange": True,
            "scaleanchor": "x",
            "scaleratio": 1
        }
    )
    return fig

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 15% 20%, rgba(125,0,255,.15), transparent 32%),
            radial-gradient(circle at 85% 25%, rgba(0,180,255,.11), transparent 30%),
            radial-gradient(circle at 50% 90%, rgba(180,0,255,.09), transparent 35%),
            #02070B;
        background-attachment: fixed;
    }
    .stApp::before {
        content: "";
        position: fixed;
        inset: -20%;
        pointer-events: none;
        z-index: 0;
        background:
            radial-gradient(circle at 20% 30%, rgba(145,0,255,.10), transparent 22%),
            radial-gradient(circle at 80% 65%, rgba(0,140,255,.08), transparent 20%);
        filter: blur(35px);
        animation: uvGlow 8s ease-in-out infinite alternate;
    }
    @keyframes uvGlow {
        0% { transform: scale(1) translate3d(-1%,-1%,0); opacity:.65; }
        100% { transform: scale(1.08) translate3d(1%,1%,0); opacity:1; }
    }
    .main .block-container {
        position: relative;
        z-index: 1;
        max-width: 1500px;
        padding: 1rem 2.5rem;
    }
    [data-testid="stHeader"] { background:#02070B; }
    [data-testid="stToolbar"] { visibility:hidden; }

    .header {
        display:grid;
        grid-template-columns:1fr 1fr 1fr;
        align-items:center;
        padding:4px 2px 10px;
    }
    .brand { font-size:30px; font-weight:800; letter-spacing:1px; }
    .brand span { color:#55D72D; }
    .brand b { color:#F4F7FA; }
    .clock { font-size:26px; font-weight:800; text-align:center; color:#F4F7FA; }
    .ready { font-size:28px; font-weight:800; text-align:right; }

    .card {
        background:linear-gradient(145deg,rgba(15,24,35,.94),rgba(3,8,13,.97));
        border:1px solid rgba(110,145,175,.28);
        border-radius:14px;
        box-shadow:inset 0 0 18px rgba(255,255,255,.015),0 0 18px rgba(0,100,180,.08);
        padding:18px 20px;
        margin:6px 0;
    }
    .card-title { font-size:22px; font-weight:800; color:#F3F6FA; letter-spacing:.5px; }
    .value { font-size:42px; font-weight:800; line-height:1.05; margin-top:7px; }
    .blue { color:#1685FF; }
    .yellow { color:#FFC51B; }
    .green { color:#55D72D; }
    .red { color:#FF4D4D; }
    .sub { font-size:17px; color:#E4E9EF; margin-top:6px; }
    .bar {
        height:12px;
        border-radius:8px;
        margin-top:14px;
        box-shadow:0 0 8px rgba(80,210,50,.12);
    }
    .bar-line {
        position:relative;
        height:18px;
        margin-top:2px;
        color:#E5EAF0;
        font-size:13px;
    }
    .bar-line span { position:absolute; transform:translateX(-50%); }
    .bar-line .a { left:0; transform:none; }
    .bar-line .b { left:50%; }
    .bar-line .c { right:0; transform:none; }

    .status-card { min-height:108px; }
    .status { font-size:30px; font-weight:800; margin-top:5px; }
    .fan-icon { font-size:34px; margin-right:8px; }
    .bottom {
        border-top:1px solid rgba(160,190,220,.25);
        border-bottom:1px solid rgba(160,190,220,.18);
        padding:12px 8px;
        margin-top:8px;
    }
    .bottom-label {
        font-size:17px;
        color:#AEB8C4;
        font-weight:800;
        letter-spacing:1px;
    }
    .bottom-value { font-size:30px; color:#F5F7FA; font-weight:800; margin-top:2px; }
    .battery-value { color:#55D72D; }

    @media(max-width:900px) {
        .header { grid-template-columns:1fr; gap:6px; text-align:center; }
        .clock,.ready { text-align:center; }
        .main .block-container { padding-left:1rem; padding-right:1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="header">
        <div class="brand"><span>EV</span> <b>SYSTEM</b></div>
        <div class="clock">{current_time}</div>
        <div class="ready" style="color:{ready_color}">{ready_label}</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

left, center, right = st.columns([3.2, 5, 3.2], gap="medium")

with left:
    temp_pct = clamp(temperature / 120, 0, 1)
    current_pct = clamp(current / 30, 0, 1)

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">🌡️ &nbsp; TEMP</div>
            <div class="value blue">{temperature:.0f}<span style="font-size:24px"> °C</span></div>
            <div class="bar" style="background:linear-gradient(90deg,#55D72D 0%,#55D72D {temp_pct*100:.0f}%,#26313D {temp_pct*100:.0f}%,#26313D 100%)"></div>
            <div class="bar-line">
                <span class="a">0</span><span class="b">60</span><span class="c">120</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">⚡ &nbsp; CURRENT</div>
            <div class="value yellow">{current:.1f}<span style="font-size:24px"> A</span></div>
            <div class="bar" style="background:linear-gradient(90deg,#55D72D 0%,#55D72D {current_pct*100:.0f}%,#26313D {current_pct*100:.0f}%,#26313D 100%)"></div>
            <div class="bar-line">
                <span class="a">0</span><span class="b">15</span><span class="c">30</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with center:
    st.plotly_chart(
        gauge_figure(speed),
        use_container_width=True,
        config={"displayModeBar": False, "staticPlot": True}
    )

with right:
    fan_color = "#55D72D" if fan_on else "#AEB8C4"
    fan_state = "ON" if fan_on else "OFF"

    st.markdown(
        f"""
        <div class="card status-card">
            <div class="card-title"><span class="fan-icon">🌀</span> FAN</div>
            <div class="status" style="color:{fan_color}">{fan_state}</div>
            <div class="sub">AUTO MODE</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="card status-card">
            <div class="card-title">🔋 &nbsp; VOLTAGE</div>
            <div class="value blue">{voltage:.1f}<span style="font-size:24px"> V</span></div>
            <div class="sub">3S BATTERY PACK</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="card status-card">
            <div class="card-title">🛡️ &nbsp; STATUS</div>
            <div class="status" style="color:{status_color}">{status_label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div class="bottom">', unsafe_allow_html=True)
b1, b2, b3, b4 = st.columns([1.5, 2.4, 2.5, 2.2])

with b1:
    st.markdown(
        '<div class="bottom-label">💡 LIGHTS</div><div class="bottom-value green">READY</div>',
        unsafe_allow_html=True
    )

with b2:
    health_text = f"{float(battery_health):.0f} %" if battery_health is not None else "-- %"
    st.markdown(
        f'<div class="bottom-label">BATTERY HEALTH</div><div class="bottom-value battery-value">{health_text}</div>',
        unsafe_allow_html=True
    )

with b3:
    st.markdown(
        f'<div class="bottom-label">ODO</div><div class="bottom-value">{odo:06d} KM</div>',
        unsafe_allow_html=True
    )

with b4:
    st.markdown(
        f'<div class="bottom-label">RANGE</div><div class="bottom-value">{range_km} KM</div>',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)
st.caption(f"Last updated: {current_date} {current_time}")

time.sleep(0.7)
st.rerun()

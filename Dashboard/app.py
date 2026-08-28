import streamlit as st
import math
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EV System Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# EV DATA
# ============================================================
# Replace these values later with your ESP32/live sensor data.

temperature = 42.0       # °C
current = 2.6            # A
speed = 45.0             # km/h
voltage = 48.6           # V

fan_on = True
gear = "D"

odo = 1256              # km
range_km = 78           # km

# ============================================================
# STATUS LOGIC
# ============================================================

if temperature >= 100 or current >= 30:
    status = "CRITICAL"
    status_symbol = "⚠"
elif temperature >= 75 or current >= 20:
    status = "WARNING"
    status_symbol = "⚠"
else:
    status = "NORMAL"
    status_symbol = "✓"

# ============================================================
# FAN LOGIC
# ============================================================

fan_status = "ON" if fan_on else "OFF"

# ============================================================
# SPEED GAUGE
# ============================================================

MAX_SPEED = 100

# Convert speed into angle
speed_ratio = max(0, min(speed / MAX_SPEED, 1))
angle = -135 + (270 * speed_ratio)

# Gauge coordinates
cx = 150
cy = 150
radius = 110

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Remove Streamlit default spacing */
    .block-container {
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-bottom: 1rem;
        max-width: 1500px;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Main dashboard */
    .dashboard {
        background: #071017;
        border: 2px solid #263641;
        border-radius: 28px;
        padding: 25px;
        min-height: 780px;
        box-shadow:
            0 0 35px rgba(0,0,0,0.7),
            inset 0 0 25px rgba(0,0,0,0.5);
    }

    /* Header */
    .top-header {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        align-items: center;
        border-bottom: 2px solid #263641;
        padding: 5px 25px 20px 25px;
        margin-bottom: 25px;
    }

    .ev-title {
        font-size: 31px;
        font-weight: 800;
        letter-spacing: 2px;
        color: #e8f0f4;
    }

    .ev-title span {
        color: #53d329;
    }

    .clock {
        text-align: center;
        font-size: 27px;
        font-weight: 700;
        color: white;
    }

    .ready {
        text-align: right;
        font-size: 25px;
        font-weight: 800;
        color: #52d329;
    }

    /* Three columns */
    .main-grid {
        display: grid;
        grid-template-columns: 1fr 1.45fr 1fr;
        gap: 25px;
        align-items: stretch;
    }

    /* Cards */
    .card {
        background: linear-gradient(
            145deg,
            #101d25,
            #0a141b
        );

        border: 1px solid #334653;
        border-radius: 20px;
        padding: 25px;
        box-shadow:
            inset 0 0 15px rgba(255,255,255,0.02),
            0 5px 15px rgba(0,0,0,0.3);

        margin-bottom: 20px;
    }

    .card-title {
        color: #e8eef2;
        font-size: 25px;
        font-weight: 800;
        text-align: center;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    .value {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        line-height: 1;
    }

    .unit {
        font-size: 22px;
        color: #d5dce0;
        margin-left: 5px;
    }

    .blue {
        color: #1888ff;
    }

    .yellow {
        color: #ffbe16;
    }

    .green {
        color: #56d832;
    }

    /* Progress bar */
    .bar {
        height: 13px;
        border-radius: 10px;
        margin-top: 25px;
        background: linear-gradient(
            90deg,
            #54d631 0%,
            #54d631 45%,
            #ffc400 70%,
            #ff3c30 100%
        );
    }

    .scale {
        display: flex;
        justify-content: space-between;
        color: #e4e9ec;
        font-size: 18px;
        margin-top: 7px;
    }

    /* Centre gauge */
    .gauge-container {
        text-align: center;
        height: 540px;
        position: relative;
    }

    .gauge-title {
        color: #8e9ba3;
        font-size: 17px;
        letter-spacing: 2px;
        margin-top: 5px;
    }

    .speed-number {
        font-size: 90px;
        font-weight: 800;
        color: white;
        line-height: 0.95;
        margin-top: -290px;
    }

    .speed-unit {
        color: #dbe2e6;
        font-size: 25px;
        font-weight: 600;
    }

    .gear {
        font-size: 55px;
        font-weight: 800;
        color: #52d329;
        margin-top: 55px;
    }

    /* Right side */
    .fan-icon {
        font-size: 65px;
        text-align: center;
        margin: 5px;
    }

    .fan-status {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #53d329;
    }

    .fan-mode {
        text-align: center;
        color: #d8dfe3;
        font-size: 18px;
        margin-top: 5px;
    }

    .battery-icon {
        font-size: 52px;
        text-align: center;
        color: #1687ff;
    }

    .voltage {
        text-align: center;
        color: #1687ff;
        font-size: 42px;
        font-weight: 800;
    }

    .status-icon {
        text-align: center;
        font-size: 55px;
        color: #53d329;
    }

    .status-value {
        text-align: center;
        color: #53d329;
        font-size: 30px;
        font-weight: 800;
    }

    /* Bottom bar */
    .bottom-bar {
        border-top: 2px solid #263641;
        margin-top: 5px;
        padding-top: 20px;

        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        text-align: center;
    }

    .bottom-label {
        color: #9aa7ae;
        font-size: 18px;
        letter-spacing: 1px;
    }

    .bottom-value {
        color: white;
        font-size: 28px;
        font-weight: 700;
    }

    .warning {
        color: #ffc400;
        font-size: 32px;
    }

    /* Responsive */
    @media(max-width: 900px) {

        .main-grid {
            grid-template-columns: 1fr;
        }

        .top-header {
            grid-template-columns: 1fr;
            gap: 10px;
        }

        .ready,
        .ev-title,
        .clock {
            text-align: center;
        }

        .bottom-bar {
            grid-template-columns: 1fr;
            gap: 15px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# GAUGE SVG
# ============================================================

def create_gauge(speed):

    max_speed = 100
    cx = 150
    cy = 150
    r = 112

    # Background arc
    points = []

    for i in range(101):
        a = math.radians(-135 + (270 * i / 100))

        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)

        points.append(f"{x:.2f},{y:.2f}")

    background_arc = " ".join(points)

    # Green section
    green_points = []

    green_end = min(speed / max_speed, 1)

    for i in range(51):
        ratio = (green_end * i) / 50
        a = math.radians(-135 + (270 * ratio))

        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)

        green_points.append(f"{x:.2f},{y:.2f}")

    green_arc = " ".join(green_points)

    # Needle
    needle_angle = math.radians(
        -135 + (270 * min(speed / max_speed, 1))
    )

    nx = cx + 100 * math.cos(needle_angle)
    ny = cy + 100 * math.sin(needle_angle)

    # Tick marks
    ticks = ""

    for i in range(0, 101, 10):

        a = math.radians(-135 + (270 * i / 100))

        x1 = cx + 100 * math.cos(a)
        y1 = cy + 100 * math.sin(a)

        x2 = cx + 112 * math.cos(a)
        y2 = cy + 112 * math.sin(a)

        ticks += f"""
        <line
            x1="{x1:.1f}"
            y1="{y1:.1f}"
            x2="{x2:.1f}"
            y2="{y2:.1f}"
            stroke="#e6edf0"
            stroke-width="2"
        />
        """

    return f"""
    <svg
        viewBox="0 0 300 300"
        width="100%"
        height="430px"
        xmlns="http://www.w3.org/2000/svg"
    >

        <!-- Outer dark gauge -->
        <polyline
            points="{background_arc}"
            fill="none"
            stroke="#263641"
            stroke-width="22"
            stroke-linecap="round"
        />

        <!-- Green active portion -->
        <polyline
            points="{green_arc}"
            fill="none"
            stroke="#52d329"
            stroke-width="22"
            stroke-linecap="round"
        />

        <!-- Blue section -->
        <path
            d="M 118 57
               A 112 112 0 0 1 150 38"
            fill="none"
            stroke="#1687ff"
            stroke-width="22"
        />

        <!-- Ticks -->
        {ticks}

        <!-- Needle -->
        <line
            x1="{cx}"
            y1="{cy}"
            x2="{nx:.1f}"
            y2="{ny:.1f}"
            stroke="white"
            stroke-width="4"
        />

        <circle
            cx="{cx}"
            cy="{cy}"
            r="8"
            fill="white"
        />

    </svg>
    """


# ============================================================
# CURRENT TIME
# ============================================================

current_time = datetime.now().strftime("%I:%M %p")

# ============================================================
# DASHBOARD
# ============================================================

st.markdown('<div class="dashboard">', unsafe_allow_html=True)

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

st.markdown(
    f"""
    <div class="top-header">

        <div class="ev-title">
            <span>EV</span> SYSTEM
        </div>

        <div class="clock">
            {current_time}
        </div>

        <div class="ready">
            READY
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# MAIN GRID
# ------------------------------------------------------------

st.markdown('<div class="main-grid">', unsafe_allow_html=True)

# ============================================================
# LEFT COLUMN
# ============================================================

st.markdown(
    f"""
    <div>

        <!-- TEMPERATURE -->
        <div class="card">

            <div class="card-title">
                🌡️ &nbsp; TEMP
            </div>

            <div class="value blue">
                {temperature:.0f}
                <span class="unit">°C</span>
            </div>

            <div class="bar"></div>

            <div class="scale">
                <span>0</span>
                <span>60</span>
                <span>120</span>
            </div>

        </div>


        <!-- CURRENT -->
        <div class="card">

            <div class="card-title">
                ⚡ &nbsp; CURRENT
            </div>

            <div class="value yellow">
                {current:.1f}
                <span class="unit">A</span>
            </div>

            <div class="bar"></div>

            <div class="scale">
                <span>0</span>
                <span>15</span>
                <span>30</span>
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# CENTRE COLUMN
# ============================================================

st.markdown(
    f"""
    <div class="gauge-container">

        {create_gauge(speed)}

        <div class="speed-number">
            {speed:.0f}
        </div>

        <div class="speed-unit">
            km/h
        </div>

        <div class="gear">
            {gear}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# RIGHT COLUMN
# ============================================================

st.markdown(
    f"""
    <div>

        <!-- FAN -->
        <div class="card">

            <div class="card-title">
                🌀 &nbsp; FAN
            </div>

            <div class="fan-icon">
                🌀
            </div>

            <div class="fan-status">
                {fan_status}
            </div>

            <div class="fan-mode">
                AUTO MODE
            </div>

        </div>


        <!-- VOLTAGE -->
        <div class="card">

            <div class="card-title">
                🔋 &nbsp; VOLTAGE
            </div>

            <div class="battery-icon">
                🔋
            </div>

            <div class="voltage">
                {voltage:.1f}
                <span class="unit">V</span>
            </div>

        </div>


        <!-- STATUS -->
        <div class="card">

            <div class="card-title">
                🛡️ &nbsp; STATUS
            </div>

            <div class="status-icon">
                {status_symbol}
            </div>

            <div class="status-value">
                {status}
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# BOTTOM INFORMATION BAR
# ============================================================

st.markdown(
    f"""
    <div class="bottom-bar">

        <div>
            <div class="bottom-label">
                💡
            </div>
        </div>

        <div>
            <div class="bottom-label">
                ODO
            </div>

            <div class="bottom-value">
                {odo} km
            </div>
        </div>

        <div>
            <div class="bottom-label">
                RANGE
            </div>

            <div class="bottom-value">
                {range_km} km
            </div>
        </div>

        <div>
            <div class="warning">
                ⚠
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)

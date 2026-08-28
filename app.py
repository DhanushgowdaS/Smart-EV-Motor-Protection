import streamlit as st
import time
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EV Motor Protection System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background: #050b10;
    color: white;
}

/* Remove Streamlit top space */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    max-width: 1400px;
}

/* Main dashboard */
.dashboard {
    background: linear-gradient(145deg, #07131c, #02070b);
    border: 2px solid #263642;
    border-radius: 28px;
    padding: 25px;
    box-shadow: 0 0 35px rgba(0,0,0,0.7);
}

/* Header */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #34434d;
    padding-bottom: 15px;
    margin-bottom: 20px;
}

.ev-title {
    font-size: 30px;
    font-weight: bold;
}

.ev-green {
    color: #54d63b;
}

.clock {
    font-size: 25px;
    font-weight: bold;
}

.ready {
    color: #54d63b;
    font-size: 25px;
    font-weight: bold;
}

/* Cards */
.card {
    background: linear-gradient(145deg, #101e28, #071018);
    border: 1px solid #33444f;
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 18px;
    min-height: 150px;
    box-shadow: inset 0 0 15px rgba(255,255,255,0.02);
}

.card-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 12px;
}

.big-value {
    font-size: 45px;
    font-weight: bold;
}

.unit {
    font-size: 22px;
    color: #d5dce0;
}

.blue {
    color: #168cff;
}

.yellow {
    color: #ffc400;
}

.green {
    color: #55d63a;
}

.red {
    color: #ff3b30;
}

/* Fan */
.fan-icon {
    font-size: 48px;
}

.fan-status {
    font-size: 38px;
    font-weight: bold;
}

/* Central gauge */
.gauge-container {
    height: 420px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.gauge {
    width: 340px;
    height: 340px;
    border-radius: 50%;
    background:
        conic-gradient(
            #54d63b 0deg,
            #54d63b 100deg,
            #168cff 150deg,
            #17232c 150deg,
            #17232c 360deg
        );
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 0 25px rgba(40,150,255,0.15);
}

.gauge-inner {
    width: 270px;
    height: 270px;
    border-radius: 50%;
    background: #071018;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.speed {
    font-size: 70px;
    font-weight: bold;
}

.speed-unit {
    font-size: 25px;
}

.drive {
    color: #54d63b;
    font-size: 35px;
    font-weight: bold;
    margin-top: 10px;
}

/* Bottom */
.bottom-bar {
    border-top: 1px solid #34434d;
    margin-top: 15px;
    padding-top: 18px;
    display: flex;
    justify-content: space-around;
    font-size: 22px;
}

.warning {
    color: #ffc400;
    font-size: 30px;
}

/* Status */
.status-normal {
    color: #55d63a;
    font-size: 32px;
    font-weight: bold;
}

.status-warning {
    color: #ffc400;
    font-size: 32px;
    font-weight: bold;
}

.status-emergency {
    color: #ff3b30;
    font-size: 32px;
    font-weight: bold;
}

/* Hide Streamlit menu */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SENSOR VALUES
# ============================================================

# ------------------------------------------------------------
# TEMPORARY VALUES
# Replace these with ESP32 live values later
# ------------------------------------------------------------

battery_voltage = 7.65
motor_current = 0.48
motor_temperature = 30.1

# Fan condition
FAN_ON_TEMP = 31.0

if motor_temperature >= FAN_ON_TEMP:
    fan_status = "ON"
    fan_class = "green"
else:
    fan_status = "OFF"
    fan_class = "green"


# ============================================================
# MOTOR STATUS
# ============================================================

if motor_temperature >= 40:
    motor_status = "EMERGENCY"
    status_class = "status-emergency"

elif motor_temperature >= 35:
    motor_status = "WARNING"
    status_class = "status-warning"

else:
    motor_status = "NORMAL"
    status_class = "status-normal"


# ============================================================
# SPEED / ODO / RANGE
# ============================================================

# These are placeholders because we don't currently have
# a speed sensor or wheel encoder.

speed = 0
gear = "D"

odo = 0
vehicle_range = 0


# ============================================================
# CURRENT TIME
# ============================================================

current_time = datetime.now().strftime("%I:%M %p")


# ============================================================
# DASHBOARD
# ============================================================

st.markdown('<div class="dashboard">', unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(f"""
<div class="header">

    <div class="ev-title">
        <span class="ev-green">EV</span>
        &nbsp; SYSTEM
    </div>

    <div class="clock">
        {current_time}
    </div>

    <div class="ready">
        READY
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# MAIN 3 COLUMN LAYOUT
# ============================================================

left, center, right = st.columns([1, 1.25, 1])


# ============================================================
# LEFT SIDE
# ============================================================

with left:

    # Temperature
    st.markdown(f"""
    <div class="card">

        <div class="card-title">
            🌡️ &nbsp; TEMP
        </div>

        <div class="big-value blue">
            {motor_temperature:.1f}
            <span class="unit">°C</span>
        </div>

        <div style="margin-top:15px;
                    height:10px;
                    background:linear-gradient(
                    90deg,
                    #54d63b,
                    #54d63b,
                    #ffc400,
                    #ff3b30);
                    border-radius:10px;">
        </div>

        <div style="display:flex;
                    justify-content:space-between;
                    margin-top:5px;">
            <span>0</span>
            <span>60</span>
            <span>120</span>
        </div>

    </div>
    """, unsafe_allow_html=True)


    # Current
    st.markdown(f"""
    <div class="card">

        <div class="card-title">
            ⚡ &nbsp; CURRENT
        </div>

        <div class="big-value yellow">
            {motor_current:.3f}
            <span class="unit">A</span>
        </div>

        <div style="margin-top:15px;
                    height:10px;
                    background:linear-gradient(
                    90deg,
                    #54d63b,
                    #54d63b,
                    #ffc400,
                    #ff3b30);
                    border-radius:10px;">
        </div>

        <div style="display:flex;
                    justify-content:space-between;
                    margin-top:5px;">
            <span>0</span>
            <span>15</span>
            <span>30</span>
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CENTER SPEED GAUGE
# ============================================================

with center:

    st.markdown(f"""
    <div class="gauge-container">

        <div class="gauge">

            <div class="gauge-inner">

                <div class="speed">
                    {speed}
                </div>

                <div class="speed-unit">
                    km/h
                </div>

                <div class="drive">
                    {gear}
                </div>

            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# RIGHT SIDE
# ============================================================

with right:

    # FAN
    st.markdown(f"""
    <div class="card">

        <div class="card-title">
            🌀 &nbsp; FAN
        </div>

        <div class="fan-icon">
            🌀
        </div>

        <div class="fan-status {fan_class}">
            {fan_status}
        </div>

        <div>
            AUTO MODE
        </div>

    </div>
    """, unsafe_allow_html=True)


    # VOLTAGE
    st.markdown(f"""
    <div class="card">

        <div class="card-title">
            🔋 &nbsp; VOLTAGE
        </div>

        <div class="big-value blue">
            {battery_voltage:.2f}
            <span class="unit">V</span>
        </div>

    </div>
    """, unsafe_allow_html=True)


    # STATUS
    st.markdown(f"""
    <div class="card">

        <div class="card-title">
            🛡️ &nbsp; STATUS
        </div>

        <div class="{status_class}">
            {motor_status}
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# BOTTOM BAR
# ============================================================

st.markdown(f"""
<div class="bottom-bar">

    <div class="ev-green">
        💡
    </div>

    <div>
        ODO &nbsp;
        <b>{odo} km</b>
    </div>

    <div>
        RANGE &nbsp;
        <b>{vehicle_range} km</b>
    </div>

    <div class="warning">
        ⚠️
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# CLOSE DASHBOARD
# ============================================================

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(1)
st.rerun()

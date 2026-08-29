import streamlit as st
import requests
import time
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart EV Motor Protection System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# API CONFIGURATION
# ============================================================

# Put your EV backend API URL here
API_URL = "https://smart-ev-motor-protection.onrender.com"

# If your API uses a different endpoint, change this
DATA_ENDPOINT = "/latest"


# ============================================================
# GET DATA FROM API
# ============================================================

def get_data():

    try:
        url = API_URL.rstrip("/") + DATA_ENDPOINT

        response = requests.get(
            url,
            timeout=5
        )

        if response.status_code == 200:

            data = response.json()

            # If API returns a list, use latest item
            if isinstance(data, list):

                if len(data) > 0:
                    data = data[-1]
                else:
                    data = {}

            return data

    except Exception:
        pass

    return {}


# ============================================================
# DATA
# ============================================================

data = get_data()


# ------------------------------------------------------------
# Read values safely
# ------------------------------------------------------------

def get_value(keys, default):

    for key in keys:

        if key in data:

            value = data[key]

            if value is not None:
                return value

    return default


temperature = float(
    get_value(
        ["temperature", "temp", "motor_temperature"],
        42
    )
)

current = float(
    get_value(
        ["current", "motor_current", "amps"],
        2.6
    )
)

voltage = float(
    get_value(
        ["voltage", "battery_voltage", "battery"],
        48.6
    )
)

speed = float(
    get_value(
        ["speed", "vehicle_speed", "motor_speed"],
        45
    )
)

fan_value = get_value(
    ["fan", "fan_status", "cooling_fan"],
    "ON"
)

status = get_value(
    ["status", "system_status"],
    "NORMAL"
)


# ============================================================
# FAN STATUS
# ============================================================

if isinstance(fan_value, bool):

    fan_status = "ON" if fan_value else "OFF"

else:

    fan_status = str(fan_value).upper()


# ============================================================
# STATUS
# ============================================================

status = str(status).upper()

if status in ["NORMAL", "READY", "OK"]:

    status_text = "NORMAL"
    status_color = "#39ff14"

else:

    status_text = status
    status_color = "#ff3b30"


# ============================================================
# READY STATUS
# ============================================================

ready = True

if ready:
    ready_text = "READY"
    ready_color = "#39ff14"
else:
    ready_text = "NOT READY"
    ready_color = "#ff3b30"


# ============================================================
# PERCENTAGES
# ============================================================

# Temperature: 0–50 °C
temp_percent = max(
    0,
    min(
        100,
        (temperature / 50) * 100
    )
)

# Current: 0–10 A
current_percent = max(
    0,
    min(
        100,
        (current / 10) * 100
    )
)

# Voltage: 0–60 V
voltage_percent = max(
    0,
    min(
        100,
        (voltage / 60) * 100
    )
)

# Speed: 0–100 km/h
speed_percent = max(
    0,
    min(
        100,
        speed
    )
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at center,
            #18202b 0%,
            #0b0f14 45%,
            #05070a 100%
        );

    color: #ffffff;
}


/* Remove Streamlit top space */

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    padding-left: 3rem;
    padding-right: 3rem;
}


/* Hide Streamlit menu */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* =========================================================
   MAIN TITLE
   ========================================================= */

.main-title {
    text-align: center;

    font-size: 38px;
    font-weight: 800;

    letter-spacing: 1px;

    color: #ffe6b3;

    margin-top: 10px;
    margin-bottom: 35px;
}

.main-title .icon {
    color: #ff6a00;
    margin-right: 12px;
}


/* =========================================================
   TOP STATUS BAR
   ========================================================= */

.status-bar {

    display: grid;

    grid-template-columns: 1fr 1fr 1fr;

    align-items: center;

    width: 100%;

    margin-bottom: 28px;

    padding-bottom: 28px;

    border-bottom: 1px solid rgba(255,255,255,0.20);
}


/* READY */

.ready-box {

    display: flex;

    align-items: center;

    justify-content: flex-start;

    padding-left: 15px;

    font-size: 28px;

    font-weight: 800;

    color: #ffe6b3;
}


/* Green status circle */

.status-dot {

    width: 24px;
    height: 24px;

    border-radius: 50%;

    margin-right: 12px;

    display: inline-block;

    box-shadow:
        0 0 10px rgba(57,255,20,0.7);

}


/* TIME */

.time-box {

    text-align: center;

    font-size: 28px;

    font-weight: 800;

    color: #fff4dc;

    transform: translateX(25px);
}


/* STATUS */

.status-box {

    display: flex;

    align-items: center;

    justify-content: flex-start;

    padding-left: 70px;

    font-size: 28px;

    font-weight: 800;

    color: #ffe6b3;

}


/* =========================================================
   FEATURE CARDS
   ========================================================= */

.feature-card {

    padding: 10px 5px 20px 5px;

    min-height: 240px;
}


.feature-title {

    font-size: 25px;

    font-weight: 800;

    color: #ffe6b3;

    margin-bottom: 18px;
}


.feature-value {

    font-size: 38px;

    font-weight: 800;

    color: #fff4dc;

    margin-bottom: 22px;
}


.feature-mode {

    font-size: 17px;

    font-weight: 700;

    color: #ffe6b3;

    margin-top: 22px;
}


/* =========================================================
   PROGRESS BAR
   ========================================================= */

.progress-background {

    width: 100%;

    height: 9px;

    background: rgba(255,255,255,0.15);

    border-radius: 20px;

    overflow: hidden;
}


.progress-fill {

    height: 100%;

    background: #20bfff;

    border-radius: 20px;

    transition: width 0.5s ease;
}


/* =========================================================
   DIVIDER
   ========================================================= */

.divider {

    width: 100%;

    height: 1px;

    background: rgba(255,255,255,0.20);

    margin: 5px 0 20px 0;
}


/* =========================================================
   GAUGE
   ========================================================= */

.gauge-container {

    position: relative;

    width: 390px;

    height: 390px;

    margin: 0 auto;

    display: flex;

    align-items: center;

    justify-content: center;
}


.gauge {

    position: relative;

    width: 350px;

    height: 350px;

    border-radius: 50%;

    background:
        conic-gradient(
            from 225deg,
            #58ff00 0deg,
            #58ff00 var(--speed-angle),
            #38b7e8 var(--speed-angle),
            #38b7e8 135deg,
            #3e4b58 135deg,
            #3e4b58 270deg,
            transparent 270deg
        );

    transform: rotate(-45deg);

    box-shadow:
        0 0 35px rgba(0,0,0,0.5);
}


.gauge::before {

    content: "";

    position: absolute;

    width: 255px;

    height: 255px;

    background: #111821;

    border-radius: 50%;

    top: 47px;

    left: 47px;
}


.gauge-center {

    position: absolute;

    z-index: 5;

    text-align: center;

    left: 50%;

    top: 50%;

    transform: translate(-50%, -50%);
}


.speed-value {

    font-size: 62px;

    font-weight: 800;

    color: #ffffff;

    line-height: 1;
}


.speed-unit {

    font-size: 22px;

    color: #ffffff;

    font-weight: 600;

    margin-top: 5px;
}


/* =========================================================
   GAUGE TICKS
   ========================================================= */

.tick {

    position: absolute;

    width: 5px;

    height: 22px;

    background: #fff4dc;

    left: 50%;

    top: 0;

    transform-origin: 50% 175px;

    border-radius: 5px;

    z-index: 10;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 900px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .main-title {
        font-size: 28px;
    }

    .ready-box,
    .time-box,
    .status-box {
        font-size: 20px;
    }

    .status-box {
        padding-left: 20px;
    }

    .gauge-container {
        width: 300px;
        height: 300px;
    }

    .gauge {
        width: 280px;
        height: 280px;
    }

    .gauge::before {
        width: 205px;
        height: 205px;
        top: 37px;
        left: 37px;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    """
<div class="main-title">
    <span class="icon">⚡</span>
    SMART EV MOTOR PROTECTION SYSTEM
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# TOP STATUS
# ============================================================

current_time = datetime.now().strftime("%I:%M %p")


st.markdown(
    f"""
<div class="status-bar">

    <div class="ready-box">

        <span
            class="status-dot"
            style="background:{ready_color};">
        </span>

        {ready_text}

    </div>


    <div class="time-box">
        {current_time}
    </div>


    <div class="status-box">

        <span
            class="status-dot"
            style="background:{status_color};">
        </span>

        STATUS: {status_text}

    </div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# MAIN DASHBOARD
# ============================================================

left_col, center_col, right_col = st.columns(
    [1.15, 1.4, 1.15],
    gap="large"
)


# ============================================================
# LEFT SIDE
# ============================================================

with left_col:

    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    st.markdown(
        f"""
<div class="feature-card">

    <div class="feature-title">
        🌡️ TEMPERATURE
    </div>

    <div class="feature-value">
        {temperature:.0f} °C
    </div>

    <div class="progress-background">

        <div
            class="progress-fill"
            style="width:{temp_percent:.1f}%;">
        </div>

    </div>

</div>
""",
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # CURRENT
    # --------------------------------------------------------

    st.markdown(
        f"""
<div class="feature-card">

    <div class="feature-title">
        ⚡ CURRENT
    </div>

    <div class="feature-value">
        {current:.1f} A
    </div>

    <div class="progress-background">

        <div
            class="progress-fill"
            style="width:{current_percent:.1f}%;">
        </div>

    </div>

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# CENTER GAUGE
# ============================================================

with center_col:

    gauge_angle = speed_percent * 270 / 100

    ticks_html = ""

    for i in range(11):

        angle = -135 + (i * 27)

        ticks_html += f"""
        <div
            class="tick"
            style="
                transform:
                translateX(-50%)
                rotate({angle}deg);
            ">
        </div>
        """


    st.markdown(
        f"""
<div class="gauge-container">

    <div
        class="gauge"
        style="--speed-angle:{gauge_angle}deg;">

        {ticks_html}

    </div>


    <div class="gauge-center">

        <div class="speed-value">
            {speed:.0f}
        </div>

        <div class="speed-unit">
            km/h
        </div>

    </div>

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# RIGHT SIDE
# ============================================================

with right_col:

    # --------------------------------------------------------
    # FAN
    # --------------------------------------------------------

    st.markdown(
        f"""
<div class="feature-card">

    <div class="feature-title">
        🔵 FAN
    </div>

    <div class="feature-value">
        {fan_status}
    </div>

    <div class="feature-mode">
        AUTO MODE
    </div>

</div>
""",
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # VOLTAGE
    # --------------------------------------------------------

    st.markdown(
        f"""
<div class="feature-card">

    <div class="feature-title">
        🔋 VOLTAGE
    </div>

    <div class="feature-value">
        {voltage:.1f} V
    </div>

    <div class="progress-background">

        <div
            class="progress-fill"
            style="width:{voltage_percent:.1f}%;">
        </div>

    </div>

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(1)

st.rerun()

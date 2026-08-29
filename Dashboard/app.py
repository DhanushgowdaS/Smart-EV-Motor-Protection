import streamlit as st
import math

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Smart EV Motor Protection System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# DEMO / SENSOR VALUES
# Replace these later with your ESP32 values
# ============================================================

speed = 45
temperature = 42
current = 2.6
battery_voltage = 48.6

gear = "D"
fan_status = "ON"
fan_mode = "AUTO MODE"
system_status = "NORMAL"

odometer = 1256
range_km = 78

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
}

.stApp {
    background: #05070a;
    color: white;
}

/* Remove Streamlit top spacing */
.block-container {
    padding-top: 25px !important;
    padding-bottom: 20px !important;
    max-width: 1500px !important;
}

/* Hide menu/footer */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* =========================================================
   TITLE
   ========================================================= */

.dashboard-title {
    width: 100%;
    text-align: center;
    white-space: nowrap;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #f4f4f4;
    margin-top: 5px;
    margin-bottom: 22px;
}

.title-icon {
    color: #ff8a00;
}

/* =========================================================
   TOP BAR
   ========================================================= */

.top-bar {
    width: 100%;
    height: 75px;
    border-top: 1px solid #24282e;
    border-bottom: 1px solid #24282e;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 35px;
    box-sizing: border-box;
}

.ready {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 23px;
    font-weight: 700;
}

.ready-dot {
    width: 18px;
    height: 18px;
    background: #5bea64;
    border-radius: 50%;
    box-shadow: 0 0 12px rgba(91,234,100,0.6);
}

.time {
    font-size: 24px;
    font-weight: 700;
}

.status {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 23px;
    font-weight: 700;
}

.status-dot {
    width: 18px;
    height: 18px;
    background: #65e870;
    border-radius: 50%;
    box-shadow: 0 0 12px rgba(101,232,112,0.6);
}

/* =========================================================
   MAIN DASHBOARD
   ========================================================= */

/*
IMPORTANT:
The right column is deliberately pushed farther right.
This is the main change you were asking for.
*/

.dashboard {
    display: grid;

    /*
       LEFT       CENTER        RIGHT
       27%        40%           33%
    */

    grid-template-columns: 27% 40% 33%;

    width: 100%;
    min-height: 610px;

    margin-top: 28px;
}

/* =========================================================
   LEFT SIDE
   ========================================================= */

.left-panel {
    padding: 30px 35px 20px 10px;
    box-sizing: border-box;
}

.right-panel {
    /*
       THIS creates the extra distance
       between speedometer and right side.
    */

    padding: 30px 5px 20px 85px;
    box-sizing: border-box;
}

.info-box {
    margin-bottom: 55px;
}

.section-title {
    font-size: 23px;
    font-weight: 800;
    color: #f5f5f5;
    margin-bottom: 25px;
}

.orange {
    color: #ff9b22;
}

.blue {
    color: #4da3ff;
}

.yellow {
    color: #e7e04e;
}

.section-subtitle {
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 15px;
    color: #eeeeee;
}

.value {
    font-size: 32px;
    font-weight: 800;
    color: #ffffff;
}

.progress {
    height: 7px;
    width: 100%;
    background: #30353b;
    border-radius: 10px;
    margin-top: 20px;
    overflow: hidden;
}

.progress-blue {
    height: 100%;
    background: #22a9e8;
    border-radius: 10px;
}

/* =========================================================
   CENTER SPEEDOMETER
   ========================================================= */

.center-panel {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: 15px;
}

.speedometer {
    width: 470px;
    height: 500px;
    position: relative;
}

/* =========================================================
   RIGHT SIDE
   ========================================================= */

.right-info {
    width: 100%;
}

.right-section {
    margin-bottom: 48px;
}

.right-title {
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 25px;
}

.right-label {
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 18px;
}

.right-value {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 18px;
}

.divider {
    height: 1px;
    background: #30343a;
    width: 95%;
    margin-top: 28px;
}

/* =========================================================
   BOTTOM INFORMATION
   ========================================================= */

.bottom-info {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    border-top: 1px solid #24282e;
    margin-top: 5px;
    padding-top: 25px;
}

.bottom-item {
    text-align: center;
}

.bottom-title {
    font-size: 19px;
    font-weight: 700;
}

.bottom-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 10px;
}

/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 900px) {

    .dashboard-title {
        font-size: 28px;
    }

    .dashboard {
        grid-template-columns: 1fr;
    }

    .left-panel,
    .right-panel {
        padding: 25px;
    }

    .right-panel {
        padding-left: 25px;
    }

    .center-panel {
        order: -1;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.markdown("""
<div class="dashboard-title">
    <span class="title-icon">⚡</span>
    SMART EV MOTOR PROTECTION SYSTEM
</div>
""", unsafe_allow_html=True)


# ============================================================
# TOP BAR
# ============================================================

from datetime import datetime

current_time = datetime.now().strftime("%I:%M %p")

st.markdown(f"""
<div class="top-bar">

    <div class="ready">
        <div class="ready-dot"></div>
        READY
    </div>

    <div class="time">
        {current_time}
    </div>

    <div class="status">
        <div class="status-dot"></div>
        STATUS: {system_status}
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# GAUGE SVG GENERATION
# ============================================================

def polar_to_cartesian(cx, cy, radius, angle):
    angle_rad = math.radians(angle)

    return (
        cx + radius * math.cos(angle_rad),
        cy + radius * math.sin(angle_rad)
    )


def describe_arc(cx, cy, radius, start_angle, end_angle):

    start_x, start_y = polar_to_cartesian(
        cx, cy, radius, start_angle
    )

    end_x, end_y = polar_to_cartesian(
        cx, cy, radius, end_angle
    )

    large_arc = 1 if abs(end_angle - start_angle) > 180 else 0

    return (
        f"M {start_x:.2f} {start_y:.2f} "
        f"A {radius} {radius} 0 {large_arc} 1 "
        f"{end_x:.2f} {end_y:.2f}"
    )


# Gauge configuration
cx = 235
cy = 250
radius = 170

# Gauge starts at 150° and ends at 390°
start_angle = 150
end_angle = 390

# Value position
value_angle = start_angle + (
    (speed / 100) * (end_angle - start_angle)
)

# ============================================================
# SVG TICKS
# ============================================================

ticks = ""

# 21 ticks from 0 to 100
for i in range(21):

    value = i * 5

    angle = start_angle + (
        (value / 100) * (end_angle - start_angle)
    )

    # Alternating long and short ticks
    if i % 2 == 0:
        outer_r = 195
        inner_r = 174
        stroke_width = 5
    else:
        outer_r = 190
        inner_r = 178
        stroke_width = 3

    x1, y1 = polar_to_cartesian(
        cx, cy, inner_r, angle
    )

    x2, y2 = polar_to_cartesian(
        cx, cy, outer_r, angle
    )

    ticks += f"""
    <line
        x1="{x1:.2f}"
        y1="{y1:.2f}"
        x2="{x2:.2f}"
        y2="{y2:.2f}"
        stroke="#f4f4f4"
        stroke-width="{stroke_width}"
        stroke-linecap="round"
    />
    """


# ============================================================
# SPEED VALUE POSITION
# ============================================================

# Green arc
green_end = start_angle + (
    min(speed, 50) / 100
) * (end_angle - start_angle)

# Blue zone around 45-55
blue_start = start_angle + (
    45 / 100
) * (end_angle - start_angle)

blue_end = start_angle + (
    55 / 100
) * (end_angle - start_angle)


# ============================================================
# SVG
# ============================================================

gauge_html = f"""

<div class="speedometer">

<svg
    width="470"
    height="500"
    viewBox="0 0 470 500"
    xmlns="http://www.w3.org/2000/svg"
>

    <!-- =================================================
         BACKGROUND GAUGE
         ================================================= -->

    <path
        d="{describe_arc(
            cx, cy, radius,
            start_angle,
            end_angle
        )}"
        fill="none"
        stroke="#202832"
        stroke-width="52"
        stroke-linecap="round"
    />

    <!-- =================================================
         GREEN SAFE AREA
         ================================================= -->

    <path
        d="{describe_arc(
            cx, cy, radius,
            start_angle,
            green_end
        )}"
        fill="none"
        stroke="#6ee900"
        stroke-width="52"
        stroke-linecap="butt"
    />

    <!-- =================================================
         BLUE AREA 45-55
         ================================================= -->

    <path
        d="{describe_arc(
            cx, cy, radius,
            blue_start,
            blue_end
        )}"
        fill="none"
        stroke="#1689e8"
        stroke-width="52"
        stroke-linecap="butt"
    />

    <!-- =================================================
         TICK MARKS
         ================================================= -->

    {ticks}


    <!-- =================================================
         0 LABEL
         ================================================= -->

    <text
        x="60"
        y="435"
        fill="#ffffff"
        font-size="20"
        font-weight="700"
        text-anchor="middle"
    >
        0
    </text>


    <!-- =================================================
         50 LABEL
         ================================================= -->

    <text
        x="235"
        y="55"
        fill="#ffffff"
        font-size="20"
        font-weight="700"
        text-anchor="middle"
    >
        50
    </text>


    <!-- =================================================
         100 LABEL
         ================================================= -->

    <text
        x="410"
        y="435"
        fill="#ffffff"
        font-size="20"
        font-weight="700"
        text-anchor="middle"
    >
        100
    </text>


    <!-- =================================================
         CENTER SPEED
         ================================================= -->

    <text
        x="235"
        y="275"
        fill="#ffffff"
        font-size="68"
        font-weight="800"
        text-anchor="middle"
    >
        {speed}
    </text>


    <!-- =================================================
         KM/H DIRECTLY BELOW 45
         ================================================= -->

    <text
        x="235"
        y="310"
        fill="#ffffff"
        font-size="25"
        font-weight="600"
        text-anchor="middle"
    >
        km/h
    </text>

</svg>

</div>
"""


# ============================================================
# DASHBOARD HTML
# ============================================================

dashboard_html = f"""

<div class="dashboard">

    <!-- =================================================
         LEFT PANEL
         ================================================= -->

    <div class="left-panel">

        <div class="info-box">

            <div class="section-title orange">
                🌡 TEMPERATURE
            </div>

            <div class="section-subtitle">
                Temperature
            </div>

            <div class="value">
                {temperature} °C
            </div>

            <div class="progress">
                <div
                    class="progress-blue"
                    style="width:{min(temperature,100)}%;"
                ></div>
            </div>

        </div>


        <div class="info-box">

            <div class="section-title orange">
                ⚡ CURRENT
            </div>

            <div class="section-subtitle">
                Current
            </div>

            <div class="value">
                {current} A
            </div>

            <div class="progress">
                <div
                    class="progress-blue"
                    style="width:{min(current * 20,100)}%;"
                ></div>
            </div>

        </div>

    </div>


    <!-- =================================================
         CENTER
         ================================================= -->

    <div class="center-panel">

        {gauge_html}

    </div>


    <!-- =================================================
         RIGHT PANEL
         ================================================= -->

    <div class="right-panel">

        <div class="right-info">


            <!-- FAN -->

            <div class="right-section">

                <div class="right-title blue">
                    🌀 FAN
                </div>

                <div class="right-label">
                    Cooling Fan
                </div>

                <div class="right-value">
                    {fan_status}
                </div>

                <div class="right-label">
                    {fan_mode}
                </div>

                <div class="divider"></div>

            </div>


            <!-- VOLTAGE -->

            <div class="right-section">

                <div class="right-title yellow">
                    🔋 VOLTAGE
                </div>

                <div class="right-label">
                    Battery Voltage
                </div>

                <div class="right-value">
                    {battery_voltage} V
                </div>

                <div class="progress">
                    <div
                        class="progress-blue"
                        style="width:{min((battery_voltage / 60) * 100,100)}%;"
                    ></div>
                </div>

            </div>

        </div>

    </div>

</div>


<!-- =====================================================
     BOTTOM INFORMATION
     ===================================================== -->

<div class="bottom-info">

    <div class="bottom-item">

        <div class="bottom-title">
            💡 ODO
        </div>

        <div class="bottom-value">
            {odometer} km
        </div>

    </div>


    <div class="bottom-item">

        <div class="bottom-title">
            🛣 RANGE
        </div>

        <div class="bottom-value">
            {range_km} km
        </div>

    </div>

</div>

"""


st.markdown(
    dashboard_html,
    unsafe_allow_html=True
)

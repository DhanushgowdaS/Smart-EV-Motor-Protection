import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from zoneinfo import ZoneInfo
import time


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
# REAL-TIME DATA
# ============================================================

# India Standard Time
india_time = datetime.now(ZoneInfo("Asia/Kolkata"))

current_time = india_time.strftime("%I:%M %p")
current_date = india_time.strftime("%d-%m-%Y")


# ============================================================
# EV DATA
# ============================================================

temperature = 42
current = 2.6
voltage = 48.6
speed = 45

gear = "D"

odo = 1256
range_km = 78

fan_on = True
fan_mode = "AUTO MODE"

# System status
if temperature >= 70:
    system_status = "CRITICAL"
elif temperature >= 55:
    system_status = "WARNING"
else:
    system_status = "NORMAL"

ready_status = "READY"


# ============================================================
# TITLE
# ============================================================

st.markdown(
    """
    # ⚡ SMART EV MOTOR PROTECTION SYSTEM
    """
)

st.divider()


# ============================================================
# TOP STATUS BAR
# ============================================================

top_left, top_middle, top_right = st.columns([4, 3, 4])


with top_left:
    st.markdown("### 🟢 READY")


with top_middle:
    st.markdown(
        f"<h2 style='text-align:center;'>{current_time}</h2>",
        unsafe_allow_html=True
    )


with top_right:
    st.markdown(
        f"<h3 style='text-align:right;'>STATUS: {system_status}</h3>",
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# MAIN DASHBOARD
# ============================================================

left, center, right = st.columns([3, 5, 3])


# ============================================================
# LEFT SIDE - TEMPERATURE
# ============================================================

with left:

    st.markdown("## 🌡️ TEMPERATURE")

    st.markdown("### Temperature")

    st.markdown(
        f"# {temperature} °C"
    )

    # Temperature progress
    temperature_percentage = min(temperature / 100, 1.0)

    st.progress(temperature_percentage)

    st.write("")

    st.divider()

    # CURRENT

    st.markdown("## ⚡ CURRENT")

    st.markdown("### Current")

    st.markdown(
        f"# {current} A"
    )

    current_percentage = min(current / 10, 1.0)

    st.progress(current_percentage)


# ============================================================
# CENTER - SPEED GAUGE
# ============================================================

with center:

    st.markdown("")

    # --------------------------------------------------------
    # SPEED GAUGE
    # --------------------------------------------------------

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=speed,

            number={
                "font": {
                    "size": 48
                }
            },

            title={
                "text": "km/h",
                "font": {
                    "size": 18
                }
            },

            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickmode": "array",
                    "tickvals": [0, 25, 50, 75, 100],
                    "ticktext": ["0", "25", "50", "75", "100"]
                },

                "bar": {
                    "thickness": 0.25
                },

                "steps": [
                    {
                        "range": [0, 50],
                        "color": "#8CFF00"
                    },
                    {
                        "range": [50, 75],
                        "color": "#66D9EF"
                    },
                    {
                        "range": [75, 100],
                        "color": "#808080"
                    }
                ],

                "threshold": {
                    "line": {
                        "width": 5
                    },
                    "thickness": 0.75,
                    "value": speed
                }
            }
        )
    )

    gauge.update_layout(
        height=430,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=10
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        font={
            "color": "white"
        }
    )

    st.plotly_chart(
        gauge,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    # --------------------------------------------------------
    # SPEED / GEAR
    # --------------------------------------------------------

    speed_col, gear_col = st.columns(2)

    with speed_col:

        st.markdown("### SPEED")

        st.markdown(
            f"# {speed} km/h"
        )

    with gear_col:

        st.markdown("### GEAR")

        st.markdown(
            f"# {gear}"
        )


# ============================================================
# RIGHT SIDE
# ============================================================

with right:

    # --------------------------------------------------------
    # FAN
    # --------------------------------------------------------

    st.markdown("## 🌀 FAN")

    st.markdown("### Cooling Fan")

    if fan_on:
        st.markdown(
            "# ON"
        )
    else:
        st.markdown(
            "# OFF"
        )

    st.markdown(
        f"**{fan_mode}**"
    )

    st.divider()

    # --------------------------------------------------------
    # VOLTAGE
    # --------------------------------------------------------

    st.markdown("## 🔋 VOLTAGE")

    st.markdown("### Battery Voltage")

    st.markdown(
        f"# {voltage} V"
    )

    voltage_percentage = min(voltage / 60, 1.0)

    st.progress(voltage_percentage)


# ============================================================
# LOWER INFORMATION SECTION
# ============================================================

st.divider()

# IMPORTANT:
# ODO and RANGE are intentionally placed more toward the right.
# This prevents them from appearing too close to SPEED / GEAR.

empty_col, odo_col, range_col, empty_right = st.columns(
    [2, 3, 3, 2]
)


# ============================================================
# ODOMETER
# ============================================================

with odo_col:

    st.markdown("## 💡 ODO")

    st.markdown(
        f"# {odo} km"
    )


# ============================================================
# RANGE
# ============================================================

with range_col:

    st.markdown("## 🛣️ RANGE")

    st.markdown(
        f"# {range_km} km"
    )


# ============================================================
# LAST UPDATED
# ============================================================

st.divider()

st.caption(
    f"Last updated: {current_date} {current_time}"
)


# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(1)

st.rerun()

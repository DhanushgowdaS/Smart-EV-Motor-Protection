import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from zoneinfo import ZoneInfo


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EV System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# EV DATA
# ============================================================

temperature = 42.0
current = 2.6
voltage = 48.6

speed = 45
gear = "D"

odo = 1256
range_km = 78

fan_status = "ON"
fan_mode = "AUTO MODE"

system_status = "NORMAL"
vehicle_status = "READY"


# ============================================================
# REAL-TIME CLOCK
# ============================================================

@st.fragment(run_every="1s")
def live_clock():

    india_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    current_time = india_time.strftime("%I:%M %p")

    st.markdown(
        f"### {current_time}"
    )


# ============================================================
# TITLE BAR
# ============================================================

title_col, clock_col, ready_col = st.columns(
    [2.2, 1.2, 2.2]
)

with title_col:
    st.title("EV SYSTEM")

with clock_col:
    live_clock()

with ready_col:
    st.success(vehicle_status)


st.divider()


# ============================================================
# SPEEDOMETER
# ============================================================

def create_speedometer(value):

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,

            number={
                "font": {
                    "size": 55,
                    "color": "white"
                },
                "suffix": ""
            },

            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickmode": "array",
                    "tickvals": [
                        0,
                        25,
                        50,
                        75,
                        100
                    ],
                    "ticktext": [
                        "0",
                        "25",
                        "50",
                        "75",
                        "100"
                    ],
                    "tickfont": {
                        "size": 14,
                        "color": "white"
                    }
                },

                "bar": {
                    "color": "#7CFC00",
                    "thickness": 0.35
                },

                "bgcolor": "#101820",

                "borderwidth": 0,

                "steps": [
                    {
                        "range": [0, 25],
                        "color": "#8BEF42"
                    },
                    {
                        "range": [25, 50],
                        "color": "#C9F77F"
                    },
                    {
                        "range": [50, 75],
                        "color": "#49BCEB"
                    },
                    {
                        "range": [75, 100],
                        "color": "#5B6570"
                    }
                ]
            }
        )
    )

    gauge.update_layout(
        height=390,
        margin=dict(
            l=20,
            r=20,
            t=25,
            b=10
        ),

        paper_bgcolor="#0B1117",

        font={
            "color": "white"
        }
    )

    return gauge


# ============================================================
# MAIN DASHBOARD
# ============================================================

left_col, center_col, right_col = st.columns(
    [1.05, 2.15, 1.30]
)


# ============================================================
# LEFT INFORMATION
# ============================================================

with left_col:

    st.subheader("🌡️ TEMPERATURE")

    st.metric(
        label="Temperature",
        value=f"{temperature:.0f} °C"
    )

    st.progress(
        min(temperature / 80, 1.0)
    )

    st.divider()

    st.subheader("⚡ CURRENT")

    st.metric(
        label="Motor Current",
        value=f"{current:.1f} A"
    )

    st.progress(
        min(current / 10, 1.0)
    )


# ============================================================
# CENTER SPEEDOMETER
# ============================================================

with center_col:

    st.plotly_chart(
        create_speedometer(speed),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    speed_col, gear_col = st.columns(2)

    with speed_col:

        st.metric(
            label="SPEED",
            value=f"{speed} km/h"
        )

    with gear_col:

        st.metric(
            label="GEAR",
            value=gear
        )


# ============================================================
# RIGHT INFORMATION
# ============================================================

with right_col:

    st.subheader("🌀 FAN")

    st.metric(
        label="Cooling Fan",
        value=fan_status
    )

    st.caption(fan_mode)

    st.divider()

    st.subheader("🔋 VOLTAGE")

    st.metric(
        label="Battery Voltage",
        value=f"{voltage:.1f} V"
    )

    st.divider()

    st.subheader("🛡️ STATUS")

    st.success(system_status)


# ============================================================
# BOTTOM INFORMATION
# ============================================================

st.divider()

bottom_left, bottom_center, bottom_right = st.columns(
    [1.15, 1.15, 1.15]
)


# ============================================================
# ODOMETER
# ============================================================

with bottom_left:

    st.subheader("💡 ODO")

    st.metric(
        label="Total Distance",
        value=f"{odo} km"
    )


# ============================================================
# RANGE
# ============================================================

with bottom_center:

    st.subheader("🛣️ RANGE")

    st.metric(
        label="Estimated Range",
        value=f"{range_km} km"
    )


# ============================================================
# SYSTEM
# ============================================================

with bottom_right:

    st.subheader("⚠️ SYSTEM")

    st.success(system_status)


# ============================================================
# LAST UPDATED
# ============================================================

india_time = datetime.now(
    ZoneInfo("Asia/Kolkata")
)

last_updated = india_time.strftime(
    "%d-%m-%Y %I:%M:%S %p"
)

st.caption(
    f"Last updated: {last_updated}"
)

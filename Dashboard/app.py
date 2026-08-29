import streamlit as st
import plotly.graph_objects as go
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
# CUSTOM STREAMLIT SETTINGS
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background-color: #05070A;
            color: white;
        }

        [data-testid="stHeader"] {
            background-color: #05070A;
        }

        [data-testid="stToolbar"] {
            display: none;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 1rem;
        }

        h1, h2, h3, h4, h5, h6, p {
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SENSOR / VEHICLE VALUES
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
# TITLE
# ============================================================

title_col1, title_col2, title_col3 = st.columns([1, 5, 1])

with title_col2:
    st.markdown(
        "<h1 style='text-align:center; white-space:nowrap;'>"
        "⚡ SMART EV MOTOR PROTECTION SYSTEM"
        "</h1>",
        unsafe_allow_html=True
    )

# ============================================================
# TOP STATUS BAR
# ============================================================

top1, top2, top3 = st.columns([1.5, 1.5, 2])

with top1:
    st.success("🟢  READY")

with top2:
    current_time = datetime.now().strftime("%I:%M %p")
    st.markdown(
        f"<h3 style='text-align:center;'>{current_time}</h3>",
        unsafe_allow_html=True
    )

with top3:
    st.markdown(
        f"<h3 style='text-align:right;'>🟢 STATUS: {system_status}</h3>",
        unsafe_allow_html=True
    )

st.divider()

# ============================================================
# MAIN DASHBOARD
#
# IMPORTANT:
# The spacer column between gauge and right panel is
# intentionally added to create MORE GAP.
# ============================================================

left, center, spacer, right = st.columns(
    [1.05, 2.20, 0.55, 1.45],
    gap="small"
)

# ============================================================
# LEFT SIDE
# ============================================================

with left:

    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    st.subheader("🌡️ TEMPERATURE")

    st.caption("Temperature")

    st.markdown(
        f"<h2>{temperature} °C</h2>",
        unsafe_allow_html=True
    )

    st.progress(
        min(max(temperature / 100, 0.0), 1.0)
    )

    st.write("")

    # --------------------------------------------------------
    # CURRENT
    # --------------------------------------------------------

    st.subheader("⚡ CURRENT")

    st.caption("Current")

    st.markdown(
        f"<h2>{current} A</h2>",
        unsafe_allow_html=True
    )

    st.progress(
        min(max(current / 10, 0.0), 1.0)
    )

# ============================================================
# CENTER GAUGE
# ============================================================

with center:

    # ========================================================
    # GAUGE
    #
    # 0 ------------- 50 ------------- 100
    #
    # Green = safe
    # Blue  = normal operating zone
    # Grey  = remaining range
    # ========================================================

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=speed,

            number={
                "font": {
                    "size": 60,
                    "color": "white"
                },
                "suffix": ""
            },

            gauge={
                "shape": "angular",

                "axis": {
                    "range": [0, 100],
                    "tickmode": "linear",
                    "tick0": 0,
                    "dtick": 5,

                    "tickfont": {
                        "size": 14,
                        "color": "white"
                    },

                    "tickcolor": "white",
                    "tickwidth": 2
                },

                "bar": {
                    "color": "#1689E8",
                    "thickness": 0.35
                },

                "bgcolor": "#11161C",

                "borderwidth": 0,

                "steps": [
                    {
                        "range": [0, 45],
                        "color": "#6BE900"
                    },
                    {
                        "range": [45, 55],
                        "color": "#1689E8"
                    },
                    {
                        "range": [55, 100],
                        "color": "#202832"
                    }
                ]
            }
        )
    )

    # --------------------------------------------------------
    # GAUGE LAYOUT
    # --------------------------------------------------------

    gauge.update_layout(
        height=470,
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20
        ),

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

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

    # km/h BELOW the speed
    st.markdown(
        "<h3 style='text-align:center; margin-top:-45px;'>km/h</h3>",
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # GEAR
    # --------------------------------------------------------

    st.markdown(
        f"<h3 style='text-align:center; margin-top:30px;'>"
        f"GEAR<br><b>{gear}</b>"
        f"</h3>",
        unsafe_allow_html=True
    )

# ============================================================
# SPACER
#
# Nothing is placed here.
#
# This column is what creates the extra distance between
# the gauge and FAN/VOLTAGE.
# ============================================================

with spacer:
    st.write("")

# ============================================================
# RIGHT SIDE
# ============================================================

with right:

    # --------------------------------------------------------
    # FAN
    # --------------------------------------------------------

    st.subheader("🌀 FAN")

    st.caption("Cooling Fan")

    st.markdown(
        f"<h2>{fan_status}</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<h4>{fan_mode}</h4>",
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------------
    # VOLTAGE
    # --------------------------------------------------------

    st.subheader("🔋 VOLTAGE")

    st.caption("Battery Voltage")

    st.markdown(
        f"<h2>{battery_voltage} V</h2>",
        unsafe_allow_html=True
    )

    st.progress(
        min(max(battery_voltage / 60, 0.0), 1.0)
    )

# ============================================================
# BOTTOM SECTION
# ============================================================

st.divider()

bottom1, bottom2 = st.columns(2)

# ============================================================
# ODOMETER
# ============================================================

with bottom1:

    st.markdown(
        "<h3 style='text-align:center;'>💡 ODO</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<h2 style='text-align:center;'>{odometer} km</h2>",
        unsafe_allow_html=True
    )

# ============================================================
# RANGE
# ============================================================

with bottom2:

    st.markdown(
        "<h3 style='text-align:center;'>🛣️ RANGE</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<h2 style='text-align:center;'>{range_km} km</h2>",
        unsafe_allow_html=True
    )

# ============================================================
# LAST UPDATED
# ============================================================

st.caption(
    f"Last updated: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}"
)

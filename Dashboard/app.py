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
# DATA
# Replace these values later with your real ESP32 data
# ============================================================

temperature = 42
current = 2.6
speed = 45
battery_voltage = 48.6

fan_status = "ON"
fan_mode = "AUTO MODE"

gear = "D"
odometer = 1256
range_km = 78

# ============================================================
# GENERAL STREAMLIT SETTINGS
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1500px;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([5.5, 1.5])

with header_left:
    st.markdown(
        """
        <h1 style="
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 5px;
            white-space: nowrap;
        ">
        ⚡ SMART EV MOTOR PROTECTION SYSTEM
        </h1>
        """,
        unsafe_allow_html=True
    )

with header_right:
    st.markdown(
        """
        <div style="
            text-align:right;
            padding-top:15px;
            font-size:22px;
            font-weight:700;
        ">
        🟢 STATUS: NORMAL
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ============================================================
# TIME / READY STATUS
# ============================================================

ready_col, time_col, status_col = st.columns([1.5, 2, 1.5])

with ready_col:
    st.markdown(
        """
        <div style="
            font-size:22px;
            font-weight:700;
        ">
        🟢 READY
        </div>
        """,
        unsafe_allow_html=True
    )

with time_col:
    current_time = datetime.now().strftime("%I:%M %p")

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:27px;
            font-weight:700;
        ">
        {current_time}
        </div>
        """,
        unsafe_allow_html=True
    )

with status_col:
    st.markdown(
        """
        <div style="
            text-align:right;
            font-size:22px;
            font-weight:700;
        ">
        🟢 STATUS: NORMAL
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ============================================================
# MAIN DASHBOARD
#
# LEFT       = Temperature + Current
# CENTER     = Speed Gauge
# RIGHT      = Fan + Voltage
#
# Wider gap is created by using 5 columns.
# ============================================================

left_col, gap1, center_col, gap2, right_col = st.columns(
    [1.4, 0.35, 2.7, 0.45, 1.5]
)

# ============================================================
# LEFT SIDE
# ============================================================

with left_col:

    # ---------------- TEMPERATURE ----------------

    st.markdown(
        """
        <h2 style="font-size:27px;">
        🌡️ TEMPERATURE
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            font-size:18px;
            margin-bottom:0px;
        ">
        Temperature
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <h1 style="
            font-size:38px;
            margin-top:5px;
            margin-bottom:5px;
        ">
        {temperature} °C
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        min(max(temperature / 100, 0.0), 1.0)
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- CURRENT ----------------

    st.markdown(
        """
        <h2 style="font-size:27px;">
        ⚡ CURRENT
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            font-size:18px;
            margin-bottom:0px;
        ">
        Current
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <h1 style="
            font-size:38px;
            margin-top:5px;
            margin-bottom:5px;
        ">
        {current} A
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        min(max(current / 10, 0.0), 1.0)
    )

# ============================================================
# CENTER SPEED GAUGE
# ============================================================

with center_col:

    # --------------------------------------------------------
    # GAUGE
    # --------------------------------------------------------

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=speed,

            number={
                "font": {
                    "size": 62,
                    "color": "white"
                },
                "suffix": ""
            },

            gauge={
                "axis": {
                    "range": [0, 100],

                    # ONLY 0, 50 and 100
                    "tickmode": "array",
                    "tickvals": [0, 50, 100],
                    "ticktext": ["0", "50", "100"],

                    "tickfont": {
                        "size": 17,
                        "color": "white"
                    },

                    "tickwidth": 4,
                    "tickcolor": "white"
                },

                "bar": {
                    "color": "#18AEEF",
                    "thickness": 0.28
                },

                "bgcolor": "#151A20",

                "borderwidth": 0,

                "steps": [
                    {
                        "range": [0, 40],
                        "color": "#7CFF00"
                    },
                    {
                        "range": [40, 55],
                        "color": "#159FEA"
                    },
                    {
                        "range": [55, 100],
                        "color": "#27313D"
                    }
                ],

                "threshold": {
                    "line": {
                        "color": "white",
                        "width": 5
                    },
                    "thickness": 0.75,
                    "value": speed
                }
            }
        )
    )

    # --------------------------------------------------------
    # GAUGE LAYOUT
    # --------------------------------------------------------

    fig.update_layout(
        height=470,

        margin=dict(
            l=15,
            r=15,
            t=50,
            b=35
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        font={
            "color": "white"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    # km/h directly below 45
    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:24px;
            font-weight:600;
            margin-top:-45px;
        ">
        km/h
        </div>
        """,
        unsafe_allow_html=True
    )

    # Gear
    st.markdown(
        f"""
        <div style="
            text-align:center;
            margin-top:55px;
        ">
            <div style="
                font-size:20px;
                font-weight:600;
            ">
            GEAR
            </div>

            <div style="
                font-size:45px;
                font-weight:800;
            ">
            {gear}
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
        """
        <h2 style="font-size:27px;">
        🌀 FAN
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            font-size:18px;
            margin-bottom:5px;
        ">
        Cooling Fan
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <h1 style="
            font-size:38px;
            margin-top:0px;
            margin-bottom:5px;
        ">
        {fan_status}
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <p style="
            font-size:18px;
            font-weight:600;
            margin-top:0px;
        ">
        {fan_mode}
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------------
    # VOLTAGE
    # --------------------------------------------------------

    st.markdown(
        """
        <h2 style="font-size:27px;">
        🔋 VOLTAGE
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            font-size:18px;
            margin-bottom:5px;
        ">
        Battery Voltage
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <h1 style="
            font-size:38px;
            margin-top:0px;
            margin-bottom:5px;
        ">
        {battery_voltage} V
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        min(max(battery_voltage / 60, 0.0), 1.0)
    )

# ============================================================
# BOTTOM INFORMATION
# ============================================================

st.divider()

bottom_left, bottom_right = st.columns([1, 1])

with bottom_left:

    st.markdown(
        f"""
        <div style="
            text-align:center;
        ">
            <div style="
                font-size:22px;
                font-weight:700;
            ">
            💡 ODO
            </div>

            <div style="
                font-size:32px;
                font-weight:800;
            ">
            {odometer} km
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with bottom_right:

    st.markdown(
        f"""
        <div style="
            text-align:center;
        ">
            <div style="
                font-size:22px;
                font-weight:700;
            ">
            🛣️ RANGE
            </div>

            <div style="
                font-size:32px;
                font-weight:800;
            ">
            {range_km} km
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# LAST UPDATED
# ============================================================

st.markdown(
    f"""
    <p style="
        font-size:14px;
        margin-top:25px;
    ">
    Last updated: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}
    </p>
    """,
    unsafe_allow_html=True
)

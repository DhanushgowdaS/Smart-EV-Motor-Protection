import streamlit as st
import plotly.graph_objects as go
import requests
from datetime import datetime

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EV System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# DASHBOARD SETTINGS
# =========================================================

API_URL = "https://smart-ev-motor-protection.onrender.com"

# Demo values
# Later we will replace these with ESP32/API values
SPEED = 45
TEMPERATURE = 42
CURRENT = 2.6
VOLTAGE = 48.6
ODO = 1256
RANGE = 78

FAN_STATUS = "ON"
DRIVE_MODE = "D"
SYSTEM_STATUS = "NORMAL"


# =========================================================
# DARK NAVY BACKGROUND
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #06111c;
        color: white;
    }

    [data-testid="stHeader"] {
        background-color: #06111c;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    [data-testid="stSidebar"] {
        background-color: #06111c;
    }

    div[data-testid="metric-container"] {
        background-color: transparent;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# TOP HEADER
# =========================================================

header1, header2, header3 = st.columns([2, 2, 2])

with header1:
    st.markdown(
        "## :green[EV] SYSTEM"
    )

with header2:
    current_time = datetime.now().strftime("%I:%M %p")
    st.markdown(
        f"<h3 style='text-align:center;'>{current_time}</h3>",
        unsafe_allow_html=True
    )

with header3:
    st.markdown(
        "<h3 style='text-align:right; color:#39ff14;'>READY</h3>",
        unsafe_allow_html=True
    )

st.divider()


# =========================================================
# MAIN DASHBOARD
# =========================================================

left, center, right = st.columns([1.15, 2.2, 1.15])


# =========================================================
# LEFT SIDE
# =========================================================

with left:

    st.markdown("### 🌡️ TEMPERATURE")

    st.metric(
        label="",
        value=f"{TEMPERATURE} °C"
    )

    st.progress(
        min(TEMPERATURE / 120, 1.0)
    )

    st.markdown("---")

    st.markdown("### ⚡ CURRENT")

    st.metric(
        label="",
        value=f"{CURRENT} A"
    )

    st.progress(
        min(CURRENT / 30, 1.0)
    )


# =========================================================
# CENTER SPEEDOMETER
# =========================================================

with center:

    # Speedometer gauge
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=SPEED,

            number={
                "font": {
                    "size": 58,
                    "color": "white"
                },
                "suffix": ""
            },

            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickmode": "array",
                    "tickvals": [0, 25, 50, 75, 100],
                    "ticktext": [
                        "0",
                        "25",
                        "50",
                        "75",
                        "100"
                    ],
                    "tickfont": {
                        "color": "white",
                        "size": 13
                    }
                },

                "bar": {
                    "color": "#39ff14",
                    "thickness": 0.25
                },

                "bgcolor": "#071018",

                "borderwidth": 0,

                "steps": [
                    {
                        "range": [0, 50],
                        "color": "#39ff14"
                    },
                    {
                        "range": [50, 60],
                        "color": "#1687ff"
                    },
                    {
                        "range": [60, 100],
                        "color": "#26323d"
                    }
                ],

                "threshold": {
                    "line": {
                        "color": "white",
                        "width": 3
                    },
                    "thickness": 0.75,
                    "value": SPEED
                }
            }
        )
    )

    fig.update_layout(
        height=420,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        paper_bgcolor="#06111c",
        plot_bgcolor="#06111c",
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

    speed_text = st.empty()

    speed_text.markdown(
        f"""
        <div style="
            text-align:center;
            margin-top:-90px;
            font-size:20px;
            color:white;
        ">
            km/h
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <h1 style="
            text-align:center;
            color:#39ff14;
            margin-top:45px;
        ">
            {DRIVE_MODE}
        </h1>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# RIGHT SIDE
# =========================================================

with right:

    st.markdown("### 🌀 FAN")

    st.markdown(
        f"""
        <h2 style="color:#39ff14;">
            {FAN_STATUS}
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.write("AUTO MODE")

    st.divider()

    st.markdown("### 🔋 VOLTAGE")

    st.metric(
        label="",
        value=f"{VOLTAGE} V"
    )

    st.divider()

    st.markdown("### 🛡️ STATUS")

    st.markdown(
        f"""
        <h2 style="color:#39ff14;">
            {SYSTEM_STATUS}
        </h2>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BOTTOM INFORMATION
# =========================================================

st.divider()

bottom1, bottom2, bottom3 = st.columns([1, 1, 1])

with bottom1:

    st.markdown(
        "### 💡 ODO"
    )

    st.markdown(
        f"## {ODO} km"
    )


with bottom2:

    st.markdown(
        "### 🛣️ RANGE"
    )

    st.markdown(
        f"## {RANGE} km"
    )


with bottom3:

    st.markdown(
        "### ⚠️ SYSTEM"
    )

    st.markdown(
        "## NORMAL"
    )


# =========================================================
# LIVE DATA SECTION
# =========================================================

st.divider()

st.caption(
    f"Last updated: {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}"
)

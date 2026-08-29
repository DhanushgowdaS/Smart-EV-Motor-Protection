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
# REAL-TIME CLOCK - INDIA
# ============================================================

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


# ============================================================
# SYSTEM STATUS
# ============================================================

if temperature >= 70:
    system_status = "CRITICAL"

elif temperature >= 55:
    system_status = "WARNING"

else:
    system_status = "NORMAL"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

        /* ====================================================
           MAIN BACKGROUND
           ==================================================== */

        .stApp {
            background-color: #02070b;
        }

        [data-testid="stHeader"] {
            background-color: #02070b;
        }

        [data-testid="stToolbar"] {
            visibility: hidden;
        }


        /* ====================================================
           PAGE WIDTH / SPACING
           ==================================================== */

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1rem;
            padding-left: 4rem;
            padding-right: 4rem;
            max-width: 1500px;
        }


        /* ====================================================
           SINGLE-LINE PROJECT TITLE
           ==================================================== */

        .project-title {
            white-space: nowrap;
            text-align: center;
            font-size: 34px;
            font-weight: 800;
            color: #FFFFFF;
            margin-top: 10px;
            margin-bottom: 10px;
        }


        /* ====================================================
           STATUS BAR
           ==================================================== */

        .status-right {
            text-align: right;
            white-space: nowrap;
        }


        /* ====================================================
           SPEEDOMETER CENTER
           ==================================================== */

        .speed-unit {
            font-size: 25px;
            color: #FFFFFF;
            font-weight: 500;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SMALL TOP SPACE
# ============================================================

st.write("")


# ============================================================
# PROJECT TITLE
# ============================================================

st.markdown(
    """
    <div class="project-title">
        ⚡ SMART EV MOTOR PROTECTION SYSTEM
    </div>
    """,
    unsafe_allow_html=True
)


st.divider()


# ============================================================
# TOP STATUS BAR
#
# READY  -> LEFT
# CLOCK  -> CENTER
# STATUS -> MORE RIGHT
# ============================================================

top_left, top_middle, top_right = st.columns(
    [4, 2.5, 5]
)


# ============================================================
# READY
# ============================================================

with top_left:

    st.markdown(
        "### 🟢 READY"
    )


# ============================================================
# REAL-TIME CLOCK
# ============================================================

with top_middle:

    st.markdown(
        f"## {current_time}"
    )


# ============================================================
# STATUS
# ============================================================

with top_right:

    if system_status == "NORMAL":

        st.markdown(
            """
            <div class="status-right">
                <h3>🟢 STATUS: NORMAL</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif system_status == "WARNING":

        st.markdown(
            """
            <div class="status-right">
                <h3>🟠 STATUS: WARNING</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="status-right">
                <h3>🔴 STATUS: CRITICAL</h3>
            </div>
            """,
            unsafe_allow_html=True
        )


st.divider()


# ============================================================
# MAIN DASHBOARD
# ============================================================

left, center, right = st.columns(
    [3, 5, 3]
)


# ============================================================
# LEFT SECTION
# ============================================================

with left:

    # ========================================================
    # TEMPERATURE
    # ========================================================

    st.markdown(
        "## 🌡️ TEMPERATURE"
    )

    st.markdown(
        "### Temperature"
    )

    st.markdown(
        f"# {temperature} °C"
    )

    temperature_percentage = min(
        temperature / 100,
        1.0
    )

    st.progress(
        temperature_percentage
    )


    st.divider()


    # ========================================================
    # CURRENT
    # ========================================================

    st.markdown(
        "## ⚡ CURRENT"
    )

    st.markdown(
        "### Current"
    )

    st.markdown(
        f"# {current} A"
    )

    current_percentage = min(
        current / 10,
        1.0
    )

    st.progress(
        current_percentage
    )


# ============================================================
# CENTER - AUTOMOTIVE SPEEDOMETER
# ============================================================

with center:

    # --------------------------------------------------------
    # SPEED LIMIT
    # --------------------------------------------------------

    min_speed = 0
    max_speed = 100


    # --------------------------------------------------------
    # CREATE SPEEDOMETER
    # --------------------------------------------------------

    speedometer = go.Figure()


    # ========================================================
    # GAUGE
    # ========================================================

    speedometer.add_trace(
        go.Indicator(

            mode="gauge+number",

            value=speed,


            # ------------------------------------------------
            # CENTER SPEED NUMBER
            # ------------------------------------------------

            number={
                "font": {
                    "size": 78,
                    "color": "#FFFFFF"
                },

                "valueformat": ".0f"
            },


            # ------------------------------------------------
            # IMPORTANT:
            #
            # NO TITLE HERE
            #
            # We will manually place "km/h"
            # directly underneath 45.
            # ------------------------------------------------

            gauge={

                # =================================================
                # SPEED RANGE
                # =================================================

                "axis": {

                    "range": [
                        min_speed,
                        max_speed
                    ],


                    # =================================================
                    # WHITE TICK MARKS
                    # =================================================

                    "tickmode": "array",

                    "tickvals": [
                        0,
                        5,
                        10,
                        15,
                        20,
                        25,
                        30,
                        35,
                        40,
                        45,
                        50,
                        55,
                        60,
                        65,
                        70,
                        75,
                        80,
                        85,
                        90,
                        95,
                        100
                    ],


                    # Only 0, 50 and 100 are displayed
                    # as numbers.

                    "ticktext": [
                        "0",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "50",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "100"
                    ],


                    "tickfont": {
                        "size": 22,
                        "color": "#FFFFFF"
                    },

                    "tickcolor": "#FFFFFF",

                    "tickwidth": 4,

                    "ticklen": 14
                },


                # =================================================
                # NO OUTER BORDER
                # =================================================

                "borderwidth": 0,

                "bordercolor": "#02070B",


                # =================================================
                # COLOUR SECTIONS
                # =================================================

                "steps": [

                    # ------------------------------------------------
                    # GREEN
                    # 0 - 40
                    # ------------------------------------------------

                    {
                        "range": [
                            0,
                            40
                        ],

                        "color": "#49E600"
                    },


                    # ------------------------------------------------
                    # BLUE
                    # 40 - 55
                    # ------------------------------------------------

                    {
                        "range": [
                            40,
                            55
                        ],

                        "color": "#1479E8"
                    },


                    # ------------------------------------------------
                    # DARK
                    # 55 - 100
                    # ------------------------------------------------

                    {
                        "range": [
                            55,
                            100
                        ],

                        "color": "#263442"
                    }
                ],


                # =================================================
                # CURRENT SPEED WHITE MARKER
                # =================================================

                "threshold": {

                    "line": {
                        "color": "#FFFFFF",
                        "width": 5
                    },

                    "thickness": 0.85,

                    "value": speed
                },


                # =================================================
                # REMOVE DEFAULT NEEDLE
                # =================================================

                "bar": {
                    "color": "rgba(0,0,0,0)",
                    "thickness": 0
                }
            }
        )
    )


    # ========================================================
    # SPEEDOMETER LAYOUT
    # ========================================================

    speedometer.update_layout(

        height=470,

        margin={
            "l": 15,
            "r": 15,
            "t": 10,
            "b": 0
        },

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font={
            "color": "#FFFFFF"
        }
    )


    # ========================================================
    # IMPORTANT:
    #
    # PUT km/h DIRECTLY UNDER 45
    # ========================================================

    speedometer.add_annotation(

        x=0.5,

        y=0.39,

        xref="paper",

        yref="paper",

        text="km/h",

        showarrow=False,

        font={
            "size": 25,
            "color": "#FFFFFF"
        },

        align="center"
    )


    # ========================================================
    # DISPLAY SPEEDOMETER
    # ========================================================

    st.plotly_chart(

        speedometer,

        use_container_width=True,

        config={
            "displayModeBar": False,
            "staticPlot": True
        }
    )


    # ========================================================
    # GEAR
    # ========================================================

    gear_col = st.columns(
        [2, 1, 2]
    )

    with gear_col[1]:

        st.markdown(
            "### GEAR"
        )

        st.markdown(
            f"# {gear}"
        )


# ============================================================
# RIGHT SECTION
# ============================================================

with right:

    # ========================================================
    # FAN
    # ========================================================

    st.markdown(
        "## 🌀 FAN"
    )

    st.markdown(
        "### Cooling Fan"
    )

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


    # ========================================================
    # VOLTAGE
    # ========================================================

    st.markdown(
        "## 🔋 VOLTAGE"
    )

    st.markdown(
        "### Battery Voltage"
    )

    st.markdown(
        f"# {voltage} V"
    )

    voltage_percentage = min(
        voltage / 60,
        1.0
    )

    st.progress(
        voltage_percentage
    )


# ============================================================
# LOWER INFORMATION
# ============================================================

st.divider()


# ============================================================
# ODO + RANGE
# ============================================================

empty_left, empty_middle, odo_col, range_col = st.columns(
    [2.5, 1.5, 3, 3]
)


# ============================================================
# ODOMETER
# ============================================================

with odo_col:

    st.markdown(
        "## 💡 ODO"
    )

    st.markdown(
        f"# {odo} km"
    )


# ============================================================
# RANGE
# ============================================================

with range_col:

    st.markdown(
        "## 🛣️ RANGE"
    )

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
# REAL-TIME REFRESH
# ============================================================

time.sleep(1)

st.rerun()

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
# STREAMLIT PAGE SPACING
# ============================================================

st.write("")


# ============================================================
# PROJECT TITLE
# ============================================================

title_col = st.columns([1, 4, 1])

with title_col[1]:

    st.markdown(
        "# ⚡ SMART EV MOTOR PROTECTION SYSTEM"
    )


st.divider()


# ============================================================
# TOP STATUS BAR
#
# LEFT   -> READY
# CENTER -> REAL TIME
# RIGHT  -> STATUS
# ============================================================

top_left, top_middle, top_right = st.columns(
    [4, 3, 4]
)


# ------------------------------------------------------------
# READY
# ------------------------------------------------------------

with top_left:

    st.markdown(
        "### 🟢 READY"
    )


# ------------------------------------------------------------
# REAL-TIME CLOCK
# ------------------------------------------------------------

with top_middle:

    st.markdown(
        f"## {current_time}"
    )


# ------------------------------------------------------------
# STATUS
# ------------------------------------------------------------

with top_right:

    if system_status == "NORMAL":

        st.markdown(
            "### 🟢 STATUS: NORMAL"
        )

    elif system_status == "WARNING":

        st.markdown(
            "### 🟠 STATUS: WARNING"
        )

    else:

        st.markdown(
            "### 🔴 STATUS: CRITICAL"
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
    # SPEEDOMETER
    #
    # GREEN = 0 - 40
    # BLUE  = 40 - 55
    # DARK  = 55 - 100
    # --------------------------------------------------------

    speedometer = go.Figure()


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
            # UNIT
            # ------------------------------------------------

            title={
                "text": "km/h",

                "font": {
                    "size": 25,
                    "color": "#FFFFFF"
                }
            },

            gauge={

                # ------------------------------------------------
                # GAUGE ANGLE
                # ------------------------------------------------

                "axis": {

                    "range": [
                        min_speed,
                        max_speed
                    ],

                    # ------------------------------------------------
                    # WHITE TICK MARKS
                    # ------------------------------------------------

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

                    # Only show 0, 50 and 100 as numbers
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


                # ------------------------------------------------
                # NO OUTER BORDER
                # ------------------------------------------------

                "borderwidth": 0,

                "bordercolor": "#02070B",


                # ------------------------------------------------
                # SPEEDOMETER COLOURS
                # ------------------------------------------------

                "steps": [

                    # GREEN
                    {
                        "range": [
                            0,
                            40
                        ],

                        "color": "#49E600"
                    },

                    # BLUE
                    {
                        "range": [
                            40,
                            55
                        ],

                        "color": "#1479E8"
                    },

                    # DARK
                    {
                        "range": [
                            55,
                            100
                        ],

                        "color": "#263442"
                    }
                ],


                # ------------------------------------------------
                # CURRENT SPEED WHITE INDICATOR
                # ------------------------------------------------

                "threshold": {

                    "line": {
                        "color": "#FFFFFF",
                        "width": 5
                    },

                    "thickness": 0.85,

                    "value": speed
                },


                # ------------------------------------------------
                # REMOVE DEFAULT NEEDLE
                # ------------------------------------------------

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
#
# ODO AND RANGE ARE SHIFTED TO THE RIGHT
# ============================================================

st.divider()


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

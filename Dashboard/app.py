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
# DARK DASHBOARD STYLE
# ============================================================

st.markdown(
    """
    <style>

        /* ----------------------------------------------------
           MAIN APPLICATION BACKGROUND
        ---------------------------------------------------- */

        .stApp {
            background-color: #02070B;
            color: #FFFFFF;
        }


        /* ----------------------------------------------------
           STREAMLIT HEADER
        ---------------------------------------------------- */

        [data-testid="stHeader"] {
            background-color: #02070B;
        }


        /* ----------------------------------------------------
           HIDE TOOLBAR
        ---------------------------------------------------- */

        [data-testid="stToolbar"] {
            visibility: hidden;
        }


        /* ----------------------------------------------------
           MAIN CONTAINER
        ---------------------------------------------------- */

        .block-container {

            padding-top: 1.5rem;
            padding-bottom: 1rem;

            padding-left: 3.5rem;
            padding-right: 3.5rem;

            max-width: 1500px;
        }


        /* ----------------------------------------------------
           REMOVE EXTRA STREAMLIT SPACING
        ---------------------------------------------------- */

        div[data-testid="stVerticalBlock"] {
            gap: 0.45rem;
        }


        /* ----------------------------------------------------
           DIVIDER
        ---------------------------------------------------- */

        hr {
            border-color: #26313A;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TOP SPACE
# ============================================================

st.write("")


# ============================================================
# PROJECT TITLE
# ============================================================

title_col = st.columns([1, 6, 1])

with title_col[1]:

    st.markdown(
        """
        <h1 style="
            white-space: nowrap;
            text-align: center;
            font-size: 32px;
            margin-bottom: 5px;
            color: #FFFFFF;
        ">
            ⚡ SMART EV MOTOR PROTECTION SYSTEM
        </h1>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# TOP STATUS BAR
# ============================================================

top_left, top_middle, top_right = st.columns(
    [4, 3, 5]
)


# ============================================================
# READY
# ============================================================

with top_left:

    st.markdown(
        """
        <div style="
            font-size: 23px;
            font-weight: 700;
            margin-top: 5px;
        ">
            <span style="
                color: #49E600;
                font-size: 25px;
            ">●</span>
            READY
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# REAL-TIME CLOCK
# ============================================================

with top_middle:

    st.markdown(
        f"""
        <div style="
            text-align: center;
            font-size: 25px;
            font-weight: 700;
        ">
            {current_time}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SYSTEM STATUS
# MOVED SLIGHTLY TO THE RIGHT
# ============================================================

with top_right:

    st.markdown(
        f"""
        <div style="
            text-align: right;
            padding-right: 10px;
            font-size: 23px;
            font-weight: 700;
        ">
            <span style="
                color: #49E600;
                font-size: 25px;
            ">●</span>
            STATUS: {system_status}
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# MAIN DASHBOARD
#
# LEFT   = TEMPERATURE + CURRENT
# CENTER = SPEEDOMETER
# RIGHT  = FAN + VOLTAGE
#
# RIGHT SECTION IS GIVEN MORE SPACE
# ============================================================

left, center, right = st.columns(
    [3, 5, 4]
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
# CENTER SECTION
# ============================================================

with center:

    # ========================================================
    # SPEED RANGE
    # ========================================================

    min_speed = 0
    max_speed = 100


    # ========================================================
    # SPEEDOMETER FIGURE
    # ========================================================

    speedometer = go.Figure()


    # ========================================================
    # MAIN SPEEDOMETER
    # ========================================================

    speedometer.add_trace(
        go.Indicator(

            mode="gauge+number",

            value=speed,


            # ------------------------------------------------
            # SPEED NUMBER
            # ------------------------------------------------

            number={
                "font": {
                    "size": 72,
                    "color": "#FFFFFF"
                },

                "valueformat": ".0f"
            },


            # ------------------------------------------------
            # UNIT UNDER SPEED
            # ------------------------------------------------

            title={
                "text": "km/h",

                "font": {
                    "size": 24,
                    "color": "#FFFFFF"
                }
            },


            # =================================================
            # GAUGE
            # =================================================

            gauge={


                # ------------------------------------------------
                # AXIS
                # ------------------------------------------------

                "axis": {

                    "range": [
                        min_speed,
                        max_speed
                    ],


                    # ------------------------------------------------
                    # TICK VALUES
                    #
                    # Every 5 km/h
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


                    # ------------------------------------------------
                    # ONLY SHOW 0, 50, 100
                    # ------------------------------------------------

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
                        "100"

                    ],


                    "tickfont": {
                        "size": 20,
                        "color": "#FFFFFF"
                    },


                    "tickcolor": "#FFFFFF",

                    "tickwidth": 3,

                    "ticklen": 12
                },


                # ------------------------------------------------
                # NO BORDER
                # ------------------------------------------------

                "borderwidth": 0,

                "bordercolor": "#02070B",


                # =================================================
                # COLOURED SECTIONS
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
                # CURRENT SPEED MARKER
                # =================================================

                "threshold": {

                    "line": {
                        "color": "#FFFFFF",
                        "width": 5
                    },

                    "thickness": 0.82,

                    "value": speed
                },


                # ------------------------------------------------
                # REMOVE DEFAULT BAR
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
            "l": 10,
            "r": 10,
            "t": 5,
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
            """
            <div style="
                text-align: center;
            ">
                <div style="
                    font-size: 20px;
                    font-weight: 600;
                ">
                    GEAR
                </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
                <div style="
                    font-size: 40px;
                    font-weight: 700;
                    margin-top: 5px;
                ">
                    {gear}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# RIGHT SECTION
#
# IMPORTANT:
# This entire section is shifted to the RIGHT.
# ============================================================

with right:

    # ========================================================
    # RIGHT SIDE SPACING
    # ========================================================

    st.markdown(
        """
        <div style="
            padding-left: 35px;
        ">
        """,
        unsafe_allow_html=True
    )


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


    # ========================================================
    # CLOSE RIGHT SECTION
    # ========================================================

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# LOWER INFORMATION
# ============================================================

st.divider()


# ============================================================
# ODO + RANGE
#
# SHIFTED TOWARD RIGHT
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

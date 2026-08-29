import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from zoneinfo import ZoneInfo
import math


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
# PAGE STYLE
# ============================================================

st.markdown(
    """
    <style>

        .stApp {
            background-color: #02070B;
        }

        [data-testid="stHeader"] {
            background-color: #02070B;
        }

        [data-testid="stToolbar"] {
            visibility: hidden;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1rem;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 1500px;
        }


        /* -------------------------------------------------- */
        /* TITLE */
        /* -------------------------------------------------- */

        .project-title {
            text-align: center;
            white-space: nowrap;
            font-size: 36px;
            font-weight: 800;
            letter-spacing: 1px;
            color: #F5F5F5;
            margin-bottom: 5px;
        }


        /* -------------------------------------------------- */
        /* TOP BAR */
        /* -------------------------------------------------- */

        .ready-text {
            font-size: 30px;
            font-weight: 800;
            color: #FFFFFF;
        }

        .clock-text {
            font-size: 30px;
            font-weight: 800;
            text-align: center;
            color: #FFFFFF;
        }

        .status-text {
            font-size: 30px;
            font-weight: 800;
            text-align: right;
            color: #FFFFFF;
        }


        /* -------------------------------------------------- */
        /* SECTION HEADINGS */
        /* -------------------------------------------------- */

        .section-heading {
            font-size: 25px;
            font-weight: 800;
            color: #F5F5F5;
            margin-top: 8px;
        }

        .sub-heading {
            font-size: 19px;
            font-weight: 600;
            color: #FFFFFF;
            margin-top: 10px;
        }

        .big-value {
            font-size: 38px;
            font-weight: 800;
            color: #FFFFFF;
            margin-top: 5px;
            margin-bottom: 10px;
        }


        /* -------------------------------------------------- */
        /* GEAR */
        /* -------------------------------------------------- */

        .gear-label {
            text-align: center;
            font-size: 20px;
            font-weight: 700;
            color: #FFFFFF;
        }

        .gear-value {
            text-align: center;
            font-size: 50px;
            font-weight: 900;
            color: #FFFFFF;
        }


        /* -------------------------------------------------- */
        /* REMOVE EXTRA STREAMLIT SPACE */
        /* -------------------------------------------------- */

        div[data-testid="stVerticalBlock"] > div {
            gap: 0.25rem;
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
# ============================================================

top_left, top_middle, top_right = st.columns(
    [4, 3.4, 4.6]
)


# ============================================================
# READY
# ============================================================

with top_left:

    st.markdown(
        """
        <div class="ready-text">
            🟢 READY
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
        <div class="clock-text">
            {current_time}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# STATUS
# ============================================================

with top_right:

    if system_status == "NORMAL":

        status_html = """
        <div class="status-text">
            🟢 STATUS: NORMAL
        </div>
        """

    elif system_status == "WARNING":

        status_html = """
        <div class="status-text">
            🟠 STATUS: WARNING
        </div>
        """

    else:

        status_html = """
        <div class="status-text">
            🔴 STATUS: CRITICAL
        </div>
        """

    st.markdown(
        status_html,
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
        """
        <div class="section-heading">
            🌡️ TEMPERATURE
        </div>
        """,
        unsafe_allow_html=True
    )

    # SUBTITLE "Temperature" REMOVED

    st.markdown(
        f"""
        <div class="big-value">
            {temperature} °C
        </div>
        """,
        unsafe_allow_html=True
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
        """
        <div class="section-heading">
            ⚡ CURRENT
        </div>
        """,
        unsafe_allow_html=True
    )

    # SUBTITLE "Current" REMOVED

    st.markdown(
        f"""
        <div class="big-value">
            {current} A
        </div>
        """,
        unsafe_allow_html=True
    )

    current_percentage = min(
        current / 10,
        1.0
    )

    st.progress(
        current_percentage
    )


# ============================================================
# CENTER
# CUSTOM AUTOMOTIVE SPEEDOMETER
# ============================================================

with center:

    min_speed = 0
    max_speed = 100


    # ========================================================
    # GAUGE GEOMETRY
    # ========================================================

    start_angle = 210
    end_angle = -30

    outer_radius = 1.0
    inner_radius = 0.72


    # ========================================================
    # CONVERT SPEED TO ANGLE
    # ========================================================

    def speed_to_angle(value):

        fraction = (
            value - min_speed
        ) / (
            max_speed - min_speed
        )

        return (
            start_angle
            + fraction * (
                end_angle - start_angle
            )
        )


    # ========================================================
    # POLAR TO CARTESIAN
    # ========================================================

    def polar_to_xy(
        radius,
        angle
    ):

        radians = math.radians(angle)

        x = radius * math.cos(radians)
        y = radius * math.sin(radians)

        return x, y


    # ========================================================
    # CREATE ANNULAR COLOUR SEGMENT
    # ========================================================

    def create_arc_segment(
        start_value,
        end_value,
        color
    ):

        points = 50

        outer_points = []
        inner_points = []

        start = speed_to_angle(
            start_value
        )

        end = speed_to_angle(
            end_value
        )

        for i in range(points + 1):

            angle = start + (
                end - start
            ) * i / points

            x, y = polar_to_xy(
                outer_radius,
                angle
            )

            outer_points.append(
                (x, y)
            )

            x, y = polar_to_xy(
                inner_radius,
                angle
            )

            inner_points.append(
                (x, y)
            )


        polygon = (
            outer_points
            + inner_points[::-1]
        )

        x_values = [
            p[0]
            for p in polygon
        ]

        y_values = [
            p[1]
            for p in polygon
        ]

        return go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            fill="toself",
            fillcolor=color,
            line={
                "color": color,
                "width": 0
            },
            hoverinfo="skip",
            showlegend=False
        )


    # ========================================================
    # CREATE FIGURE
    # ========================================================

    speedometer = go.Figure()


    # ========================================================
    # GREEN SECTION
    # 0 - 40
    # ========================================================

    speedometer.add_trace(
        create_arc_segment(
            0,
            40,
            "#49E600"
        )
    )


    # ========================================================
    # BLUE SECTION
    # 40 - 55
    # ========================================================

    speedometer.add_trace(
        create_arc_segment(
            40,
            55,
            "#1479E8"
        )
    )


    # ========================================================
    # DARK SECTION
    # 55 - 100
    # ========================================================

    speedometer.add_trace(
        create_arc_segment(
            55,
            100,
            "#263442"
        )
    )


    # ========================================================
    # WHITE TICK MARKS
    # ========================================================

    for value in range(
        0,
        101,
        5
    ):

        angle = speed_to_angle(
            value
        )


        if value % 10 == 0:

            tick_outer = 1.17
            tick_inner = 1.02
            tick_width = 6

        else:

            tick_outer = 1.14
            tick_inner = 1.04
            tick_width = 4


        x1, y1 = polar_to_xy(
            tick_outer,
            angle
        )

        x2, y2 = polar_to_xy(
            tick_inner,
            angle
        )


        speedometer.add_trace(
            go.Scatter(
                x=[
                    x1,
                    x2
                ],

                y=[
                    y1,
                    y2
                ],

                mode="lines",

                line={
                    "color": "#FFFFFF",
                    "width": tick_width
                },

                hoverinfo="skip",
                showlegend=False
            )
        )


    # ========================================================
    # ONLY 0, 50 AND 100 LABELS
    # ========================================================

    label_values = [
        0,
        50,
        100
    ]


    for value in label_values:

        angle = speed_to_angle(
            value
        )

        label_radius = 1.31

        x, y = polar_to_xy(
            label_radius,
            angle
        )


        speedometer.add_annotation(

            x=x,
            y=y,

            text=str(value),

            showarrow=False,

            font={
                "size": 22,
                "color": "#FFFFFF",
                "family": "Arial"
            },

            xanchor="center",
            yanchor="middle"
        )


    # ========================================================
    # CURRENT SPEED INDICATOR
    # ========================================================

    speed_angle = speed_to_angle(
        speed
    )


    indicator_outer = 1.00
    indicator_inner = 0.74


    x1, y1 = polar_to_xy(
        indicator_outer,
        speed_angle
    )

    x2, y2 = polar_to_xy(
        indicator_inner,
        speed_angle
    )


    speedometer.add_trace(
        go.Scatter(

            x=[
                x1,
                x2
            ],

            y=[
                y1,
                y2
            ],

            mode="lines",

            line={
                "color": "#FFFFFF",
                "width": 7
            },

            hoverinfo="skip",
            showlegend=False
        )
    )


    # ========================================================
    # CENTER SPEED NUMBER
    # ========================================================

    speedometer.add_annotation(

        x=0,
        y=0.04,

        text=str(speed),

        showarrow=False,

        font={
            "size": 76,
            "color": "#FFFFFF",
            "family": "Arial"
        },

        xanchor="center",
        yanchor="middle"
    )


    # ========================================================
    # KM/H
    # ========================================================

    speedometer.add_annotation(

        x=0,
        y=-0.25,

        text="km/h",

        showarrow=False,

        font={
            "size": 25,
            "color": "#FFFFFF",
            "family": "Arial"
        },

        xanchor="center",
        yanchor="middle"
    )


    # ========================================================
    # SPEEDOMETER LAYOUT
    # ========================================================

    speedometer.update_layout(

        height=470,

        margin={
            "l": 10,
            "r": 10,
            "t": 10,
            "b": 5
        },

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        showlegend=False,

        xaxis={
            "visible": False,
            "range": [
                -1.45,
                1.45
            ],
            "fixedrange": True
        },

        yaxis={
            "visible": False,
            "range": [
                -1.40,
                1.40
            ],
            "fixedrange": True,

            "scaleanchor": "x",
            "scaleratio": 1
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
            <div class="gear-label">
                GEAR
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="gear-value">
                {gear}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# RIGHT SECTION
# ============================================================

with right:

    # ========================================================
    # FAN
    # ========================================================

    st.markdown(
        """
        <div class="section-heading">
            🌀 FAN
        </div>
        """,
        unsafe_allow_html=True
    )

    # SUBTITLE "Cooling Fan" REMOVED


    if fan_on:

        st.markdown(
            """
            <div class="big-value">
                ON
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="big-value">
                OFF
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        f"""
        <div class="sub-heading">
            {fan_mode}
        </div>
        """,
        unsafe_allow_html=True
    )


    st.divider()


    # ========================================================
    # VOLTAGE
    # ========================================================

    st.markdown(
        """
        <div class="section-heading">
            🔋 VOLTAGE
        </div>
        """,
        unsafe_allow_html=True
    )

    # SUBTITLE "Battery Voltage" REMOVED


    st.markdown(
        f"""
        <div class="big-value">
            {voltage} V
        </div>
        """,
        unsafe_allow_html=True
    )


    voltage_percentage = min(
        voltage / 60,
        1.0
    )

    st.progress(
        voltage_percentage
    )

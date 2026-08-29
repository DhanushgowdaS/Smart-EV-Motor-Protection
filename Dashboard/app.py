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
# PAGE BACKGROUND
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

top_left, top_middle, top_right = st.columns(
    [4, 3, 5]
)


# ============================================================
# READY
# ============================================================

with top_left:
    st.write("🟢 **READY**")


# ============================================================
# REAL-TIME CLOCK
# ============================================================

with top_middle:
    st.write(f"### {current_time}")


# ============================================================
# STATUS
# ============================================================

with top_right:

    if system_status == "NORMAL":
        st.write("🟢 **STATUS: NORMAL**")

    elif system_status == "WARNING":
        st.write("🟠 **STATUS: WARNING**")

    else:
        st.write("🔴 **STATUS: CRITICAL**")


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

    st.subheader("🌡️ TEMPERATURE")

    st.write("Temperature")

    st.write(f"## {temperature} °C")

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

    st.subheader("⚡ CURRENT")

    st.write("Current")

    st.write(f"## {current} A")

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

    # --------------------------------------------------------
    # SPEED RANGE
    # --------------------------------------------------------

    min_speed = 0
    max_speed = 100


    # --------------------------------------------------------
    # GAUGE GEOMETRY
    #
    # LEFT  = 0
    # TOP   = 50
    # RIGHT = 100
    # --------------------------------------------------------

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
    #
    # BIG
    # SMALL
    # BIG
    # SMALL
    #
    # EVERY 5 KM/H
    # BIG TICK = 10 KM/H
    # SMALL TICK = 5 KM/H
    # ========================================================

    for value in range(
        0,
        101,
        5
    ):

        angle = speed_to_angle(
            value
        )


        # --------------------------------------------
        # BIG TICK
        # --------------------------------------------

        if value % 10 == 0:

            tick_outer = 1.17
            tick_inner = 1.02
            tick_width = 6


        # --------------------------------------------
        # SMALL TICK
        # --------------------------------------------

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
    # NUMBER LABELS
    #
    # ONLY:
    # 0
    # 50
    # 100
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
    # DIRECTLY UNDER SPEED
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

        st.write("**GEAR**")

        st.write(f"# {gear}")


# ============================================================
# RIGHT SECTION
# ============================================================

with right:

    # ========================================================
    # FAN
    # ========================================================

    st.subheader("🌀 FAN")

    st.write("Cooling Fan")


    if fan_on:
        st.write("## ON")

    else:
        st.write("## OFF")


    st.write(fan_mode)


    st.divider()


    # ========================================================
    # VOLTAGE
    # ========================================================

    st.subheader("🔋 VOLTAGE")

    st.write("Battery Voltage")

    st.write(f"## {voltage} V")


    voltage_percentage = min(
        voltage / 60,
        1.0
    )

    st.progress(
        voltage_percentage
    )


# ============================================================
# ODOMETER + RANGE
# ============================================================

st.divider()

odo_col, range_col = st.columns(2)


# ============================================================
# ODOMETER
# ============================================================

with odo_col:

    st.write("💡 **ODO**")

    st.write(f"## {odo} km")


# ============================================================
# RANGE
# ============================================================

with range_col:

    st.write("🛣️ **RANGE**")

    st.write(f"## {range_km} km")


# ============================================================
# LAST UPDATED
# ============================================================

st.caption(
    f"Last updated: {current_date} {current_time}"
)

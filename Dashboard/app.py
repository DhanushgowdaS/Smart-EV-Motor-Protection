import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from zoneinfo import ZoneInfo
import math
import requests
import time

st.set_page_config(
    page_title="Smart EV Motor Protection System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "https://smart-ev-motor-protection.onrender.com/data"

try:
    response = requests.get(API_URL, timeout=5)

    if response.status_code == 200:
        data = response.json()
    else:
        data = None

except Exception:
    data = None

if data is None:
    temperature = 0.0
    current = 0.0
    voltage = 0.0
    fan_on = False
    system_on = False
    system_status = "NOT CONNECTED"
    speed = 0.0
    battery_health = None

else:
    temperature = float(data.get("temperature", 0.0))
    current = float(data.get("current", 0.0))
    voltage = float(data.get("voltage", 0.0))
    fan_on = bool(data.get("fan", False))
    system_on = bool(data.get("system", False))
    system_status = data.get("status", "NORMAL")
    speed = float(data.get("speed", 0.0))
    battery_health = data.get("battery_health", None)

    speed = max(0.0, min(speed, 100.0))

odo = 1256
range_km = 78
fan_mode = "AUTO MODE"

india_time = datetime.now(ZoneInfo("Asia/Kolkata"))

current_time = india_time.strftime("%I:%M %p")
current_date = india_time.strftime("%d-%m-%Y")

st.markdown(
    """
    <style>

        .stApp {
            background-color: #02070B;
            background-image:
                radial-gradient(circle at 50% 45%, rgba(20,121,232,0.10), transparent 38%),
                radial-gradient(circle at 10% 90%, rgba(73,230,0,0.06), transparent 25%),
                radial-gradient(circle, rgba(255,255,255,0.12) 1px, transparent 1.5px),
                linear-gradient(108deg, transparent 42%, rgba(20,121,232,0.08) 50%, transparent 58%);
            background-size: auto, auto, 90px 90px, 220% 100%;
            background-position: center, center, 0 0, -120% 0;
            animation: particleDrift 20s linear infinite, neonSweep 9s ease-in-out infinite;
        }

        @keyframes neonSweep {
            0% { background-position: center, center, 0 0, -120% 0; }
            15% { background-position: center, center, 13px 13px, -80% 0; }
            55% { background-position: center, center, 45px 45px, 80% 0; }
            100% { background-position: center, center, 90px 90px, 120% 0; }
        }

        @keyframes particleDrift {
            0% { background-position: center, center, 0 0, -120% 0; }
            100% { background-position: center, center, 90px 90px, -120% 0; }
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

        .project-title {
            text-align: center;
            white-space: nowrap;
            font-size: 36px;
            font-weight: 800;
            letter-spacing: 1px;
            color: #F5F5F5;
            margin-bottom: 5px;
        }

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

        .battery-health-title {
            font-size: 25px;
            font-weight: 800;
            color: #F5F5F5;
            white-space: nowrap;
        }

        .big-value {
            font-size: 38px;
            font-weight: 800;
            color: #FFFFFF;
            margin-top: 5px;
            margin-bottom: 10px;
        }

        div[data-testid="stVerticalBlock"] > div {
            gap: 0.25rem;
        }

    </style>
    """,
    unsafe_allow_html=True
)

st.write("")

st.markdown(
    """
    <div class="project-title">
        ⚡ SMART EV MOTOR PROTECTION SYSTEM
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

top_left, top_middle, top_right = st.columns(
    [4, 3.4, 4.6]
)

with top_left:

    if system_on:
        ready_text = "🟢 READY"
    else:
        ready_text = "🔴 NOT READY"

    st.markdown(
        f"""
        <div class="ready-text">
            {ready_text}
        </div>
        """,
        unsafe_allow_html=True
    )

with top_middle:

    st.markdown(
        f"""
        <div class="clock-text">
            {current_time}
        </div>
        """,
        unsafe_allow_html=True
    )

with top_right:

    if system_status == "NORMAL":

        status_html = """
        <div class="status-text">
            <span style="color:#49E600;">
                🟢 STATUS: NORMAL
            </span>
        </div>
        """

    elif system_status == "WARNING":

        status_html = """
        <div class="status-text">
            <span style="color:#FF0000;">
                🔴 STATUS: WARNING
            </span>
        </div>
        """

    elif system_status == "CRITICAL":

        status_html = """
        <div class="status-text">
            <span style="color:#FF0000;">
                🔴 STATUS: CRITICAL
            </span>
        </div>
        """

    elif system_status == "LOAD RISING":

        status_html = """
        <div class="status-text">
            <span style="color:#FF0000;">
                🔴 STATUS: LOAD RISING
            </span>
        </div>
        """

    elif system_status == "NOT CONNECTED":

        status_html = """
        <div class="status-text">
            <span style="color:#FF0000;">
                🔴 STATUS: NOT CONNECTED
            </span>
        </div>
        """

    else:

        status_html = f"""
        <div class="status-text">
            <span style="color:#FFFFFF;">
                STATUS: {system_status}
            </span>
        </div>
        """

    st.markdown(
        status_html,
        unsafe_allow_html=True
    )

st.divider()

left, center, right = st.columns(
    [3, 5, 3]
)

with left:

    st.markdown(
        """
        <div class="section-heading">
            🌡️ TEMPERATURE
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="big-value">
            {temperature:.2f} °C
        </div>
        """,
        unsafe_allow_html=True
    )

    temperature_percentage = min(
        max(temperature / 100, 0.0),
        1.0
    )

    st.progress(
        temperature_percentage
    )

    st.divider()

    st.markdown(
        """
        <div class="section-heading">
            ⚡ CURRENT
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="big-value">
            {current:.2f} A
        </div>
        """,
        unsafe_allow_html=True
    )

    current_percentage = min(
        max(current / 10, 0.0),
        1.0
    )

    st.progress(
        current_percentage
    )

with center:

    min_speed = 0
    max_speed = 100

    start_angle = 220
    end_angle = -40

    def speed_to_angle(value):
        fraction = (value - min_speed) / (max_speed - min_speed)
        return start_angle + fraction * (end_angle - start_angle)

    def polar_to_xy(radius, angle):
        radians = math.radians(angle)
        return radius * math.cos(radians), radius * math.sin(radians)

    def create_arc_segment(start_value, end_value, color, width=22, radius=1.0):
        points = 80
        x_values = []
        y_values = []

        start = speed_to_angle(start_value)
        end = speed_to_angle(end_value)

        for i in range(points + 1):
            angle = start + (end - start) * i / points
            x, y = polar_to_xy(radius, angle)
            x_values.append(x)
            y_values.append(y)

        return go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            line={
                "color": color,
                "width": width
            },
            hoverinfo="skip",
            showlegend=False
        )

    speedometer = go.Figure()

    # Deep instrument face
    face_points = 160
    face_x = []
    face_y = []

    for i in range(face_points + 1):
        angle = 360 * i / face_points
        x, y = polar_to_xy(1.08, angle)
        face_x.append(x)
        face_y.append(y)

    speedometer.add_trace(
        go.Scatter(
            x=face_x,
            y=face_y,
            mode="lines",
            fill="toself",
            fillcolor="#06111B",
            line={
                "color": "#0D1822",
                "width": 2
            },
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Premium outer bezel
    speedometer.add_trace(
        go.Scatter(
            x=face_x,
            y=face_y,
            mode="lines",
            line={
                "color": "#5E6A75",
                "width": 12
            },
            hoverinfo="skip",
            showlegend=False
        )
    )

    speedometer.add_trace(
        go.Scatter(
            x=face_x,
            y=face_y,
            mode="lines",
            line={
                "color": "#121D27",
                "width": 7
            },
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Colored performance arc
    speedometer.add_trace(
        create_arc_segment(
            0,
            40,
            "#49E600",
            24,
            1.00
        )
    )

    speedometer.add_trace(
        create_arc_segment(
            40,
            55,
            "#1479E8",
            24,
            1.00
        )
    )

    speedometer.add_trace(
        create_arc_segment(
            55,
            100,
            "#263442",
            24,
            1.00
        )
    )

    # Inner highlight ring
    inner_points = 160
    inner_x = []
    inner_y = []

    for i in range(inner_points + 1):
        angle = 360 * i / inner_points
        x, y = polar_to_xy(0.82, angle)
        inner_x.append(x)
        inner_y.append(y)

    speedometer.add_trace(
        go.Scatter(
            x=inner_x,
            y=inner_y,
            mode="lines",
            line={
                "color": "#152431",
                "width": 2
            },
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Automotive-style graduations
    for value in range(0, 101, 2):
        angle = speed_to_angle(value)

        if value % 10 == 0:
            tick_outer = 1.19
            tick_inner = 1.08
            tick_width = 5
        else:
            tick_outer = 1.17
            tick_inner = 1.105
            tick_width = 2

        x1, y1 = polar_to_xy(tick_outer, angle)
        x2, y2 = polar_to_xy(tick_inner, angle)

        speedometer.add_trace(
            go.Scatter(
                x=[x1, x2],
                y=[y1, y2],
                mode="lines",
                line={
                    "color": "#F4F7FA",
                    "width": tick_width
                },
                hoverinfo="skip",
                showlegend=False
            )
        )

    # Numeric scale
    for value in range(0, 101, 10):
        angle = speed_to_angle(value)
        x, y = polar_to_xy(1.34, angle)

        speedometer.add_annotation(
            x=x,
            y=y,
            text=str(value),
            showarrow=False,
            font={
                "size": 17,
                "color": "#E9EEF2",
                "family": "Arial"
            },
            xanchor="center",
            yanchor="middle"
        )

    # Digital center display
    speedometer.add_annotation(
        x=0,
        y=0.13,
        text=f"{speed:.0f}",
        showarrow=False,
        font={
            "size": 72,
            "color": "#FFFFFF",
            "family": "Arial Black"
        },
        xanchor="center",
        yanchor="middle"
    )

    speedometer.add_annotation(
        x=0,
        y=-0.18,
        text="km/h",
        showarrow=False,
        font={
            "size": 22,
            "color": "#D7E0E8",
            "family": "Arial"
        },
        xanchor="center",
        yanchor="middle"
    )

    # Needle shadow
    speed_angle = speed_to_angle(speed)

    x1, y1 = polar_to_xy(0.91, speed_angle)
    x2, y2 = polar_to_xy(0.17, speed_angle)

    speedometer.add_trace(
        go.Scatter(
            x=[x1 + 0.018, x2 + 0.018],
            y=[y1 - 0.018, y2 - 0.018],
            mode="lines",
            line={
                "color": "rgba(0,0,0,0.75)",
                "width": 11
            },
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Needle
    speedometer.add_trace(
        go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode="lines",
            line={
                "color": "#FF5A36",
                "width": 6
            },
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Needle tip
    tip_x, tip_y = polar_to_xy(0.98, speed_angle)

    speedometer.add_trace(
        go.Scatter(
            x=[tip_x],
            y=[tip_y],
            mode="markers",
            marker={
                "size": 9,
                "color": "#FF6B45",
                "line": {
                    "color": "#FFFFFF",
                    "width": 1
                }
            },
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Central metallic hub
    speedometer.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            marker={
                "size": 18,
                "color": "#1B2732",
                "line": {
                    "color": "#D6DEE5",
                    "width": 3
                }
            },
            hoverinfo="skip",
            showlegend=False
        )
    )

    speedometer.update_layout(
        height=500,
        margin={
            "l": 10,
            "r": 10,
            "t": 8,
            "b": 5
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis={
            "visible": False,
            "range": [-1.48, 1.48],
            "fixedrange": True
        },
        yaxis={
            "visible": False,
            "range": [-1.48, 1.48],
            "fixedrange": True,
            "scaleanchor": "x",
            "scaleratio": 1
        }
    )

    st.plotly_chart(
        speedometer,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "staticPlot": True
        }
    )

with right:

    st.markdown(
        """
        <div class="section-heading">
            🌀 FAN
        </div>
        """,
        unsafe_allow_html=True
    )

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

    st.markdown(
        """
        <div class="section-heading">
            🔋 VOLTAGE
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="big-value">
            {voltage:.2f} V
        </div>
        """,
        unsafe_allow_html=True
    )

    voltage_percentage = min(
        max(voltage / 12, 0.0),
        1.0
    )

    st.progress(
        voltage_percentage
    )

st.divider()

battery_col, empty_middle, odo_col, range_col = st.columns(
    [2.5, 1.5, 3, 3]
)

with battery_col:

    st.markdown(
        '<div class="battery-health-title">🔋 BATTERY HEALTH</div>',
        unsafe_allow_html=True
    )

    if battery_health is None:
        battery_health_text = "-- %"
    else:
        battery_health_text = f"{float(battery_health):.0f} %"

    st.markdown(
        f"# {battery_health_text}"
    )

with odo_col:

    st.markdown(
        "## 💡 ODO"
    )

    st.markdown(
        f"# {odo} km"
    )

with range_col:

    st.markdown(
        "## 🛣️ RANGE"
    )

    st.markdown(
        f"# {range_km} km"
    )

st.divider()

st.caption(
    f"Last updated: {current_date} {current_time}"
)

time.sleep(0.5)

st.rerun()

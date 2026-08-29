import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from zoneinfo import ZoneInfo
import math


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Smart EV Motor Protection System",
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

temperature_limit = 80
current_limit = 10
voltage_max = 60


# ============================================================
# REAL TIME
# ============================================================

now = datetime.now(ZoneInfo("Asia/Kolkata"))

current_time = now.strftime("%I:%M %p")
last_updated = now.strftime("%d-%m-%Y %I:%M:%S %p")


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
# TITLE
# ============================================================

st.title("⚡ SMART EV MOTOR PROTECTION SYSTEM")


# ============================================================
# TOP STATUS BAR
# ============================================================

top1, top2, top3 = st.columns(3)


with top1:
    st.success("READY")


with top2:
    st.markdown(f"## {current_time}")


with top3:
    if system_status == "NORMAL":
        st.success(f"STATUS: {system_status}")
    elif system_status == "WARNING":
        st.warning(f"STATUS: {system_status}")
    else:
        st.error(f"STATUS: {system_status}")


st.divider()


# ============================================================
# MAIN LAYOUT
# ============================================================

left, middle, right = st.columns(
    [2.5, 5, 2.5],
    gap="large"
)


# ============================================================
# LEFT COLUMN
# ============================================================

with left:

    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    st.subheader("🌡️ TEMPERATURE")

    st.caption("Temperature")

    st.metric(
        label="",
        value=f"{temperature:.0f} °C"
    )

    st.progress(
        min(temperature / temperature_limit, 1.0)
    )


    st.divider()


    # --------------------------------------------------------
    # CURRENT
    # --------------------------------------------------------

    st.subheader("⚡ CURRENT")

    st.caption("Current")

    st.metric(
        label="",
        value=f"{current:.1f} A"
    )

    st.progress(
        min(current / current_limit, 1.0)
    )


# ============================================================
# SPEEDOMETER FUNCTION
# ============================================================

def create_speedometer(value):

    fig = go.Figure()


    # --------------------------------------------------------
    # MAIN OUTER DARK ARC
    # --------------------------------------------------------

    fig.add_trace(
        go.Pie(
            values=[45, 25, 30],
            labels=["GREEN", "BLUE", "DARK"],
            hole=0.72,
            sort=False,
            direction="clockwise",
            rotation=135,

            marker=dict(
                colors=[
                    "#55FF00",
                    "#168BFF",
                    "#202A35"
                ],
                line=dict(
                    color="#0A1118",
                    width=0
                )
            ),

            textinfo="none",
            hoverinfo="skip",
            showlegend=False
        )
    )


    # --------------------------------------------------------
    # WHITE TICK MARKS
    # --------------------------------------------------------

    # Gauge goes approximately from 135° to 405°
    start_angle = 135
    end_angle = 405

    radius_outer = 1.00
    radius_inner = 0.88

    for i in range(21):

        angle = math.radians(
            start_angle +
            (end_angle - start_angle) * i / 20
        )

        x1 = radius_inner * math.cos(angle)
        y1 = radius_inner * math.sin(angle)

        x2 = radius_outer * math.cos(angle)
        y2 = radius_outer * math.sin(angle)

        width = 5 if i % 5 == 0 else 3

        fig.add_trace(
            go.Scatter(
                x=[x1, x2],
                y=[y1, y2],

                mode="lines",

                line=dict(
                    color="white",
                    width=width
                ),

                hoverinfo="skip",
                showlegend=False
            )
        )


    # --------------------------------------------------------
    # GAUGE LABELS
    # --------------------------------------------------------

    # 0
    angle = math.radians(138)

    fig.add_annotation(
        x=0.82 * math.cos(angle),
        y=0.82 * math.sin(angle),

        text="0",

        showarrow=False,

        font=dict(
            size=22,
            color="white"
        )
    )


    # 50
    angle = math.radians(270)

    fig.add_annotation(
        x=0,
        y=0.82,

        text="50",

        showarrow=False,

        font=dict(
            size=22,
            color="white"
        )
    )


    # 100
    angle = math.radians(402)

    fig.add_annotation(
        x=0.82 * math.cos(angle),
        y=0.82 * math.sin(angle),

        text="100",

        showarrow=False,

        font=dict(
            size=22,
            color="white"
        )
    )


    # --------------------------------------------------------
    # SPEED NUMBER
    # --------------------------------------------------------

    fig.add_annotation(
        x=0,
        y=-0.02,

        text=f"<b>{value}</b>",

        showarrow=False,

        font=dict(
            size=76,
            color="white"
        )
    )


    # --------------------------------------------------------
    # KM/H
    # --------------------------------------------------------

    fig.add_annotation(
        x=0,
        y=-0.32,

        text="km/h",

        showarrow=False,

        font=dict(
            size=27,
            color="white"
        )
    )


    # --------------------------------------------------------
    # GEAR
    # --------------------------------------------------------

    fig.add_annotation(
        x=0,
        y=-0.78,

        text=f"<b>{gear}</b>",

        showarrow=False,

        font=dict(
            size=48,
            color="#55FF00"
        )
    )


    # --------------------------------------------------------
    # BOTTOM LINES
    # --------------------------------------------------------

    fig.add_shape(
        type="line",

        x0=-0.72,
        y0=-0.78,

        x1=-0.30,
        y1=-0.78,

        line=dict(
            color="#35404A",
            width=2
        )
    )


    fig.add_shape(
        type="line",

        x0=0.30,
        y0=-0.78,

        x1=0.72,
        y1=-0.78,

        line=dict(
            color="#35404A",
            width=2
        )
    )


    # --------------------------------------------------------
    # SPEED / GEAR INFORMATION
    # --------------------------------------------------------

    fig.add_annotation(
        x=-0.45,
        y=-1.12,

        text="<b>SPEED</b><br><br>"
             f"<span style='font-size:28px'>{value} km/h</span>",

        showarrow=False,

        align="center",

        font=dict(
            size=16,
            color="white"
        )
    )


    fig.add_annotation(
        x=0.45,
        y=-1.12,

        text="<b>GEAR</b><br><br>"
             f"<span style='font-size:28px;color:#55FF00'>{gear}</span>",

        showarrow=False,

        align="center",

        font=dict(
            size=16,
            color="white"
        )
    )


    # --------------------------------------------------------
    # LAYOUT
    # --------------------------------------------------------

    fig.update_layout(

        height=650,

        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),

        paper_bgcolor="#061019",

        plot_bgcolor="#061019",

        showlegend=False,

        xaxis=dict(
            visible=False,
            range=[-1.25, 1.25]
        ),

        yaxis=dict(
            visible=False,
            range=[-1.35, 1.20],

            scaleanchor="x",
            scaleratio=1
        )
    )

    return fig


# ============================================================
# CENTER COLUMN
# ============================================================

with middle:

    speedometer = create_speedometer(speed)

    st.plotly_chart(
        speedometer,
        use_container_width=True,

        config={
            "displayModeBar": False,
            "staticPlot": True
        }
    )


# ============================================================
# RIGHT COLUMN
# ============================================================

with right:

    # --------------------------------------------------------
    # FAN
    # --------------------------------------------------------

    st.subheader("🌀 FAN")

    st.caption("Cooling Fan")

    st.metric(
        label="",
        value=fan_status
    )

    st.write(f"**{fan_mode}**")


    st.divider()


    # --------------------------------------------------------
    # VOLTAGE
    # --------------------------------------------------------

    st.subheader("🔋 VOLTAGE")

    st.caption("Battery Voltage")

    st.metric(
        label="",
        value=f"{voltage:.1f} V"
    )

    st.progress(
        min(voltage / voltage_max, 1.0)
    )


# ============================================================
# BOTTOM ODO + RANGE
# ============================================================

st.divider()


bottom1, bottom2 = st.columns(
    [1, 1],
    gap="large"
)


# ------------------------------------------------------------
# ODOMETER
# ------------------------------------------------------------

with bottom1:

    st.subheader("💡 ODO")

    st.metric(
        label="",
        value=f"{odo} km"
    )


# ------------------------------------------------------------
# RANGE
# ------------------------------------------------------------

with bottom2:

    st.subheader("🛣️ RANGE")

    st.metric(
        label="",
        value=f"{range_km} km"
    )


# ============================================================
# LAST UPDATED
# ============================================================

st.caption(
    f"Last updated: {last_updated}"
)

import streamlit as st
#import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EV System",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# DATA
# Later these values can come from ESP32/API
# ============================================================

temperature = 42.0
current = 2.6
voltage = 48.6
speed = 45
gear = "D"

fan_status = "ON"
fan_mode = "AUTO MODE"

system_status = "NORMAL"

odo = 1256
range_km = 78


# ============================================================
# COLORS
# ============================================================

NAVY = "#061019"
WHITE = "#FFFFFF"
GREEN = "#55E51B"
BLUE = "#1688FF"
ORANGE = "#FFB21C"
GREY = "#26333D"
LIGHT_GREY = "#B8C0C5"


# ============================================================
# HEADER
# ============================================================

col1, col2, col3 = st.columns([1.5, 1, 1.5])

with col1:
    st.markdown("## ⚡ EV SYSTEM")

with col2:
    current_time = datetime.now().strftime("%I:%M %p")
    st.markdown(
        f"<h3 style='text-align:center'>{current_time}</h3>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        "<h3 style='text-align:right;color:#55E51B'>● READY</h3>",
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# MAIN DASHBOARD
# ============================================================

left, centre, right = st.columns([1.2, 2.2, 1.2])


# ============================================================
# LEFT SIDE
# ============================================================

with left:

    st.subheader("🌡 TEMPERATURE")

    st.markdown(
        f"### <span style='color:{BLUE}'>{temperature:.0f} °C</span>",
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("⚡ CURRENT")

    st.markdown(
        f"### <span style='color:{ORANGE}'>{current:.1f} A</span>",
        unsafe_allow_html=True
    )


# ============================================================
# SPEEDOMETER FUNCTION
# ============================================================

def create_speedometer(speed_value):

    fig, ax = plt.subplots(
        figsize=(6, 3.8),
        facecolor=NAVY
    )

    ax.set_facecolor(NAVY)

    # --------------------------------------------------------
    # Gauge limits
    # --------------------------------------------------------

    max_speed = 100

    start_angle = 210
    end_angle = -30

    # Convert angles
    theta = np.linspace(
        np.radians(start_angle),
        np.radians(end_angle),
        300
    )

    # --------------------------------------------------------
    # Outer gauge
    # --------------------------------------------------------

    ax.plot(
        theta,
        np.ones_like(theta),
        linewidth=25,
        color=GREY,
        solid_capstyle="round"
    )

    # --------------------------------------------------------
    # Active green section
    # --------------------------------------------------------

    green_limit = 50

    green_theta = np.linspace(
        np.radians(start_angle),
        np.radians(
            start_angle
            - ((start_angle - end_angle) * green_limit / max_speed)
        ),
        200
    )

    ax.plot(
        green_theta,
        np.ones_like(green_theta),
        linewidth=25,
        color=GREEN,
        solid_capstyle="round"
    )

    # --------------------------------------------------------
    # Blue section
    # --------------------------------------------------------

    blue_start = 50
    blue_end = 65

    blue_theta = np.linspace(
        np.radians(
            start_angle
            - ((start_angle - end_angle) * blue_start / max_speed)
        ),
        np.radians(
            start_angle
            - ((start_angle - end_angle) * blue_end / max_speed)
        ),
        100
    )

    ax.plot(
        blue_theta,
        np.ones_like(blue_theta),
        linewidth=25,
        color=BLUE,
        solid_capstyle="butt"
    )

    # --------------------------------------------------------
    # Tick marks
    # --------------------------------------------------------

    for value in range(0, 101, 10):

        angle = np.radians(
            start_angle
            - ((start_angle - end_angle) * value / max_speed)
        )

        x1 = 0.91 * np.cos(angle)
        y1 = 0.91 * np.sin(angle)

        x2 = 1.03 * np.cos(angle)
        y2 = 1.03 * np.sin(angle)

        ax.plot(
            [x1, x2],
            [y1, y2],
            color=WHITE,
            linewidth=2
        )

        # Only show important numbers
        if value in [0, 50, 100]:

            tx = 0.78 * np.cos(angle)
            ty = 0.78 * np.sin(angle)

            ax.text(
                tx,
                ty,
                str(value),
                color=WHITE,
                fontsize=12,
                ha="center",
                va="center",
                fontweight="bold"
            )

    # --------------------------------------------------------
    # Speed
    # --------------------------------------------------------

    ax.text(
        0,
        0.15,
        str(int(speed_value)),
        color=WHITE,
        fontsize=48,
        ha="center",
        va="center",
        fontweight="bold"
    )

    ax.text(
        0,
        -0.08,
        "km/h",
        color=LIGHT_GREY,
        fontsize=15,
        ha="center",
        va="center"
    )

    # --------------------------------------------------------
    # Gear
    # --------------------------------------------------------

    ax.text(
        0,
        -0.43,
        gear,
        color=GREEN,
        fontsize=32,
        ha="center",
        va="center",
        fontweight="bold"
    )

    # --------------------------------------------------------
    # Clean graph
    # --------------------------------------------------------

    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-0.65, 1.15)

    ax.axis("off")

    plt.tight_layout()

    return fig


# ============================================================
# CENTRE SPEEDOMETER
# ============================================================

with centre:

    speedometer = create_speedometer(speed)

    st.pyplot(
        speedometer,
        use_container_width=True
    )

    plt.close(speedometer)


# ============================================================
# RIGHT SIDE
# ============================================================

with right:

    st.subheader("🌀 FAN")

    st.markdown(
        f"### <span style='color:{GREEN}'>{fan_status}</span>",
        unsafe_allow_html=True
    )

    st.caption(fan_mode)

    st.write("")

    st.subheader("🔋 VOLTAGE")

    st.markdown(
        f"### <span style='color:{BLUE}'>{voltage:.1f} V</span>",
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("🛡 STATUS")

    st.markdown(
        f"### <span style='color:{GREEN}'>{system_status}</span>",
        unsafe_allow_html=True
    )


# ============================================================
# BOTTOM INFORMATION
# ============================================================

st.divider()

bottom1, bottom2, bottom3 = st.columns(3)

with bottom1:

    st.caption("ODO")

    st.markdown(
        f"### {odo} km"
    )


with bottom2:

    st.caption("RANGE")

    st.markdown(
        f"### {range_km} km"
    )


with bottom3:

    st.caption("SYSTEM")

    st.markdown(
        f"### 🟢 {system_status}"
    )


# ============================================================
# FOOTER
# ============================================================

st.write("")

st.caption(
    "EV System Dashboard • Real-time vehicle monitoring"
)

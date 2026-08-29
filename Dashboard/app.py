import streamlit as st
import time
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
# CUSTOM STREAMLIT THEME
# NOTE:
# No HTML and no unsafe_allow_html are used.
# ============================================================

st.title("⚡ SMART EV MOTOR PROTECTION SYSTEM")

st.caption("Real-time EV motor monitoring and protection dashboard")

# ============================================================
# DEMO / SENSOR VALUES
# Replace these values with your ESP32 data later.
# ============================================================

temperature = 42.0
current = 2.6
voltage = 48.6
speed = 45.0
fan_on = True

# ============================================================
# PROTECTION LIMITS
# ============================================================

TEMP_WARNING = 40.0
TEMP_DANGER = 50.0

CURRENT_WARNING = 10.0
CURRENT_DANGER = 15.0

VOLTAGE_MIN = 40.0
VOLTAGE_MAX = 55.0

SPEED_MAX = 100.0


# ============================================================
# DETERMINE SYSTEM STATUS
# ============================================================

if temperature >= TEMP_DANGER:
    system_status = "CRITICAL"
elif temperature >= TEMP_WARNING:
    system_status = "WARNING"
else:
    system_status = "NORMAL"


# ============================================================
# HEADER STATUS
# ============================================================

header_col1, header_col2, header_col3 = st.columns([1, 2, 1])

with header_col1:
    if system_status == "NORMAL":
        st.success("🟢 READY")
    elif system_status == "WARNING":
        st.warning("🟡 WARNING")
    else:
        st.error("🔴 ALERT")

with header_col2:
    current_time = datetime.now().strftime("%I:%M %p")
    st.metric("TIME", current_time)

with header_col3:
    if system_status == "NORMAL":
        st.success("🟢 STATUS: NORMAL")
    elif system_status == "WARNING":
        st.warning("🟡 STATUS: WARNING")
    else:
        st.error("🔴 STATUS: CRITICAL")


st.divider()


# ============================================================
# MAIN DASHBOARD
# ============================================================

left, center, right = st.columns([1, 1.5, 1])


# ============================================================
# LEFT SIDE
# ============================================================

with left:

    st.subheader("🌡️ TEMPERATURE")

    st.metric(
        label="Motor Temperature",
        value=f"{temperature:.0f} °C"
    )

    temp_progress = min(
        max(temperature / TEMP_DANGER, 0.0),
        1.0
    )

    st.progress(
        temp_progress,
        text=f"{temperature:.0f} °C / {TEMP_DANGER:.0f} °C"
    )

    if temperature >= TEMP_DANGER:
        st.error("🔥 HIGH TEMPERATURE")
    elif temperature >= TEMP_WARNING:
        st.warning("⚠️ Temperature is elevated")
    else:
        st.success("Temperature is normal")


    st.divider()


    st.subheader("⚡ CURRENT")

    st.metric(
        label="Motor Current",
        value=f"{current:.1f} A"
    )

    current_progress = min(
        max(current / CURRENT_DANGER, 0.0),
        1.0
    )

    st.progress(
        current_progress,
        text=f"{current:.1f} A / {CURRENT_DANGER:.0f} A"
    )

    if current >= CURRENT_DANGER:
        st.error("🔴 OVERCURRENT")
    elif current >= CURRENT_WARNING:
        st.warning("⚠️ High current")
    else:
        st.success("Current is normal")


# ============================================================
# CENTER - SPEED
# ============================================================

with center:

    st.subheader("🚗 VEHICLE SPEED")

    st.metric(
        label="Current Speed",
        value=f"{speed:.0f} km/h"
    )

    speed_progress = min(
        max(speed / SPEED_MAX, 0.0),
        1.0
    )

    st.progress(
        speed_progress,
        text=f"{speed:.0f} km/h / {SPEED_MAX:.0f} km/h"
    )

    st.write("")

    if speed < 30:
        st.info("Low speed")
    elif speed < 70:
        st.success("Normal driving speed")
    else:
        st.warning("High speed")

    st.write("")

    st.info(
        "Motor speed is being monitored continuously "
        "for safe operation."
    )


# ============================================================
# RIGHT SIDE
# ============================================================

with right:

    st.subheader("🌀 FAN")

    if fan_on:
        st.success("ON")
    else:
        st.info("OFF")

    st.write("Mode: **AUTO MODE**")

    if fan_on:
        st.info("Cooling system active")
    else:
        st.success("Cooling system standby")


    st.divider()


    st.subheader("🔋 VOLTAGE")

    st.metric(
        label="Battery Voltage",
        value=f"{voltage:.1f} V"
    )

    voltage_progress = min(
        max(
            (voltage - VOLTAGE_MIN) /
            (VOLTAGE_MAX - VOLTAGE_MIN),
            0.0
        ),
        1.0
    )

    st.progress(
        voltage_progress,
        text=f"{voltage:.1f} V"
    )

    if voltage < VOLTAGE_MIN:
        st.error("🔴 LOW VOLTAGE")
    elif voltage > VOLTAGE_MAX:
        st.warning("⚠️ HIGH VOLTAGE")
    else:
        st.success("Voltage is normal")


# ============================================================
# PROTECTION INFORMATION
# ============================================================

st.divider()

st.subheader("🛡️ MOTOR PROTECTION")

p1, p2, p3, p4 = st.columns(4)

with p1:
    if temperature < TEMP_WARNING:
        st.success("🌡️ Temperature\n\nNORMAL")
    elif temperature < TEMP_DANGER:
        st.warning("🌡️ Temperature\n\nWARNING")
    else:
        st.error("🌡️ Temperature\n\nCRITICAL")

with p2:
    if current < CURRENT_WARNING:
        st.success("⚡ Current\n\nNORMAL")
    elif current < CURRENT_DANGER:
        st.warning("⚡ Current\n\nWARNING")
    else:
        st.error("⚡ Current\n\nCRITICAL")

with p3:
    if VOLTAGE_MIN <= voltage <= VOLTAGE_MAX:
        st.success("🔋 Voltage\n\nNORMAL")
    else:
        st.error("🔋 Voltage\n\nABNORMAL")

with p4:
    if fan_on:
        st.success("🌀 Cooling\n\nACTIVE")
    else:
        st.info("🌀 Cooling\n\nSTANDBY")


# ============================================================
# SYSTEM SUMMARY
# ============================================================

st.divider()

st.subheader("📊 SYSTEM SUMMARY")

summary1, summary2, summary3 = st.columns(3)

with summary1:
    st.metric(
        "Temperature",
        f"{temperature:.0f} °C"
    )

with summary2:
    st.metric(
        "Current",
        f"{current:.1f} A"
    )

with summary3:
    st.metric(
        "Voltage",
        f"{voltage:.1f} V"
    )


# ============================================================
# LAST UPDATE
# ============================================================

st.divider()

st.caption(
    f"Last updated: {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}"
)

st.caption(
    "Smart EV Motor Protection System • ESP32 Monitoring"
)

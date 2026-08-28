import streamlit as st
import random
from datetime import datetime

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Smart EV Motor Protection",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0b1220;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: white;
}

.dashboard-card {
    background-color: #151e2d;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #263449;
    margin-bottom: 15px;
}

.card-title {
    font-size: 16px;
    color: #9aa7b8;
    margin-bottom: 8px;
}

.card-value {
    font-size: 32px;
    font-weight: bold;
    color: white;
}

.card-unit {
    font-size: 15px;
    color: #9aa7b8;
}

.status-normal {
    background-color: #123b29;
    color: #4ade80;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
}

.status-warning {
    background-color: #493815;
    color: #facc15;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
}

.status-danger {
    background-color: #4a1d1d;
    color: #f87171;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("⚡ Smart EV Motor Protection System")

st.caption(
    "Real-time monitoring and protection dashboard for an electric vehicle motor"
)

st.divider()

# ---------------------------------------------------------
# DEMO SENSOR DATA
# ---------------------------------------------------------
# These values are currently generated for testing.
# Later we can replace this section with ESP32 data.

temperature = round(random.uniform(28, 40), 1)
voltage = round(random.uniform(44, 52), 1)
current = round(random.uniform(3, 12), 1)
motor_load = round(random.uniform(20, 80), 1)

speed = random.randint(0, 80)
odo = round(random.uniform(1200, 3500), 1)
range_km = random.randint(50, 120)

fan_on = temperature >= 35

# ---------------------------------------------------------
# PROTECTION LOGIC
# ---------------------------------------------------------

if temperature >= 45 or current >= 15:
    system_status = "DANGER"
elif temperature >= 38 or current >= 12:
    system_status = "WARNING"
else:
    system_status = "NORMAL"

# ---------------------------------------------------------
# TOP STATUS
# ---------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="dashboard-card">'
        '<div class="card-title">SYSTEM</div>'
        '<div class="card-value">⚡ EV</div>'
        '<div class="card-unit">Motor Protection System</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col2:
    current_time = datetime.now().strftime("%I:%M %p")

    st.markdown(
        f'<div class="dashboard-card">'
        f'<div class="card-title">TIME</div>'
        f'<div class="card-value">{current_time}</div>'
        f'<div class="card-unit">Live system time</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col3:
    if system_status == "NORMAL":
        st.markdown(
            '<div class="status-normal">● SYSTEM NORMAL</div>',
            unsafe_allow_html=True
        )
    elif system_status == "WARNING":
        st.markdown(
            '<div class="status-warning">⚠ SYSTEM WARNING</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-danger">⚠ MOTOR PROTECTION ACTIVE</div>',
            unsafe_allow_html=True
        )

# ---------------------------------------------------------
# MAIN SENSOR VALUES
# ---------------------------------------------------------

st.subheader("Live Parameters")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        label="🌡 Temperature",
        value=f"{temperature} °C"
    )

with c2:
    st.metric(
        label="🔋 Voltage",
        value=f"{voltage} V"
    )

with c3:
    st.metric(
        label="⚡ Current",
        value=f"{current} A"
    )

with c4:
    st.metric(
        label="⚙ Motor Load",
        value=f"{motor_load} %"
    )

# ---------------------------------------------------------
# MOTOR INFORMATION
# ---------------------------------------------------------

st.subheader("Motor Information")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        label="🚗 Speed",
        value=f"{speed} km/h"
    )

with m2:
    st.metric(
        label="🛣 ODO",
        value=f"{odo} km"
    )

with m3:
    st.metric(
        label="🔋 Range",
        value=f"{range_km} km"
    )

with m4:
    fan_status = "ON" if fan_on else "OFF"

    st.metric(
        label="🌀 Cooling Fan",
        value=fan_status
    )

# ---------------------------------------------------------
# LOAD BAR
# ---------------------------------------------------------

st.subheader("Motor Load")

st.progress(
    min(max(int(motor_load), 0), 100),
    text=f"Motor Load: {motor_load}%"
)

# ---------------------------------------------------------
# TEMPERATURE / CURRENT STATUS
# ---------------------------------------------------------

left, right = st.columns(2)

with left:

    st.markdown("### 🌡 Temperature Status")

    if temperature >= 45:
        st.error("CRITICAL TEMPERATURE")
    elif temperature >= 38:
        st.warning("HIGH TEMPERATURE")
    else:
        st.success("TEMPERATURE NORMAL")

with right:

    st.markdown("### ⚡ Current Status")

    if current >= 15:
        st.error("OVER-CURRENT DETECTED")
    elif current >= 12:
        st.warning("HIGH CURRENT")
    else:
        st.success("CURRENT NORMAL")

# ---------------------------------------------------------
# COOLING FAN
# ---------------------------------------------------------

st.subheader("Cooling System")

if fan_on:
    st.info("🌀 Cooling Fan: ON — Temperature is above the cooling threshold.")
else:
    st.success("🌀 Cooling Fan: OFF — Temperature is within normal range.")

# ---------------------------------------------------------
# PROTECTION STATUS
# ---------------------------------------------------------

st.subheader("Protection Status")

if system_status == "NORMAL":

    st.success(
        "✓ Motor operating normally. "
        "Temperature, current and load are within safe limits."
    )

elif system_status == "WARNING":

    st.warning(
        "⚠ Warning condition detected. "
        "Motor parameters should be monitored."
    )

else:

    st.error(
        "🚨 Protection condition detected! "
        "Motor may require immediate shutdown."
    )

# ---------------------------------------------------------
# SYSTEM DETAILS
# ---------------------------------------------------------

st.divider()

st.subheader("System Information")

info1, info2, info3 = st.columns(3)

with info1:
    st.write("**Controller:** ESP32")

with info2:
    st.write("**Communication:** Wi-Fi")

with info3:
    st.write("**Dashboard:** Streamlit")

# ---------------------------------------------------------
# REFRESH
# ---------------------------------------------------------

st.divider()

st.caption(
    "Smart EV Motor Protection System • Live Monitoring Dashboard"
)

if st.button("🔄 Refresh Data"):
    st.rerun()

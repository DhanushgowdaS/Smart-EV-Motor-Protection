import streamlit as st
from datetime import datetime

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="EV System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- DARK EV BACKGROUND ----------------

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background: #061019;
    color: white;
}

.block-container {
    padding-top: 25px;
    padding-left: 45px;
    padding-right: 45px;
    max-width: 1400px;
}

/* Remove default Streamlit spacing */
div[data-testid="column"] {
    padding: 0px 10px;
}

/* EV title */
.ev-title {
    font-size: 32px;
    font-weight: 800;
    letter-spacing: 2px;
}

.ev-green {
    color: #55e51b;
}

.ev-white {
    color: #ffffff;
}

/* Header time */
.header-time {
    text-align: center;
    color: #ffffff;
    font-size: 20px;
    font-weight: 600;
}

/* Header status */
.header-status {
    text-align: right;
    color: #55e51b;
    font-size: 20px;
    font-weight: 700;
}

/* Information blocks */
.info-title {
    color: #eeeeee;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 8px;
}

.info-value {
    font-size: 32px;
    font-weight: 700;
}

.blue {
    color: #1688ff;
}

.orange {
    color: #ffb21c;
}

.green {
    color: #55e51b;
}

.white {
    color: white;
}

/* Speedometer */
.speed-area {
    text-align: center;
    margin-top: 25px;
}

.speed-number {
    color: white;
    font-size: 70px;
    font-weight: 800;
    line-height: 0.9;
}

.speed-unit {
    color: #eeeeee;
    font-size: 20px;
    margin-top: 8px;
}

.gear {
    color: #55e51b;
    font-size: 50px;
    font-weight: 700;
    margin-top: 15px;
}

/* Gauge */
.gauge {
    width: 310px;
    height: 155px;
    margin: auto;
    border-radius: 310px 310px 0 0;
    background:
        conic-gradient(
            from 270deg,
            #55e51b 0deg 100deg,
            #1688ff 100deg 125deg,
            #26333d 125deg 180deg,
            transparent 180deg
        );
    position: relative;
}

.gauge-inner {
    position: absolute;
    width: 250px;
    height: 125px;
    left: 30px;
    bottom: 0;
    background: #061019;
    border-radius: 250px 250px 0 0;
}

/* Bottom information */
.bottom-line {
    border-top: 1px solid #33414a;
    margin-top: 35px;
    padding-top: 20px;
}

.bottom-label {
    color: #bbbbbb;
    font-size: 15px;
    text-align: center;
}

.bottom-value {
    color: white;
    font-size: 25px;
    font-weight: 700;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

header1, header2, header3 = st.columns([2, 2, 2])

with header1:
    st.markdown(
        '<div class="ev-title"><span class="ev-green">EV</span> '
        '<span class="ev-white">SYSTEM</span></div>',
        unsafe_allow_html=True
    )

with header2:
    current_time = datetime.now().strftime("%I:%M %p")

    st.markdown(
        f'<div class="header-time">{current_time}</div>',
        unsafe_allow_html=True
    )

with header3:
    st.markdown(
        '<div class="header-status">● READY</div>',
        unsafe_allow_html=True
    )


st.markdown("<hr>", unsafe_allow_html=True)


# ---------------- MAIN DASHBOARD ----------------

left, center, right = st.columns([1.15, 2.2, 1.15])


# ==================================================
# LEFT SIDE
# ==================================================

with left:

    st.markdown(
        """
        <div class="info-title">🌡 TEMPERATURE</div>
        <div class="info-value blue">42 °C</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-title">⚡ CURRENT</div>
        <div class="info-value orange">2.6 A</div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# CENTER SPEEDOMETER
# ==================================================

with center:

    st.markdown('<div class="speed-area">', unsafe_allow_html=True)

    # Gauge
    st.markdown(
        """
        <div class="gauge">
            <div class="gauge-inner"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Speed
    st.markdown(
        """
        <div class="speed-number">45</div>
        <div class="speed-unit">km/h</div>
        <div class="gear">D</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# RIGHT SIDE
# ==================================================

with right:

    st.markdown(
        """
        <div class="info-title">🌀 FAN</div>
        <div class="info-value green">ON</div>
        <div style="color:#aaaaaa;font-size:14px;">AUTO MODE</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-title">🔋 VOLTAGE</div>
        <div class="info-value blue">48.6 V</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-title">🛡 STATUS</div>
        <div class="info-value green">NORMAL</div>
        """,
        unsafe_allow_html=True
    )


# ---------------- BOTTOM ----------------

st.markdown('<div class="bottom-line"></div>', unsafe_allow_html=True)

b1, b2, b3 = st.columns([1, 2, 1])

with b1:
    st.markdown(
        """
        <div class="bottom-label">ODO</div>
        <div class="bottom-value">1256 km</div>
        """,
        unsafe_allow_html=True
    )

with b2:
    st.markdown(
        """
        <div class="bottom-label">RANGE</div>
        <div class="bottom-value">78 km</div>
        """,
        unsafe_allow_html=True
    )

with b3:
    st.markdown(
        """
        <div class="bottom-label">⚠</div>
        <div class="bottom-value">READY</div>
        """,
        unsafe_allow_html=True
    )

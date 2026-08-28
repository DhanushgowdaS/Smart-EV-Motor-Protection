import streamlit as st
import requests
import time
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="EV System",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# BACKEND URL
# ============================================================

BACKEND_URL = "YOUR_BACKEND_URL/data"


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #03080d;
    color: white;
}

.block-container {
    max-width: 1450px;
    padding-top: 25px;
}


/* MAIN DASHBOARD */

.dashboard {

    background:
    linear-gradient(
        145deg,
        #08151f,
        #02070b
    );

    border:
    2px solid #263642;

    border-radius:
    30px;

    padding:
    25px;

    box-shadow:
    0 0 40px rgba(0,0,0,0.8);

}


/* HEADER */

.header {

    display:
    flex;

    justify-content:
    space-between;

    align-items:
    center;

    border-bottom:
    1px solid #34434d;

    padding-bottom:
    15px;

    margin-bottom:
    20px;

}

.ev {

    font-size:
    30px;

    font-weight:
    bold;

}

.green {

    color:
    #55d63a;

}

.ready {

    color:
    #55d63a;

    font-size:
    25px;

    font-weight:
    bold;

}

.clock {

    font-size:
    24px;

    font-weight:
    bold;

}


/* CARD */

.card {

    background:
    linear-gradient(
        145deg,
        #101e28,
        #071018
    );

    border:
    1px solid #33444f;

    border-radius:
    20px;

    padding:
    22px;

    margin-bottom:
    18px;

    min-height:
    150px;

}


/* TITLE */

.title {

    font-size:
    20px;

    font-weight:
    bold;

    margin-bottom:
    10px;

}


/* VALUE */

.value {

    font-size:
    45px;

    font-weight:
    bold;

}

.blue {

    color:
    #168cff;

}

.yellow {

    color:
    #ffc400;

}


/* FAN */

.fan-icon {

    font-size:
    45px;

}

.fan-value {

    font-size:
    35px;

    font-weight:
    bold;

}


/* STATUS */

.normal {

    color:
    #55d63a;

    font-size:
    32px;

    font-weight:
    bold;

}

.warning {

    color:
    #ffc400;

    font-size:
    32px;

    font-weight:
    bold;

}

.emergency {

    color:
    #ff3b30;

    font-size:
    32px;

    font-weight:
    bold;

}


/* GAUGE */

.gauge {

    width:
    330px;

    height:
    330px;

    border-radius:
    50%;

    background:
    conic-gradient(
        #55d63a 0deg,
        #168cff 140deg,
        #182630 140deg,
        #182630 360deg
    );

    margin:
    auto;

    display:
    flex;

    align-items:
    center;

    justify-content:
    center;

}


.gauge-inner {

    width:
    260px;

    height:
    260px;

    border-radius:
    50%;

    background:
    #071018;

    display:
    flex;

    flex-direction:
    column;

    align-items:
    center;

    justify-content:
    center;

}


.speed {

    font-size:
    65px;

    font-weight:
    bold;

}


.speed-unit {

    font-size:
    22px;

}


.drive {

    color:
    #55d63a;

    font-size:
    30px;

    font-weight:
    bold;

    margin-top:
    10px;

}


/* BOTTOM */

.bottom {

    border-top:
    1px solid #34434d;

    margin-top:
    15px;

    padding-top:
    18px;

    display:
    flex;

    justify-content:
    space-around;

    font-size:
    20px;

}


/* REMOVE STREAMLIT */

#MainMenu {

    visibility:
    hidden;

}

footer {

    visibility:
    hidden;

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# GET SENSOR DATA
# ============================================================

try:

    response = requests.get(
        BACKEND_URL,
        timeout=3
    )

    if response.status_code == 200:

        data = response.json()

    else:

        data = None

except:

    data = None


# ============================================================
# DEFAULT VALUES
# ============================================================

if data is None:

    voltage = 0

    current = 0

    temperature = 0

    current_trend = "NO DATA"

    temperature_trend = "NO DATA"

    load_status = "NO CONNECTION"

    motor_status = "NO CONNECTION"

    fan = False

else:

    voltage = data.get(
        "voltage",
        0
    )

    current = data.get(
        "current",
        0
    )

    temperature = data.get(
        "temperature",
        0
    )

    current_trend = data.get(
        "current_trend",
        "STABLE"
    )

    temperature_trend = data.get(
        "temperature_trend",
        "STABLE"
    )

    load_status = data.get(
        "load_status",
        "NORMAL"
    )

    motor_status = data.get(
        "motor_status",
        "NORMAL"
    )

    fan = data.get(
        "fan",
        False
    )


# ============================================================
# TIME
# ============================================================

current_time = datetime.now().strftime(
    "%I:%M %p"
)


# ============================================================
# STATUS CLASS
# ============================================================

if motor_status == "EMERGENCY":

    status_class = "emergency"

elif motor_status == "WARNING":

    status_class = "warning"

else:

    status_class = "normal"


# ============================================================
# FAN
# ============================================================

if fan:

    fan_text = "ON"

else:

    fan_text = "OFF"


# ============================================================
# DASHBOARD
# ============================================================

st.markdown(
    '<div class="dashboard">',
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    f"""
    <div class="header">

        <div class="ev">
            <span class="green">EV</span>
            &nbsp; SYSTEM
        </div>

        <div class="clock">
            {current_time}
        </div>

        <div class="ready">
            READY
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# THREE COLUMNS
# ============================================================

left, center, right = st.columns(
    [1, 1.3, 1]
)


# ============================================================
# LEFT
# ============================================================

with left:

    # TEMP

    st.markdown(
        f"""
        <div class="card">

            <div class="title">
                🌡️ &nbsp; TEMP
            </div>

            <div class="value blue">
                {temperature:.2f}
                <span style="font-size:20px">
                °C
                </span>
            </div>

            <div style="
                margin-top:15px;
                height:10px;
                border-radius:10px;
                background:
                linear-gradient(
                    90deg,
                    #55d63a,
                    #55d63a,
                    #ffc400,
                    #ff3b30
                );
            "></div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-top:5px;
            ">
                <span>0</span>
                <span>60</span>
                <span>120</span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # CURRENT

    st.markdown(
        f"""
        <div class="card">

            <div class="title">
                ⚡ &nbsp; CURRENT
            </div>

            <div class="value yellow">
                {current:.3f}
                <span style="font-size:20px">
                A
                </span>
            </div>

            <div style="
                margin-top:15px;
                height:10px;
                border-radius:10px;
                background:
                linear-gradient(
                    90deg,
                    #55d63a,
                    #55d63a,
                    #ffc400,
                    #ff3b30
                );
            "></div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-top:5px;
            ">
                <span>0</span>
                <span>15</span>
                <span>30</span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CENTER
# ============================================================

with center:

    # Since we don't have a speed sensor yet,
    # show motor load percentage instead.

    load_percentage = min(
        max((current / 5.0) * 100, 0),
        100
    )


    st.markdown(
        f"""
        <div style="
            height:420px;
            display:flex;
            align-items:center;
            justify-content:center;
        ">

            <div class="gauge">

                <div class="gauge-inner">

                    <div class="speed">
                        {load_percentage:.0f}
                    </div>

                    <div class="speed-unit">
                        LOAD %
                    </div>

                    <div class="drive">
                        D
                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RIGHT
# ============================================================

with right:

    # FAN

    st.markdown(
        f"""
        <div class="card">

            <div class="title">
                🌀 &nbsp; FAN
            </div>

            <div class="fan-icon">
                🌀
            </div>

            <div class="fan-value green">
                {fan_text}
            </div>

            <div>
                AUTO MODE
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # VOLTAGE

    st.markdown(
        f"""
        <div class="card">

            <div class="title">
                🔋 &nbsp; VOLTAGE
            </div>

            <div class="value blue">
                {voltage:.2f}
                <span style="font-size:20px">
                V
                </span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # STATUS

    st.markdown(
        f"""
        <div class="card">

            <div class="title">
                🛡️ &nbsp; STATUS
            </div>

            <div class="{status_class}">
                {motor_status}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BOTTOM BAR
# ============================================================

st.markdown(
    """
    <div class="bottom">

        <div class="green">
            💡
        </div>

        <div>
            ODO &nbsp; <b>---</b>
        </div>

        <div>
            RANGE &nbsp; <b>---</b>
        </div>

        <div>
            ⚠️
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# EXTRA LIVE INFORMATION
# ============================================================

st.markdown(
    f"""
    <div style="
        margin-top:15px;
        text-align:center;
        color:#8c9aa3;
    ">

        Current Trend:
        <b>{current_trend}</b>
        &nbsp;&nbsp; | &nbsp;&nbsp;

        Temperature Trend:
        <b>{temperature_trend}</b>
        &nbsp;&nbsp; | &nbsp;&nbsp;

        Load:
        <b>{load_status}</b>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CLOSE DASHBOARD
# ============================================================

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(1)

st.rerun()

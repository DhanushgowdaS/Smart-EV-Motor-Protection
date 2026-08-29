import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="EV System",
    page_icon="⚡",
    layout="wide"
)

# ============================================================
# DATA
# Later these values will come from ESP32/API
# ============================================================

speed = 45
temperature = 42
current = 2.6
voltage = 48.6

fan = "ON"
status = "NORMAL"
gear = "D"

odo = 1256
range_km = 78

# ============================================================
# BACKGROUND
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #061018;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 0rem;
    max-width: 1250px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

header1, header2, header3 = st.columns([2, 3, 2])

with header1:
    st.markdown(
        "<h2 style='margin:0;'>"
        "<span style='color:#39D353;'>EV</span> SYSTEM"
        "</h2>",
        unsafe_allow_html=True
    )

with header2:
    st.markdown(
        "<div style='text-align:center; font-size:22px; "
        "font-weight:bold;'>"
        f"{datetime.now().strftime('%I:%M %p')}"
        "</div>",
        unsafe_allow_html=True
    )

with header3:
    st.markdown(
        "<div style='text-align:right; "
        "color:#39D353; font-size:20px; "
        "font-weight:bold;'>● READY</div>",
        unsafe_allow_html=True
    )

st.divider()

# ============================================================
# MAIN DASHBOARD
# ============================================================

left, center, right = st.columns(
    [1.15, 2.2, 1.15],
    gap="medium"
)

# ============================================================
# LEFT SIDE
# ============================================================

with left:

    st.markdown(
        "<h4 style='color:#BFC9D4;'>🌡 TEMPERATURE</h4>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style='font-size:36px;
                    font-weight:bold;
                    color:#2F80ED;'>
            {temperature}
            <span style='font-size:18px;'>°C</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<h4 style='color:#BFC9D4;'>⚡ CURRENT</h4>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style='font-size:36px;
                    font-weight:bold;
                    color:#F2B01E;'>
            {current}
            <span style='font-size:18px;'>A</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# CENTER SPEEDOMETER
# ============================================================

with center:

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=speed,

            number={
                "font": {
                    "size": 58,
                    "color": "white"
                }
            },

            gauge={
                "shape": "angular",

                "axis": {
                    "range": [0, 100],

                    "tickmode": "array",

                    "tickvals": [
                        0,
                        10,
                        20,
                        30,
                        40,
                        50,
                        60,
                        70,
                        80,
                        90,
                        100
                    ],

                    "ticktext": [
                        "0",
                        "",
                        "",
                        "",
                        "",
                        "50",
                        "",
                        "",
                        "",
                        "",
                        "100"
                    ],

                    "tickfont": {
                        "size": 14,
                        "color": "#E8EDF2"
                    },

                    "tickcolor": "white",

                    "tickwidth": 2
                },

                "bar": {
                    "color": "#39D353",
                    "thickness": 0.15
                },

                "bgcolor": "#111C25",

                "borderwidth": 0,

                "steps": [

                    {
                        "range": [0, 35],
                        "color": "#39D353"
                    },

                    {
                        "range": [35, 55],
                        "color": "#2878E8"
                    },

                    {
                        "range": [55, 100],
                        "color": "#26333E"
                    }

                ]
            }
        )
    )

    fig.update_layout(

        height=390,

        margin=dict(
            l=10,
            r=10,
            t=15,
            b=0
        ),

        paper_bgcolor="#061018",

        plot_bgcolor="#061018",

        font={
            "color": "white"
        },

        annotations=[

            # KM/H
            dict(
                x=0.5,
                y=0.35,

                text="km/h",

                showarrow=False,

                font=dict(
                    size=19,
                    color="#DCE3E8"
                )
            ),

            # GEAR
            dict(
                x=0.5,
                y=0.10,

                text=f"<b>{gear}</b>",

                showarrow=False,

                font=dict(
                    size=40,
                    color="#39D353"
                )
            )

        ]
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

# ============================================================
# RIGHT SIDE
# ============================================================

with right:

    st.markdown(
        "<h4 style='color:#BFC9D4;'>🌀 FAN</h4>",
        unsafe_allow_html=True
    )

    fan_color = "#39D353" if fan == "ON" else "#777777"

    st.markdown(
        f"""
        <div style='font-size:34px;
                    font-weight:bold;
                    color:{fan_color};'>
            {fan}
        </div>

        <div style='font-size:14px;
                    color:#8D9AA5;'>
            AUTO MODE
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<h4 style='color:#BFC9D4;'>🔋 VOLTAGE</h4>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style='font-size:32px;
                    font-weight:bold;
                    color:#2878E8;'>
            {voltage}
            <span style='font-size:17px;'>V</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<h4 style='color:#BFC9D4;'>🛡 STATUS</h4>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style='font-size:25px;
                    font-weight:bold;
                    color:#39D353;'>
            {status}
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# BOTTOM INFORMATION BAR
# ============================================================

st.divider()

bottom1, bottom2, bottom3, bottom4 = st.columns(
    [1, 2, 2, 1]
)

with bottom1:

    st.markdown(
        "<div style='font-size:28px;'>💡</div>",
        unsafe_allow_html=True
    )

with bottom2:

    st.markdown(
        f"""
        <div style='text-align:center;'>
            <div style='font-size:15px;
                        color:#9BA7B2;'>
                ODO
            </div>

            <div style='font-size:25px;
                        font-weight:bold;
                        color:white;'>
                {odo} km
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with bottom3:

    st.markdown(
        f"""
        <div style='text-align:center;'>
            <div style='font-size:15px;
                        color:#9BA7B2;'>
                RANGE
            </div>

            <div style='font-size:25px;
                        font-weight:bold;
                        color:white;'>
                {range_km} km
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with bottom4:

    st.markdown(
        "<div style='text-align:right; "
        "font-size:28px; color:#F2B01E;'>⚠</div>",
        unsafe_allow_html=True
    )

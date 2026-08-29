import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="EV Speedometer",
    layout="wide"
)

# ---------------- SPEED VALUE ----------------
speed = 45

# ---------------- SPEEDOMETER ----------------
fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=speed,

        number={
            "font": {
                "size": 90,
                "color": "white"
            },
            "suffix": ""
        },

        gauge={
            "shape": "angular",

            "axis": {
                "range": [0, 100],
                "tickmode": "array",
                "tickvals": [0, 50, 100],
                "ticktext": ["0", "50", "100"],
                "tickfont": {
                    "size": 20,
                    "color": "white"
                },
                "tickwidth": 3,
                "tickcolor": "white"
            },

            "bar": {
                "color": "rgba(0,0,0,0)"
            },

            "bgcolor": "#071017",

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
                    "color": "#26323D"
                }
            ],

            "threshold": {
                "line": {
                    "color": "white",
                    "width": 3
                },
                "thickness": 0.75,
                "value": speed
            }
        },

        domain={
            "x": [0, 1],
            "y": [0.12, 1]
        }
    )
)

# ---------------- LAYOUT ----------------

fig.update_layout(
    paper_bgcolor="#071017",
    plot_bgcolor="#071017",

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=0
    ),

    height=600,

    font={
        "color": "white"
    },

    annotations=[
        # km/h
        dict(
            x=0.5,
            y=0.32,
            text="km/h",
            showarrow=False,
            font=dict(
                size=28,
                color="white"
            )
        ),

        # Drive mode
        dict(
            x=0.5,
            y=0.13,
            text="<b>D</b>",
            showarrow=False,
            font=dict(
                size=55,
                color="#39D353"
            )
        )
    ]
)

# ---------------- DISPLAY ----------------

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)

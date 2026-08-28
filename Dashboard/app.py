import streamlit as st

st.set_page_config(
    page_title="EV System Dashboard",
    layout="wide"
)

# ---------------- NAVY BLUE BACKGROUND ----------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #071A2D;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TEST TITLE ----------------

st.markdown(
    """
    <h1 style="
        color: white;
        text-align: center;
        margin-top: 30px;
    ">
        EV SYSTEM
    </h1>
    """,
    unsafe_allow_html=True
)

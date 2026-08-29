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


# ---------------- ODOMETER ----------------

st.markdown("""
<style>

.odo-container {
    width: 100%;
    margin-top: 20px;
    padding: 18px 0;
    border-top: 1px solid #263746;
    border-bottom: 1px solid #263746;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 25px;
}

.odo-label {
    color: #b8c3cc;
    font-size: 20px;
    font-weight: 500;
    letter-spacing: 2px;
}

.odo-value {
    color: white;
    font-size: 28px;
    font-weight: 600;
}

.odo-unit {
    color: #b8c3cc;
    font-size: 20px;
}

</style>

<div class="odo-container">

    <div class="odo-label">
        ODO
    </div>

    <div class="odo-value">
        1256
    </div>

    <div class="odo-unit">
        km
    </div>

</div>
""", unsafe_allow_html=True)

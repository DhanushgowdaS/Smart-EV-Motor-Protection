import streamlit as st

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------
st.set_page_config(
    page_title="EV System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# NAVY BLUE BACKGROUND + BASIC STYLING
# --------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #00121c;
        color: white;
    }

    /* Remove Streamlit top spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }

    /* Bottom dashboard section */
    .bottom-box {
        border-top: 1px solid #33434d;
        margin-top: 30px;
        padding-top: 15px;
    }

    .bottom-label {
        color: #b8c1c7;
        font-size: 20px;
        text-align: center;
    }

    .bottom-value {
        color: white;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
    }

    .warning {
        color: #ffc107;
        font-size: 35px;
        text-align: center;
    }

    .light {
        color: #42d65c;
        font-size: 30px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    "<h1 style='text-align:center; color:white;'>EV SYSTEM</h1>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# ODOMETER + BOTTOM SECTION
# --------------------------------------------------
st.markdown("<div class='bottom-box'>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1, 2, 2, 1])

# Headlight
with col1:
    st.markdown(
        "<div class='light'>💡</div>",
        unsafe_allow_html=True
    )

# Odometer
with col2:
    st.markdown(
        """
        <div class='bottom-label'>ODO</div>
        <div class='bottom-value'>1256 km</div>
        """,
        unsafe_allow_html=True
    )

# Range
with col3:
    st.markdown(
        """
        <div class='bottom-label'>RANGE</div>
        <div class='bottom-value'>78 km</div>
        """,
        unsafe_allow_html=True
    )

# Warning
with col4:
    st.markdown(
        "<div class='warning'>⚠</div>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

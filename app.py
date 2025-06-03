import streamlit as st
from app_pages.dashboard import dashboard_page
from app_pages.settings import settings_page
from components.sidebar import sidebar


def main():
    st.set_page_config(
        page_title="Doc Copilot",
        page_icon="🛠️",
        layout="centered",
        initial_sidebar_state="auto",
    )
    
    st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(135deg, #23333D, #23333D) !important; /* Smooth gradient */
            border: 1px solid #253B5C !important; /* Softer border */
            color: white !important;
            font-size: 16px !important;
            padding: 10px 15px !important;
            border-radius: 8px !important; /* Rounded edges */
            transition: background 0.3s ease-in-out, transform 0.2s ease-in-out;
        }
        div.stButton > button:hover {
            background: linear-gradient(135deg, #1E3A5F, #BE232F) !important; /* Lighter on hover */
            transform: scale(1.05); /* Slight zoom effect */
        }
        </style>
        """, unsafe_allow_html=True)

    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"

    sidebar()
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    pages = {
        "dashboard": dashboard_page,
        "settings": settings_page
    }
    
    selected_page = st.session_state.page
    if selected_page in pages:
        pages[selected_page]()
    else:
        st.error(f"Page '{selected_page}' not found")

    st.markdown("</div>", unsafe_allow_html=True)
        
if __name__ == "__main__":
    main()
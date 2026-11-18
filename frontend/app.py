
import sys
from pathlib import Path

import streamlit as st
from streamlit_option_menu import option_menu


# ==================================================
# PROJECT PATH
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AEIOS | Autonomous AI System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# PRINT STYLES
# ==================================================

def apply_print_styles():
    st.markdown(
        """
        <style>
        @media print {
            @page {
                size: A4 portrait;
                margin: 15mm;
            }

            [data-testid="stSidebar"],
            [data-testid="stHeader"],
            [data-testid="stToolbar"],
            [data-testid="stStatusWidget"],
            [data-testid="stDecoration"],
            footer,
            #MainMenu {
                display: none !important;
            }

            html,
            body,
            [data-testid="stApp"],
            [data-testid="stAppViewContainer"],
            [data-testid="stMain"],
            [data-testid="stMainBlockContainer"],
            .main {
                background: #ffffff !important;
                color: #000000 !important;
                width: 100% !important;
                max-width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                box-shadow: none !important;
            }

            h1, h2, h3, h4, h5, h6,
            p, span, div, li, label,
            td, th, blockquote {
                color: #000000 !important;
                text-shadow: none !important;
            }

            h1, h2, h3, h4 {
                break-after: avoid;
                page-break-after: avoid;
            }

            table {
                width: 100% !important;
                border-collapse: collapse !important;
                font-size: 10pt !important;
            }

            th, td {
                background: #ffffff !important;
                color: #000000 !important;
                border: 1px solid #999999 !important;
                padding: 6px !important;
                overflow-wrap: anywhere !important;
            }

            thead {
                display: table-header-group;
            }

            tr, img, pre, blockquote {
                break-inside: avoid;
                page-break-inside: avoid;
            }

            pre, code {
                white-space: pre-wrap !important;
                overflow-wrap: anywhere !important;
            }

            a {
                color: #000000 !important;
                text-decoration: none !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


apply_print_styles()


# ==================================================
# BACKEND SERVICE
# ==================================================

@st.cache_resource
def get_service():
    from backend.service import AEIOSService

    return AEIOSService()


try:
    service = get_service()
    st.session_state["aeios_service"] = service

except Exception as exc:
    st.error("Unable to initialize the AEIOS backend.")
    st.exception(exc)
    st.stop()


# ==================================================
# PAGE IMPORTS
# ==================================================

from frontend.views.dashboard import dashboard_page
from frontend.views.chat import chat_page
from frontend.views.memory import memory_page
from frontend.views.analytics import analytics_page
from frontend.views.explainability import explainability_page
from frontend.views.settings import settings_page


# ==================================================
# SIDEBAR BRANDING AND NAVIGATION
# ==================================================

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 4px 20px 4px;">
            <h2>🧠 AEIOS</h2>
            <p style="color: #9CA3AF; font-size: 14px;">
                Autonomous Explainable Intelligent
                Orchestration System
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    selected_page = option_menu(
        menu_title="Navigation",
        options=[
            "Dashboard",
            "Chat",
            "Memory",
            "Analytics",
            "Decision Trace",
            "Settings",
        ],
        icons=[
            "speedometer2",
            "chat-dots",
            "database",
            "bar-chart-line",
            "journal-text",
            "gear",
        ],
        menu_icon="display",
        default_index=0,
        orientation="vertical",
    )

    st.divider()

    st.caption("AEIOS • Multi-Agent AI Project")


# ==================================================
# PAGE ROUTING
# ==================================================

if selected_page == "Dashboard":
    dashboard_page()

elif selected_page == "Chat":
    chat_page(service)

elif selected_page == "Memory":
    memory_page(service)

elif selected_page == "Analytics":
    analytics_page(service)

elif selected_page == "Decision Trace":
    # FIX: Match the exact label used in the navigation menu.
    explainability_page(service)

elif selected_page == "Settings":
    settings_page()

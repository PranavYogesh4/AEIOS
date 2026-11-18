
import os
import streamlit as st


def _get_config(name, default=""):
    """Read configuration safely from environment variables or Streamlit secrets."""
    value = os.getenv(name)

    if value:
        return value

    try:
        value = st.secrets.get(name, default)
        return value if value else default
    except Exception:
        return default


def settings_page():
    st.title("⚙️ AEIOS Settings")
    st.caption("Configuration, system status, and preferences")

    # API configuration
    st.subheader("🔐 API Configuration")

    api_key = _get_config("GROQ_API_KEY")
    model = _get_config("GROQ_MODEL", "openai/gpt-oss-120b")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Groq API Key**")
        if api_key:
            st.success("API key configured")
        else:
            st.error("API key not found")

    with col2:
        st.markdown("**Configured Model**")
        st.code(model, language=None)

    st.caption(
        "The model shown here comes from GROQ_MODEL or the default above. "
        "Individual agents may use their own model configuration."
    )

    st.divider()

    # Execution information
    st.subheader("⚙️ Execution")

    st.info(
        "AEIOS execution settings, including retries and agent selection, "
        "are currently managed by the existing backend configuration."
    )

    st.divider()

    # Memory information
    st.subheader("🧠 Memory")

    st.write(
        "AEIOS memory is managed by the existing MemoryManager. "
        "Memory controls will be added here when they are connected "
        "to the backend."
    )

    st.divider()

    # Diagnostics
    st.subheader("🩺 Configuration Diagnostics")

    with st.expander("View configuration status"):
        st.write(
            f"**Groq API key configured:** "
            f"{'Yes' if api_key else 'No'}"
        )
        st.write(f"**Model configuration:** {model}")
        st.write(f"**Python version:** {os.sys.version.split()[0]}")

        if not api_key:
            st.warning(
                "Set GROQ_API_KEY in your environment or Streamlit secrets "
                "before making Groq API requests."
            )

    st.divider()
    st.caption("AEIOS — Autonomous Explainable Intelligent Orchestration System")

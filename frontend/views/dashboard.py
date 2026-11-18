
import streamlit as st
from datetime import datetime


def dashboard_page():
    st.title("🧠 AEIOS Dashboard")
    st.caption(
        "Autonomous Explainable Intelligent Orchestration System"
    )

    # System status
    st.success("AEIOS Dashboard Loaded Successfully")

    st.divider()

    # Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Configured Agents", "10")

    with col2:
        memory_count = "--"
        service = st.session_state.get("aeios_service")

        if service:
            try:
                memory_manager = service.orchestrator.memory_manager
                if hasattr(memory_manager, "get_all_memories"):
                    memories = memory_manager.get_all_memories()
                    memory_count = len(memories)
            except Exception:
                pass

        st.metric("Memory Records", memory_count)

    with col3:
        last_result = st.session_state.get("aeios_last_result")
        confidence = "--"

        if isinstance(last_result, dict):
            score = last_result.get("confidence_score")
            if score is not None:
                confidence = (
                    f"{score}%"
                    if isinstance(score, (int, float))
                    else str(score)
                )

        st.metric("Last Confidence Score", confidence)

    st.divider()

    # Latest execution
    st.subheader("📊 Latest Execution")

    last_result = st.session_state.get("aeios_last_result")

    if isinstance(last_result, dict):
        st.write("**Latest Query**")
        st.write(last_result.get("query", "No query recorded"))

        st.write("**Response**")
        st.write(last_result.get("response", "No response recorded"))

        execution_time = last_result.get("execution_time")
        if execution_time is not None:
            st.caption(f"Execution time: {execution_time} seconds")

        selected_agents = last_result.get("selected_agents", [])
        if selected_agents:
            st.write("**Agents involved**")
            st.write(", ".join(map(str, selected_agents)))

    else:
        st.info(
            "No completed execution is available in this session yet. "
            "Submit a query in the Chat page to populate this section."
        )

    st.divider()

    # Navigation guidance
    st.subheader("🚀 Explore AEIOS")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "**💬 Chat**\n\n"
            "Submit a task and review the system's response."
        )
        st.markdown(
            "**🧠 Memory Explorer**\n\n"
            "Inspect stored memories when available."
        )

    with col2:
        st.markdown(
            "**🔍 Explainability**\n\n"
            "Review available decision traces and confidence details."
        )
        st.markdown(
            "**📈 Analytics**\n\n"
            "Explore execution statistics when recorded."
        )

    st.divider()
    st.caption(
        f"AEIOS • Dashboard viewed at "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

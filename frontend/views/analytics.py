
import streamlit as st


def analytics_page(service):
    st.title("📊 AEIOS Analytics Dashboard")
    st.caption("Execution statistics, agent usage, and recent queries")

    # Load analytics safely
    try:
        stats = service.get_analytics() or {}
    except Exception as exc:
        st.error("Unable to load analytics from the AEIOS backend.")
        st.caption(f"Details: {exc}")
        return

    # Read metrics with defaults
    total_queries = stats.get("total_queries", 0)
    avg_execution_time = stats.get("average_execution_time", 0)
    avg_confidence = stats.get("average_confidence", 0)
    memory_hit_rate = stats.get("memory_hit_rate", 0)

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Queries", total_queries)
    col2.metric("Avg Execution Time", f"{avg_execution_time} sec")
    col3.metric("Avg Confidence", f"{avg_confidence}%")
    col4.metric("Memory Hit Rate", f"{memory_hit_rate}%")

    st.divider()

    # Agent usage
    st.subheader("🤖 Agent Usage")

    agent_usage = stats.get("agent_usage", {})

    if isinstance(agent_usage, dict) and agent_usage:
        st.bar_chart(agent_usage)
    elif isinstance(agent_usage, (list, tuple)) and agent_usage:
        st.bar_chart(agent_usage)
    else:
        st.info("No agent usage data recorded yet.")

    st.divider()

    # Recent queries
    st.subheader("📝 Recent Queries")

    query_history = stats.get("query_history", [])

    if not query_history:
        st.info("No queries executed yet.")
    else:
        for index, item in enumerate(query_history):
            if not isinstance(item, dict):
                continue

            query = item.get("query", "Query text unavailable")
            query_time = item.get("time", "Time unavailable")

            with st.expander(
                f"Query {index + 1}: {str(query)[:80]}"
            ):
                st.write("**Query**")
                st.write(query)
                st.caption(f"🕒 {query_time}")

    st.divider()

    # Raw statistics for troubleshooting
    with st.expander("🔍 View raw analytics data"):
        st.json(stats)

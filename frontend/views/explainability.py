
import streamlit as st


def explainability_page(service=None):
    """Display AEIOS execution metadata and decision trace."""

    st.title("🔎 Decision Trace")
    st.write(
        "Understand which agents participated, how AEIOS evaluated "
        "the response, and what execution information supports the result."
    )

    st.divider()

    # Retrieve the latest result saved by the Chat page.
    result = st.session_state.get("aeios_last_result")

    if not result:
        st.info(
            "No execution details are available yet. "
            "Submit a query in the Chat page first."
        )
        return

    if not isinstance(result, dict):
        st.error(
            "The saved execution result is not in the expected format. "
            "Check how the Chat page stores the result."
        )
        return

    # --------------------------------------------------
    # 1. Execution Overview
    # --------------------------------------------------

    st.subheader("🧠 Execution Overview")

    col1, col2, col3 = st.columns(3)

    confidence = result.get("confidence_score")
    execution_time = result.get("execution_time")
    memory_used = result.get("memory_used")

    with col1:
        if confidence is not None:
            st.metric("Displayed Confidence", f"{confidence}/100")
        else:
            st.metric("Displayed Confidence", "N/A")

    with col2:
        if execution_time is not None:
            st.metric("Execution Time", f"{execution_time} s")
        else:
            st.metric("Execution Time", "N/A")

    with col3:
        if memory_used is True:
            st.metric("Memory Context", "Used")
        elif memory_used is False:
            st.metric("Memory Context", "Not used")
        else:
            st.metric("Memory Context", "Unknown")

    st.caption(
        "The displayed confidence score is produced by the configured "
        "Confidence Agent. It is not necessarily a calibrated probability "
        "that the response is correct."
    )

    st.divider()

    # --------------------------------------------------
    # 2. Participating Agents
    # --------------------------------------------------

    st.subheader("🤖 Participating Agents")

    agents = result.get("selected_agents", [])

    if isinstance(agents, str):
        agents = [agents]

    if agents:
        for agent in agents:
            st.write(f"✅ {agent}")
    else:
        st.info(
            "No selected-agent information was saved for this execution."
        )

    st.divider()

    # --------------------------------------------------
    # 3. Original Query
    # --------------------------------------------------

    with st.expander("🔎 View Original Query"):
        st.write(result.get("query") or "No query was recorded.")

    # --------------------------------------------------
    # 4. Decision Trace
    # --------------------------------------------------

    st.subheader("🧭 Decision Trace")

    trace = result.get("decision_trace")

    if trace:
        if isinstance(trace, dict):
            for key, value in trace.items():
                st.markdown(f"**{key.replace('_', ' ').title()}**")

                if isinstance(value, (dict, list, tuple)):
                    st.json(value)
                else:
                    st.write(value)

        elif isinstance(trace, (list, tuple)):
            for index, item in enumerate(trace, start=1):
                st.markdown(f"**Step {index}**")

                if isinstance(item, (dict, list, tuple)):
                    st.json(item)
                else:
                    st.write(item)

        else:
            st.markdown(str(trace))
    else:
        st.info(
            "The Explainability Agent did not provide a detailed trace "
            "in the saved result."
        )

    st.divider()

    # --------------------------------------------------
    # 5. Self-Evaluation
    # --------------------------------------------------

    st.subheader("📝 Self-Evaluation")

    evaluation = result.get("evaluation")

    if evaluation:
        if isinstance(evaluation, dict):
            for key, value in evaluation.items():
                st.markdown(f"**{key.replace('_', ' ').title()}**")
                st.write(value)
        else:
            st.markdown(str(evaluation))
    else:
        st.info("No self-evaluation details were saved.")

    # --------------------------------------------------
    # 6. Recommendation
    # --------------------------------------------------

    st.subheader("💡 Evaluation Recommendation")

    recommendation = result.get("recommendation")

    if recommendation:
        recommendation = str(recommendation).upper().strip()

        if recommendation == "IMPROVE":
            st.warning("The evaluation recommended improvement.")
        elif recommendation == "KEEP":
            st.success("The evaluation recommended keeping the response.")
        else:
            st.write(recommendation)
    else:
        st.info("No evaluation recommendation was saved.")

    st.divider()

    # --------------------------------------------------
    # 7. Response Improvement
    # --------------------------------------------------

    st.subheader("🔄 Response Improvement")

    revision_performed = result.get("revision_performed")

    if revision_performed is True:
        st.success(
            "A response revision was recorded by the orchestrator."
        )
    elif revision_performed is False:
        st.info(
            "The orchestrator recorded that no revision was recommended."
        )
    else:
        st.info(
            "Revision status is unavailable in the saved execution result."
        )

    # --------------------------------------------------
    # 8. Confidence Details
    # --------------------------------------------------

    st.subheader("📊 Confidence Explanation")

    confidence_details = result.get("confidence_details")

    if confidence_details:
        if isinstance(confidence_details, dict):
            for key, value in confidence_details.items():
                st.markdown(f"**{key.replace('_', ' ').title()}**")

                if isinstance(value, (dict, list, tuple)):
                    st.json(value)
                else:
                    st.write(value)
        else:
            st.markdown(str(confidence_details))
    else:
        st.info("No detailed confidence information was saved.")

    # --------------------------------------------------
    # 9. Execution Limitations
    # --------------------------------------------------

    st.divider()
    st.subheader("ℹ️ Execution Limitations")

    st.write(
        "This page displays information returned by AEIOS and saved by "
        "the Chat page. Missing metadata may mean it was not returned "
        "or saved; it does not automatically mean an agent failed."
    )

    st.caption(
        "Decision Trace explains the recorded workflow. It does not "
        "independently verify the correctness of the generated report "
        "or prove that every listed agent completed successfully."
    )

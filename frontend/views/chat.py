
import streamlit as st
import time


def _looks_incomplete(response):
    """Flag likely truncated output without claiming certainty."""
    text = str(response or "").strip()

    if not text:
        return True, "The response is empty."

    # Check common signs of a generation that stopped mid-sentence.
    if text.endswith(("...", "…")):
        return True, "The response ends with an ellipsis."

    last_line = text.splitlines()[-1].strip()

    if last_line.endswith((":", "-", "—", "and", "or", "with")):
        return True, "The response may have stopped mid-section."

    # An unfinished Markdown heading may indicate a cut-off report.
    if last_line.startswith("#") and len(last_line.split()) < 3:
        return True, "The response ends at a possibly unfinished heading."

    return False, ""


def chat_page(service):
    st.title("💬 AEIOS Chat Assistant")
    st.write(
        "Interact with the Autonomous Explainable Intelligent "
        "Orchestration System."
    )

    # Keep the service available to other pages.
    st.session_state["aeios_service"] = service

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask AEIOS...")

    if not prompt:
        return

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        progress_placeholder = st.empty()
        response_placeholder = st.empty()

        try:
            job_id = service.start_processing(prompt)

            # Poll until the backend reports a terminal status.
            while True:
                progress = service.get_progress()

                progress_text = "## ⚙️ AEIOS Live Execution\n\n"

                if progress:
                    for step in progress:
                        if isinstance(step, dict):
                            step_name = step.get(
                                "step", "Execution step"
                            )
                            progress_text += (
                                f"🟢 {step_name}\n\n"
                            )
                else:
                    progress_text += (
                        "Waiting for execution updates...\n"
                    )

                progress_placeholder.markdown(progress_text)

                status = service.get_status(job_id)

                if status == "completed":
                    break

                if status == "failed":
                    error = None
                    manager = getattr(
                        service, "execution_manager", None
                    )

                    if manager and hasattr(manager, "get_error"):
                        error = manager.get_error(job_id)

                    progress_placeholder.error(
                        "❌ AEIOS execution failed."
                    )

                    if error:
                        st.code(str(error))

                    return

                if status == "not_found":
                    progress_placeholder.error(
                        "❌ Execution job was not found."
                    )
                    return

                time.sleep(0.5)

            # Retrieve the result only after completion.
            result = service.get_result(job_id)

            if result is None:
                progress_placeholder.warning(
                    "⚠️ The job completed but returned no result."
                )
                return

            if isinstance(result, dict):
                saved_result = dict(result)
                response = str(
                    saved_result.get("response") or ""
                ).strip()

                saved_result.setdefault("query", prompt)
                st.session_state["aeios_last_result"] = saved_result
            else:
                response = str(result).strip()
                st.session_state["aeios_last_result"] = {
                    "query": prompt,
                    "response": response,
                    "execution_time": None,
                    "confidence_score": None,
                    "memory_used": False,
                    "selected_agents": [],
                }

            if not response:
                progress_placeholder.warning(
                    "⚠️ AEIOS returned an empty response."
                )
                return

            # Render the entire response returned by the backend.
            response_placeholder.markdown(response)

            incomplete, reason = _looks_incomplete(response)

            if incomplete:
                progress_placeholder.warning(
                    f"⚠️ The job completed, but the response may "
                    f"be incomplete. {reason}"
                )
            else:
                progress_placeholder.success(
                    "✅ Execution Completed"
                )

            # Preserve the exact returned text in chat history.
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response,
                }
            )

        except Exception as error:
            progress_placeholder.error(
                "❌ An unexpected error occurred while processing "
                "your request."
            )
            st.code(str(error))

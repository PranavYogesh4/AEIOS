
import streamlit as st
from backend.service import AEIOSService


def memory_page(service=None):
    st.title("🧠 Memory Explorer")
    st.caption("Inspect and manage memories stored by AEIOS.")

    # Reuse the shared service when provided by app.py.
    if service is None:
        service = AEIOSService()

    memory_manager = service.orchestrator.memory_manager

    # Fetch current memories.
    try:
        memories = memory_manager.get_all_memories()
    except Exception as exc:
        st.error(f"Could not load memories: {exc}")
        return

    # Summary metrics.
    col1, col2 = st.columns(2)
    col1.metric("Total Memories", len(memories))
    col2.metric(
        "Collection Status",
        "Empty" if not memories else "Active"
    )

    st.divider()

    # Search.
    st.subheader("🔎 Search Memories")
    search_query = st.text_input(
        "Search by meaning",
        placeholder="e.g. Explain my previous research query"
    )

    if search_query.strip():
        try:
            displayed_memories = memory_manager.search_memories(
                search_query,
                limit=20
            )
        except Exception as exc:
            st.error(f"Memory search failed: {exc}")
            return
    else:
        displayed_memories = memories

    # Delete-all controls.
    st.subheader("📚 Stored Memories")

    if memories:
        if st.button("🗑️ Clear All Memories", type="secondary"):
            st.session_state["confirm_clear_memories"] = True

        if st.session_state.get("confirm_clear_memories", False):
            st.warning(
                "This permanently deletes every memory in the AEIOS collection."
            )
            confirm_col, cancel_col = st.columns(2)

            if confirm_col.button(
                "Yes, clear all",
                type="primary"
            ):
                try:
                    memory_manager.clear_memories()
                    st.session_state["confirm_clear_memories"] = False
                    st.success("All memories cleared.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not clear memories: {exc}")

            if cancel_col.button("Cancel"):
                st.session_state["confirm_clear_memories"] = False
                st.rerun()

    if not displayed_memories:
        if search_query.strip():
            st.info("No memories matched your search.")
        else:
            st.info(
                "No memories have been stored yet. Chat with AEIOS to "
                "populate this page, provided memory storage is enabled."
            )
        return

    st.write(f"Showing {len(displayed_memories)} memory item(s).")

    for index, memory in enumerate(displayed_memories):
        metadata = memory.get("metadata") or {}
        memory_id = memory.get("id", "")
        document = memory.get("document") or ""

        with st.expander(
            f"Memory {index + 1} — "
            f"{metadata.get('timestamp', 'Timestamp unavailable')}"
        ):
            st.markdown("**Memory content**")
            st.text(document)

            if metadata.get("user_input"):
                st.markdown("**Original query**")
                st.write(metadata["user_input"])

            st.caption(f"Memory ID: {memory_id}")

            confirm_key = f"confirm_delete_{memory_id}"

            if st.button(
                "Delete this memory",
                key=f"delete_{memory_id}"
            ):
                st.session_state[confirm_key] = True

            if st.session_state.get(confirm_key, False):
                st.warning("Delete this memory permanently?")
                yes_col, no_col = st.columns(2)

                if yes_col.button(
                    "Confirm delete",
                    key=f"confirm_yes_{memory_id}"
                ):
                    try:
                        memory_manager.delete_memory(memory_id)
                        st.session_state.pop(confirm_key, None)
                        st.success("Memory deleted.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not delete memory: {exc}")

                if no_col.button(
                    "Cancel",
                    key=f"confirm_no_{memory_id}"
                ):
                    st.session_state.pop(confirm_key, None)
                    st.rerun()

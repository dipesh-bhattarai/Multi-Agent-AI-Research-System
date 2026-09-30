import time
import streamlit as st

from pipeline import run_research_pipeline

# ---------------------------------------------------------------- page setup
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)

STEPS = {
    1: ("🔍", "Search agent", "Finding recent, reliable sources"),
    2: ("📖", "Reader agent", "Scraping the most relevant page"),
    3: ("✍️", "Writer", "Drafting the report"),
    4: ("🧐", "Critic", "Reviewing the report"),
}

EXAMPLES = [
    "AI applications in precision agriculture",
    "Post-quantum cryptography",
    "Low-cost IoT for smallholder farms",
]

# ------------------------------------------------------------ session state
if "result" not in st.session_state:
    st.session_state.result = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {topic, result, seconds}
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""


def set_example(text: str):
    st.session_state.topic_input = text


# ------------------------------------------------------------------ sidebar
with st.sidebar:
    st.title("🔎 Research Agents")
    st.caption("Search → Read → Write → Critique")

    st.markdown("**Pipeline**")
    for _, (icon, name, desc) in STEPS.items():
        st.markdown(f"{icon} **{name}** — {desc}")

    st.divider()
    st.markdown("**Try an example**")
    for ex in EXAMPLES:
        st.button(ex, key=f"ex_{ex}", on_click=set_example, args=(ex,), use_container_width=True)

    if st.session_state.history:
        st.divider()
        st.markdown("**Past runs (this session)**")
        for i, item in enumerate(reversed(st.session_state.history)):
            if st.button(f"↩ {item['topic'][:40]}", key=f"hist_{i}", use_container_width=True):
                st.session_state.result = item["result"]
                st.session_state.topic = item["topic"]
                st.rerun()
        if st.button("Clear history", use_container_width=True):
            st.session_state.history = []
            st.session_state.result = None
            st.rerun()

# --------------------------------------------------------------------- main
st.title("Multi-Agent Research System")
st.caption("Enter a topic and four agents will research, write and review a report for you.")

with st.form("research_form", clear_on_submit=False):
    topic = st.text_input(
        "Research topic",
        key="topic_input",
        placeholder="e.g. AI applications in precision agriculture",
    )
    submitted = st.form_submit_button("Run research", type="primary")

# ------------------------------------------------------------ run pipeline
if submitted:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        st.session_state.result = None
        progress = st.progress(0.0, text="Starting…")
        checklist = st.empty()
        status = {i: "⏳" for i in STEPS}  # ⏳ waiting, 🔄 running, ✅ done

        def render_checklist():
            lines = []
            for i, (icon, name, desc) in STEPS.items():
                lines.append(f"{status[i]} {icon} **{name}** — {desc}")
            checklist.markdown("\n\n".join(lines))

        def on_step(idx, label, output=None):
            if output is None:
                status[idx] = "🔄"
                progress.progress((idx - 1) / len(STEPS), text=f"Step {idx}/4 — {label} is working…")
            else:
                status[idx] = "✅"
                progress.progress(idx / len(STEPS), text=f"Step {idx}/4 — {label} finished")
            render_checklist()

        render_checklist()
        start = time.time()
        try:
            result = run_research_pipeline(topic.strip(), on_step=on_step)
            elapsed = time.time() - start
            st.session_state.result = result
            st.session_state.topic = topic.strip()
            st.session_state.history.append(
                {"topic": topic.strip(), "result": result, "seconds": elapsed}
            )
            progress.progress(1.0, text=f"Done in {elapsed:.0f}s")
        except Exception as e:
            progress.empty()
            st.error(f"Pipeline failed: {e}")
            with st.expander("Details"):
                st.exception(e)

# ------------------------------------------------------------------ results
result = st.session_state.result
if result:
    st.divider()
    st.subheader(f"Results: {st.session_state.topic}")

    report = str(result.get("report", ""))
    feedback = str(result.get("feedback", ""))

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Report", "🧐 Critic feedback", "🔍 Search results", "📖 Scraped content"]
    )

    with tab_report:
        st.markdown(report)
        st.download_button(
            "⬇ Download report (.md)",
            data=report,
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        st.markdown(feedback)

    with tab_search:
        st.markdown(str(result.get("search_results", "")))

    with tab_scraped:
        st.markdown(str(result.get("scraped_content", "")))
import streamlit as st
from dotenv import load_dotenv
from states.agent_state import AgentState
from tools.pdf_reader import read_pdf
from graph import build_graph
import tempfile
import os

load_dotenv()

# ─── Page Config ───────────────────────────────────────
st.set_page_config(
    page_title="AI Job Application Agent",
    page_icon="💼",
    layout="wide"
)

# ─── Header ────────────────────────────────────────────
st.title("💼 AI Job Application Agent")
st.markdown(
    "Paste a job description, upload your resume "
    "and let AI do the hard work!"
)
st.divider()

# ─── Input Section ─────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        label="Paste the job description here",
        height=300,
        placeholder="Copy and paste the full job description here..."
    )

with col2:
    st.subheader("📄 Your Resume")
    uploaded_file = st.file_uploader(
        label="Upload your resume PDF",
        type=["pdf"]
    )
    if uploaded_file:
        st.success(f"✅ Resume uploaded: {uploaded_file.name}")

st.divider()

# ─── Generate Button ───────────────────────────────────
generate_btn = st.button(
    "🚀 Generate Application",
    type="primary",
    use_container_width=True
)

# ─── Run Graph ─────────────────────────────────────────
# ✅ this block only runs when generate is clicked
if generate_btn:

    # validate inputs
    if not job_description.strip():
        st.error("❌ Please paste a job description!")
        st.stop()

    if not uploaded_file:
        st.error("❌ Please upload your resume PDF!")
        st.stop()

    # save uploaded PDF to temp file
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".pdf"
    ) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # read resume text from PDF
    try:
        resume_text = read_pdf(tmp_path)
    except Exception as e:
        st.error(f"❌ Could not read PDF: {e}")
        st.stop()
    finally:
        os.unlink(tmp_path)

    # show progress
    st.divider()
    st.subheader("⚙️ Agent Progress")

    progress_bar = st.progress(0)
    status = st.status("🚀 Starting agents...", expanded=True)

    with status:
        steps = [
            "🔍 Analyzing Job Description...",
            "📄 Analyzing Resume...",
            "🌐 Researching Market & Company...",
            "🔍 Analyzing Match...",
            "✍️ Writing Cover Letter...",
            "📝 Generating Resume Suggestions...",
            "✅ Running Quality Check...",
        ]
        for i, step in enumerate(steps):
            st.write(step)
            progress_bar.progress((i + 1) * 14)

    # build initial state
    initial_state: AgentState = {
        "job_description": job_description,
        "resume_text":     resume_text,
        "jd_analysis":     None,
        "resume_analysis": None,
        "market_research": None,
        "match_analysis":  None,
        "cover_letter":    None,
        "resume_suggestions": None,
        "quality_approved": None,
        "final_output":    None,
        "error":           None,
    }

    # run the graph
    with st.spinner("🤖 Agents are working... this may take a minute!"):
        try:
            graph       = build_graph()
            final_state = graph.invoke(initial_state)

            # ✅ save to session state so results persist
            st.session_state["final_state"] = final_state

            progress_bar.progress(100)
            status.update(
                label="✅ All agents done!",
                state="complete"
            )
        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
            st.stop()

# ─── Show Results ──────────────────────────────────────
# ✅ this block is OUTSIDE if generate_btn
# ✅ so it persists even after download button click
if "final_state" in st.session_state:
    final_state = st.session_state["final_state"]

    st.success("🎉 Your application package is ready!")
    st.divider()

    # ─── Results in Tabs ───────────────────────────────
    st.subheader("📊 Your Results")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Match Analysis",
        "✍️ Cover Letter",
        "📝 Resume Tips",
        "🔍 JD Analysis",
        "✅ Quality Report"
    ])

    with tab1:
        st.subheader("🎯 Match Analysis")
        st.markdown(final_state["match_analysis"])

        # extract and show match score visually
        match_text = final_state["match_analysis"]
        if "Match Score:" in match_text:
            for line in match_text.split("\n"):
                if "Match Score:" in line:
                    try:
                        score = int(
                            line.split(":")[1]
                            .strip()
                            .split("/")[0]
                            .strip()
                        )
                        st.divider()
                        st.metric(
                            label="Overall Match Score",
                            value=f"{score}/100"
                        )
                        st.progress(score)
                    except:
                        pass

    with tab2:
        st.subheader("✍️ Cover Letter")
        st.markdown(final_state["cover_letter"])
        st.divider()
        st.download_button(
            label="📋 Download Cover Letter",
            data=final_state["cover_letter"],
            file_name="cover_letter.txt",
            mime="text/plain",
            use_container_width=True
        )

    with tab3:
        st.subheader("📝 Resume Improvement Tips")
        st.markdown(final_state["resume_suggestions"])

    with tab4:
        st.subheader("🔍 Job Description Analysis")
        st.markdown(final_state["jd_analysis"])

    with tab5:
        st.subheader("✅ Quality Report")
        approved = final_state["quality_approved"]
        if approved:
            st.success("✅ All outputs passed quality check!")
        else:
            st.warning("⚠️ Some outputs may need revision")
        st.markdown(final_state["final_output"])
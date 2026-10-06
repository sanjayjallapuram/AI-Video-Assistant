import streamlit as st
from dotenv import load_dotenv

from main import run_pipeline
from core.rag_engine import ask_question

load_dotenv()


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

    /* =========================
       GLOBAL APP
       ========================= */

    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }

    .main {
        background-color: #000000;
    }

    /* =========================
       TEXT
       ========================= */

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    p, label, span {
        color: #FFFFFF !important;
    }

    [data-testid="stMarkdownContainer"] {
        color: #FFFFFF !important;
    }

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] strong {
        color: #FFFFFF !important;
    }

    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background-color: #000000;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* =========================
       INPUT BOXES
       ========================= */

    input,
    textarea {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #AAAAAA !important;
    }

    /* =========================
       SELECT BOX
       ========================= */

    div[data-baseweb="select"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
        background-color: #000000 !important;
    }

    /* Dropdown menu */
    ul[role="listbox"] {
        background-color: #000000 !important;
    }

    li[role="option"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    li[role="option"]:hover {
        background-color: #222222 !important;
    }

    /* =========================
       FILE UPLOADER
       ========================= */

    section[data-testid="stFileUploader"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    section[data-testid="stFileUploader"] * {
        color: #FFFFFF !important;
    }

    /* =========================
       BUTTONS
       ========================= */

    button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
    }

    button:hover {
        background-color: #222222 !important;
        color: #FFFFFF !important;
    }

    /* =========================
       TABS
       ========================= */

    button[data-baseweb="tab"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FFFFFF !important;
    }

    /* =========================
       METRICS
       ========================= */

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #FFFFFF !important;
    }

    /* =========================
       CHAT
       ========================= */

    [data-testid="stChatMessage"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    [data-testid="stChatMessage"] * {
        color: #FFFFFF !important;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        background-color: #000000 !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    /* =========================
       ALERT / INFO BOXES
       ========================= */

    [data-testid="stAlert"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🎥 AI Video Assistant")

    st.markdown("---")

    st.markdown("### 📥 Video Source")

    source_type = st.radio(
        "Choose input",
        ["YouTube URL", "Local File"],
        horizontal=False
    )

    source = ""

    if source_type == "YouTube URL":

        source = st.text_input(
            "YouTube URL",
            placeholder="https://www.youtube.com/watch?v=..."
        )

    else:

        uploaded_file = st.file_uploader(
            "Upload audio/video",
            type=[
                "mp3",
                "wav",
                "m4a",
                "mp4",
                "webm",
                "mov"
            ]
        )

        if uploaded_file:

            import os

            upload_dir = "downloads"

            os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(
                upload_dir,
                uploaded_file.name
            )

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            source = file_path

            st.success("File uploaded successfully")


    st.markdown("### 🌐 Language")

    language = st.selectbox(
        "Select language",
        ["english", "hinglish"]
    )


    st.markdown("---")


    process_button = st.button(
        "🚀 Analyze Video",
        use_container_width=True,
        type="primary"
    )


    if st.session_state.result:

        st.markdown("---")

        if st.button(
            "🗑️ Clear Results",
            use_container_width=True
        ):
            st.session_state.result = None
            st.session_state.chat_history = []

            st.rerun()


    st.markdown("---")

    st.caption(
        "AI Video Assistant • Transcription • Summarization • RAG"
    )


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎥 AI Video Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Turn videos into searchable knowledge with AI-powered transcription, '
    'summaries and RAG chat.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# PROCESS VIDEO
# --------------------------------------------------

if process_button:

    if not source:

        st.error(
            "Please provide a YouTube URL or upload a file."
        )

    else:

        st.session_state.chat_history = []

        progress = st.status(
            "🚀 Processing video...",
            expanded=True
        )

        try:

            progress.write("🎵 Extracting audio...")

            result = run_pipeline(
                source,
                language
            )

            progress.write("✅ Audio processed")

            progress.write("📝 Transcription completed")

            progress.write("🧠 Generating summary")

            progress.write("📌 Extracting action items")

            progress.write("🔑 Extracting key decisions")

            progress.write("❓ Extracting open questions")

            progress.write("🔎 Building RAG knowledge base")

            st.session_state.result = result

            progress.update(
                label="✅ Video analysis completed!",
                state="complete",
                expanded=False
            )

            st.rerun()

        except Exception as e:

            progress.update(
                label="❌ Processing failed",
                state="error"
            )

            st.exception(e)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

result = st.session_state.result


if result:

    # Title
    st.markdown(
        f"## 📌 {result['title']}"
    )

    st.markdown("---")


    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    transcript_words = len(
        result["transcript"].split()
    )

    summary_words = len(
        result["summary"].split()
    )

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">
                    {transcript_words:,}
                </div>
                <div class="metric-label">
                    Transcript Words
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">
                    {summary_words:,}
                </div>
                <div class="metric-label">
                    Summary Words
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">
                    ✓
                </div>
                <div class="metric-label">
                    AI Analysis
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">
                    RAG
                </div>
                <div class="metric-label">
                    Knowledge Base
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("")


    # --------------------------------------------------
    # TABS
    # --------------------------------------------------

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Summary",
        "✅ Action Items",
        "🔑 Decisions",
        "❓ Open Questions",
        "📝 Transcript",
        "💬 Ask Video"
    ])


    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    with tab1:

        st.markdown("### 📋 Meeting Summary")

        st.markdown(result["summary"])


    # --------------------------------------------------
    # ACTION ITEMS
    # --------------------------------------------------

    with tab2:

        st.markdown("### ✅ Action Items")

        st.markdown(result["action_items"])


    # --------------------------------------------------
    # DECISIONS
    # --------------------------------------------------

    with tab3:

        st.markdown("### 🔑 Key Decisions")

        st.markdown(result["key_decisions"])


    # --------------------------------------------------
    # QUESTIONS
    # --------------------------------------------------

    with tab4:

        st.markdown("### ❓ Open Questions")

        st.markdown(result["open_questions"])


    # --------------------------------------------------
    # TRANSCRIPT
    # --------------------------------------------------

    with tab5:

        st.markdown("### 📝 Full Transcript")

        st.text_area(
            "Transcript",
            result["transcript"],
            height=600,
            label_visibility="collapsed"
        )


    # --------------------------------------------------
    # RAG CHAT
    # --------------------------------------------------

    with tab6:

        st.markdown(
            '<div class="chat-header">💬 Chat with your video</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Ask questions about the video, meeting or discussion."
        )


        # Display previous messages

        for message in st.session_state.chat_history:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])


        question = st.chat_input(
            "Ask something about the video..."
        )


        if question:

            # User message

            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user"):

                st.markdown(question)


            # Assistant response

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    try:

                        answer = ask_question(
                            result["rag_chain"],
                            question
                        )

                        st.markdown(answer)

                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": answer
                        })

                    except Exception as e:

                        st.error(
                            f"Unable to answer question: {e}"
                        )
import streamlit as st
import tempfile
import os
from stt import load_model, transcribe
from agent import run_agent

st.set_page_config(
    page_title="Chronos AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;400;600;700&family=Cormorant+Garamond:wght@300;400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: #ffffff !important;
    color: #111111 !important;
    font-family: 'Josefin Sans', sans-serif !important;
}

.block-container {
    padding: 0 5rem !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}

#MainMenu, footer, .stDeployButton, header { display: none !important; }

/* ── HERO ── */
.hero {
    position: relative;
    width: 100vw;
    margin-left: calc(-5rem);
    min-height: 100vh;
    background: #ffffff;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.hero-bg {
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 50% 40%, rgba(186,225,255,0.4) 0%, transparent 70%),
        radial-gradient(ellipse 40% 40% at 80% 20%, rgba(200,235,255,0.25) 0%, transparent 60%),
        radial-gradient(ellipse 30% 30% at 20% 80%, rgba(180,220,255,0.2) 0%, transparent 60%);
    pointer-events: none;
}

.hero-glass {
    position: relative;
    z-index: 2;
    background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(220,240,255,0.65) 50%, rgba(255,255,255,0.8) 100%);
    backdrop-filter: blur(32px);
    -webkit-backdrop-filter: blur(32px);
    border: 1px solid rgba(180,220,255,0.5);
    border-radius: 32px;
    padding: 5rem 8rem;
    text-align: center;
    box-shadow: 0 8px 64px rgba(120,180,255,0.14), 0 2px 16px rgba(120,180,255,0.08), inset 0 1px 0 rgba(255,255,255,0.95);
    max-width: 860px;
    width: 90%;
}

.hero-logo {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(5rem, 12vw, 9rem);
    font-weight: 300;
    letter-spacing: 8px;
    background: linear-gradient(135deg, #b8ddf5 0%, #7bbfea 35%, #4a9fd4 65%, #8dc8ec 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 1rem;
    filter: drop-shadow(0 2px 16px rgba(120,180,255,0.25));
}

.hero-tagline {
    font-family: 'Josefin Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 400;
    color: #888;
    letter-spacing: 5px;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.hero-desc {
    font-family: 'Josefin Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 300;
    text-align: center;
    color: #777;
    line-height: 2;
    max-width: 480px;
    margin: 0 auto 2.5rem auto;
    letter-spacing: 0.3px;
    
}

.hero-badges {
    display: flex;
    gap: 0.6rem;
    justify-content: center;
    flex-wrap: wrap;
}

.hero-badge {
    background: rgba(180,220,255,0.2);
    border: 1px solid rgba(120,180,255,0.3);
    color: #4a9fd4;
    padding: 0.3rem 1rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.scroll-hint {
    position: absolute;
    bottom: 2.5rem;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #bbb;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
}

.scroll-line {
    width: 1px;
    height: 40px;
    background: linear-gradient(to bottom, #bbb, transparent);
    animation: sp 2s ease-in-out infinite;
}

@keyframes sp {
    0%,100%{opacity:.3} 50%{opacity:1}
}

.light-divider {
    width: 100vw;
    margin-left: calc(-5rem);
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(180,220,255,0.5), transparent);
}

/* ── SECTION LABELS ── */
.section-label {
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4a9fd4;
    font-weight: 600;
    margin-bottom: 0.75rem;
}

.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 300;
    color: #111;
    letter-spacing: 2px;
    line-height: 1.15;
    margin-bottom: 1rem;
}

.section-subtitle {
    font-size: 0.88rem;
    font-weight: 300;
    color: #888;
    line-height: 1.9;
    max-width: 560px;
    letter-spacing: 0.3px;
    margin-bottom: 2.5rem;
}

/* ── PANEL LABEL ── */
.panel-label {
    font-size: 0.62rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #999;
    font-weight: 600;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #f0f4f8;
}

/* ── CHAT BUBBLES ── */
.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-height: 520px;
    overflow-y: auto;
    padding-right: 4px;
}

.chat-wrap::-webkit-scrollbar { width: 3px; }
.chat-wrap::-webkit-scrollbar-thumb { background: rgba(180,220,255,0.4); border-radius: 2px; }

.bubble-user {
    background: linear-gradient(135deg, #eaf4fd, #d6ecfa);
    border: 1px solid rgba(120,180,255,0.2);
    border-radius: 16px 16px 4px 16px;
    padding: 0.875rem 1.1rem;
    font-size: 0.85rem;
    color: #222;
    line-height: 1.6;
    font-style: italic;
    font-weight: 300;
    align-self: flex-end;
    max-width: 88%;
}

.bubble-agent {
    background: #fff;
    border: 1px solid #eef2f7;
    border-radius: 16px 16px 16px 4px;
    padding: 0.875rem 1.1rem;
    font-size: 0.82rem;
    color: #333;
    line-height: 1.75;
    white-space: pre-wrap;
    font-family: 'Courier New', monospace;
    align-self: flex-start;
    max-width: 88%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.intent-tag {
    display: inline-block;
    padding: 0.18rem 0.7rem;
    border-radius: 999px;
    font-size: 0.63rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
    font-family: 'Josefin Sans', sans-serif;
}

.tag-create_file  { background:#e8fdf0; color:#16a34a; border:1px solid #bbf7d0; }
.tag-write_code   { background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe; }
.tag-summarize    { background:#fffbeb; color:#d97706; border:1px solid #fde68a; }
.tag-general_chat { background:#faf5ff; color:#7c3aed; border:1px solid #e9d5ff; }
.tag-run_code     { background:#fff1f2; color:#e11d48; border:1px solid #fecdd3; }
.tag-launch_file  { background:#fff7ed; color:#ea580c; border:1px solid #fed7aa; }
.tag-error        { background:#fef2f2; color:#dc2626; border:1px solid #fecaca; }

/* ── TRANSCRIPTION ── */
.transcript-box {
    font-size: 0.95rem;
    font-weight: 300;
    color: #222;
    line-height: 1.9;
    font-style: italic;
    border-left: 2px solid rgba(74,159,212,0.35);
    padding-left: 1rem;
    margin-bottom: 1.5rem;
}

.out-label {
    font-size: 0.6rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #bbb;
    font-weight: 600;
    margin-bottom: 0.4rem;
    margin-top: 1.25rem;
}

/* ── AWAITING ── */
.awaiting {
    height: 280px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}

.aw-ring {
    width: 52px; height: 52px;
    border-radius: 50%;
    border: 1px solid rgba(180,220,255,0.5);
    display:flex; align-items:center; justify-content:center;
}

.aw-dot {
    width: 24px; height: 24px;
    border-radius: 50%;
    background: rgba(180,220,255,0.25);
}

.aw-text {
    font-size: 0.68rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #ccc;
    font-weight: 400;
}

/* ── FEATURES ── */
.feat-grid {
    display: grid;
    grid-template-columns: repeat(6,1fr);
    gap: 1.25rem;
    margin-top: 2.5rem;
}

.feat-card {
    background: #fafcff;
    border: 1px solid rgba(180,220,255,0.3);
    border-radius: 14px;
    padding: 1.5rem 1rem;
    text-align: center;
    transition: box-shadow .2s, transform .2s;
}

.feat-card:hover { box-shadow: 0 6px 24px rgba(120,180,255,0.1); transform: translateY(-2px); }

.feat-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg,rgba(168,216,240,.3),rgba(74,159,212,.2));
    border: 1px solid rgba(120,180,255,.25);
    border-radius: 8px;
    margin: 0 auto .75rem auto;
    display:flex; align-items:center; justify-content:center;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1rem; font-weight: 300; color: #4a9fd4;
}

.feat-name { font-size:.68rem; letter-spacing:2px; text-transform:uppercase; font-weight:700; color:#222; margin-bottom:.4rem; }
.feat-desc { font-size:.75rem; color:#aaa; line-height:1.6; font-weight:300; }

/* ── TECH ── */
.tech-grid {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 1.25rem;
    margin-top: 2.5rem;
}

.tech-card {
    background: #fff;
    border: 1px solid rgba(180,220,255,.3);
    border-radius: 14px;
    padding: 1.75rem;
    position: relative;
    overflow: hidden;
}

.tech-card::before {
    content:'';
    position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, rgba(168,216,240,.6), rgba(74,159,212,.6));
}

.tech-num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.5rem; font-weight: 300;
    color: rgba(180,220,255,.5);
    line-height: 1; margin-bottom: .6rem;
}

.tech-name { font-size:.68rem; letter-spacing:2.5px; text-transform:uppercase; font-weight:700; color:#4a9fd4; margin-bottom:.4rem; }
.tech-desc { font-size:.8rem; color:#888; line-height:1.75; font-weight:300; }

/* ── PIPELINE ── */
.pipe-steps {
    display: flex;
    align-items: flex-start;
    margin-top: 2.5rem;
    position: relative;
}

.pipe-steps::before {
    content:'';
    position:absolute; top:27px; left:10%; right:10%; height:1px;
    background: linear-gradient(to right, rgba(120,180,255,.3), rgba(120,180,255,.3));
}

.pipe-step { flex:1; text-align:center; position:relative; }

.pipe-dot {
    width:54px; height:54px;
    border-radius:50%;
    background:#fff;
    border:1px solid rgba(120,180,255,.35);
    margin:0 auto .75rem auto;
    display:flex; align-items:center; justify-content:center;
    font-family:'Cormorant Garamond',serif;
    font-size:1.1rem; font-weight:400; color:#4a9fd4;
    position:relative; z-index:1;
    box-shadow: 0 2px 12px rgba(120,180,255,.1);
}

.pipe-name { font-size:.65rem; letter-spacing:2px; text-transform:uppercase; font-weight:700; color:#333; margin-bottom:.35rem; }
.pipe-desc { font-size:.72rem; color:#aaa; font-weight:300; line-height:1.5; padding:0 .5rem; }

# Audio recorderr!
div[class*="audio-recorder"] {
    background: #ffffff !important;
}
div[class*="audio_recorder"] {
    background: #ffffff !important;
}
.css-audio-recorder {
    background: #ffffff !important;
}
section[data-testid="stFileUploadDropzone"] {
    background: #fafcff !important;
}            

/* ── FOOTER ── */
.foot {
    width:100vw;
    margin-left:calc(-5rem);
    background:#111;
    padding:4rem 8rem;
    display:flex;
    justify-content:space-between;
    gap:3rem;
    flex-wrap:wrap;
    margin-top:4rem;
}

.foot-logo {
    font-family:'Cormorant Garamond',serif;
    font-size:2.5rem; font-weight:300;
    letter-spacing:4px;
    background:linear-gradient(135deg,#b8ddf5,#4a9fd4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    margin-bottom:.5rem;
}

.foot-tag { font-size:.65rem; color:#555; letter-spacing:2px; text-transform:uppercase; }
.foot-col-t { font-size:.62rem; letter-spacing:2.5px; text-transform:uppercase; font-weight:700; color:#555; margin-bottom:.75rem; }
.foot-col-i { font-size:.8rem; color:#777; font-weight:300; margin-bottom:.4rem; line-height:1.6; }

.foot-bottom {
    width:100vw;
    margin-left:calc(-5rem);
    background:#0a0a0a;
    padding:1.25rem 8rem;
    display:flex;
    justify-content:space-between;
    font-size:.68rem; color:#444; letter-spacing:1px;
}

/* ── STREAMLIT OVERRIDES ── */
.stRadio label p { color:#111 !important; font-size:.72rem !important; letter-spacing:1.5px !important; text-transform:uppercase !important; font-weight:600 !important; }
.stRadio > div { gap:.75rem !important; }

.stFileUploader section {
    background:#fafcff !important;
    border:1px dashed rgba(74,159,212,.35) !important;
    border-radius:10px !important;
}
.stFileUploader label p { color:#111 !important; font-family:'Josefin Sans',sans-serif !important; }
.stFileUploader span { color:#111 !important; }
.stFileUploader small { color:#888 !important; }

.stTextArea textarea {
    border:1px solid rgba(180,220,255,.4) !important;
    border-radius:10px !important;
    font-family:'Josefin Sans',sans-serif !important;
    font-size:.88rem !important;
    background:#fafcff !important;
    color:#111 !important;
}

div[data-testid="column"] {
    background:#fff !important;
    border:1px solid rgba(180,220,255,.2) !important;
    border-radius:16px !important;
    padding:1.5rem !important;
}
            
div[data-testid="stAlert"] {
    background: #1a1a2e !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

div[data-testid="stAlert"] p {
    color: #e2e8f0 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 1px !important;
}

.stButton > button {
    background:linear-gradient(135deg,#b8ddf5,#4a9fd4) !important;
    color:#fff !important;
    border:none !important;
    border-radius:8px !important;
    padding:.6rem 1.5rem !important;
    font-family:'Josefin Sans',sans-serif !important;
    font-weight:600 !important;
    font-size:.72rem !important;
    letter-spacing:2px !important;
    text-transform:uppercase !important;
    width:100% !important;
    box-shadow:0 4px 14px rgba(74,159,212,.2) !important;
    transition:opacity .2s !important;
}

.stButton > button:hover { opacity:.82 !important; }

.stWarning { border-radius:10px !important; }

audio-recorder { background:transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── Sticky Header ─────────────────────────────────────────────────────────────
st.components.v1.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;400;600&family=Cormorant+Garamond:wght@300;400&display=swap');
#sh {
    position:fixed; top:0; left:0; right:0; z-index:9999;
    background:rgba(255,255,255,.96);
    backdrop-filter:blur(20px);
    border-bottom:1px solid rgba(180,220,255,.3);
    padding:.9rem 5rem;
    display:flex; align-items:center; justify-content:space-between;
    transform:translateY(-100%);
    transition:transform .4s cubic-bezier(.4,0,.2,1);
    font-family:'Josefin Sans',sans-serif;
}
#sh.vis { transform:translateY(0); }
.sh-logo {
    font-family:'Cormorant Garamond',serif;
    font-size:1.6rem; font-weight:300; letter-spacing:4px;
    background:linear-gradient(135deg,#b8ddf5,#4a9fd4);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.sh-nav { display:flex; gap:2.5rem; font-size:.68rem; letter-spacing:2.5px; text-transform:uppercase; font-weight:600; color:#bbb; }
</style>
<div id="sh">
    <div class="sh-logo">C H R O N O S</div>
    <div class="sh-nav"><span>Dashboard</span><span>Features</span><span>Stack</span></div>
</div>
<script>
window.parent.document.addEventListener('scroll', function() {
    var h = window.parent.document.getElementById('sh') || document.getElementById('sh');
    if(!h) return;
    if(window.parent.scrollY > window.parent.innerHeight*.6) h.classList.add('vis');
    else h.classList.remove('vis');
}, {passive:true});
</script>
""", height=0)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-bg"></div>
    <div class="hero-glass">
        <div class="hero-logo">Chronos</div>
        <div class="hero-tagline">Voice Controlled Local AI Agent</div>
        <p class="hero-desc">
            Speak your intent. Chronos listens, understands, and acts.
            Powered entirely by local models — your voice, your machine, your data.
            No cloud. No compromise.
        </p>
        <div class="hero-badges">
            <span class="hero-badge">Whisper STT</span>
            <span class="hero-badge">qwen2.5-coder</span>
            <span class="hero-badge">Ollama</span>
            <span class="hero-badge">100% Offline</span>
            <span class="hero-badge">RTX 4050</span>
        </div>
    </div>
    <div class="scroll-hint">
        <span>Scroll</span>
        <div class="scroll-line"></div>
    </div>
</div>
<div class="light-divider"></div>
""", unsafe_allow_html=True)

# ── Dashboard Header ──────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:3rem 0 1.5rem 0;">
    <div class="section-label">Dashboard</div>
    <div class="section-title">Command Center</div>
    <p class="section-subtitle">Upload or record audio. Chronos transcribes, classifies your intent and executes the right action in real time.</p>
</div>
""", unsafe_allow_html=True)

# ── Load Whisper ──────────────────────────────────────────────────────────────
@st.cache_resource
def get_whisper_model():
    return load_model()

model = get_whisper_model()

# ── Session State ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "pending" not in st.session_state:
    st.session_state.pending = None
if "pending_transcription" not in st.session_state:
    st.session_state.pending_transcription = None

# ── 3 Columns ─────────────────────────────────────────────────────────────────
col_input, col_chat, col_output = st.columns([1, 1.4, 1], gap="medium")

with col_input:
    st.markdown('<div class="panel-label">Audio Input</div>', unsafe_allow_html=True)

    input_method = st.radio(
        "Method",
        ["Upload File", "Record from Mic"],
        label_visibility="collapsed",
        horizontal=True
    )

    audio_path = None

    if input_method == "Upload File":
        uploaded_file = st.file_uploader(
            "Drop .wav or .mp3",
            type=["wav", "mp3"],
            label_visibility="collapsed"
        )
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(uploaded_file.read())
                audio_path = tmp.name
            st.audio(uploaded_file)
    else:
        try:
            from audio_recorder_streamlit import audio_recorder
            audio_bytes = audio_recorder(text="", icon_size="3x", neutral_color="#4a9fd4")
            if audio_bytes:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(audio_bytes)
                    audio_path = tmp.name
                st.audio(audio_bytes, format="audio/wav")
        except ImportError:
            st.warning("pip install audio-recorder-streamlit")

    st.markdown("<br>", unsafe_allow_html=True)

    if audio_path and st.button("Run Agent"):
        with st.spinner("Transcribing..."):
            transcription = transcribe(model, audio_path)
        with st.spinner("Detecting intent..."):
            output = run_agent(transcription)
        intent = output["intent"]
        if intent in ["create_file", "write_code"]:
            st.session_state.pending = output
            st.session_state.pending_transcription = transcription
        else:
            st.session_state.history.append({
                "transcription": transcription,
                "intent": intent,
                "result": output["result"]
            })
        try:
            os.unlink(audio_path)
        except:
            pass

    if st.session_state.pending:
        pending = st.session_state.pending
        intent_name = pending['intent'].replace('_', ' ').title()
        filename = pending['intent_data'].get('filename', 'unknown')
        st.warning(f"Confirm: {intent_name} — {filename}")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Confirm"):
                st.session_state.history.append({
                    "transcription": st.session_state.pending_transcription,
                    "intent": pending["intent"],
                    "result": pending["result"]
                })
                st.session_state.pending = None
                st.rerun()
        with c2:
            if st.button("Cancel"):
                st.session_state.pending = None
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="panel-label">Direct Summarizer</div>', unsafe_allow_html=True)
    text_input = st.text_area(
        "Paste text",
        placeholder="Paste any text to summarize...",
        height=110,
        label_visibility="collapsed"
    )
    if st.button("Summarize Text"):
        if text_input.strip():
            from tools import summarize
            with st.spinner("Summarizing..."):
                result = summarize(text_input.strip())
            st.session_state.history.append({
                "transcription": "[Direct Text Input]",
                "intent": "summarize",
                "result": result
            })
            st.rerun()
        else:
            st.warning("Paste some text first.")

with col_chat:
    st.markdown('<div class="panel-label">Agent Conversation</div>', unsafe_allow_html=True)
    if st.session_state.history:
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
        for item in st.session_state.history:
            intent = item["intent"]
            label = intent.replace("_", " ").title()
            st.markdown(f"""
            <div class="bubble-user">{item["transcription"]}</div>
            <div class="bubble-agent">
                <span class="intent-tag tag-{intent}">{label}</span><br>
                {item["result"]}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="awaiting">
            <div class="aw-ring"><div class="aw-dot"></div></div>
            <div class="aw-text">Awaiting your voice command</div>
        </div>
        """, unsafe_allow_html=True)

with col_output:
    st.markdown('<div class="panel-label">Live Output</div>', unsafe_allow_html=True)
    if st.session_state.history:
        latest = st.session_state.history[-1]
        intent = latest["intent"]
        label = intent.replace("_", " ").title()
        st.markdown('<div class="out-label">Transcription</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="transcript-box">"{latest["transcription"]}"</div>', unsafe_allow_html=True)
        st.markdown('<div class="out-label">Detected Intent</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="intent-tag tag-{intent}" style="margin-top:.4rem;display:inline-block;">{label}</span>', unsafe_allow_html=True)
        st.markdown('<div class="out-label">Result</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:.8rem;color:#333;line-height:1.75;margin-top:.4rem;white-space:pre-wrap;font-family:Courier New,monospace;">{latest["result"][:600]}{"..." if len(latest["result"])>600 else ""}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="out-label" style="margin-top:1.5rem;">Session Commands</div><div style="font-size:1.5rem;font-family:Cormorant Garamond,serif;font-weight:300;color:#4a9fd4;">{len(st.session_state.history)}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="awaiting">
            <div class="aw-ring"><div class="aw-dot"></div></div>
            <div class="aw-text">Output appears here</div>
        </div>
        """, unsafe_allow_html=True)

# ── Features ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="light-divider" style="margin-top:3rem;"></div>
<div style="padding:4rem 0;">
    <div class="section-label">Capabilities</div>
    <div class="section-title">What Chronos Can Do</div>
    <div class="feat-grid">
        <div class="feat-card"><div class="feat-icon">F</div><div class="feat-name">Create File</div><div class="feat-desc">Creates any file type with voice-specified content instantly</div></div>
        <div class="feat-card"><div class="feat-icon">C</div><div class="feat-name">Write Code</div><div class="feat-desc">Generates and saves Python code files on command</div></div>
        <div class="feat-card"><div class="feat-icon">S</div><div class="feat-name">Summarize</div><div class="feat-desc">Condenses long text into clear, concise summaries</div></div>
        <div class="feat-card"><div class="feat-icon">R</div><div class="feat-name">Run Code</div><div class="feat-desc">Executes Python files and returns live terminal output</div></div>
        <div class="feat-card"><div class="feat-icon">L</div><div class="feat-name">Launch File</div><div class="feat-desc">Opens any file in its default system application</div></div>
        <div class="feat-card"><div class="feat-icon">A</div><div class="feat-name">General Chat</div><div class="feat-desc">Answers questions and holds open-ended conversations</div></div>
    </div>
</div>
<div class="light-divider"></div>
""", unsafe_allow_html=True)

# ── Tech Stack ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:4rem 0; background:#fafcff; width:100vw; margin-left:calc(-5rem); padding-left:5rem; padding-right:5rem;">
    <div class="section-label">Architecture</div>
    <div class="section-title">Built With</div>
    <div class="tech-grid">
        <div class="tech-card">
            <div class="tech-num">01</div>
            <div class="tech-name">OpenAI Whisper</div>
            <div class="tech-desc">Medium model on CPU. Converts voice audio to accurate text in seconds without GPU contention.</div>
        </div>
        <div class="tech-card">
            <div class="tech-num">02</div>
            <div class="tech-name">qwen2.5-coder</div>
            <div class="tech-desc">7B parameter model on RTX 4050 GPU via Ollama. Handles intent detection and code generation.</div>
        </div>
        <div class="tech-card">
            <div class="tech-num">03</div>
            <div class="tech-name">Ollama</div>
            <div class="tech-desc">Local model runtime with Anthropic-compatible API at localhost:11434. Zero cloud dependency.</div>
        </div>
        <div class="tech-card">
            <div class="tech-num">04</div>
            <div class="tech-name">Streamlit</div>
            <div class="tech-desc">Python-native web framework powering the real-time dashboard and all interactive components.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Pipeline ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:4rem 0;">
    <div class="section-label">Pipeline</div>
    <div class="section-title">How It Works</div>
    <div class="pipe-steps">
        <div class="pipe-step">
            <div class="pipe-dot">1</div>
            <div class="pipe-name">Audio Input</div>
            <div class="pipe-desc">Upload .wav/.mp3 or record from microphone</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-dot">2</div>
            <div class="pipe-name">Transcription</div>
            <div class="pipe-desc">Whisper converts speech to text on CPU</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-dot">3</div>
            <div class="pipe-name">Intent Detection</div>
            <div class="pipe-desc">qwen2.5 classifies command and extracts parameters</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-dot">4</div>
            <div class="pipe-name">Confirmation</div>
            <div class="pipe-desc">Human-in-the-loop approval for file operations</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-dot">5</div>
            <div class="pipe-name">Execution</div>
            <div class="pipe-desc">Python tools execute the action locally</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="foot">
    <div>
        <div class="foot-logo">Chronos</div>
        <div class="foot-tag">Voice Controlled Local AI Agent</div>
    </div>
    <div>
        <div class="foot-col-t">Stack</div>
        <div class="foot-col-i">Whisper Medium (STT)</div>
        <div class="foot-col-i">qwen2.5-coder:7b (LLM)</div>
        <div class="foot-col-i">Ollama (Runtime)</div>
        <div class="foot-col-i">Streamlit (UI)</div>
    </div>
    <div>
        <div class="foot-col-t">Capabilities</div>
        <div class="foot-col-i">File Creation</div>
        <div class="foot-col-i">Code Generation</div>
        <div class="foot-col-i">Text Summarization</div>
        <div class="foot-col-i">Code Execution</div>
    </div>
    <div>
        <div class="foot-col-t">Privacy</div>
        <div class="foot-col-i">100% Local Inference</div>
        <div class="foot-col-i">No Cloud API Calls</div>
        <div class="foot-col-i">No Data Transmission</div>
        <div class="foot-col-i">Air-gap Compatible</div>
    </div>
</div>
<div class="foot-bottom">
    <span>Chronos AI</span>
    <span>Whisper + qwen2.5 + Ollama + Streamlit</span>
</div>
""", unsafe_allow_html=True)
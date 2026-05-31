import streamlit as st
import time
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

st.set_page_config(page_title="InsightFlow", page_icon="🎬", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:wght@300;400;500&display=swap');
:root {
    --bg:#F2EFE8; --bg-card:#FFFFFF; --bg-dark:#1A1A18; --bg-d2:#242420; --bg-d3:#2E2E28;
    --border:rgba(0,0,0,0.10); --bd:rgba(255,255,255,0.08);
    --gold:#C8922A; --gold-l:#E8B84B; --teal:#2A7A6A; --amber:#B8750A; --amber-l:#FDF4E7;
    --red:#A83232; --red-l:#FAEAEA; --ink:#1A1A18; --ink2:#4A4A42; --ink3:#8A8A7A; --ink4:#AEAE9E;
}
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif!important;background-color:var(--bg)!important;color:var(--ink)!important;}
.stApp{background:var(--bg)!important;}
.main .block-container{padding:0!important;max-width:100%!important;}
[data-testid="stSidebar"]{background:var(--bg-dark)!important;border-right:1px solid var(--bd)!important;min-width:280px!important;max-width:280px!important;}
[data-testid="stSidebar"]>div{padding:2rem 1.5rem!important;}
[data-testid="stSidebar"] *{color:#E8E8E0!important;}
.sb-brand{margin-bottom:2rem;padding-bottom:1.5rem;border-bottom:1px solid var(--bd);}
.sb-logo{font-family:'Playfair Display',serif;font-size:1.7rem;font-weight:600;line-height:1;margin-bottom:0.3rem;}
.sb-lw{color:#fff;}.sb-lg{color:var(--gold);font-style:italic;}
.sb-tag{font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.18em;text-transform:uppercase;color:var(--ink3)!important;}
.sb-lbl{font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.18em;text-transform:uppercase;color:var(--ink3)!important;margin:1.5rem 0 0.5rem;display:flex;align-items:center;gap:6px;}
.sb-lbl::before{content:'▶';font-size:0.5rem;color:var(--gold)!important;}
.sb-hint{font-size:0.72rem;color:var(--ink3)!important;margin-top:0.4rem;line-height:1.5;}
.stTextInput>div>div>input{background:var(--bg-d2)!important;border:1px solid var(--bd)!important;border-radius:6px!important;color:#E8E8E0!important;font-family:'IBM Plex Mono',monospace!important;font-size:0.78rem!important;padding:0.65rem 0.9rem!important;transition:border-color 0.15s!important;}
.stTextInput>div>div>input:focus{border-color:var(--gold)!important;box-shadow:0 0 0 2px rgba(200,146,42,0.15)!important;}
.stTextInput>div>div>input::placeholder{color:rgba(255,255,255,0.2)!important;font-style:italic;}
.stSelectbox>div>div{background:var(--bg-d2)!important;border:1px solid var(--bd)!important;border-radius:6px!important;color:#E8E8E0!important;font-size:0.85rem!important;}
.stButton>button{background:var(--bg-d3)!important;color:#E8E8E0!important;border:1px solid rgba(255,255,255,0.12)!important;border-radius:6px!important;font-family:'IBM Plex Mono',monospace!important;font-size:0.78rem!important;letter-spacing:0.08em!important;padding:0.65rem 1.25rem!important;transition:all 0.15s!important;text-transform:uppercase!important;}
.stButton>button:hover{background:rgba(200,146,42,0.15)!important;border-color:var(--gold)!important;color:var(--gold-l)!important;}
.stButton>button[kind="secondary"]{background:transparent!important;border:1px solid var(--border)!important;color:var(--ink2)!important;}
.stButton>button[kind="secondary"]:hover{background:var(--bg-card)!important;}
.pipe-sec{margin-top:1.5rem;padding-top:1.5rem;border-top:1px solid var(--bd);}
.pipe-lbl{font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.18em;text-transform:uppercase;color:var(--ink3)!important;margin-bottom:0.75rem;}
.ps{display:flex;align-items:center;gap:10px;padding:0.4rem 0.6rem;border-radius:5px;margin:3px 0;font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:rgba(232,232,224,0.45)!important;}
.ps.done{color:rgba(232,232,224,0.85)!important;}
.ps.active{background:rgba(200,146,42,0.1);color:var(--gold-l)!important;}
.pd{width:6px;height:6px;border-radius:50%;flex-shrink:0;}
.pd.pending{background:rgba(255,255,255,0.15);}
.pd.active{background:var(--gold);box-shadow:0 0 6px var(--gold);animation:bl 1.4s infinite;}
.pd.done{background:#5ABFA0;}
@keyframes bl{0%,100%{opacity:1;}50%{opacity:0.3;}}
.mw{padding:3rem 3.5rem 5rem;max-width:1300px;margin:0 auto;}
.ph{display:flex;align-items:flex-end;justify-content:space-between;padding-bottom:1.5rem;border-bottom:1px solid var(--border);margin-bottom:2.5rem;}
.ph-logo{font-family:'Playfair Display',serif;font-size:3rem;font-weight:600;letter-spacing:-0.02em;color:var(--ink);}
.ph-logo em{color:var(--gold);font-style:italic;}
.ph-r{text-align:right;font-family:'IBM Plex Mono',monospace;font-size:0.62rem;letter-spacing:0.16em;text-transform:uppercase;color:var(--ink4);line-height:2.2;}
.sb{background:var(--bg-dark);border-radius:10px;padding:2rem 2.25rem;margin-bottom:2rem;position:relative;overflow:hidden;}
.sb::after{content:'';position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,var(--gold),transparent);}
.s-ey{font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;text-transform:uppercase;color:rgba(174,174,158,0.7);margin-bottom:0.6rem;}
.s-ti{font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;color:#fff;margin-bottom:0.75rem;line-height:1.25;}
.s-bd{display:inline-block;padding:0.2rem 0.65rem;border:1px solid var(--gold);border-radius:3px;font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--gold);background:rgba(200,146,42,0.08);}
.cc{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1.75rem;}
.ccl{font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;text-transform:uppercase;color:var(--ink3);margin-bottom:1rem;padding-bottom:0.75rem;border-bottom:1px solid var(--border);}
.ccb{font-size:0.9rem;line-height:1.8;color:var(--ink2);}
.ccb ul{padding-left:1.2rem;margin:0.4rem 0;}.ccb li{margin-bottom:0.3rem;}.ccb strong{color:var(--ink);font-weight:600;}
.at{border-top:2.5px solid var(--teal);}.aa{border-top:2.5px solid var(--amber);}.ar{border-top:2.5px solid var(--red);}
.ts{background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:1.25rem;font-family:'IBM Plex Mono',monospace;font-size:0.78rem;line-height:1.9;max-height:380px;overflow-y:auto;color:var(--ink2);white-space:pre-wrap;word-break:break-word;margin-top:0.5rem;}
.streamlit-expanderHeader{background:var(--bg-card)!important;border:1px solid var(--border)!important;border-radius:6px!important;font-size:0.875rem!important;color:var(--ink2)!important;}
.csh{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:1.25rem;}
.ch{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:400;color:var(--ink);}
.cpw{font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.16em;text-transform:uppercase;color:var(--ink4);}
.cw{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1.5rem;min-height:180px;max-height:420px;overflow-y:auto;margin-bottom:1rem;}
.ce{display:flex;align-items:center;justify-content:center;height:140px;font-family:'IBM Plex Mono',monospace;font-size:0.75rem;letter-spacing:0.08em;color:var(--ink4);font-style:italic;}
.cr{margin-bottom:1.25rem;overflow:hidden;}.cr:last-child{margin-bottom:0;}
.cw2{font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.16em;text-transform:uppercase;margin-bottom:0.35rem;}
.cw2.you{color:var(--ink3);text-align:right;}.cw2.bot{color:var(--gold);}
.cb{display:inline-block;padding:0.75rem 1.1rem;border-radius:8px;font-size:0.875rem;line-height:1.65;max-width:82%;}
.by{background:#E8EEF8;color:var(--ink);border-radius:8px 8px 2px 8px;float:right;clear:both;}
.bb{background:var(--amber-l);color:var(--ink);border:1px solid rgba(184,117,10,0.15);border-radius:8px 8px 8px 2px;float:left;clear:both;}
hr{border:none!important;border-top:1px solid var(--border)!important;margin:2rem 0!important;}
.ww{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:7rem 2rem;text-align:center;}
.wl{font-family:'Playfair Display',serif;font-size:3.5rem;font-weight:600;color:var(--ink);margin-bottom:0.5rem;}
.wl em{color:var(--gold);font-style:italic;}
.ws{font-family:'IBM Plex Mono',monospace;font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:var(--ink3);margin-bottom:2rem;}
.wd{font-size:0.925rem;color:var(--ink3);max-width:400px;line-height:1.75;margin-bottom:2.5rem;}
.wts{display:flex;gap:0.5rem;flex-wrap:wrap;justify-content:center;}
.wt{display:inline-block;padding:0.3rem 0.9rem;border:1px solid var(--border);border-radius:3px;font-family:'IBM Plex Mono',monospace;font-size:0.65rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--ink3);background:var(--bg-card);}
label{color:var(--ink3)!important;font-size:0.75rem!important;font-family:'IBM Plex Mono',monospace!important;letter-spacing:0.08em!important;}
.stProgress>div>div>div{background:var(--gold)!important;}.stSpinner>div{border-top-color:var(--gold)!important;}
[data-testid="stMarkdownContainer"] p{color:var(--ink2)!important;font-size:0.9rem!important;}
::-webkit-scrollbar{width:4px;height:4px;}::-webkit-scrollbar-track{background:transparent;}::-webkit-scrollbar-thumb{background:rgba(0,0,0,0.12);border-radius:2px;}
</style>
""", unsafe_allow_html=True)

for key, default in {"result":None,"chat_history":[],"processing":False,"pipeline_done":False,"pipeline_steps":{}}.items():
    if key not in st.session_state: st.session_state[key] = default

def gcls(k): return st.session_state.pipeline_steps.get(k,"pending")

def rstep(label, key, icon):
    c = gcls(key)
    st.markdown(f'<div class="ps {c}"><div class="pd {c}"></div><span style="opacity:0.6">{icon}</span><span>{label}</span></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sb-brand"><div class="sb-logo"><span class="sb-lw">Insight</span><span class="sb-lg">Flow</span></div><div class="sb-tag">Intelligent Meeting Analysis</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-lbl">New Session</div>', unsafe_allow_html=True)
    source = st.text_input("src", placeholder="https://youtu.be/XXXXXXXXX", label_visibility="collapsed")
    st.markdown('<div class="sb-hint">YouTube URL or local .mp4 / .wav / .mp3</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-lbl">Language</div>', unsafe_allow_html=True)
    language = st.selectbox("lang", ["english","hinglish"], index=0, label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("▶  Run Analysis", use_container_width=True)
    if st.session_state.pipeline_done:
        st.markdown('<div class="pipe-sec"><div class="pipe-lbl">Pipeline</div></div>', unsafe_allow_html=True)
        for step, icon, label in [("audio","◉","Audio extract"),("transcript","▷","Transcription"),("title","▷","Title generation"),("summary","▷","Summarisation"),("extract","▷","Extraction"),("rag","▷","RAG index")]:
            rstep(label, step, icon)

st.markdown('<div class="mw">', unsafe_allow_html=True)
st.markdown('<div class="ph"><div class="ph-logo">Insight<em>Flow</em></div><div class="ph-r">Intelligent Meeting Analysis<br><span>Transcribe &nbsp;/&nbsp; Summarise &nbsp;/&nbsp; Query</span></div></div>', unsafe_allow_html=True)

if run_btn:
    if not source.strip():
        st.error("Please enter a YouTube URL or file path.")
    else:
        st.session_state.update({"pipeline_done":False,"result":None,"chat_history":[],"pipeline_steps":{}})
        ph = st.empty()
        def upd(k,s): st.session_state.pipeline_steps[k]=s
        try:
            ph.info("⚙️  Running — watch sidebar for live progress.")
            upd("audio","active");      chunks     = process_input(source);             upd("audio","done")
            upd("transcript","active"); transcript = transcribe_all(chunks,language);   upd("transcript","done")
            upd("title","active");      title      = generate_title(transcript);        upd("title","done")
            upd("summary","active");    summary    = summarize(transcript);             upd("summary","done")
            upd("extract","active"); action_items=extract_action_items(transcript); decisions=extract_key_decisions(transcript); questions=extract_questions(transcript); upd("extract","done")
            upd("rag","active");        rag_chain  = build_rag_chain(transcript);       upd("rag","done")
            st.session_state.result = {"title":title,"transcript":transcript,"summary":summary,"action_items":action_items,"key_decisions":decisions,"open_questions":questions,"rag_chain":rag_chain}
            st.session_state.pipeline_done = True
            ph.success("✅  Analysis complete!"); time.sleep(0.7); ph.empty(); st.rerun()
        except Exception as e:
            for k in ["audio","transcript","title","summary","extract","rag"]:
                if st.session_state.pipeline_steps.get(k)=="active": st.session_state.pipeline_steps[k]="pending"
            ph.error(f"❌  Error: {e}")

if st.session_state.result:
    r = st.session_state.result
    st.markdown(f'<div class="sb"><div class="s-ey">Session</div><div class="s-ti">{r["title"]}</div><span class="s-bd">Analysed</span></div>', unsafe_allow_html=True)

    cl, cr = st.columns([1.55,1], gap="medium")
    with cl:
        st.markdown(f'<div class="cc"><div class="ccl">Summary</div><div class="ccb">{r["summary"]}</div></div>', unsafe_allow_html=True)
    with cr:
        st.markdown('<div class="cc" style="height:100%"><div class="ccl">Full Transcript</div></div>', unsafe_allow_html=True)
        with st.expander("› Expand transcript", expanded=False):
            st.markdown(f'<div class="ts">{r["transcript"]}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3, gap="medium")
    with c1: st.markdown(f'<div class="cc at"><div class="ccl">✓ &nbsp;Action Items</div><div class="ccb">{r["action_items"]}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="cc aa"><div class="ccl">◆ &nbsp;Key Decisions</div><div class="ccb">{r["key_decisions"]}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="cc ar"><div class="ccl">? &nbsp;Open Questions</div><div class="ccb">{r["open_questions"]}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="csh"><div class="ch">Ask the transcript</div><div class="cpw">Powered by RAG</div></div>', unsafe_allow_html=True)

    if st.session_state.chat_history:
        h = '<div class="cw">'
        for m in st.session_state.chat_history:
            if m["role"]=="user": h+=f'<div class="cr"><div class="cw2 you">You</div><div class="cb by">{m["content"]}</div></div>'
            else: h+=f'<div class="cr"><div class="cw2 bot">InsightFlow</div><div class="cb bb">{m["content"]}</div></div>'
        h+='</div>'; st.markdown(h, unsafe_allow_html=True)
    else:
        st.markdown('<div class="cw"><div class="ce">No messages yet — ask anything about the transcript</div></div>', unsafe_allow_html=True)

    ic,bc = st.columns([6,1], gap="small")
    with ic: user_input = st.text_input("q", placeholder="What is the key message?", label_visibility="collapsed")
    with bc: ask_btn = st.button("Ask →", use_container_width=True)

    if ask_btn and user_input.strip():
        with st.spinner("Thinking…"): answer = ask_question(r["rag_chain"], user_input.strip())
        st.session_state.chat_history += [{"role":"user","content":user_input.strip()},{"role":"assistant","content":answer}]
        st.rerun()
    if st.session_state.chat_history:
        if st.button("Clear conversation", type="secondary"): st.session_state.chat_history=[]; st.rerun()

else:
    st.markdown("""
    <div class="ww">
        <div class="wl">Insight<em>Flow</em></div>
        <div class="ws">Intelligent Meeting Analysis</div>
        <div class="wd">Paste a YouTube URL or local file path in the sidebar, select your language, and click <strong>Run Analysis</strong> to get a full breakdown of your meeting.</div>
        <div class="wts">
            <span class="wt">Transcription</span><span class="wt">Summarisation</span>
            <span class="wt">Action Items</span><span class="wt">RAG Chat</span><span class="wt">Hinglish</span>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

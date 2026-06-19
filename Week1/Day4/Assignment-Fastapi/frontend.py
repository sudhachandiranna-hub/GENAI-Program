import streamlit as st
import requests
from datetime import date

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Standup", page_icon="◆", layout="wide", initial_sidebar_state="expanded")

# ════════════════════════════════════════════════════════════════════════════
# STYLES — Linear / Stripe / Notion inspired glassmorphism
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --ink: #0A0A0F;
    --ink-soft: #6E6E80;
    --ink-faint: #A0A0B0;
    --indigo: #5B5FEF;
    --violet: #8B5CF6;
    --green: #10B981;
    --coral: #FF5D5D;
    --amber: #F59E0B;
    --surface: rgba(255,255,255,0.72);
    --border: rgba(10,10,15,0.07);
}

html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif; }

/* ── ambient gradient mesh background ── */
.stApp {
    background:
        radial-gradient(ellipse 800px 500px at 8% -5%, rgba(91,95,239,0.10), transparent 60%),
        radial-gradient(ellipse 700px 500px at 95% 10%, rgba(139,92,246,0.08), transparent 60%),
        radial-gradient(ellipse 600px 600px at 50% 100%, rgba(16,185,129,0.05), transparent 60%),
        #FFFFFF;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.5rem; max-width: 1180px; }

/* ── top nav bar ── */
.nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 4px 28px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 32px;
}
.nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}
.nav-mark {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, var(--indigo), var(--violet));
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; font-size: 14px;
    box-shadow: 0 4px 14px rgba(91,95,239,0.35);
}
.nav-title {
    font-weight: 700; font-size: 15px; color: var(--ink); letter-spacing: -0.01em;
}
.nav-date {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; color: var(--ink-faint);
    background: rgba(10,10,15,0.04);
    padding: 5px 11px; border-radius: 7px;
}

/* ── glass stat tiles ── */
.glass-stat {
    background: var(--surface);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 1px 2px rgba(10,10,15,0.04), 0 8px 24px rgba(10,10,15,0.03);
}
.glass-stat-num { font-size: 30px; font-weight: 800; color: var(--ink); letter-spacing: -0.02em; line-height: 1; }
.glass-stat-label { font-size: 11.5px; color: var(--ink-soft); font-weight: 600; margin-top: 6px; text-transform: uppercase; letter-spacing: 0.05em; }
.dot { display:inline-block; width:7px; height:7px; border-radius:50%; margin-right:7px; vertical-align:1px; }

/* ── section label ── */
.sec-label {
    font-size: 12.5px; font-weight: 700; color: var(--ink-soft);
    text-transform: uppercase; letter-spacing: 0.07em;
    margin: 36px 0 16px; display: flex; align-items: center; gap: 8px;
}
.sec-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }

/* ── glass card (standup) ── */
.glass-card {
    background: var(--surface);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 22px 22px 14px;
    margin-bottom: 14px;
    box-shadow: 0 1px 2px rgba(10,10,15,0.04), 0 8px 28px rgba(10,10,15,0.04);
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--indigo), var(--violet));
}
.glass-card.is-done::before { background: linear-gradient(90deg, var(--green), #34D399); }
.glass-card.is-done { opacity: 0.68; }

.gc-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.gc-avatar {
    width: 30px; height: 30px; border-radius: 9px;
    background: linear-gradient(135deg, var(--indigo), var(--violet));
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 700; font-size: 13px;
}
.gc-name { font-weight: 700; font-size: 14.5px; color: var(--ink); letter-spacing: -0.01em; }
.gc-name-row { display:flex; align-items:center; gap: 10px; }
.gc-name.is-done { text-decoration: line-through; color: var(--ink-faint); }

.gc-pill {
    font-size: 10.5px; font-weight: 700; padding: 3px 10px; border-radius: 100px;
    text-transform: uppercase; letter-spacing: 0.04em;
}
.pill-active { background: rgba(91,95,239,0.1); color: var(--indigo); }
.pill-done { background: rgba(16,185,129,0.1); color: var(--green); }

.gc-label { font-size: 10.5px; font-weight: 700; color: var(--ink-faint); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 3px; margin-top: 12px; }
.gc-value { font-size: 13.5px; color: var(--ink); line-height: 1.55; }

.gc-blocker { display: inline-block; background: rgba(255,93,93,0.12); color: var(--coral); font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: 8px; margin-top: 2px; }
.gc-clean { font-size: 12.5px; color: var(--ink-faint); }

.gc-foot {
    display: flex; align-items: center; justify-content: space-between;
    margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--border);
}
.gc-meta { font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: var(--ink-faint); }

/* ── buttons ── */
div.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    border: 1px solid var(--border) !important;
    background: rgba(255,255,255,0.6) !important;
    color: var(--ink) !important;
    transition: all 0.15s ease;
    box-shadow: none !important;
}
div.stButton > button:hover {
    background: rgba(10,10,15,0.04) !important;
    border-color: rgba(10,10,15,0.12) !important;
    transform: translateY(-1px);
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--indigo), var(--violet)) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(91,95,239,0.3) !important;
}
div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 18px rgba(91,95,239,0.4) !important;
    transform: translateY(-1px);
}

/* ── form glass panel ── */
.form-glass {
    background: var(--surface);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 28px;
    box-shadow: 0 1px 2px rgba(10,10,15,0.04), 0 12px 32px rgba(10,10,15,0.05);
}

/* inputs */
.stTextInput input, .stTextArea textarea, .stDateInput input, .stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    background: rgba(255,255,255,0.7) !important;
    font-size: 13.5px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--indigo) !important;
    box-shadow: 0 0 0 3px rgba(91,95,239,0.12) !important;
}
label { font-weight: 600 !important; font-size: 12.5px !important; color: var(--ink-soft) !important; }

[data-testid="stSidebar"] {
    background: rgba(250,250,251,0.8) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# DATA HELPERS
# ════════════════════════════════════════════════════════════════════════════

def fetch_standups(filter_date=None, status=None):
    params = {}
    if filter_date:
        params["date"] = str(filter_date)
    if status and status != "All":
        params["status"] = status.lower()
    try:
        r = requests.get(f"{API}/standup", params=params, timeout=5)
        return r.json().get("standups", [])
    except Exception:
        st.error("Can't reach the API. Run `uvicorn app:app --reload` first.")
        return []


def fetch_summary():
    try:
        return requests.get(f"{API}/standup/summary/today", timeout=5).json()
    except Exception:
        return {}


def post_standup(name, did, doing, blockers):
    r = requests.post(f"{API}/standup", json={"name": name, "did": did, "doing": doing, "blockers": blockers})
    return r.status_code == 201


def put_standup(sid, **kwargs):
    return requests.put(f"{API}/standup/{sid}", json=kwargs).status_code == 200


def delete_standup(sid):
    return requests.delete(f"{API}/standup/{sid}").status_code == 200


def initials(name):
    parts = name.strip().split()
    return (parts[0][0] + (parts[1][0] if len(parts) > 1 else parts[0][-1] if len(parts[0]) > 1 else "")).upper()


if "show_form" not in st.session_state: st.session_state.show_form = False
if "edit_id" not in st.session_state: st.session_state.edit_id = None


# ════════════════════════════════════════════════════════════════════════════
# NAV BAR
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="nav-bar">
    <div class="nav-brand">
        <div class="nav-mark">S</div>
        <div class="nav-title">Standup</div>
    </div>
    <div class="nav-date">{date.today().strftime("%a · %d %b %Y")}</div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# STAT ROW
# ════════════════════════════════════════════════════════════════════════════
summary = fetch_summary()
s1, s2, s3, s4 = st.columns(4)
stats = [
    (s1, summary.get("total_entries", 0), "Total today", "var(--indigo)"),
    (s2, summary.get("done", 0), "Completed", "var(--green)"),
    (s3, summary.get("active", 0), "In progress", "var(--amber)"),
    (s4, len(summary.get("members_with_blockers", [])), "Blocked", "var(--coral)"),
]
for col, num, label, color in stats:
    with col:
        st.markdown(f"""<div class="glass-stat">
            <div class="glass-stat-num" style="color:{color}">{num}</div>
            <div class="glass-stat-label"><span class="dot" style="background:{color}"></span>{label}</div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TOOLBAR
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-label">Board</div>', unsafe_allow_html=True)
tb1, tb2, tb3 = st.columns([1.3, 1.3, 1.3])
with tb1:
    if st.button("＋  New standup", type="primary", use_container_width=True):
        st.session_state.show_form = not st.session_state.show_form
        st.session_state.edit_id = None
with tb2:
    filter_date = st.date_input("Date", value=date.today(), label_visibility="collapsed")
with tb3:
    filter_status = st.selectbox("Status", ["All", "Active", "Done"], label_visibility="collapsed")


# ════════════════════════════════════════════════════════════════════════════
# CREATE FORM
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.show_form:
    st.markdown('<div class="form-glass">', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1:
        new_name = st.text_input("Name", placeholder="Sudha")
        new_did = st.text_area("Yesterday", placeholder="Shipped the login flow", height=88)
    with f2:
        new_doing = st.text_area("Today", placeholder="Building the API layer", height=88)
        new_blockers = st.text_input("Blockers", placeholder="None")
    if st.button("Post standup", type="primary"):
        if new_name and new_did and new_doing:
            if post_standup(new_name, new_did, new_doing, new_blockers or "None"):
                st.session_state.show_form = False
                st.rerun()
        else:
            st.warning("Name, Yesterday and Today are required.")
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# EDIT FORM
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.edit_id:
    entry = next((d for d in fetch_standups() if d["id"] == st.session_state.edit_id), None)
    if entry:
        st.markdown('<div class="form-glass">', unsafe_allow_html=True)
        e1, e2 = st.columns(2)
        with e1:
            e_did = st.text_area("Yesterday", value=entry["did"], height=88, key="e_did")
            e_doing = st.text_area("Today", value=entry["doing"], height=88, key="e_doing")
        with e2:
            e_blockers = st.text_input("Blockers", value=entry["blockers"], key="e_blockers")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Save changes", type="primary", use_container_width=True):
                put_standup(entry["id"], did=e_did, doing=e_doing, blockers=e_blockers)
                st.session_state.edit_id = None
                st.rerun()
        with c2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.edit_id = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# CARD GRID
# ════════════════════════════════════════════════════════════════════════════
standups = fetch_standups(filter_date=filter_date, status=filter_status)

if not standups:
    st.markdown("""<div class="form-glass" style="text-align:center; color:var(--ink-faint); padding:48px;">
        No standups for this filter yet. Post one above to populate the board.
    </div>""", unsafe_allow_html=True)
else:
    cols = st.columns(3)
    for i, entry in enumerate(standups):
        col = cols[i % 3]
        with col:
            is_done = entry["status"] == "done"
            has_blocker = entry["blockers"].lower() not in ("none", "", "-")
            card_cls = "glass-card is-done" if is_done else "glass-card"
            name_cls = "gc-name is-done" if is_done else "gc-name"
            pill = '<span class="gc-pill pill-done">Done</span>' if is_done else '<span class="gc-pill pill-active">Active</span>'
            blocker_html = f'<span class="gc-blocker">{entry["blockers"]}</span>' if has_blocker else '<span class="gc-clean">No blockers</span>'

            st.markdown(f"""
            <div class="{card_cls}">
                <div class="gc-head">
                    <div class="gc-name-row">
                        <div class="gc-avatar">{initials(entry['name'])}</div>
                        <div class="{name_cls}">{entry['name']}</div>
                    </div>
                    {pill}
                </div>
                <div class="gc-label">Yesterday</div>
                <div class="gc-value">{entry['did']}</div>
                <div class="gc-label">Today</div>
                <div class="gc-value">{entry['doing']}</div>
                <div class="gc-label">Blockers</div>
                <div class="gc-value">{blocker_html}</div>
                <div class="gc-foot">
                    <span class="gc-meta">{entry['date']}</span>
                    <span class="gc-meta">#{entry['id']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("Edit", key=f"e_{entry['id']}", use_container_width=True):
                    st.session_state.edit_id = entry["id"]
                    st.session_state.show_form = False
                    st.rerun()
            with b2:
                if st.button("Undo" if is_done else "Done", key=f"d_{entry['id']}", use_container_width=True):
                    put_standup(entry["id"], status="active" if is_done else "done")
                    st.rerun()
            with b3:
                if st.button("Delete", key=f"x_{entry['id']}", use_container_width=True):
                    delete_standup(entry["id"])
                    st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("**Member lookup**")
    lookup_name = st.text_input("Name", placeholder="Sudha", label_visibility="collapsed")
    if st.button("Search", use_container_width=True):
        if lookup_name:
            try:
                r = requests.get(f"{API}/standup/{lookup_name}", timeout=5)
                if r.status_code == 200:
                    for h in r.json().get("standups", []):
                        with st.expander(f"{h['date']} — {h['status']}"):
                            st.caption(f"Yesterday: {h['did']}")
                            st.caption(f"Today: {h['doing']}")
                            st.caption(f"Blockers: {h['blockers']}")
                else:
                    st.warning("No entries found.")
            except Exception:
                st.error("API unreachable.")

    st.markdown("---")
    st.markdown("**API reference**")
    st.code(
        "POST   /standup\n"
        "GET    /standup\n"
        "GET    /standup/{name}\n"
        "PUT    /standup/{id}\n"
        "DELETE /standup/{id}",
        language=None
    )
    st.caption("Swagger docs → 127.0.0.1:8000/docs")

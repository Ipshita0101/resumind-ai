import streamlit as st
from utils import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import io

st.set_page_config(page_title="ResuMind AI", layout="centered", page_icon="⚡")

# ─────────────────────────────────────────────────────────────────────────────
# PREMIUM UI — Obsidian Terminal Aesthetic
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* ── ROOT VARIABLES ── */
:root {
    --bg:        #080c10;
    --surface:   #0d1117;
    --panel:     #111820;
    --border:    rgba(255,255,255,0.06);
    --accent:    #39ff14;
    --accent2:   #00e5ff;
    --accent3:   #ff3c6e;
    --warn:      #ffb300;
    --text:      #e2e8f0;
    --muted:     #6b7a90;
    --font-head: 'Syne', sans-serif;
    --font-mono: 'Space Mono', monospace;
}

/* ── GLOBAL RESET ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-head);
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 2px; }

/* ── CONTAINER ── */
.block-container {
    max-width: 820px !important;
    padding: 2rem 1.5rem 4rem !important;
    margin: auto;
}

/* ── NOISE OVERLAY ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.35;
}

/* ── HERO HEADER ── */
.hero {
    position: relative;
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 520px; height: 260px;
    background: radial-gradient(ellipse at center,
        rgba(57,255,20,0.12) 0%,
        rgba(0,229,255,0.06) 40%,
        transparent 70%);
    pointer-events: none;
    filter: blur(20px);
}

.hero-label {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.3em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 14px;
    opacity: 0.9;
}

.hero-title {
    font-family: var(--font-head);
    font-size: clamp(42px, 7vw, 68px);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    color: var(--text);
    margin: 0 0 12px;
}

.hero-title span {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-family: var(--font-mono);
    font-size: 13px;
    color: var(--muted);
    letter-spacing: 0.04em;
}

/* ── DIVIDER ── */
.hr {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), var(--accent2), transparent);
    border: none;
    margin: 2rem 0;
    opacity: 0.4;
}

/* ────────────────────────────────────────────────
   RADIO → PILL BUTTONS
   Replaces st.selectbox to avoid Streamlit's
   BaseWeb popup which ignores injected CSS.
   ──────────────────────────────────────────────── */

/* Section label above the pills */
.stRadio > label {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: var(--accent) !important;
    margin-bottom: 12px !important;
    display: block !important;
}

/* Hide the default radio circle dot */
.stRadio > div > label > div:first-child {
    display: none !important;
}

/* Flex row of pills */
.stRadio > div {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    background: transparent !important;
    padding: 0 !important;
}

/* Each individual pill */
.stRadio > div > label {
    background: rgba(57,255,20,0.05) !important;
    border: 1px solid rgba(57,255,20,0.22) !important;
    border-radius: 8px !important;
    padding: 9px 18px !important;
    cursor: pointer !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    color: var(--muted) !important;
    transition: all 0.18s ease !important;
    white-space: nowrap !important;
    user-select: none !important;
    margin: 0 !important;
}

/* Hover state */
.stRadio > div > label:hover {
    background: rgba(57,255,20,0.12) !important;
    border-color: rgba(57,255,20,0.55) !important;
    color: var(--text) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(57,255,20,0.1) !important;
}

/* Selected pill */
.stRadio > div > label:has(input:checked) {
    background: rgba(57,255,20,0.14) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    box-shadow: 0 0 16px rgba(57,255,20,0.2) !important;
    transform: translateY(-1px) !important;
}

/* ── FILE UPLOADER ── */
.stFileUploader > div {
    background: #111820 !important;          ← outer box dark bg
    border: 1px dashed rgba(57,255,20,0.3) !important; ← dashed green border
    border-radius: 12px !important;
    transition: all 0.25s !important;
}
.stFileUploader > div:hover {
    border-color: #39ff14 !important;
    background: rgba(57,255,20,0.04) !important;
    box-shadow: 0 0 24px rgba(57,255,20,0.08) !important;
}

/* ── THE WHITE INNER DROPZONE BOX ── */
[data-testid="stFileUploaderDropzone"] {
    background: rgb(51, 115, 8, 0.2)!important;      ← kills the white fill
    border: none !important;                  ← removes inner border
    border-radius: 0 !important;
    padding: 16px !important;
}

/* ── "Drag and drop file here" text ── */
[data-testid="stFileUploaderDropzone"] p {
    color: rgba(57,255,20,0.6) !important;  ← change drag text colour
    font-family: var(--font-mono) !important;
    font-size: 13px !important;
    letter-spacing: 0.03em !important;
}

/* ── "Limit 200MB · PDF" small text ── */
[data-testid="stFileUploaderDropzone"] small {
    color: white !important;             ← change limit text colour
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
}

/* ── Upload cloud icon ── */
[data-testid="stFileUploaderDropzone"] svg {
    stroke: rgba(57,255,20,0.4) !important;  ← tint the cloud icon
}

/* ── "Browse files" button ── */
[data-testid="baseButton-secondary"] {
    background: rgba(57,255,20,0.08) !important;
    color: #000000 !important;
    border: 1px solid rgba(57,255,20,0.35) !important;
    border-radius: 8px !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    letter-spacing: 0.08em !important;
    transition: all 0.18s !important;
}
[data-testid="baseButton-secondary"]:hover {
    background: rgba(57,255,20,0.18) !important;
    border-color: #39ff14 !important;
    box-shadow: 0 0 14px rgba(57,255,20,0.2) !important;
    transform: translateY(-1px) !important;
}

/* ── SECTION CARD ── */
.r-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 28px 24px;
    margin: 20px 0;
    position: relative;
    overflow: hidden;
}

.r-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: 0.7;
}

.r-card-title {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── SKILL BADGES ── */
.badge-wrap { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }

.badge {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.05em;
    padding: 5px 12px;
    border-radius: 6px;
    background: rgba(57,255,20,0.08);
    border: 1px solid rgba(57,255,20,0.3);
    color: var(--accent);
    display: inline-flex;
    align-items: center;
    gap: 5px;
    transition: all 0.15s;
}

.badge:hover {
    background: rgba(57,255,20,0.16);
    border-color: var(--accent);
    transform: translateY(-1px);
}

.badge .count {
    background: rgba(57,255,20,0.2);
    border-radius: 4px;
    padding: 1px 5px;
    font-size: 10px;
}

/* ── SCORE DISPLAY ── */
.score-ring-wrap {
    display: flex;
    align-items: center;
    gap: 32px;
    margin-top: 8px;
}

.score-big {
    font-family: var(--font-head);
    font-size: 80px;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.04em;
}

.score-label {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 6px;
}

.score-bar-track {
    flex: 1;
    height: 8px;
    background: rgba(255,255,255,0.06);
    border-radius: 99px;
    overflow: hidden;
    margin-top: 8px;
}

.score-bar-fill {
    height: 100%;
    border-radius: 99px;
    box-shadow: 0 0 12px currentColor;
}

/* ── MISSING SKILL ROW ── */
.miss-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    background: rgba(255,60,110,0.07);
    border: 1px solid rgba(255,60,110,0.2);
    border-radius: 10px;
    font-family: var(--font-mono);
    font-size: 12px;
    color: #ff8fa3;
    transition: border-color 0.15s;
}

.miss-row:hover { border-color: rgba(255,60,110,0.5); }
.miss-row .icon { font-size: 14px; flex-shrink: 0; }

/* ── TIP ROWS ── */
.tip-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    border-radius: 10px;
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.5;
}

.tip-info  { background: rgba(0,229,255,0.06);  border: 1px solid rgba(0,229,255,0.2);  color: #80eaff; }
.tip-warn  { background: rgba(255,179,0,0.07);  border: 1px solid rgba(255,179,0,0.25); color: #ffd54f; }
.tip-ok    { background: rgba(57,255,20,0.06);  border: 1px solid rgba(57,255,20,0.25); color: var(--accent); }

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton button {
    width: 100%;
    background: linear-gradient(135deg, rgba(57,255,20,0.12), rgba(0,229,255,0.08)) !important;
    color: var(--accent) !important;
    border: 1px solid rgba(57,255,20,0.4) !important;
    border-radius: 10px !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 14px 20px !important;
    transition: all 0.2s !important;
    font-weight: 700 !important;
}

.stDownloadButton button:hover {
    background: rgba(57,255,20,0.18) !important;
    border-color: var(--accent) !important;
    box-shadow: 0 0 20px rgba(57,255,20,0.2) !important;
    transform: translateY(-1px) !important;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── NATIVE WIDGET FIXES ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    box-shadow: 0 0 10px rgba(57,255,20,0.5) !important;
}

.stAlert {
    border-radius: 10px !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
}

/* ── FORCE TEXT WHITE ── */
label, p, span, div, h1, h2, h3 {
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">⚡ AI-Powered Career Tool</div>
    <div class="hero-title">Resu<span>Mind</span></div>
    <div class="hero-sub">// resume intelligence system v2.0</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ─── ROLE SELECTOR — pill-style radio (replaces selectbox) ───────────────────
# st.radio renders its options as normal DOM labels — fully styleable via CSS,
# no BaseWeb popup portals to fight.
role = st.radio(
    "🎯 Target Role",
    options=[
        "Software Developer",
        "Frontend Developer",
        "Backend Developer",
        "AI Engineer",
        "Data Scientist",
        "UI/UX Designer",
    ],
    horizontal=True,
)

st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

# ─── FILE UPLOADER ────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("📂 Upload Resume (.pdf)", type=["pdf"])

# ─── MAIN ANALYSIS ────────────────────────────────────────────────────────────
if uploaded_file:
    text    = extract_text_from_pdf(uploaded_file)
    skills  = extract_skills(text)
    score   = calculate_score(skills)
    missing = missing_skills(skills, role)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    # ── 1. DETECTED SKILLS ────────────────────────────────────────────────────
    badges_html = "".join(
        f'<span class="badge">{s.title()}<span class="count">{c}</span></span>'
        for s, c in skills.items()
    )

    st.markdown(f"""
    <div class="r-card">
        <div class="r-card-title">◈ &nbsp; Detected Skills</div>
        <div class="badge-wrap">
            {badges_html if badges_html
             else '<span style="color:var(--muted);font-family:var(--font-mono);font-size:12px;">No skills detected.</span>'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 2. ATS SCORE ──────────────────────────────────────────────────────────
    if score < 40:
        score_color   = "var(--accent3)"
        score_verdict = "WEAK RESUME"
        verdict_class = "tip-warn"
        verdict_icon  = "⚠"
        verdict_msg   = "Add more projects and technical depth to strengthen your profile."
    elif score < 70:
        score_color   = "var(--warn)"
        score_verdict = "AVERAGE RESUME"
        verdict_class = "tip-warn"
        verdict_icon  = "◎"
        verdict_msg   = "Improve keyword density and add quantified achievements."
    else:
        score_color   = "var(--accent)"
        score_verdict = "STRONG RESUME"
        verdict_class = "tip-ok"
        verdict_icon  = "✓"
        verdict_msg   = "You're in great shape — polish formatting and tailor per role."

    st.markdown(f"""
    <div class="r-card">
        <div class="r-card-title">◈ &nbsp; ATS Score</div>
        <div class="score-ring-wrap">
            <div>
                <div class="score-big" style="color:{score_color}">
                    {score}<span style="font-size:32px;color:var(--muted)">%</span>
                </div>
                <div class="score-label">{score_verdict}</div>
            </div>
            <div style="flex:1">
                <div style="font-family:var(--font-mono);font-size:10px;color:var(--muted);
                            letter-spacing:.15em;text-transform:uppercase;margin-bottom:8px;">
                    ATS COMPATIBILITY
                </div>
                <div class="score-bar-track">
                    <div class="score-bar-fill"
                         style="width:{score}%; background:{score_color}; color:{score_color};">
                    </div>
                </div>
                <div class="tip-row {verdict_class}" style="margin-top:14px;">
                    <span class="icon">{verdict_icon}</span>
                    <span>{verdict_msg}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 3. SKILL GAPS ─────────────────────────────────────────────────────────
    if missing:
        miss_rows = "".join(
            f'<div class="miss-row"><span class="icon">✕</span><span>{m}</span></div>'
            for m in missing
        )
    else:
        miss_rows = (
            '<div style="font-family:var(--font-mono);font-size:12px;color:var(--accent);">'
            '✓ No skill gaps detected for this role.</div>'
        )

    st.markdown(f"""
    <div class="r-card">
        <div class="r-card-title">◈ &nbsp; Skill Gaps for {role}</div>
        {miss_rows}
    </div>
    """, unsafe_allow_html=True)

    # ── 4. SMART RECOMMENDATIONS ──────────────────────────────────────────────
    tips = []
    if "react" in missing:
        tips.append(("◈", "tip-warn",
                      "Learn React.js — critical for frontend roles. Start with the official docs + a real project."))
    if "tensorflow" in missing:
        tips.append(("◈", "tip-warn",
                      "Add TensorFlow / PyTorch to your stack to unlock AI & ML engineering roles."))
    if "dsa" in missing:
        tips.append(("◈", "tip-warn",
                      "Practice DSA on LeetCode — most SWE interviews test this heavily."))
    if score < 50:
        tips.append(("→", "tip-info",
                      "Boost your score: add certifications, open-source contributions, and quantified results."))
    elif score < 80:
        tips.append(("→", "tip-info",
                      "Level up: tailor resume keywords to each job description for a higher ATS match rate."))
    else:
        tips.append(("✓", "tip-ok",
                      "Great resume! Consider adding a 2-line summary and a personal portfolio link."))

    tip_rows = "".join(
        f'<div class="tip-row {cls}"><span class="icon">{icon}</span><span>{msg}</span></div>'
        for icon, cls, msg in tips
    )

    st.markdown(f"""
    <div class="r-card">
        <div class="r-card-title">◈ &nbsp; Smart Recommendations</div>
        {tip_rows}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    # ── 5. PDF REPORT ─────────────────────────────────────────────────────────
    def generate_pdf():
        buffer = io.BytesIO()
        doc    = SimpleDocTemplate(
            buffer,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )
        styles = getSampleStyleSheet()
        content = [
            Paragraph("ResuMind AI — Resume Report", styles["h1"]),
            Spacer(1, 0.15 * inch),
            Paragraph(f"<b>Target Role:</b> {role}", styles["Normal"]),
            Spacer(1, 0.08 * inch),
            Paragraph(f"<b>ATS Score:</b> {score}% — {score_verdict}", styles["Normal"]),
            Spacer(1, 0.08 * inch),
            Paragraph(
                f"<b>Skills Detected:</b> {', '.join(skills.keys()) if skills else 'None'}",
                styles["Normal"],
            ),
            Spacer(1, 0.08 * inch),
            Paragraph(
                f"<b>Missing Skills:</b> {', '.join(missing) if missing else 'None'}",
                styles["Normal"],
            ),
        ]
        doc.build(content)
        return buffer

    pdf = generate_pdf()

    st.download_button(
        "⬇  Download Full Report (PDF)",
        data=pdf,
        file_name="resumind_report.pdf",
        mime="application/pdf",
    )

else:
    # ── EMPTY STATE ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding:3rem 0; opacity:0.4;">
        <div style="font-size:48px; margin-bottom:16px;">⬆</div>
        <div style="font-family:var(--font-mono); font-size:12px;
                    letter-spacing:.2em; text-transform:uppercase; color:var(--muted);">
            Upload your resume to begin analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

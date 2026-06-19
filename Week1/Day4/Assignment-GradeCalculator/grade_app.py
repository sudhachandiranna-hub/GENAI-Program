"""
grade_app.py
A small Streamlit app that converts a numeric mark (0-100) into a letter grade.

Run with:
    streamlit run grade_app.py
"""

import random

import streamlit as st

# ---------------------------------------------------------------------------
# Pure Python grading logic (no Streamlit dependencies — easy to test/reuse)
# ---------------------------------------------------------------------------

GRADE_SCALE = [
    (90, 100, "A"),
    (80, 89, "B"),
    (70, 79, "C"),
    (60, 69, "D"),
    (0, 59, "E"),
]

# Visual + copy metadata per grade.
GRADE_META = {
    "A": {"bg": "#dcfce7", "text": "#15803d", "label": "Excellent"},
    "B": {"bg": "#dbeafe", "text": "#1d4ed8", "label": "Good"},
    "C": {"bg": "#fef3c7", "text": "#b45309", "label": "Satisfactory"},
    "D": {"bg": "#ffedd5", "text": "#c2410c", "label": "Needs improvement"},
    "E": {"bg": "#fee2e2", "text": "#b91c1c", "label": "Below passing"},
}

MOTIVATIONAL_MESSAGES = [
    "One mark doesn't define your ability. Figure out what tripped you up, and go again.",
    "This is feedback, not a verdict. Identify the gap, close it, and re-test.",
    "Every strong result starts with a rough one. Use this to target your next study session.",
    "Setbacks are data. Review what went wrong, adjust your approach, and come back stronger.",
]


def get_grade(mark: float) -> str:
    """Convert a mark (0-100, inclusive) into a letter grade.

    Raises ValueError if mark is outside the 0-100 range.
    """
    if mark < 0 or mark > 100:
        raise ValueError("Mark must be between 0 and 100.")

    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


def fire_confetti() -> None:
    """Launch a confetti burst over the whole app window, not just a small iframe.

    Injects canvas-confetti into the PARENT document (the actual Streamlit page)
    so the animation covers the full viewport instead of being clipped to this
    component's own (zero-size) iframe.
    """
    st.iframe(
        """
        <script>
        (function () {
            function shoot() {
                var c = window.parent.confetti;
                if (!c) return;
                c({ particleCount: 140, spread: 80, origin: { y: 0.6 },
                    colors: ['#16a34a', '#6366f1', '#f59e0b', '#ec4899'] });
                c({ particleCount: 60, angle: 60, spread: 70, origin: { x: 0, y: 0.7 } });
                c({ particleCount: 60, angle: 120, spread: 70, origin: { x: 1, y: 0.7 } });
            }
            if (window.parent.confetti) {
                shoot();
            } else {
                var s = window.parent.document.createElement('script');
                s.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js';
                s.onload = shoot;
                window.parent.document.body.appendChild(s);
            }
        })();
        </script>
        """,
        height=1,
    )


# ---------------------------------------------------------------------------
# Page setup + Linear / Stripe / Figma–style theming
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Mark to Grade Converter", page_icon="🎓", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    [data-testid="stAppViewContainer"] { background: #fafafa; }

    .block-container {
        max-width: 600px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    .app-title {
        font-size: 1.9rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        font-size: 0.98rem;
        color: #64748b;
        margin-bottom: 1.75rem;
    }

    .card {
        background: #ffffff;
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 16px;
        padding: 1.75rem 1.75rem 1.5rem;
        box-shadow: 0 1px 2px rgba(15,23,42,0.04), 0 8px 24px rgba(15,23,42,0.05);
        margin-bottom: 1.25rem;
    }

    .field-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #94a3b8;
        margin-bottom: 0.4rem;
    }

    div[data-testid="stNumberInput"] input {
        border-radius: 10px !important;
        border: 1px solid rgba(15, 23, 42, 0.12) !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #0f172a !important;
        padding: 0.55rem 0.75rem !important;
    }

    div[data-testid="stNumberInput"] input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
        border: none;
        box-shadow: 0 1px 2px rgba(15,23,42,0.04);
    }

    .result-row {
        display: flex;
        align-items: center;
        gap: 1.1rem;
    }

    .grade-badge {
        flex-shrink: 0;
        width: 64px;
        height: 64px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: 800;
    }

    .result-mark {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 0.1rem;
    }

    .result-label {
        font-size: 1.2rem;
        font-weight: 700;
    }

    .motivation-card {
        background: #eef2ff;
        border: 1px solid rgba(99, 102, 241, 0.18);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        color: #3730a3;
        font-size: 0.95rem;
        font-weight: 500;
        margin-top: 1rem;
    }

    .empty-card {
        color: #64748b;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-title">🎓 Mark to Grade Converter</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Enter a mark between 0 and 100 to see the matching letter grade.</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

#   st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="field-label">Mark</div>', unsafe_allow_html=True)
mark = st.number_input(
    "Mark",
    min_value=-1000,   # intentionally wider than 0-100 so out-of-range entries
    max_value=1000,    # can be caught and handled gracefully below, not blocked
    value=None,
    step=1,
    placeholder="e.g. 85",
    format="%d",
    label_visibility="collapsed",
)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------

if mark is None:
    st.markdown(
        '<div class="card empty-card">👆 Enter a mark above to see your grade.</div>',
        unsafe_allow_html=True,
    )
elif mark < 0 or mark > 100:
    st.warning(f"⚠️ **{mark:.0f}** is not a valid mark. Please enter a number between 0 and 100.")
else:
    grade = get_grade(mark)
    meta = GRADE_META[grade]

    st.markdown(
        f"""
        <div class="card">
            <div class="result-row">
                <div class="grade-badge" style="background:{meta['bg']}; color:{meta['text']};">
                    {grade}
                </div>
                <div>
                    <div class="result-mark">Mark entered: {mark:.0f} / 100</div>
                    <div class="result-label" style="color:{meta['text']};">{meta['label']}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if grade == "A":
        fire_confetti()

    if grade == "E":
        message = random.choice(MOTIVATIONAL_MESSAGES)
        st.markdown(f'<div class="motivation-card">💪 {message}</div>', unsafe_allow_html=True)

with st.expander("See the full grading scale"):
    st.table(
        {
            "Mark range": ["90 - 100", "80 - 89", "70 - 79", "60 - 69", "Below 60"],
            "Grade": ["A", "B", "C", "D", "E"],
        }
    )

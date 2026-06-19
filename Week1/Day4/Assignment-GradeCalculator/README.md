# Mark to Grade Converter

A small Streamlit web app that converts a numeric mark (0–100) into a letter grade, with a clean, Linear/Stripe/Figma-inspired UI.

## Grading scale

| Mark range | Grade |
|---|---|
| 90 – 100 | A |
| 80 – 89 | B |
| 70 – 79 | C |
| 60 – 69 | D |
| Below 60 | E |

Boundaries are inclusive (90 = A, 80 = B, etc.).

## Requirements

- Python 3.8+
- Streamlit

## Setup

```bash
# create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# install dependencies
pip install streamlit
```

## Run

```bash
streamlit run grade_app.py
```

This opens the app in your browser at `http://localhost:8501`.

## Usage

1. Enter a mark in the number input (or leave it empty).
2. The app displays the mark and its corresponding grade.
3. The grading scale is available under "See the full grading scale".

## UI details

- Card-based layout, Inter font, indigo accent, color-coded grade badge — modeled on Linear/Stripe/Figma design conventions.
- **Grade A** — confetti animation fires across the full page.
- **Grade E** — a supportive, action-oriented message is shown alongside the result (not just the grade).
- Grading scale reference table is tucked into an expander so the main view stays uncluttered.

## Edge cases

- **Empty input** — neutral prompt to enter a mark; no crash.
- **Mark below 0 or above 100** — shown as a `st.warning` alert (yellow, with icon), not a hard error; no crash.
- **Valid mark (0–100)** — shows the mark, grade, and grade-specific styling/behavior above.

## Files

- `grade_app.py` — single-file app: pure-Python `get_grade()` grading logic plus the Streamlit UI.

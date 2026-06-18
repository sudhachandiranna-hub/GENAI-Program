# GENAI-Program

## Daily workflow

- Every day at 6:00 AM, `scripts/create_day_folder.py` runs automatically and creates the next `WeekN/DayM/Assignment` and `WeekN/DayM/Practice` folders (7 days per week, state tracked in `.tracker.json`). Drop that day's work into those two folders.
- When you say **PUSH** to Claude, it runs `scripts/push_day.py`, which: writes that day's `README.md`, commits with a message built from the Assignment folder's filenames, and attempts `git push origin main`.
- Known limitation: the automated push only succeeds from an environment that already has GitHub push credentials. If it reports `push_ok: false`, the commit is still made locally -- run `git push origin main` once from a machine/session that's authenticated to this repo to finish sending it.

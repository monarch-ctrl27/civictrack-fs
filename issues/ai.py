"""
AI-assisted categorisation for incoming reports.

This is intentionally a small, transparent, dependency-free classifier so
the project runs anywhere Django runs. It looks for category keywords in
the report description and picks the category with the most matches.

For a production deployment, swap `suggest_category` for a call to a
trained NLP/ML model (e.g. a fine-tuned transformer, spaCy text
classifier, or a hosted classification API) — the view code in
`views.py` only depends on this function returning a category id or
None, so the rest of the app does not need to change.
"""
from .constants import CATEGORIES


def suggest_category(text):
    """Return the best-matching category id for `text`, or None.

    Returns None when the text is too short to judge, or when no
    category keywords are found (the caller should fall back to
    "Other / Service Delivery" in that case).
    """
    if not text:
        return None
    normalised = text.lower()
    if len(normalised.strip()) < 8:
        return None

    best_id = None
    best_hits = 0
    for category in CATEGORIES:
        hits = sum(1 for keyword in category["keywords"] if keyword in normalised)
        if hits > best_hits:
            best_hits = hits
            best_id = category["id"]

    return best_id

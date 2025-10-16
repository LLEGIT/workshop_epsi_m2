# backend/nlu.py
import re
from difflib import SequenceMatcher

# Primary spell list (at least 8)
SPELLS = [
    "Expelliarmus",
    "Lumos",
    "Nox",
    "Wingardium Leviosa",
    "Alohomora",
    "Accio",
    "Expecto Patronum",
    "Avada Kedavra"
]

# Basic normalization: lowercase, strip punctuation, replace accented chars if any


def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    # remove common punctuation
    text = re.sub(r"[^\w\s]", " ", text)
    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

# fuzzy ratio using SequenceMatcher


def fuzzy_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

# match_spell returns (matched_bool, score, canonical_spell)


def match_spell(normalized_text: str, threshold: float = 0.6):
    best = ("", 0.0)
    for s in SPELLS:
        s_norm = normalize_text(s)
        # try direct contains first
        if s_norm in normalized_text:
            return True, 1.0, s
        # otherwise fuzzy compare tokens
        # compute best token vs spell fuzzy
        for token in normalized_text.split():
            score = fuzzy_ratio(token, s_norm)
            if score > best[1]:
                best = (s, score)
    if best[1] >= threshold:
        return True, best[1], best[0]
    return False, best[1], None

# optional simple pronunciation score (distance between recognized and target)


def compute_pronunciation_score(target_spell: str, recognized: str) -> float:
    # normalized
    t = normalize_text(target_spell)
    r = normalize_text(recognized)
    # simple token-level similarity
    return fuzzy_ratio(t, r)

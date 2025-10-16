#!/usr/bin/env python3
# analyse_hp_spacy_v3.py
# Version améliorée pour Harry Potter (7 tomes)
# - Harry cicatrice : détection étendue
# - Actes illégaux : pondération majeur / mineur
# - Corrélations + heatmap
# - Traitement chunks pour longs textes

import os
import math
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy

# ----------------------------
# Config
# ----------------------------
BOOKS = [
    ("01_HP_PhilosophersStone", "Harry Potter à l’école des sorciers"),
    ("02_HP_ChamberOfSecrets", "Harry Potter et la Chambre des secrets"),
    ("03_HP_PrisonerOfAzkaban", "Harry Potter et le Prisonnier d’Azkaban"),
    ("04_HP_GobletOfFire", "Harry Potter et la Coupe de feu"),
    ("05_HP_OrderOfPhoenix", "Harry Potter et l’Ordre du Phénix"),
    ("06_HP_HalfBloodPrince", "Harry Potter et le Prince de sang-mêlé"),
    ("07_HP_DeathlyHallows", "Harry Potter et les Reliques de la Mort"),
]

BOOK_DIR = Path("books")
OUT_DIR = Path("output")
OUT_DIR.mkdir(exist_ok=True)

# ----------------------------
# Modèle spaCy
# ----------------------------
try:
    nlp = spacy.load("fr_core_news_md")
except OSError:
    nlp = spacy.load("fr_core_news_sm")
nlp.max_length = 2_000_000  # autoriser textes longs

# ----------------------------
# Listes de verbes / adjectifs
# ----------------------------
verbs_cicatrice = {"toucher", "brûler", "picoter",
                   "faire", "faire mal", "piquer", "hurter"}
verbs_dumbledore = {"dire", "mentir", "planifier", "cacher", "organiser",
                    "modifier", "changer", "conceal", "plan", "hide", "change"}
verbs_illegal_major = {"tuer", "crucio", "imperio",
                       "avada", "assassiner", "violence", "kill", "murder"}
verbs_illegal_minor = {"mentir", "trahir", "voler", "steal", "betray"}
adj_rogue = {"mystérieux", "sombre", "menaçant", "suspect",
             "secret", "dark", "threatening", "secretive"}

# ----------------------------
# Fonctions utilitaires
# ----------------------------


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def estimate_pages(text: str, words_per_page=300):
    return max(1, math.ceil(len([t for t in text.split() if t.isalpha()]) / words_per_page))

# ----------------------------
# Analyse d'un livre
# ----------------------------


def analyze_book(title, text):
    chunk_size = 60_000
    stats = dict(
        Harry_touche_scar=0, Hermione_mais=0, Dumbledore_mod=0,
        Rogue_mysterieux=0, Acts_illegaux=0,
        Harry_lines=0, Hermione_lines=0, Ron_lines=0
    )

    for i in range(0, len(text), chunk_size):
        doc = nlp(text[i:i+chunk_size])
        for sent in doc.sents:
            s = sent.text.lower()

            # Harry + cicatrice
            if "harry" in s and ("cicatrice" in s or "scar" in s):
                if any(v in s for v in verbs_cicatrice):
                    stats["Harry_touche_scar"] += 1

            # Hermione + "Mais"
            if "hermione" in s and "mais" in s.split()[:3]:
                stats["Hermione_mais"] += 1

            # Dumbledore manipule
            if "dumbledore" in s and any(v in s for v in verbs_dumbledore):
                stats["Dumbledore_mod"] += 1

            # Rogue mystérieux
            if any(x in s for x in ["rogue", "snape", "severus"]) and any(a in s for a in adj_rogue):
                stats["Rogue_mysterieux"] += 1

            # Actes illégaux pondérés
            major_count = sum(1 for v in verbs_illegal_major if v in s)
            minor_count = sum(0.3 for v in verbs_illegal_minor if v in s)
            stats["Acts_illegaux"] += major_count + minor_count

            # Prises de parole
            if "harry" in s and "dit" in s:
                stats["Harry_lines"] += 1
            if "hermione" in s and "dit" in s:
                stats["Hermione_lines"] += 1
            if "ron" in s and "dit" in s:
                stats["Ron_lines"] += 1

    pages = estimate_pages(text)
    stats["Pages"] = pages
    stats["Book"] = title

    # ratios normalisés
    for k in ["Harry_touche_scar", "Hermione_mais", "Dumbledore_mod", "Rogue_mysterieux", "Acts_illegaux"]:
        stats[f"Ratio_{k}/page"] = stats[k] / pages

    return stats

# ----------------------------
# Programme principal
# ----------------------------


def main():
    results = []
    for key, title in BOOKS:
        path = BOOK_DIR / f"{key}.txt"
        if not path.exists():
            print(f"❌ Livre manquant : {title}")
            continue
        print(f"📘 Analyse de {title}...")
        text = load_text(path)
        res = analyze_book(title, text)
        results.append(res)

    df = pd.DataFrame(results)
    df.to_csv(OUT_DIR / "harrypotter_spacy_v3.csv", index=False)
    print("✅ Résultats sauvegardés dans output/harrypotter_spacy_v3.csv")

    # ----------------------------
    # Graphiques
    # ----------------------------
    plt.figure(figsize=(10, 5))
    plt.plot(df["Book"], df["Harry_touche_scar"],
             marker='o', label="Harry touche sa cicatrice")
    plt.plot(df["Book"], df["Rogue_mysterieux"],
             marker='s', label="Rogue mystérieux")
    plt.plot(df["Book"], df["Dumbledore_mod"],
             marker='^', label="Dumbledore manipule")
    plt.plot(df["Book"], df["Acts_illegaux"],
             marker='x', label="Actes illégaux pondérés")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / "harrypotter_tendances_v3.png")
    print("📊 Graphique enregistré dans output/harrypotter_tendances_v3.png")

    # ----------------------------
    # Heatmap corrélations
    # ----------------------------
    corr_cols = ["Harry_touche_scar", "Hermione_mais", "Dumbledore_mod",
                 "Rogue_mysterieux", "Acts_illegaux", "Harry_lines",
                 "Hermione_lines", "Ron_lines"]
    corr = df[corr_cols].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Corrélations entre métriques Harry Potter")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "harrypotter_corr_v3.png")
    print("📊 Heatmap enregistrée dans output/harrypotter_corr_v3.png")


if __name__ == "__main__":
    main()

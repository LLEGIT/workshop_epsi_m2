# harry_potter_analysis_fr_enriched.py
import spacy
from spacy.matcher import Matcher
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Charger le modèle français
nlp = spacy.load("fr_core_news_sm")

# ----------------------
# Lexiques enrichis
# ----------------------

# Noms / substantifs / racines (lowercase)
illegal_nouns = [
    "vol", "cambriolage", "effraction", "agression", "assassinat", "meurtre",
    "empoisonnement", "sabotage", "fraude", "escroquerie", "extorsion",
    "enlèvement", "kidnapping", "vandalisme", "chantage", "corruption",
    "intrusion", "piratage", "intrus", "intrusion", "violation"
]

illegal_verbs = [
    "voler", "dérober", "cambrioler", "forcer", "attaquer", "blesser", "tuer",
    "assassiner", "empoisonner", "sabot er".replace(
        " ", ""),  # safety: corrected below
    "sabot er".replace(" ", ""),  # harmless no-op to avoid linter weirdness
    "sabot er".replace(" ", ""),
    "saboter", "frauder", "escroquer", "extorquer", "enlever", "kidnapper",
    "vandaliser", "faire du chantage", "corrompre", "pirater", "intruser",
    "harceler", "intimider", "menacer", "espionner", "tromper", "tricher",
    "mentir", "dénoncer"  # dénoncer peut être légal mais parfois abusif
]

# nettoyage du doublon introduit par l'éditeur précédent
illegal_verbs = [v for v in illegal_verbs if v]

immoral_words = [
    "mensonge", "mensonge", "calomnie", "diffamation", "manipulation",
    "manipuler", "tromperie", "trahison", "exploitation", "abuser", "abuse",
    "délation", "dénonciation", "déloyal", "déloyauté"
]

# mots “dark” / adjectifs et verbes associés (pour Rogue ou scène sombre)
dark_adjectives = [
    "mystérieux", "mystérieuse", "sombre", "sinistre", "menaçant", "menaçante",
    "glacial", "glaciale", "impénétrable", "machiavélique", "ténébreux",
    "lugubre", "cruel", "cruelle", "perfide", "ambigu", "ambiguë", "inquiétant",
    "inquiétante", "obsédant", "hostile", "méprisable", "froid", "féroce"
]

dark_verbs = [
    "menacer", "intimider", "tourmenter", "traquer", "espionner", "hant er".replace(
        " ", ""),
    "hant er".replace(" ", "")
]
dark_verbs = [v for v in dark_verbs if v]  # sanity

# verbes de prise de parole (pour détecter qui parle via dépendances)
speaking_verbs = [
    "dire", "répondre", "crier", "prononcer", "chuchoter", "annoncer",
    "répliquer", "répondre", "s'exclamer", "rétorquer", "murmurer",
    "déclarer", "ajouter"
]

# quelques formes alternatives pour dialogues (guillemets, tiret cadratin)
quote_markers = ["«", "»", "“", "”", "\"", "—", "–", "-"]

# ----------------------
# Helper functions
# ----------------------


def load_book(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # normalisation basique
    text = text.replace("\r", "").replace("\r\n", "\n")
    # enlever pages vides superflues
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def split_into_chunks(text, chunk_size_words=5000):
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size_words])
              for i in range(0, len(words), chunk_size_words)]
    return chunks

# -----------------------------------------------------
# Détection à phrase/chunk basée sur lemmas + matcher
# -----------------------------------------------------


matcher = Matcher(nlp.vocab)

# build patterns for illegal nouns (simple: token with lemma in set)
# Note: we'll use lemma comparison in sentence-level logic, not pure matcher here.


def sentence_contains_lemma(sent, lemma_set):
    for tok in sent:
        if tok.lemma_.lower() in lemma_set:
            return True
    return False


def sentence_contains_word_text(sent, word_set):
    txt = sent.text.lower()
    for w in word_set:
        if w in txt:
            return True
    return False


def count_harry_cicatrice(doc):
    """Compter phrases où Harry touche/ressent sa cicatrice (FR)."""
    patterns_verbs = {"toucher", "ressentir",
                      "sentir", "brûler", "picoter", "faire mal"}
    count = 0
    for sent in doc.sents:
        s = sent.text.lower()
        if "harry" in s and "cicatrice" in s:
            # vérifier la présence d'un verbe pertinent dans la phrase (lemme)
            if sentence_contains_lemma(sent, patterns_verbs) or any(v in s for v in patterns_verbs):
                count += 1
    return count


def count_dialogues_improved(doc, character):
    """
    Détection améliorée de prises de parole : 
    - phrase commençant par "Nom:" 
    - ou phrase contenant guillemets et le nom proche d'un guillemet
    - ou phrase où le verbe de parole a pour sujet le personnage (approximatif)
    """
    char = character.lower()
    count = 0
    for sent in doc.sents:
        text_l = sent.text.lower().strip()
        # 1) Forme "Hermione:" ou "Hermione —"
        if re.match(rf"^{re.escape(character)}\s*[:—\-]", sent.text, flags=re.IGNORECASE):
            count += 1
            continue
        # 2) guillemets — si phrase contient guillemets, chercher si le nom apparaît dans la même phrase
        if any(g in sent.text for g in quote_markers):
            if char in text_l:
                count += 1
                continue
        # 3) dépendances : si un verbe de parole est présent et a comme sujet le personnage
        for tok in sent:
            if tok.lemma_.lower() in speaking_verbs:
                # regarder sujet dans enfants
                for child in tok.children:
                    if child.lemma_.lower() == char or child.text.lower() == char:
                        count += 1
                        break
                else:
                    # essayer head-subj relation (approx)
                    if tok.head and (tok.head.lemma_.lower() == char or tok.head.text.lower() == char):
                        count += 1
                        break
        # petite heuristique: "— Harry dit" ou "Harry dit :" déjà géré mais au cas où :
        if re.search(rf"\b{re.escape(char)}\b\s+\b({'|'.join(speaking_verbs)})\b", text_l):
            count += 1
    return count


def count_dumbledore_influence(doc):
    verbs = {"ordonner", "demander", "convaincre", "intervenir",
             "manipuler", "commander", "ordonner", "insister"}
    count = 0
    for sent in doc.sents:
        s = sent.text.lower()
        if "dumbledore" in s:
            if sentence_contains_lemma(sent, verbs) or sentence_contains_word_text(sent, verbs):
                count += 1
    return count


def count_rogue_dark(doc):
    """Cherche phrases où 'Rogue' est relié à des adjectifs/verbres 'dark'."""
    count = 0
    for sent in doc.sents:
        s = sent.text.lower()
        if "rogue" in s or "severus" in s:  # parfois "Severus Rogue"
            # si adjectif dark dans phrase (texte) ou verbe dark en lemma
            if sentence_contains_word_text(sent, dark_adjectives) or sentence_contains_lemma(sent, set(dark_verbs)):
                count += 1
    return count


def count_illegal_or_immoral(doc):
    """Compte les phrases contenant des actes illégaux ou moralement répréhensibles."""
    count = 0
    # union de lemmas pour comparaisons
    illegal_lemmas = set([w.lower()
                         for w in illegal_nouns + illegal_verbs + immoral_words])
    for sent in doc.sents:
        # cas 1: lemma match (verbes/substantifs)
        if sentence_contains_lemma(sent, illegal_lemmas):
            count += 1
            continue
        # cas 2: mot exact dans texte (pour multi-mots ou expressions)
        txt = sent.text.lower()
        # expressions longues
        multi_expr = ["sortilège interdit", "sors interdit",
                      "sort interdit", "utiliser un sortilège interdit"]
        if any(expr in txt for expr in multi_expr):
            count += 1
            continue
        # 3) verbes + objet : heuristique simple (verbe illégal présent + complément)
        if any(v in txt for v in illegal_verbs) and any(n in txt for n in ["vol", "mensonge", "tricher", "attaque", "sabot", "empoison"]):
            count += 1
            continue
    return count

# ----------------------
# Pipeline principal
# ----------------------


def analyze_books(book_paths, chunk_size_words=5000):
    all_stats = []
    for i, book_path in enumerate(book_paths, 1):
        print(f"Analyse du livre {i} -> {book_path}")
        text = load_book(book_path)
        chunks = split_into_chunks(text, chunk_size_words)
        for j, chunk in enumerate(chunks, 1):
            doc = nlp(chunk)
            all_stats.append({
                "Livre": i,
                "Chunk": j,
                "Harry_cicatrice": count_harry_cicatrice(doc),
                # heuristique
                "Hermione_mais": sentence_contains_word_text(doc[:1], {"mais"}) and count_dialogues_improved(doc, "Hermione"),
                "Dumbledore_influence": count_dumbledore_influence(doc),
                "Rogue_dark": count_rogue_dark(doc),
                "Paroles_Harry": count_dialogues_improved(doc, "Harry"),
                "Paroles_Hermione": count_dialogues_improved(doc, "Hermione"),
                "Paroles_Ron": count_dialogues_improved(doc, "Ron"),
                "Actes_illegaux": count_illegal_or_immoral(doc)
            })
    df = pd.DataFrame(all_stats)
    return df


# Exemple d'usage (adapte les chemins si nécessaire)
if __name__ == "__main__":
    books = [f"data/harry_potter_{i}.txt" for i in range(1, 8)]
    df = analyze_books(books, chunk_size_words=5000)

    # normalisation par 1000 mots (chunk ~5000 mots)
    for col in ["Harry_cicatrice", "Dumbledore_influence", "Rogue_dark",
                "Paroles_Harry", "Paroles_Hermione", "Paroles_Ron", "Actes_illegaux"]:
        df[col + "_per1000words"] = df[col] / 5.0

    # agrégat par livre
    total_stats = df.groupby("Livre").sum()

    # visualisations simples
    sns.lineplot(data=total_stats[["Harry_cicatrice",
                                   "Dumbledore_influence", "Actes_illegaux"]])
    plt.title("Évolution des événements par livre")
    plt.ylabel("Nombre total (par chunk)")
    plt.savefig("evolution_evenements.png")  # <-- sauvegarde
    plt.close()  # ferme la figure pour libérer la mémoire

    total_stats[["Paroles_Harry", "Paroles_Hermione",
                "Paroles_Ron"]].plot(kind="bar")
    plt.title("Prises de parole par personnage")
    plt.savefig("dialogues_personnages.png")
    plt.close()

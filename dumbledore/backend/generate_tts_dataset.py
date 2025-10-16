# backend/generate_tts_dataset.py
import os
import csv
import pyttsx3


def generate_pyttsx3(out_dir="dataset", per_spell=5):
    spells = [
        "Expelliarmus", "Lumos", "Nox", "Wingardium Leviosa",
        "Alohomora", "Accio", "Expecto Patronum", "Avada Kedavra"
    ]

    os.makedirs(out_dir, exist_ok=True)

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    samples = []
    rate_list = [140, 150, 160, 170]  # vitesses différentes

    for idx, spell in enumerate(spells):
        for i in range(per_spell):
            fname = f"{idx}_{spell.replace(' ', '_')}_{i}.mp3"
            path = os.path.join(out_dir, fname)

            # choisir voix et vitesse
            voice = voices[i % len(voices)]
            engine.setProperty('voice', voice.id)
            engine.setProperty('rate', rate_list[i % len(rate_list)])

            # sauvegarde fichier audio
            engine.save_to_file(spell, path)
            engine.runAndWait()  # ⚠️ doit être appelé pour chaque fichier

            samples.append((fname, spell))

    # créer le CSV labels
    with open(os.path.join(out_dir, "labels.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "label"])
        writer.writerows(samples)

    print(f"✅ Dataset généré : {len(samples)} fichiers dans '{out_dir}'")


if __name__ == "__main__":
    generate_pyttsx3()

# app.py
import os
import tempfile
import subprocess
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import whisper

# ---------------------------------------------
# ⚙️ Configuration générale
# ---------------------------------------------
app = FastAPI(title="Magic Spell Voice Recognition")

# Autoriser le frontend React ou statique
app.add_middleware(
    CORSMiddleware,
    # à restreindre si besoin (ex: ["http://localhost:5173"])
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------
# 📁 Servir le frontend (build React ou dossier public/)
# ---------------------------------------------
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "../frontend/dist")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR,
              html=True), name="frontend")
    print(f"✅ Frontend servi depuis : {FRONTEND_DIR}")
else:
    print("⚠️ Aucun build frontend trouvé — lance `npm run build` côté frontend.")

# ---------------------------------------------
# 🧠 Chargement du modèle Whisper (léger, CPU-friendly)
# ---------------------------------------------
print("🪄 Chargement du modèle Whisper (tiny)...")
model = whisper.load_model("base")  # ou "base" pour plus de précision

# ---------------------------------------------
# 🪄 Liste des sorts connus
# ---------------------------------------------
SPELLS = {
    "expelliarmus": "Sort de désarmement !",
    "lumos": "Une lumière jaillit de votre baguette ! 💡",
    "nox": "La lumière s’éteint doucement. 🌑",
    "wingardium leviosa": "Les objets se soulèvent dans les airs ! 🪄",
    "alohomora": "La porte s’ouvre lentement... 🚪",
    "accio": "Un objet fonce vers vous à toute vitesse ! 🪶",
    "expecto patronum": "Un Patronus majestueux apparaît ! ✨",
    "avada kedavra": "Un éclair vert jaillit de votre baguette... 💀"
}

# ---------------------------------------------
# 🧩 Fonction de reconnaissance du sort
# ---------------------------------------------


def recognize_spell(transcription: str) -> str:
    import difflib
    text = transcription.lower().strip()
    best_match = difflib.get_close_matches(
        text, SPELLS.keys(), n=1, cutoff=0.6)
    if best_match:
        spell = best_match[0]
        return f"🪄 {spell.title()} détecté : {SPELLS[spell]}"
    else:
        return "❓ Sort inconnu du registre magique..."

# ---------------------------------------------
# 🎙️ Endpoint principal : transcription + détection
# ---------------------------------------------


@app.post("/api/transcribe")
async def transcribe_audio(
    file: UploadFile = File(None),
    audio: UploadFile = File(None),
    user_id: str = Form(None)
):
    try:
        upload = file or audio  # accepte 'file' ou 'audio'
        if not upload:
            return {"error": "Aucun fichier reçu — clé attendue : 'file' ou 'audio'"}

        # 🔄 Sauvegarde temporaire
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
            tmp.write(await upload.read())
            tmp.flush()
            webm_path = tmp.name
            wav_path = tmp.name + ".wav"

        # 🎧 Conversion webm → wav
        subprocess.run(
            ["ffmpeg", "-y", "-i", webm_path, wav_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        result = model.transcribe(wav_path)
        transcription = result.get("text", "").strip()
        response = recognize_spell(transcription)

        os.remove(webm_path)
        os.remove(wav_path)

        print(f"✅ Transcription: {transcription} (user_id={user_id})")
        return {"transcription": transcription, "result": response, "user_id": user_id}

    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------
# 🚀 Lancer le serveur
# ---------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Magic Spell Voice Recognition

## Requirements
- Python 3.10+
- ffmpeg (if using local whisper)
- Node not required for the single-file frontend, but recommended for a full React app.

## Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Option A: Use OpenAI Whisper API (recommended for accuracy)
export OPENAI_API_KEY="sk-..."

# Option B: Use local whisper
export USE_LOCAL_WHISPER=true
pip install -U openai-whisper

# Run
python app.py
# server accessible at http://localhost:8000

## Frontend
Open frontend/public/index.html in the browser (or serve with a static server).
Click "Lancer le sort", speak, and stop to send audio to the backend.

## Dataset
python generate_tts_dataset.py

# Generative AI Assistant for Technical Debugging

A RAG-based AI assistant for roller-bearing fault diagnosis. Paste a log snippet or sensor reading and receive a structured JSON diagnosis.

## Phase 1 — Baseline Assistant (no RAG)

A thin chat loop that calls OpenAI and returns a structured JSON diagnosis with:

- **symptoms_detected** — observable anomalies from the input
- **top_fault_hypotheses** — ranked list of likely faults
- **evidence_needed** — additional data that would help narrow the diagnosis
- **next_tests** — concrete, actionable diagnostic steps
- **confidence** — 0–1 score for the top hypothesis

### Quick Start

```bash
# 1. Create and activate the conda environment
conda create -n debug-assistant python=3.11 -y
conda activate debug-assistant

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your OpenAI API key
cp .env.example .env
# Edit .env and paste your key

# 4. Run the server
uvicorn app.main:app --reload

# 5. Open http://localhost:8000 in your browser
```

### API Usage

```bash
curl -X POST http://localhost:8000/diagnose \
  -H "Content-Type: application/json" \
  -d '{"log_snippet": "Vibration sensor #3: RMS velocity = 12.8 mm/s (threshold 7.0)"}'
```

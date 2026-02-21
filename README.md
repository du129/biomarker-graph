# BioNutriGraph (Food-Biomarker Insight Graph)

An interactive, scientifically-grounded web application that maps foods to human biomarkers. Users can explore how specific foods impact biomarkers (e.g., LDL, Glucose) based on peer-reviewed literature.

## Project Structure
- `frontend/`: React + Vite + Tailwind CSS application.
- `backend/`: FastAPI application + Neo4j (optional) + AI Ingestion.

## Architecture
- **Frontend**: Force-directed graph visualization using `react-force-graph`.
- **Backend API**: FastAPI serving graph data. 
    - *Note*: Currently running in "Mock Mode" using static JSON data (`mvp_dataset.json`) as Neo4j requires Docker/Cloud setup.
- **AI Pipeline**: Scripts to ingest scientific papers and extract relationships using GPT-4o.

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- Docker (optional, for Neo4j)

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Access at `http://localhost:5173`

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```
Access API at `http://localhost:8000`

### AI Data Ingestion (Optional)
Requires `OPENAI_API_KEY` environment variable.
```bash
export OPENAI_API_KEY=sk-...
python ingest.py path/to/study.pdf
```

## Features
- **Interactive Graph**: Visualize connections between foods and biomarkers.
- **Evidence HUD**: Click a node to see detailed scientific evidence, confidence scores, and citations.
- **Search**: Quickly find specific nutrients or health markers.

## Roadmap Status
- [x] Phase 1: Architecture & Prototype
- [x] Phase 2: Interactive UI (HUD, Evidence Cards)
- [x] Phase 3: Backend API (JSON Mock implemented)
- [x] Phase 4: AI Ingestion Scripts
- [ ] Phase 5: Neo4j Integration (Pending Docker/Cloud)

import json
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="BioNutriGraph API")

# Comma-separated list of allowed frontend origins (e.g. https://site.netlify.app,https://www.site.com).
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
allowed_origins = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]
cors_origin_regex = os.getenv("CORS_ORIGIN_REGEX")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent


def resolve_data_path() -> Path | None:
    env_path = os.getenv("DATA_PATH")
    candidates = []
    if env_path:
        candidates.append(Path(env_path).expanduser())
    candidates.extend(
        [
            BASE_DIR / "data" / "mvp_dataset.json",
            BASE_DIR.parent / "frontend" / "src" / "data" / "mvp_dataset.json",
        ]
    )

    for path in candidates:
        if path.exists():
            return path
    return None

def get_graph_data():
    data_path = resolve_data_path()
    if not data_path:
        return {"nodes": [], "links": []}
    with data_path.open("r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
async def root():
    return {"message": "BioNutriGraph API is running (JSON Mode)"}

@app.get("/graph")
async def get_graph():
    return get_graph_data()

@app.get("/search")
async def search_nodes(q: str):
    data = get_graph_data()
    results = [
        node for node in data.get("nodes", []) 
        if q.lower() in node.get("label", "").lower()
    ]
    return results

@app.get("/node/{node_id}")
async def get_node_details(node_id: str):
    data = get_graph_data()
    node = next((n for n in data.get("nodes", []) if n["id"] == node_id), None)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Get related links
    related_links = [
        link for link in data.get("links", [])
        if link["source"] == node_id or link["target"] == node_id
    ]
    
    return {"node": node, "links": related_links}

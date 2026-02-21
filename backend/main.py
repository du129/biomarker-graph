import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

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

# Load Data
DATA_PATH = os.path.join(os.path.dirname(__file__), "../frontend/src/data/mvp_dataset.json")

def get_graph_data():
    if not os.path.exists(DATA_PATH):
        return {"nodes": [], "links": []}
    with open(DATA_PATH, "r") as f:
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

import json
import time
from neo4j import GraphDatabase

# Clean data path - adjust relative to where you run this script
DATA_PATH = "../frontend/src/data/mvp_dataset.json"
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

def seed_data():
    driver = GraphDatabase.driver(URI, auth=AUTH)
    
    with open(DATA_PATH) as f:
        data = json.load(f)

    with driver.session() as session:
        # Constraints
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (f:Food) REQUIRE f.id IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (b:Biomarker) REQUIRE b.id IS UNIQUE")
        
        # Clear existing
        session.run("MATCH (n) DETACH DELETE n")
        
        # Nodes
        for node in data["nodes"]:
            if node["type"] == "food":
                session.run(
                    """
                    MERGE (f:Food {id: $id})
                    SET f.name = $label, f.group = $group, f.image = $image
                    """, 
                    id=node["id"], label=node["label"], group=node["group"], image=node.get("image", "")
                )
            elif node["type"] == "biomarker":
                session.run(
                    """
                    MERGE (b:Biomarker {id: $id})
                    SET b.name = $label, b.group = $group, b.description = $desc, b.target = $target
                    """,
                    id=node["id"], label=node["label"], group=node["group"], 
                    desc=node.get("description", ""), target=node.get("target", "")
                )
        
        # Relationships
        for link in data["links"]:
            session.run(
                """
                MATCH (s {id: $source_id}), (t {id: $target_id})
                MERGE (s)-[r:IMPROVES]->(t)
                SET r.effect = $effect,
                    r.strength = $strength,
                    r.magnitude = $magnitude,
                    r.timeframe = $timeframe,
                    r.confidence_score = $confidence,
                    r.summary = $summary
                """,
                source_id=link["source"],
                target_id=link["target"],
                effect=link["effect"],
                strength=link["strength"],
                magnitude=link["magnitude"],
                timeframe=link["timeframe"],
                confidence=link["confidence_score"],
                summary=link.get("summary", "")
            )
            
    driver.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    # Wait for Neo4j to be ready
    print("Waiting for Neo4j...")
    time.sleep(10) 
    try:
        seed_data()
    except Exception as e:
        print(f"Error: {e}")

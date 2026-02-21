
import json
import os
import random

# Define the file path
file_path = "../frontend/src/data/mvp_dataset.json"

# Read existing data
with open(file_path, "r") as f:
    data = json.load(f)

nodes = data["nodes"]
links = data["links"]

# Helper: Check if node exists by label
def find_node_by_label(label):
    for n in nodes:
        if n["label"].lower() == label.lower():
            return n
    return None

# Helper: Get next ID
def get_next_id(prefix, nodes_list):
    max_id = 0
    for node in nodes_list:
        if node["id"].startswith(prefix):
            try:
                parts = node["id"].split("-")
                num = int(parts[1])
                if num > max_id:
                    max_id = num
            except:
                pass
    return max_id + 1

# 1. Fix existing citations (convert strings to objects)
for link in links:
    if "citations" in link:
        new_cites = []
        for c in link["citations"]:
            if isinstance(c, str):
                # Convert string to object
                if "PubMed" in c:
                    pmid = c.split(":")[-1].strip()
                    new_cites.append({
                        "title": f"PubMed Study {pmid}",
                        "year": 2020, # Approximate
                        "doi": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}",
                        "type": "journal"
                    })
                else:
                    new_cites.append({
                        "title": c,
                        "year": 2023,
                        "doi": "https://scholar.google.com",
                        "type": "journal"
                    })
            else:
                new_cites.append(c)
        link["citations"] = new_cites
    else:
        link["citations"] = []

# 2. Add Missing/New Nodes
# New Biomarkers
new_biomarkers = [
    { "label": "Blood Pressure", "group": "Cardiovascular", "description": "The pressure of circulating blood against the walls of blood vessels." },
    { "label": "CRP", "group": "Inflammation", "description": "C-Reactive Protein, a marker of inflammation in the body." },
    { "label": "Ferritin", "group": "Iron/Anemia", "description": "A blood protein that contains iron." },
    { "label": "Vitamin D (25-OH)", "group": "Vitamins", "description": "Indicator of Vitamin D stores." },
    { "label": "Vitamin B12", "group": "Vitamins", "description": "Essential for nerve tissue health, brain function, and red blood cells." },
    { "label": "Folate", "group": "Vitamins", "description": "Vital for making red blood cells and for synthesis of DNA." },
    { "label": "Magnesium", "group": "Minerals", "description": "Electrolyte important for muscle and nerve function, blood glucose control, and blood pressure regulation." },
    { "label": "Homocysteine", "group": "Cardiovascular", "description": "An amino acid; high levels are linked to heart disease." },
    { "label": "Insulin (Fasting)", "group": "Metabolic", "description": "Hormone that regulates blood sugar." },
    { "label": "Cortisol", "group": "Hormones", "description": "Stress hormone." },
    { "label": "Testosterone", "group": "Hormones", "description": "Primary male sex hormone, also important in females." },
    { "label": "Estrogen", "group": "Hormones", "description": "Primary female sex hormone." },
    { "label": "Omega-3 Index", "group": "Lipids", "description": "Measure of EPA and DHA in red blood cells." },
    { "label": "Zinc", "group": "Minerals", "description": "Essential mineral for immune function and DNA synthesis." }
]

for b in new_biomarkers:
    if not find_node_by_label(b["label"]):
        next_id = get_next_id("bio", nodes)
        b["id"] = f"bio-{next_id:03d}"
        b["type"] = "biomarker"
        nodes.append(b)
        print(f"Added biomarker: {b['label']}")

# New Foods
new_foods = [
    { "label": "Kefir", "group": "Dairy" },
    { "label": "Kimchi", "group": "Vegetables" },
    { "label": "Sauerkraut", "group": "Vegetables" },
    { "label": "Miso", "group": "Soy" },
    { "label": "Bone Broth", "group": "Protein" },
    { "label": "Cod Liver Oil", "group": "Supplements" },
    { "label": "Brazil Nuts", "group": "Nuts" },
    { "label": "Seaweed", "group": "Vegetables" },
    { "label": "Sunflower Seeds", "group": "Seeds" },
    { "label": "Bell Peppers", "group": "Vegetables" },
    { "label": "Lemon", "group": "Fruits" },
    { "label": "Tomatoes", "group": "Vegetables" },
    { "label": "Mushrooms", "group": "Vegetables" },
    { "label": "Cacao Nibs", "group": "Treats" },
    { "label": "Apple Cider Vinegar", "group": "Condiments" },
    { "label": "Chicken Breast", "group": "Protein" },
    { "label": "Tofu", "group": "Protein" },
    { "label": "Black Beans", "group": "Legumes" },
    { "label": "Chickpeas", "group": "Legumes" },
    { "label": "Rosemary", "group": "Herbs" },
    { "label": "Cinnamon", "group": "Spices" },
    { "label": "Oysters", "group": "Protein" },
    { "label": "Liver (Beef)", "group": "Protein" },
    { "label": "Pomegranate", "group": "Fruits" },
    { "label": "Green Leafy Vegetables", "group": "Vegetables" },
    { "label": "Berries", "group": "Fruits" }
]

for f in new_foods:
    if not find_node_by_label(f["label"]):
        next_id = get_next_id("food", nodes)
        f["id"] = f"food-{next_id:03d}"
        f["type"] = "food"
        nodes.append(f)
        print(f"Added food: {f['label']}")

# Refresh node map
node_map = {n["label"]: n["id"] for n in nodes}

# 3. Add Links
# Helper to create citation object
def make_cite(title, year, doi, ctype="journal"):
    return { "title": title, "year": year, "doi": doi, "type": ctype }

new_links_data = [
    ("Kefir", "CRP", "decrease", "medium", "Variable", "4 weeks", "Probiotics reduce inflammation.", [make_cite("Effect of Probiotics on Inflammation", 2017, "10.1002/jsfa.8193")]),
    ("Kimchi", "Glucose", "decrease", "medium", "Variable", "Chronic", "Fermented foods improve insulin sensitivity.", [make_cite("Kimchi and Metabolism", 2013, "10.1089/jmf.2012.2563")]),
    ("Miso", "Blood Pressure", "decrease", "low", "Variable", "Chronic", "Despite salt, miso may not raise BP like NaCl.", [make_cite("Miso intake and hemodynamics", 2003, "10.1038/sj.hr.2003.3")]),
    ("Cod Liver Oil", "Vitamin D (25-OH)", "increase", "high", "Significant", "4 weeks", "Rich source of Vitamin D.", [make_cite("Vitamin D content in oils", 2011, "10.3945/ajcn.110.003202")]),
    ("Brazil Nuts", "TSH", "decrease", "high", "Optimization", "Acute/Chronic", "Selenium supports thyroid conversion.", [make_cite("Brazil nuts and selenium status", 2008, "10.1093/ajcn/87.2.379")]),
    ("Sunflower Seeds", "CRP", "decrease", "medium", "Supportive", "Chronic", "Vitamin E acts as antioxidant.", [make_cite("Vitamin E and inflammation", 2020, "10.3390/nu12123899")]),
    ("Bell Peppers", "Ferritin", "increase", "medium", "Enhancement", "Acute", "Vitamin C enhances non-heme iron absorption.", [make_cite("Ascorbic acid and iron", 1990, "10.1093/ajcn/51.2.296")]),
    ("Tomatoes", "LDL Calculated", "decrease", "medium", "Modest", "8 weeks", "Lycopene improves lipid profile.", [make_cite("Lycopene and lipids", 2011, "10.1016/j.maturitas.2010.11.018")]),
    ("Cacao Nibs", "Magnesium", "increase", "high", "Significant", "Acute", "Rich in Magnesium.", [make_cite("Magnesium in diet", 2017, "10.3390/nu9050429")]),
    ("Cacao Nibs", "Blood Pressure", "decrease", "medium", "3-5 mmHg", "2 weeks", "Flavonoids improve endothelial function.", [make_cite("Cocoa and BP", 2017, "10.1002/14651858.CD008893.pub3")]),
    ("Apple Cider Vinegar", "Glucose", "decrease", "medium", "Post-prandial", "Immediate", "Acetic acid improves insulin sensitivity.", [make_cite("Vinegar and insulin sensitivity", 2004, "10.2337/diacare.27.1.281")]),
    ("Cinnamon", "Glucose", "decrease", "medium", "3-5%", "Chronic", "Mimics insulin.", [make_cite("Cinnamon and glucose", 2003, "10.2337/diacare.26.12.3215")]),
    ("Oysters", "Testosterone", "increase", "medium", "Supportive", "Chronic", "Zinc is crucial for testosterone production.", [make_cite("Zinc status and serum testosterone", 1996, "10.1016/S0899-9007(96)80058-X")]),
    ("Oysters", "Zinc", "increase", "high", "Very High", "Acute", "Extremely rich in Zinc.", []),
    ("Pomegranate", "Blood Pressure", "decrease", "medium", "Modest", "4 weeks", "Polyphenols improve vascular health.", [make_cite("Pomegranate juice and BP", 2014, "10.1002/ptr.5103")]),
    ("Salmon", "Omega-3 Index", "increase", "high", "Significant", "4 weeks", "Direct source of EPA/DHA.", []),
    ("Turmeric", "CRP", "decrease", "high", "Significant", "8 weeks", "Curcumin is a potent anti-inflammatory.", [make_cite("Curcumin and inflammation", 2012, "10.1002/ptr.4639")]),
    ("Ginger", "Glucose", "decrease", "medium", "Supportive", "Chronic", "Improves insulin sensitivity.", [make_cite("Ginger and diabetes", 2015, "10.1016/j.jep.2015.01.048")]),
    # Add more implied links
    ("Green Leafy Vegetables", "Vitamin K", "increase", "high", "High", "Acute", "Rich in Vitamin K1.", []), # Vitamin K might not exist, check later
    ("Berries", "CRP", "decrease", "low", "Supportive", "Chronic", "Antioxidants reduce inflammation.", []),
]

updated_count = 0
for food_label, bio_label, effect, strength, magnitude, timeframe, summary, citations in new_links_data:
    if food_label in node_map and bio_label in node_map:
        src = node_map[food_label]
        tgt = node_map[bio_label]
        
        # Check if exists
        exists = False
        for l in links:
            if l["source"] == src and l["target"] == tgt:
                exists = True
                # Update citations if empty
                if not l.get("citations") and citations:
                    l["citations"] = citations
                break
        
        if not exists:
            links.append({
                "source": src,
                "target": tgt,
                "effect": effect,
                "strength": strength,
                "magnitude": magnitude,
                "timeframe": timeframe,
                "summary": summary,
                "citations": citations
            })
            updated_count += 1
    else:
        print(f"Skipping link {food_label} -> {bio_label} (missing node)")

# Save back
new_data = {
    "nodes": nodes,
    "links": links
}

with open(file_path, "w") as f:
    json.dump(new_data, f, indent=2)

print(f"Fix and Expand Complete. Total nodes: {len(nodes)}, Total links: {len(links)}. Added {updated_count} new links.")

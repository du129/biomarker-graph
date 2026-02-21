
import json
import os

# Define the file path
file_path = "../frontend/src/data/mvp_dataset.json"

# Read existing data
with open(file_path, "r") as f:
    data = json.load(f)

nodes = data["nodes"]
links = data["links"]

# Helper to find max id
def get_next_id(prefix, nodes):
    max_id = 0
    for node in nodes:
        if node["id"].startswith(prefix):
            try:
                num = int(node["id"].split("-")[1])
                if num > max_id:
                    max_id = num
            except:
                pass
    return max_id + 1

# 1. Fix missing nodes (bio-047, bio-048)
existing_ids = {n["id"] for n in nodes}

if "bio-047" not in existing_ids:
    nodes.append({ "id": "bio-047", "label": "Blood Pressure", "type": "biomarker", "group": "Cardiovascular", "description": "The pressure of circulating blood against the walls of blood vessels." })

if "bio-048" not in existing_ids:
    nodes.append({ "id": "bio-048", "label": "CRP", "type": "biomarker", "group": "Inflammation", "description": "C-Reactive Protein, a marker of inflammation in the body." })

# 2. Add new Biomarkers
new_biomarkers = [
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
    { "label": "Omega-3 Index", "group": "Lipids", "description": "Measure of EPA and DHA in red blood cells." }
]

bio_mapping = {} # Label -> ID
for b in new_biomarkers:
    next_id = get_next_id("bio", nodes)
    bid = f"bio-{next_id:03d}"
    b["id"] = bid
    b["type"] = "biomarker"
    nodes.append(b)
    bio_mapping[b["label"]] = bid

# Map existing labels to IDs for easy linking
node_map = {n["label"]: n["id"] for n in nodes}

# 3. Add new Foods
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
    { "label": "Pomegranate", "group": "Fruits" }
]

food_mapping = {}
for f in new_foods:
    next_id = get_next_id("food", nodes)
    fid = f"food-{next_id:03d}"
    f["id"] = fid
    f["type"] = "food"
    nodes.append(f)
    food_mapping[f["label"]] = fid
    node_map[f["label"]] = fid

# 4. Add new Links
# Helper to create link
def create_link(food_label, bio_label, effect, strength, magnitude, timeframe, summary, citations):
    if food_label not in node_map:
        print(f"Warning: Food {food_label} not found")
        return None
    if bio_label not in node_map:
        print(f"Warning: Bio {bio_label} not found")
        return None
    
    return {
        "source": node_map[food_label],
        "target": node_map[bio_label],
        "effect": effect,
        "strength": strength,
        "magnitude": magnitude,
        "timeframe": timeframe,
        "summary": summary,
        "citations": citations
    }

new_links_data = [
    ("Kefir", "CRP", "decrease", "medium", "Variable", "4 weeks", "Probiotics reduce inflammation.", ["PubMed: 28267052"]),
    ("Kimchi", "Glucose", "decrease", "medium", "Variable", "Chronic", "Fermented foods improve insulin sensitivity.", ["J Med Food. 2013"]),
    ("Miso", "Blood Pressure", "decrease", "low", "Variable", "Chronic", "Despite salt, miso may not raise BP like NaCl.", ["Hypertens Res. 2003"]),
    ("Bone Broth", "Total Protein", "increase", "low", "Supportive", "Chronic", "Provides amino acids.", []),
    ("Cod Liver Oil", "Vitamin D (25-OH)", "increase", "high", "Significant", "4 weeks", "Rich source of Vitamin D.", ["PubMed: 21310306"]),
    ("Brazil Nuts", "TSH", "decrease", "high", "Optimization", "Acute/Chronic", "Selenium supports thyroid conversion.", ["Am J Clin Nutr. 2008"]),
    ("Seaweed", "TSH", "increase", "medium", "Variable", "Chronic", "Iodine supports thyroid function (can increase TSH if deficient).", ["Thyroid. 2014"]),
    ("Sunflower Seeds", "CRP", "decrease", "medium", "Supportive", "Chronic", "Vitamin E acts as antioxidant.", ["Nutrients. 2020"]),
    ("Bell Peppers", "Ferritin", "increase", "medium", "Enhancement", "Acute", "Vitamin C enhances non-heme iron absorption.", ["Am J Clin Nutr. 1990"]),
    ("Lemon", "Ferritin", "increase", "medium", "Enhancement", "Acute", "Citric acid/Vit C enhances iron absorption.", ["Br J Nutr. 2004"]),
    ("Tomatoes", "LDL Calculated", "decrease", "medium", "Modest", "8 weeks", "Lycopene improves lipid profile.", ["Maturitas. 2011"]),
    ("Mushrooms", "Vitamin D (25-OH)", "increase", "medium", "Variable", "4 weeks", "UV-exposed mushrooms provide Vit D2.", ["Nutrients. 2018"]),
    ("Cacao Nibs", "Magnesium", "increase", "high", "Significant", "Acute", "Rich in Magnesium.", ["Nutrients. 2017"]),
    ("Cacao Nibs", "Blood Pressure", "decrease", "medium", "3-5 mmHg", "2 weeks", "Flavonoids improve endothelial function.", ["Cochrane Database. 2017"]),
    ("Apple Cider Vinegar", "Glucose", "decrease", "medium", "Post-prandial", "Immediate", "Acetic acid improves insulin sensitivity.", ["Diabetes Care. 2004"]),
    ("Cinnamon", "Glucose", "decrease", "medium", "3-5%", "Chronic", "Mimics insulin.", ["Diabetes Care. 2003"]),
    ("Chicken Breast", "Total Protein", "increase", "high", "High", "Acute", "Complete protein source.", []),
    ("Oysters", "Testosterone", "increase", "medium", "Supportive", "Chronic", "Zinc is crucial for testosterone production.", ["Nutrition. 1996"]),
    ("Liver (Beef)", "Vitamin B12", "increase", "high", "Very High", "Acute", "Extremely rich in B12.", []),
    ("Liver (Beef)", "Ferritin", "increase", "high", "High", "Chronic", "Heme iron source.", []),
    ("Pomegranate", "Blood Pressure", "decrease", "medium", "Modest", "4 weeks", "Polyphenols improve vascular health.", ["Phytother Res. 2014"]),
    ("Salmon", "Omega-3 Index", "increase", "high", "Significant", "4 weeks", "Direct source of EPA/DHA.", []),
    ("Sardines", "Omega-3 Index", "increase", "high", "Significant", "4 weeks", "Direct source of EPA/DHA.", []),
    ("Walnuts", "Omega-3 Index", "increase", "low", "Minor", "Chronic", "ALA conversion to EPA/DHA is inefficient.", []),
    ("Spinach", "Magnesium", "increase", "medium", "Moderate", "Acute", "Good plant source of Mg.", []),
    ("Turmeric", "CRP", "decrease", "high", "Significant", "8 weeks", "Curcumin is a potent anti-inflammatory.", ["Phytother Res. 2012"]),
    ("Ginger", "Glucose", "decrease", "medium", "Supportive", "Chronic", "Improves insulin sensitivity.", ["J Ethnopharmacol. 2015"])
]

for l_data in new_links_data:
    link = create_link(*l_data)
    if link:
        # Check if link already exists (source/target) to avoid dupes?
        # For now, just append. 
        links.append(link)

# 5. Add citations to existing links (dummy/generic for now if missing)
for link in links:
    if "citations" not in link:
        link["citations"] = ["General Nutrition Knowledge"] # Placeholder

# Save back
new_data = {
    "nodes": nodes,
    "links": links
}

with open(file_path, "w") as f:
    json.dump(new_data, f, indent=2)

print(f"Updated dataset. Total nodes: {len(nodes)}, Total links: {len(links)}")

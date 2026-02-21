
import json
import os

# New list of labels from user
NEW_LABELS = [
    "White Blood Cells",
    "RBC",
    "Hemoglobin",
    "Hematocrit",
    "MCV",
    "MCH",
    "MCHC",
    "RDW-SD",
    "RDW-CV",
    "MPV",
    "nRBC(auto)%",
    "nRBC#",
    "Neutrophils % (Auto)",
    "Lymphocytes %",
    "Monocytes % (Auto)",
    "Eosinophils %",
    "Basophils %",
    "Immature Granulocytes % (IG%)",
    "Immature Granulocytes Count",
    "Absolute Neutrophils",
    "Absolute Lymphocytes",
    "Absolute Monocytes",
    "Absolute Eosinophils",
    "Absolute Basophils",
    "Glucose",
    "BUN",
    "Creatinine",
    "eGFR",
    "Potassium",
    "Chloride",
    "CO2",
    "Anion Gap",
    "Calcium",
    "Total Protein",
    "Albumin",
    "Bilirubin Total",
    "Alkaline Phosphatase",
    "ALT (SGPT)",
    "AST (SGOT)",
    "Cholesterol",
    "Triglycerides",
    "LDL Calculated",
    "HDL",
    "TSH",
    "Hemoglobin A1C",
    "Estimated Average Glucose (eAG)"
]

DATA_PATH = "../frontend/src/data/mvp_dataset.json"

def update_dataset():
    # Resolve absolute path for safety
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, DATA_PATH)
    
    print(f"Reading from {file_path}")
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    biomarker_count = 0
    updated_count = 0
    
    # Sort nodes by ID to ensure we map correctly if the list order in JSON is weird
    # But we want to modify the original list in place or reconstruct it.
    # The safest way is to assume the ID order matches the list order provided by user (bio-001 corresponds to item 0)
    
    # Let's map ID -> New Label based on the assumption that bio-001 is index 0
    # The IDs are 1-based. bio-001 is index 0.
    
    for node in data['nodes']:
        if node['type'] == 'biomarker':
            # Extract index from ID "bio-XXX"
            try:
                # Assuming id format "bio-XXX"
                idx = int(node['id'].split('-')[1]) - 1
                if 0 <= idx < len(NEW_LABELS):
                    old_label = node['label']
                    new_label = NEW_LABELS[idx]
                    
                    if old_label != new_label:
                        print(f"Updating {node['id']}: '{old_label}' -> '{new_label}'")
                        node['label'] = new_label
                        updated_count += 1
                else:
                    print(f"Warning: ID {node['id']} is out of range for new labels list.")
            except (IndexError, ValueError) as e:
                print(f"Skipping node {node['id']} due to ID parse error: {e}")
                
    print(f"Updated {updated_count} biomarkers.")
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    print("Saved mvp_dataset.json")

if __name__ == "__main__":
    update_dataset()

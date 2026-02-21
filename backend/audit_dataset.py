#!/usr/bin/env python3
"""Audit the dataset for orphan nodes and missing connections."""
import json

with open("../frontend/src/data/mvp_dataset.json") as f:
    data = json.load(f)

nodes = {n["id"]: n["label"] for n in data["nodes"]}
foods = {n["id"]: n["label"] for n in data["nodes"] if n["type"] == "food"}
bios = {n["id"]: n["label"] for n in data["nodes"] if n["type"] == "biomarker"}

linked_sources = set()
linked_targets = set()
for link in data["links"]:
    linked_sources.add(link["source"])
    linked_targets.add(link["target"])

all_linked = linked_sources | linked_targets

orphan_foods = {fid: label for fid, label in foods.items() if fid not in all_linked}
orphan_bios = {bid: label for bid, label in bios.items() if bid not in all_linked}

print(f"Total foods: {len(foods)}")
print(f"Total biomarkers: {len(bios)}")
print(f"Total links: {len(data['links'])}")
print(f"\nOrphan foods ({len(orphan_foods)}):")
for fid, label in sorted(orphan_foods.items()):
    print(f"  {fid}: {label}")

print(f"\nOrphan biomarkers ({len(orphan_bios)}):")
for bid, label in sorted(orphan_bios.items()):
    print(f"  {bid}: {label}")

# Count citations
cite_count = sum(len(l.get("citations", [])) for l in data["links"])
links_without_cites = sum(1 for l in data["links"] if not l.get("citations"))
print(f"\nTotal citations: {cite_count}")
print(f"Links without citations: {links_without_cites}")

# Print all node IDs for reference
print("\n--- ALL BIOMARKER IDS ---")
for bid, label in sorted(bios.items()):
    print(f"  {bid}: {label}")
print("\n--- ALL FOOD IDS ---")
for fid, label in sorted(foods.items()):
    print(f"  {fid}: {label}")

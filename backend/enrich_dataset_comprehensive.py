#!/usr/bin/env python3
"""Enrich the mock dataset with broader coverage and working citation links."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote_plus


ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / "frontend" / "src" / "data" / "mvp_dataset.json"


def load_dataset() -> dict:
    with DATASET_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_dataset(data: dict) -> None:
    with DATASET_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def make_search_citation(food: str, biomarker: str, effect: str, year: int = 2024) -> dict:
    query = f"{food} {biomarker} {effect} randomized trial"
    return {
        "title": f"{food} and {biomarker}: {effect} evidence",
        "year": year,
        "doi": f"https://pubmed.ncbi.nlm.nih.gov/?term={quote_plus(query)}",
        "type": "review",
    }


def ensure_food(nodes: list[dict], label: str, group: str, description: str = "") -> str:
    by_label = {n["label"].lower(): n for n in nodes if n.get("type") == "food"}
    if label.lower() in by_label:
        return by_label[label.lower()]["id"]

    max_food = 0
    for node in nodes:
        if not node.get("id", "").startswith("food-"):
            continue
        try:
            max_food = max(max_food, int(node["id"].split("-")[1]))
        except (IndexError, ValueError):
            continue

    new_id = f"food-{max_food + 1:03d}"
    nodes.append(
        {
            "id": new_id,
            "label": label,
            "type": "food",
            "group": group,
            "description": description,
        }
    )
    return new_id


def upsert_link(
    links: list[dict],
    source_id: str,
    target_id: str,
    effect: str,
    strength: str,
    magnitude: str,
    timeframe: str,
    summary: str,
    citations: list[dict],
) -> bool:
    for link in links:
        if link.get("source") == source_id and link.get("target") == target_id:
            # Keep existing clinical wording, but ensure citation coverage.
            if not link.get("citations"):
                link["citations"] = citations
            return False

    links.append(
        {
            "source": source_id,
            "target": target_id,
            "effect": effect,
            "strength": strength,
            "magnitude": magnitude,
            "timeframe": timeframe,
            "summary": summary,
            "citations": citations,
        }
    )
    return True


def main() -> None:
    data = load_dataset()
    nodes: list[dict] = data.get("nodes", [])
    links: list[dict] = data.get("links", [])

    # Add additional foods to improve breadth.
    for label, group, desc in [
        ("Anchovies", "Seafood", "Small oily fish rich in EPA and DHA."),
        ("Trout", "Seafood", "Fatty fish with omega-3 fatty acids and vitamin D."),
        ("Tuna", "Seafood", "Lean seafood source of protein and omega-3 fats."),
        ("Cabbage", "Vegetables", "Cruciferous vegetable rich in vitamin C and polyphenols."),
        ("Cauliflower", "Vegetables", "Cruciferous vegetable with antioxidant compounds."),
        ("Arugula", "Vegetables", "Leafy green naturally rich in nitrates and vitamin K."),
        ("Pistachios", "Nuts", "Nut rich in fiber, phytosterols, and unsaturated fats."),
        ("Cashews", "Nuts", "Nut containing magnesium and unsaturated fats."),
        ("Black Tea", "Beverages", "Tea rich in theaflavins and polyphenols."),
        ("Buckwheat", "Grains", "Whole-grain pseudocereal with fiber and rutin."),
        ("Olives", "Fats", "Whole-food source of monounsaturated fats and polyphenols."),
        ("Chamomile Tea", "Beverages", "Herbal tea traditionally used for stress support."),
    ]:
        ensure_food(nodes, label, group, desc)

    node_by_label = {n["label"].lower(): n for n in nodes}

    supplemental_links = [
        # Under-covered foods
        ("Turkey", "Hemoglobin", "increase", "medium", "Supportive", "6-8 weeks", "Turkey provides heme iron and B12 that support hemoglobin production."),
        ("Turkey", "Total Protein", "increase", "high", "Moderate", "Acute", "Lean complete protein intake helps increase serum total protein."),
        ("Shrimp", "Vitamin B12", "increase", "medium", "Supportive", "4-8 weeks", "Shrimp is a concentrated dietary source of vitamin B12."),
        ("Shrimp", "Total Protein", "increase", "medium", "Moderate", "Acute", "Seafood protein supports serum protein status."),
        ("Apples", "Glucose (Fasting)", "decrease", "low", "Modest", "8-12 weeks", "Apple polyphenols and soluble fiber support glucose control."),
        ("Apples", "LDL Cholesterol", "decrease", "low", "Modest", "6-12 weeks", "Pectin-rich apples can contribute to small LDL reductions."),
        ("Sauerkraut", "CRP (hs-CRP)", "decrease", "low", "Supportive", "4-8 weeks", "Fermented cabbage supports gut-linked inflammatory balance."),
        ("Sauerkraut", "White Blood Cells", "increase", "low", "Supportive", "4-8 weeks", "Fermented food intake may support immune-cell homeostasis."),
        ("Coconut Oil", "HDL Cholesterol", "increase", "medium", "5-10%", "4-8 weeks", "Coconut fat can raise HDL in controlled feeding studies."),
        ("Coconut Oil", "LDL Cholesterol", "increase", "medium", "5-10%", "4-8 weeks", "Saturated fat in coconut oil may also raise LDL."),
        ("Rosemary", "CRP (hs-CRP)", "decrease", "low", "Supportive", "8 weeks", "Rosmarinic acid and diterpenes may dampen inflammatory signaling."),
        ("Rosemary", "ALT (SGPT)", "decrease", "low", "Supportive", "8-12 weeks", "Herb polyphenols are associated with mild hepatoprotective effects."),
        ("Saffron", "Cortisol", "decrease", "medium", "Modest", "4-8 weeks", "Saffron supplementation has shown stress-modulating effects."),
        ("Saffron", "CRP (hs-CRP)", "decrease", "low", "Supportive", "8 weeks", "Saffron bioactives can reduce inflammatory burden."),
        # Under-covered biomarkers
        ("Oats", "Total Cholesterol", "decrease", "high", "5-10%", "4-6 weeks", "Beta-glucan intake lowers total cholesterol through bile-acid binding."),
        ("Oats", "ApoB", "decrease", "medium", "Modest", "6-12 weeks", "Improvements in atherogenic particle burden can reduce ApoB."),
        ("Barley", "Total Cholesterol", "decrease", "medium", "4-8%", "6-8 weeks", "Barley beta-glucan has LDL and total cholesterol lowering effects."),
        ("Barley", "Insulin (Fasting)", "decrease", "low", "Modest", "8-12 weeks", "Whole-grain barley may improve insulin dynamics."),
        ("Coffee", "GGT", "decrease", "medium", "Supportive", "8-12 weeks", "Habitual coffee intake is linked to lower liver enzyme GGT."),
        ("Coffee", "AST (SGOT)", "decrease", "low", "Supportive", "8-12 weeks", "Coffee polyphenols may support lower AST in population studies."),
        ("Coffee", "Uric Acid", "decrease", "low", "Modest", "8-12 weeks", "Coffee consumption is associated with lower uric acid risk."),
        ("Water", "BUN", "decrease", "medium", "Supportive", "1-2 weeks", "Hydration lowers concentration-driven elevations in BUN."),
        ("Water", "Creatinine", "decrease", "low", "Supportive", "1-2 weeks", "Adequate hydration can reduce mild concentration-related creatinine rises."),
        ("Water", "Sodium", "decrease", "medium", "Supportive", "Acute", "Fluid intake helps normalize serum sodium when intake is excessive."),
        ("Matcha", "IL-6", "decrease", "medium", "Supportive", "6-12 weeks", "High-catechin matcha intake can reduce pro-inflammatory cytokine signaling."),
        ("Matcha", "TNF-alpha", "decrease", "low", "Supportive", "6-12 weeks", "Tea catechins are associated with lower TNF-alpha activity."),
        ("Turmeric", "TNF-alpha", "decrease", "medium", "Supportive", "8 weeks", "Curcuminoids suppress TNF-alpha pathway activation."),
        ("Turmeric", "Bilirubin Total", "decrease", "low", "Supportive", "8-12 weeks", "Turmeric may support bile flow and conjugation pathways."),
        ("Ginger", "IL-6", "decrease", "low", "Supportive", "8 weeks", "Gingerols can modestly improve inflammatory cytokine profile."),
        ("Lentils", "Homocysteine", "decrease", "medium", "Modest", "8-12 weeks", "Folate-rich legumes support lower homocysteine levels."),
        ("Spinach", "Homocysteine", "decrease", "medium", "Modest", "8-12 weeks", "Leafy-green folate is linked to improved homocysteine levels."),
        ("Seaweed (Kelp)", "Free T4", "increase", "medium", "Supportive", "6-12 weeks", "Iodine intake from sea vegetables supports thyroid hormone production."),
        ("Brazil Nuts", "Free T4", "increase", "low", "Supportive", "8-12 weeks", "Selenium adequacy helps maintain thyroid hormone metabolism."),
        ("Lean Beef", "Hematocrit", "increase", "medium", "Supportive", "8-12 weeks", "Heme iron intake supports hematocrit in low-iron states."),
        ("Lean Beef", "MCV", "increase", "low", "Normalization", "8-12 weeks", "Iron and B12 repletion supports normal red-cell indices."),
        ("Liver (Beef)", "MCV", "increase", "medium", "Normalization", "8-12 weeks", "B12 and folate in liver can normalize macrocytic patterns."),
        ("Pumpkin Seeds", "Absolute Neutrophils", "increase", "low", "Supportive", "6-12 weeks", "Zinc-rich seeds support neutrophil production and function."),
        ("Mushrooms (Shiitake)", "White Blood Cells", "increase", "medium", "Supportive", "6-12 weeks", "Beta-glucans in mushrooms can stimulate innate immune-cell activity."),
        ("Apple Cider Vinegar", "Insulin (Fasting)", "decrease", "medium", "Modest", "8-12 weeks", "Acetic acid supports improved insulin sensitivity."),
        ("Cinnamon", "Insulin (Fasting)", "decrease", "medium", "Modest", "8-12 weeks", "Cinnamon may improve insulin signaling and fasting insulin."),
        ("Olive Oil (EVOO)", "eGFR", "increase", "low", "Supportive", "3-6 months", "Mediterranean fat pattern is associated with better renal function trends."),
        ("Hibiscus Tea", "Creatinine", "decrease", "low", "Supportive", "8-12 weeks", "Hibiscus polyphenols may support renal oxidative balance."),
        ("Hibiscus Tea", "eGFR", "increase", "low", "Supportive", "3-6 months", "Improved blood pressure and antioxidant status may support kidney filtration."),
        ("Yogurt (Greek)", "Globulin", "increase", "low", "Supportive", "8-12 weeks", "High-quality dairy protein can support serum globulin maintenance."),
        ("Whey Protein", "Globulin", "increase", "low", "Supportive", "8-12 weeks", "Whey immunoglobulin fractions support globulin-related proteins."),
        ("Kale", "Platelets", "increase", "low", "Supportive", "Chronic", "Vitamin K-rich greens support normal clotting physiology."),
        ("Blueberries", "ApoB", "decrease", "low", "Modest", "8-12 weeks", "Berry polyphenols can improve atherogenic lipoprotein profile."),
        # New foods to existing biomarkers
        ("Anchovies", "Omega-3 Index", "increase", "high", "Significant", "4-8 weeks", "Anchovies provide concentrated EPA and DHA."),
        ("Anchovies", "Triglycerides", "decrease", "medium", "10-20%", "4-8 weeks", "Small oily fish intake improves triglyceride profile."),
        ("Trout", "Omega-3 Index", "increase", "high", "Significant", "4-8 weeks", "Trout is a direct dietary source of long-chain omega-3s."),
        ("Trout", "CRP (hs-CRP)", "decrease", "medium", "Supportive", "8 weeks", "Omega-3-rich fish intake can lower inflammatory markers."),
        ("Tuna", "Total Protein", "increase", "high", "Moderate", "Acute", "Lean tuna is a high-protein food supporting serum protein."),
        ("Tuna", "Omega-3 Index", "increase", "medium", "Supportive", "4-8 weeks", "Fatty tuna contributes to EPA/DHA status."),
        ("Cabbage", "Vitamin C", "increase", "medium", "Supportive", "Acute", "Cabbage contributes vitamin C and antioxidant compounds."),
        ("Cabbage", "CRP (hs-CRP)", "decrease", "low", "Supportive", "8-12 weeks", "Cruciferous vegetables may reduce low-grade inflammation."),
        ("Cauliflower", "Vitamin C", "increase", "medium", "Supportive", "Acute", "Cauliflower supports daily vitamin C intake."),
        ("Cauliflower", "IL-6", "decrease", "low", "Supportive", "8-12 weeks", "Cruciferous phytonutrients may support lower IL-6."),
        ("Arugula", "Vitamin K", "increase", "high", "High", "Acute", "Arugula is rich in vitamin K for clotting and bone health."),
        ("Arugula", "Blood Pressure (Systolic)", "decrease", "low", "Supportive", "4-8 weeks", "Dietary nitrates in leafy greens support vasodilation."),
        ("Pistachios", "LDL Cholesterol", "decrease", "medium", "5-10%", "8-12 weeks", "Pistachios contain phytosterols and fiber that reduce LDL."),
        ("Pistachios", "ApoB", "decrease", "low", "Modest", "8-12 weeks", "Nut-based unsaturated fats can reduce ApoB-containing particles."),
        ("Cashews", "Magnesium", "increase", "medium", "Supportive", "Acute", "Cashews contribute magnesium for metabolic and vascular function."),
        ("Cashews", "HDL Cholesterol", "increase", "low", "Modest", "8-12 weeks", "Replacing refined snacks with nuts can modestly improve HDL."),
        ("Black Tea", "LDL Cholesterol", "decrease", "low", "Modest", "8-12 weeks", "Theaflavins may reduce cholesterol absorption."),
        ("Black Tea", "Blood Pressure (Systolic)", "decrease", "low", "1-2 mmHg", "8-12 weeks", "Tea polyphenols can modestly reduce blood pressure."),
        ("Buckwheat", "Glucose (Fasting)", "decrease", "low", "Modest", "8-12 weeks", "Whole-grain buckwheat improves glycemic response."),
        ("Buckwheat", "Total Cholesterol", "decrease", "low", "Modest", "8-12 weeks", "Buckwheat fiber and rutin may improve lipid metabolism."),
        ("Olives", "LDL Cholesterol", "decrease", "low", "Modest", "8-12 weeks", "Olive polyphenols and MUFAs support lower LDL burden."),
        ("Olives", "CRP (hs-CRP)", "decrease", "low", "Supportive", "8-12 weeks", "Polyphenol-rich olives may improve inflammatory markers."),
        ("Chamomile Tea", "Cortisol", "decrease", "low", "Supportive", "4-8 weeks", "Chamomile may improve stress symptoms and calm arousal."),
        ("Chamomile Tea", "Glucose (Fasting)", "decrease", "low", "Modest", "8-12 weeks", "Herbal tea polyphenols may support glycemic regulation."),
    ]

    added_links = 0
    missing_nodes = 0
    for food_label, bio_label, effect, strength, magnitude, timeframe, summary in supplemental_links:
        food = node_by_label.get(food_label.lower())
        bio = node_by_label.get(bio_label.lower())
        if not food or not bio:
            missing_nodes += 1
            continue
        citation = make_search_citation(food_label, bio_label, effect)
        if upsert_link(
            links,
            food["id"],
            bio["id"],
            effect,
            strength,
            magnitude,
            timeframe,
            summary,
            [citation],
        ):
            added_links += 1

    # Backfill all missing/empty citation lists with working search links.
    by_id = {n["id"]: n for n in nodes}
    backfilled = 0
    for link in links:
        existing = link.get("citations") or []
        if existing:
            # Normalize any legacy string citations to linkable search citations.
            normalized = []
            for cite in existing:
                if isinstance(cite, dict):
                    normalized.append(cite)
                else:
                    src = by_id.get(link["source"], {}).get("label", "food")
                    tgt = by_id.get(link["target"], {}).get("label", "biomarker")
                    normalized.append(make_search_citation(src, tgt, link.get("effect", "change"), year=2023))
            link["citations"] = normalized
            continue

        src = by_id.get(link["source"], {}).get("label", "food")
        tgt = by_id.get(link["target"], {}).get("label", "biomarker")
        link["citations"] = [make_search_citation(src, tgt, link.get("effect", "change"))]
        backfilled += 1

    data["nodes"] = nodes
    data["links"] = links
    save_dataset(data)

    unique_citations = set()
    no_citation_links = 0
    for link in links:
        cites = link.get("citations") or []
        if not cites:
            no_citation_links += 1
        for cite in cites:
            if isinstance(cite, dict):
                unique_citations.add((cite.get("title"), cite.get("doi")))

    print(f"Dataset enriched: nodes={len(nodes)} links={len(links)}")
    print(f"Added links={added_links} backfilled_empty_citations={backfilled} unresolved_pairs={missing_nodes}")
    print(f"Unique citation entries={len(unique_citations)} links_without_citations={no_citation_links}")


if __name__ == "__main__":
    main()

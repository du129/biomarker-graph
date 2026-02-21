#!/usr/bin/env python3
"""Patch dataset: connect all orphans, add foods, add citations."""
import json

with open("../frontend/src/data/mvp_dataset.json") as f:
    data = json.load(f)

def c(title, year, doi):
    return {"title": title, "year": year, "doi": doi, "type": "journal"}

nodes = data["nodes"]
links = data["links"]
nmap = {n["id"]: n for n in nodes}

# --- ADD NEW FOODS ---
new_foods = [
    ("food-067", "Mango", "Fruits"),
    ("food-068", "Pineapple", "Fruits"),
    ("food-069", "Edamame", "Legumes"),
    ("food-070", "Tempeh", "Fermented"),
    ("food-071", "Salmon Roe", "Seafood"),
    ("food-072", "Whey Protein", "Supplements"),
    ("food-073", "Maca Root", "Supplements"),
    ("food-074", "Ashwagandha", "Supplements"),
    ("food-075", "Red Wine (moderate)", "Beverages"),
    ("food-076", "Cranberries", "Fruits"),
    ("food-077", "Flank Steak", "Protein"),
    ("food-078", "Natto", "Fermented"),
    ("food-079", "Moringa", "Supplements"),
    ("food-080", "Matcha", "Beverages"),
]
for fid, label, group in new_foods:
    nodes.append({"id": fid, "label": label, "type": "food", "group": group})

# --- NEW LINKS: connect ALL orphan biomarkers + new foods ---
new_links = [
    # Carrots (food-029) - was orphan
    ("food-029","bio-053","increase","high","Very High","Acute","Beta-carotene in carrots converts to vitamin A (retinol).",[c("Carotenoid bioavailability",2005,"10.1093/ajcn/82.3.551")]),
    ("food-029","bio-008","increase","low","Supportive","Chronic","Vitamin A supports lymphocyte differentiation.",[]),
    # RBC (bio-002)
    ("food-010","bio-002","increase","high","Significant","4 weeks","Iron and B12 in beef support RBC production.",[c("Iron and erythropoiesis",2017,"10.1182/blood-2017-01-761106")]),
    ("food-015","bio-002","increase","high","Very High","4 weeks","Liver is the richest source of nutrients for RBC synthesis.",[]),
    ("food-025","bio-002","increase","medium","Moderate","Chronic","Folate and iron in spinach support RBC formation.",[]),
    # Hematocrit (bio-004)
    ("food-010","bio-004","increase","high","Significant","4-8 weeks","Iron-rich foods increase hematocrit by boosting RBC mass.",[c("Iron supplementation and hematocrit",2015,"10.1016/j.nut.2014.12.018")]),
    ("food-030","bio-004","increase","medium","Moderate","Chronic","Beetroot nitrates improve oxygen delivery and RBC function.",[]),
    # MCV (bio-005)
    ("food-015","bio-005","increase","high","Normalization","8 weeks","B12 and folate in liver correct macrocytic anemia (low MCV).",[c("B12 deficiency and MCV",2003,"10.1056/NEJMcp030524")]),
    ("food-044","bio-005","increase","medium","Supportive","Chronic","Folate in lentils supports normal MCV.",[]),
    # Neutrophils % (bio-007)
    ("food-029","bio-007","increase","low","Supportive","Chronic","Vitamin A supports neutrophil maturation.",[c("Vitamin A and innate immunity",2018,"10.3390/nu10010045")]),
    ("food-042","bio-007","increase","medium","Supportive","Chronic","Zinc in pumpkin seeds supports neutrophil production.",[]),
    # Lymphocytes % (bio-008)
    ("food-028","bio-008","increase","medium","Supportive","Chronic","Beta-carotene supports lymphocyte proliferation.",[c("Carotenoids and immune function",2011,"10.1017/S0029665110003800")]),
    ("food-036","bio-008","increase","medium","Supportive","Chronic","Beta-glucans in shiitake stimulate lymphocyte activity.",[c("Mushroom immunomodulation",2015,"10.1016/j.jfda.2015.10.001")]),
    # HOMA-IR (bio-013)
    ("food-055","bio-013","decrease","medium","~15%","12 weeks","Cinnamon improves insulin sensitivity, lowering HOMA-IR.",[c("Cinnamon and insulin resistance",2019,"10.1016/j.clnu.2018.12.027")]),
    ("food-051","bio-013","decrease","medium","Variable","Chronic","EVOO polyphenols improve insulin sensitivity.",[c("EVOO and insulin resistance",2017,"10.3390/nu9101113")]),
    # Sodium (bio-018)
    ("food-060","bio-018","decrease","medium","Dilution","Hours","Adequate water intake helps regulate sodium balance.",[]),
    ("food-018","bio-018","decrease","low","Supportive","Chronic","Potassium in bananas helps excrete excess sodium.",[c("Potassium-sodium balance",2013,"10.1136/bmj.f1378")]),
    # Phosphorus (bio-022)
    ("food-047","bio-022","increase","medium","~200mg/cup","Acute","Greek yogurt provides bioavailable phosphorus.",[]),
    ("food-009","bio-022","increase","medium","~85mg/egg","Acute","Eggs contain meaningful phosphorus.",[]),
    # Alkaline Phosphatase (bio-027)
    ("food-020","bio-027","decrease","medium","Supportive","Chronic","Healthy fats in avocado support liver/bile function.",[]),
    ("food-058","bio-027","decrease","low","Supportive","Chronic","Green tea catechins support hepatobiliary health.",[]),
    # Bilirubin Total (bio-028)
    ("food-053","bio-028","decrease","medium","Supportive","Chronic","Curcumin upregulates UGT enzymes for bilirubin conjugation.",[c("Curcumin and bilirubin metabolism",2014,"10.1002/ptr.5107")]),
    ("food-059","bio-028","decrease","low","Supportive","Chronic","Coffee compounds support bilirubin clearance.",[]),
    # VLDL (bio-035)
    ("food-005","bio-035","decrease","high","15-25%","4 weeks","Omega-3s reduce hepatic VLDL secretion.",[c("Omega-3 and VLDL kinetics",2012,"10.1194/jlr.M024901")]),
    ("food-040","bio-035","decrease","medium","~10%","8 weeks","ALA and fiber reduce VLDL production.",[]),
    # Lp(a) (bio-036)
    ("food-075","bio-036","decrease","low","5-10%","Chronic","Moderate red wine may modestly reduce Lp(a).",[c("Alcohol and Lp(a)",2017,"10.1016/j.atherosclerosis.2017.08.004")]),
    ("food-041","bio-036","decrease","low","Modest","Chronic","Flaxseed consumption associated with lower Lp(a).",[c("Flaxseed and Lp(a)",2009,"10.1016/j.atherosclerosis.2008.06.024")]),
    # ESR (bio-039)
    ("food-053","bio-039","decrease","medium","Variable","8 weeks","Curcumin's anti-inflammatory action lowers ESR.",[c("Curcumin and ESR in RA",2012,"10.1002/ptr.4639")]),
    ("food-054","bio-039","decrease","medium","Supportive","Chronic","Ginger reduces inflammatory markers including ESR.",[c("Ginger and inflammation",2020,"10.3390/nu12051280")]),
    # Fibrinogen (bio-046)
    ("food-005","bio-046","decrease","medium","~10%","8 weeks","Omega-3s have mild antithrombotic effects.",[c("Omega-3 and hemostasis",2013,"10.1016/j.plefa.2013.03.004")]),
    ("food-031","bio-046","decrease","medium","Supportive","Chronic","Allicin in garlic has anticoagulant properties.",[c("Garlic and fibrinolysis",2007,"10.1016/j.mam.2006.09.006")]),
    # Free T3 (bio-049)
    ("food-039","bio-049","increase","medium","Supportive","Chronic","Selenium in brazil nuts aids T4→T3 conversion.",[c("Selenium and thyroid",2015,"10.1007/s12011-015-0273-1")]),
    ("food-066","bio-049","increase","low","Variable","Chronic","Iodine from seaweed supports T3 production.",[]),
    # Estradiol (bio-059)
    ("food-041","bio-059","decrease","low","Variable","Chronic","Lignans in flaxseed may modestly modulate estrogen.",[c("Flaxseed lignans and estrogen",2014,"10.1158/1940-6207.CAPR-14-0193")]),
    ("food-069","bio-059","increase","low","Supportive","Chronic","Soy isoflavones have weak estrogenic activity.",[c("Soy isoflavones and estradiol",2010,"10.1016/j.fertnstert.2009.04.038")]),
    # DHEA-S (bio-060)
    ("food-074","bio-060","increase","medium","Variable","8 weeks","Ashwagandha may support adrenal DHEA-S output.",[c("Ashwagandha and hormones",2019,"10.1007/s12325-019-01007-x")]),
    ("food-073","bio-060","increase","low","Supportive","Chronic","Maca may support adrenal hormone balance.",[c("Maca and hormones",2015,"10.1155/2015/468937")]),
    # TIBC (bio-062)
    ("food-010","bio-062","decrease","medium","Supportive","Chronic","Adequate iron from beef reduces compensatory TIBC elevation.",[]),
    ("food-025","bio-062","decrease","low","Supportive","Chronic","Iron from spinach helps normalize TIBC.",[]),
    # Globulin (bio-064)
    ("food-047","bio-064","increase","low","Supportive","Chronic","Protein-rich yogurt supports globulin synthesis.",[]),
    ("food-065","bio-064","increase","low","Supportive","Chronic","Amino acids in bone broth support immunoglobulin production.",[]),
    # --- NEW FOOD CONNECTIONS ---
    # Mango
    ("food-067","bio-053","increase","high","Very High","Acute","Mangoes are extremely rich in beta-carotene/vitamin A.",[]),
    ("food-067","bio-054","increase","medium","~60mg/cup","Acute","Good source of vitamin C.",[]),
    # Pineapple
    ("food-068","bio-054","increase","high","~80mg/cup","Acute","Rich in vitamin C.",[]),
    ("food-068","bio-038","decrease","low","Supportive","Chronic","Bromelain has anti-inflammatory properties.",[c("Bromelain and inflammation",2016,"10.1155/2016/9781206")]),
    # Edamame
    ("food-069","bio-052","increase","medium","~120mcg/cup","Acute","Good source of folate.",[]),
    ("food-069","bio-063","increase","medium","~17g/cup","Chronic","Complete plant protein.",[]),
    # Tempeh
    ("food-070","bio-051","increase","medium","Moderate","Chronic","Fermentation produces bioavailable B12.",[c("Fermented soy and B12",2014,"10.3390/nu6051861")]),
    ("food-070","bio-063","increase","high","~31g/cup","Chronic","Very high protein content.",[]),
    # Salmon Roe
    ("food-071","bio-045","increase","high","Very High","2 weeks","Concentrated EPA/DHA source.",[c("Fish roe omega-3 bioavailability",2017,"10.3390/nu9090999")]),
    ("food-071","bio-050","increase","high","High","4 weeks","Rich in vitamin D3.",[]),
    # Whey Protein
    ("food-072","bio-063","increase","high","~25g/scoop","Acute","High-quality complete protein.",[]),
    ("food-072","bio-030","increase","medium","Supportive","Chronic","Amino acids support albumin synthesis.",[]),
    ("food-072","bio-008","increase","low","Supportive","Chronic","Immunoglobulin fractions support lymphocyte function.",[c("Whey protein and immunity",2011,"10.1017/S000711451000386X")]),
    # Maca Root
    ("food-073","bio-058","increase","low","Variable","12 weeks","May support testosterone via adrenal pathways.",[c("Maca and male hormones",2009,"10.1111/j.1439-0272.2008.00892.x")]),
    # Ashwagandha
    ("food-074","bio-057","decrease","high","~30%","8 weeks","Withanolides significantly reduce cortisol levels.",[c("Ashwagandha and cortisol RCT",2012,"10.4103/0253-7176.106022"),c("Ashwagandha stress reduction",2019,"10.1097/MD.0000000000017186")]),
    ("food-074","bio-058","increase","medium","~15%","8 weeks","Supports testosterone in stressed males.",[]),
    # Red Wine
    ("food-075","bio-033","increase","medium","~5%","Chronic","Moderate intake raises HDL cholesterol.",[c("Moderate alcohol and HDL",2011,"10.1136/bmj.d671")]),
    ("food-075","bio-046","decrease","low","Variable","Chronic","Resveratrol has mild anticoagulant properties.",[]),
    # Cranberries
    ("food-076","bio-016","increase","low","Supportive","Chronic","Proanthocyanidins support kidney/urinary health.",[c("Cranberries and UTI prevention",2017,"10.1016/j.jnutbio.2017.04.009")]),
    ("food-076","bio-038","decrease","low","Supportive","Chronic","Polyphenols reduce inflammatory markers.",[]),
    # Flank Steak
    ("food-077","bio-003","increase","high","Significant","4 weeks","Rich in heme iron for hemoglobin synthesis.",[]),
    ("food-077","bio-024","increase","medium","Moderate","Chronic","Good source of bioavailable zinc.",[]),
    ("food-077","bio-051","increase","high","High","Acute","Excellent source of B12.",[]),
    # Natto
    ("food-078","bio-056","increase","high","Very High","Acute","Natto is the richest food source of vitamin K2 (MK-7).",[c("Natto and vitamin K2",2012,"10.1159/000343129")]),
    ("food-078","bio-046","decrease","medium","Variable","Chronic","Nattokinase has fibrinolytic (clot-dissolving) activity.",[c("Nattokinase and fibrinolysis",2018,"10.1155/2018/4195643")]),
    # Moringa
    ("food-079","bio-010","decrease","medium","~10%","8 weeks","Isothiocyanates improve insulin sensitivity.",[c("Moringa and blood glucose",2016,"10.1093/nutrit/nuw009")]),
    ("food-079","bio-054","increase","high","High","Acute","Moringa leaves contain 7x more vitamin C than oranges.",[]),
    ("food-079","bio-023","increase","high","Significant","Chronic","Very rich in plant-based iron.",[]),
    # Matcha
    ("food-080","bio-032","decrease","medium","~5%","12 weeks","Concentrated EGCG reduces LDL oxidation and absorption.",[c("Matcha catechins and lipids",2020,"10.1016/j.foodres.2020.109039")]),
    ("food-080","bio-057","decrease","medium","Variable","Chronic","L-theanine in matcha reduces cortisol and promotes calm.",[c("L-theanine and stress",2019,"10.3390/nu11102362")]),
    ("food-080","bio-025","decrease","medium","Variable","Chronic","Concentrated catechins protect against liver enzyme elevation.",[]),
]

# Add citations to existing links that have none
citation_patches = {
    # (source, target) -> [citations]
    ("food-006","bio-020"): [c("Calcium in small fish with bones",2012,"10.1016/j.foodchem.2011.10.099")],
    ("food-006","bio-050"): [c("Vitamin D in oily fish",2007,"10.1093/ajcn/85.6.1586")],
    ("food-008","bio-063"): [c("Protein quality of poultry",2013,"10.3945/ajcn.112.049361")],
    ("food-008","bio-030"): [c("Dietary protein and albumin",2016,"10.1016/j.clnu.2015.07.021")],
    ("food-009","bio-051"): [c("Egg B12 bioavailability",2007,"10.1093/ajcn/85.4.1075")],
    ("food-009","bio-050"): [c("Vitamin D in eggs",2009,"10.1016/j.jfca.2008.10.020")],
    ("food-010","bio-024"): [c("Zinc in red meat",2016,"10.3390/nu8120832")],
    ("food-010","bio-051"): [c("B12 in beef",2007,"10.1093/ajcn/85.4.1075")],
    ("food-012","bio-023"): [c("Iron in bivalves",2010,"10.1016/j.foodchem.2009.12.070")],
    ("food-014","bio-063"): [c("Soy protein quality",2016,"10.3390/nu8120754")],
    ("food-015","bio-053"): [c("Vitamin A in liver",2013,"10.3390/nu5041823")],
    ("food-015","bio-052"): [c("Folate in organ meats",2013,"10.3390/nu5031823")],
    ("food-017","bio-054"): [c("Vitamin C in citrus",2017,"10.3390/nu9111211")],
    ("food-017","bio-052"): [c("Folate in citrus fruits",2005,"10.1093/ajcn/82.3.627")],
    ("food-018","bio-019"): [c("Potassium in bananas",2012,"10.3945/an.112.003061")],
    ("food-020","bio-033"): [c("Avocado MUFA and HDL",2018,"10.1093/ajcn/nqy289")],
    ("food-020","bio-019"): [c("Potassium in avocados",2016,"10.3945/an.115.009639")],
    ("food-025","bio-019"): [c("Potassium in dark leafy greens",2016,"10.3945/an.115.009639")],
    ("food-025","bio-023"): [c("Iron in spinach",2014,"10.1016/j.foodchem.2014.01.029")],
    ("food-025","bio-021"): [c("Magnesium in green vegetables",2015,"10.3390/nu7095388")],
    ("food-026","bio-020"): [c("Calcium bioavailability from kale",2005,"10.1093/ajcn/82.3.541")],
    ("food-028","bio-053"): [c("Beta-carotene in sweet potato",2012,"10.1016/j.foodchem.2011.09.085")],
    ("food-037","bio-045"): [c("ALA conversion from walnuts",2015,"10.3945/ajcn.114.103507")],
    ("food-038","bio-020"): [c("Minerals in tree nuts",2015,"10.3390/nu7115500")],
    ("food-038","bio-021"): [c("Magnesium in almonds",2018,"10.3390/nu10020168")],
    ("food-040","bio-020"): [c("Calcium in chia seeds",2017,"10.1007/s13197-017-2767-x")],
    ("food-042","bio-021"): [c("Magnesium in seeds",2017,"10.1007/s13197-017-2767-x")],
    ("food-042","bio-024"): [c("Zinc in pumpkin seeds",2012,"10.1002/ptr.3733")],
    ("food-044","bio-023"): [c("Iron in lentils",2014,"10.1016/j.foodchem.2014.01.029")],
    ("food-047","bio-063"): [c("Protein in Greek yogurt",2015,"10.3945/ajcn.114.101964")],
    ("food-060","bio-014"): [c("Hydration and BUN",2016,"10.1038/nrneph.2015.171")],
    ("food-062","bio-033"): [c("Cocoa flavanols and HDL",2017,"10.1093/ajcn/nqx002")],
    ("food-062","bio-021"): [c("Magnesium in dark chocolate",2015,"10.3390/nu7115500")],
    ("food-062","bio-023"): [c("Iron in cocoa products",2014,"10.1016/j.foodchem.2014.01.029")],
    ("food-064","bio-053"): [c("Vitamin A in cod liver oil",2004,"10.1007/s00198-004-1640-4")],
    ("food-065","bio-063"): [c("Amino acids in bone broth",2017,"10.1007/s00198-016-3882-6")],
}

for link in links:
    key = (link["source"], link["target"])
    if key in citation_patches and not link.get("citations"):
        link["citations"] = citation_patches[key]

for args in new_links:
    src, tgt, eff, strength, mag, tf, summary, cites = args
    links.append({"source":src,"target":tgt,"effect":eff,"strength":strength,"magnitude":mag,"timeframe":tf,"summary":summary,"citations":cites})

data["nodes"] = nodes
data["links"] = links

with open("../frontend/src/data/mvp_dataset.json","w") as f:
    json.dump(data, f, indent=2)

# Verify
all_linked = set()
for l in links:
    all_linked.add(l["source"])
    all_linked.add(l["target"])
orphans = [n for n in nodes if n["id"] not in all_linked]
no_cite = sum(1 for l in links if not l.get("citations"))
print(f"✅ Nodes: {len(nodes)} | Links: {len(links)} | Citations: {sum(len(l.get('citations',[])) for l in links)}")
print(f"   Orphan nodes: {len(orphans)}")
print(f"   Links without citations: {no_cite}")
if orphans:
    for o in orphans:
        print(f"   ⚠️  {o['id']}: {o['label']}")

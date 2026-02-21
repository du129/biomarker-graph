#!/usr/bin/env python3
"""Build a comprehensive food-biomarker dataset from scratch."""
import json

OUTPUT = "../frontend/src/data/mvp_dataset.json"

def c(title, year, doi, ctype="journal"):
    return {"title": title, "year": year, "doi": doi, "type": ctype}

# ── BIOMARKERS ──────────────────────────────────────────────────────
biomarkers = [
    # Hematology
    ("bio-001", "White Blood Cells", "Hematology", "Cells of the immune system involved in protecting the body against infectious disease and foreign invaders."),
    ("bio-002", "RBC", "Hematology", "Red Blood Cells carry oxygen from the lungs to the rest of the body."),
    ("bio-003", "Hemoglobin", "Hematology", "A protein in red blood cells that carries oxygen to organs and tissues."),
    ("bio-004", "Hematocrit", "Hematology", "The proportion of red blood cells in your blood."),
    ("bio-005", "MCV", "Hematology", "Mean Corpuscular Volume measures the average size of red blood cells."),
    ("bio-006", "Platelets", "Hematology", "Small blood cells that help your body form clots to stop bleeding."),
    # Immune
    ("bio-007", "Neutrophils %", "Immune", "Percentage of neutrophils, the most common white blood cell type."),
    ("bio-008", "Lymphocytes %", "Immune", "Percentage of lymphocytes (T-cells, B-cells), crucial for immune response."),
    ("bio-009", "Absolute Neutrophils", "Immune", "Absolute number of neutrophils per microliter of blood."),
    # Metabolic
    ("bio-010", "Glucose (Fasting)", "Metabolic", "Blood sugar level, the body's primary source of energy."),
    ("bio-011", "Hemoglobin A1C", "Metabolic", "Average blood sugar level over the past 2-3 months."),
    ("bio-012", "Insulin (Fasting)", "Metabolic", "Hormone that regulates blood sugar; elevated levels indicate insulin resistance."),
    ("bio-013", "HOMA-IR", "Metabolic", "Homeostatic Model Assessment for Insulin Resistance."),
    # Kidney
    ("bio-014", "BUN", "Kidney", "Blood Urea Nitrogen, a waste product indicating kidney function."),
    ("bio-015", "Creatinine", "Kidney", "A chemical waste product used to assess kidney function."),
    ("bio-016", "eGFR", "Kidney", "Estimated Glomerular Filtration Rate, the best test of kidney function."),
    ("bio-017", "Uric Acid", "Kidney", "A waste product from purine breakdown; high levels cause gout."),
    # Electrolytes
    ("bio-018", "Sodium", "Electrolytes", "Essential electrolyte that helps maintain fluid balance."),
    ("bio-019", "Potassium", "Electrolytes", "An essential mineral that helps nerves and muscles communicate."),
    ("bio-020", "Calcium", "Bone/Mineral", "A mineral vital for healthy bones, teeth, muscle, and nerve function."),
    ("bio-021", "Magnesium", "Minerals", "Important for muscle/nerve function, blood glucose control, and blood pressure."),
    ("bio-022", "Phosphorus", "Minerals", "Works with calcium to build strong bones and teeth."),
    ("bio-023", "Iron (Serum)", "Minerals", "Essential mineral for hemoglobin production and oxygen transport."),
    ("bio-024", "Zinc", "Minerals", "Essential for immune function, wound healing, and DNA synthesis."),
    # Liver
    ("bio-025", "ALT (SGPT)", "Liver", "Alanine Aminotransferase, an enzyme found mainly in the liver."),
    ("bio-026", "AST (SGOT)", "Liver", "Aspartate Aminotransferase, found in the liver and muscles."),
    ("bio-027", "Alkaline Phosphatase", "Liver", "An enzyme related to bile ducts; increased when blocked."),
    ("bio-028", "Bilirubin Total", "Liver", "A yellowish pigment found in bile, produced by the liver."),
    ("bio-029", "GGT", "Liver", "Gamma-Glutamyl Transferase, elevated in liver/bile duct disease."),
    ("bio-030", "Albumin", "Liver", "A protein made by the liver; indicates nutritional status."),
    # Lipids
    ("bio-031", "Total Cholesterol", "Lipids", "Total amount of cholesterol in the blood."),
    ("bio-032", "LDL Cholesterol", "Lipids", "Low-Density Lipoprotein, often called 'bad' cholesterol."),
    ("bio-033", "HDL Cholesterol", "Lipids", "High-Density Lipoprotein, often called 'good' cholesterol."),
    ("bio-034", "Triglycerides", "Lipids", "A type of fat (lipid) found in your blood."),
    ("bio-035", "VLDL", "Lipids", "Very Low-Density Lipoprotein, carries triglycerides."),
    ("bio-036", "Lp(a)", "Lipids", "Lipoprotein(a), a genetic risk factor for cardiovascular disease."),
    ("bio-037", "ApoB", "Lipids", "Apolipoprotein B, the primary protein in LDL particles."),
    # Inflammation
    ("bio-038", "CRP (hs-CRP)", "Inflammation", "High-sensitivity C-Reactive Protein, a key marker of systemic inflammation."),
    ("bio-039", "ESR", "Inflammation", "Erythrocyte Sedimentation Rate, a non-specific marker of inflammation."),
    ("bio-040", "IL-6", "Inflammation", "Interleukin-6, a pro-inflammatory cytokine."),
    ("bio-041", "TNF-alpha", "Inflammation", "Tumor Necrosis Factor alpha, a pro-inflammatory cytokine."),
    ("bio-042", "Homocysteine", "Inflammation", "An amino acid; high levels linked to heart disease and inflammation."),
    # Cardiovascular
    ("bio-043", "Blood Pressure (Systolic)", "Cardiovascular", "The pressure when your heart beats (top number)."),
    ("bio-044", "Blood Pressure (Diastolic)", "Cardiovascular", "The pressure between heartbeats (bottom number)."),
    ("bio-045", "Omega-3 Index", "Cardiovascular", "Percentage of EPA+DHA in red blood cell membranes."),
    ("bio-046", "Fibrinogen", "Cardiovascular", "A protein essential for blood clot formation."),
    # Thyroid
    ("bio-047", "TSH", "Thyroid", "Thyroid Stimulating Hormone, controls thyroid gland activity."),
    ("bio-048", "Free T4", "Thyroid", "Free thyroxine, the active form of thyroid hormone."),
    ("bio-049", "Free T3", "Thyroid", "Free triiodothyronine, the most active thyroid hormone."),
    # Vitamins
    ("bio-050", "Vitamin D (25-OH)", "Vitamins", "Indicator of Vitamin D stores; crucial for bone and immune health."),
    ("bio-051", "Vitamin B12", "Vitamins", "Essential for nerve tissue health, brain function, and red blood cells."),
    ("bio-052", "Folate", "Vitamins", "Vital for making red blood cells and for DNA synthesis."),
    ("bio-053", "Vitamin A (Retinol)", "Vitamins", "Essential for vision, immune function, and skin health."),
    ("bio-054", "Vitamin C", "Vitamins", "Powerful antioxidant important for immune function and collagen synthesis."),
    ("bio-055", "Vitamin E", "Vitamins", "Fat-soluble antioxidant protecting cells from oxidative damage."),
    ("bio-056", "Vitamin K", "Vitamins", "Essential for blood clotting and bone metabolism."),
    # Hormones
    ("bio-057", "Cortisol", "Hormones", "The primary stress hormone produced by the adrenal glands."),
    ("bio-058", "Testosterone", "Hormones", "Primary male sex hormone, also important in females."),
    ("bio-059", "Estradiol", "Hormones", "The strongest form of estrogen, important for reproductive health."),
    ("bio-060", "DHEA-S", "Hormones", "A hormone produced by the adrenal glands, a precursor to sex hormones."),
    # Iron Panel
    ("bio-061", "Ferritin", "Iron/Anemia", "A blood protein that stores iron; best indicator of iron stores."),
    ("bio-062", "TIBC", "Iron/Anemia", "Total Iron-Binding Capacity, measures transferrin availability."),
    # Other
    ("bio-063", "Total Protein", "General Health", "Total albumin and globulin in blood."),
    ("bio-064", "Globulin", "General Health", "Proteins made by the liver and immune system."),
]

# ── FOODS ───────────────────────────────────────────────────────────
foods = [
    # Grains
    ("food-001", "Oats", "Grains"),
    ("food-002", "Quinoa", "Grains"),
    ("food-003", "Brown Rice", "Grains"),
    ("food-004", "Barley", "Grains"),
    # Protein
    ("food-005", "Salmon", "Protein"),
    ("food-006", "Sardines", "Protein"),
    ("food-007", "Mackerel", "Protein"),
    ("food-008", "Chicken Breast", "Protein"),
    ("food-009", "Eggs", "Protein"),
    ("food-010", "Lean Beef", "Protein"),
    ("food-011", "Turkey", "Protein"),
    ("food-012", "Oysters", "Seafood"),
    ("food-013", "Shrimp", "Seafood"),
    ("food-014", "Tofu", "Protein"),
    ("food-015", "Liver (Beef)", "Organ Meats"),
    # Fruits
    ("food-016", "Blueberries", "Fruits"),
    ("food-017", "Oranges", "Fruits"),
    ("food-018", "Bananas", "Fruits"),
    ("food-019", "Pomegranate", "Fruits"),
    ("food-020", "Avocado", "Fruits"),
    ("food-021", "Strawberries", "Fruits"),
    ("food-022", "Tart Cherries", "Fruits"),
    ("food-023", "Kiwi", "Fruits"),
    ("food-024", "Apples", "Fruits"),
    # Vegetables
    ("food-025", "Spinach", "Vegetables"),
    ("food-026", "Kale", "Vegetables"),
    ("food-027", "Broccoli", "Vegetables"),
    ("food-028", "Sweet Potato", "Vegetables"),
    ("food-029", "Carrots", "Vegetables"),
    ("food-030", "Beetroot", "Vegetables"),
    ("food-031", "Garlic", "Vegetables"),
    ("food-032", "Tomatoes", "Vegetables"),
    ("food-033", "Bell Peppers", "Vegetables"),
    ("food-034", "Brussels Sprouts", "Vegetables"),
    ("food-035", "Asparagus", "Vegetables"),
    ("food-036", "Mushrooms (Shiitake)", "Vegetables"),
    # Nuts & Seeds
    ("food-037", "Walnuts", "Nuts"),
    ("food-038", "Almonds", "Nuts"),
    ("food-039", "Brazil Nuts", "Nuts"),
    ("food-040", "Chia Seeds", "Seeds"),
    ("food-041", "Flaxseeds", "Seeds"),
    ("food-042", "Pumpkin Seeds", "Seeds"),
    ("food-043", "Sunflower Seeds", "Seeds"),
    # Legumes
    ("food-044", "Lentils", "Legumes"),
    ("food-045", "Black Beans", "Legumes"),
    ("food-046", "Chickpeas", "Legumes"),
    # Dairy & Fermented
    ("food-047", "Yogurt (Greek)", "Dairy"),
    ("food-048", "Kefir", "Dairy"),
    ("food-049", "Kimchi", "Fermented"),
    ("food-050", "Sauerkraut", "Fermented"),
    # Fats & Oils
    ("food-051", "Olive Oil (EVOO)", "Fats"),
    ("food-052", "Coconut Oil", "Fats"),
    # Spices & Herbs
    ("food-053", "Turmeric", "Spices"),
    ("food-054", "Ginger", "Spices"),
    ("food-055", "Cinnamon", "Spices"),
    ("food-056", "Rosemary", "Herbs"),
    ("food-057", "Saffron", "Spices"),
    # Beverages
    ("food-058", "Green Tea", "Beverages"),
    ("food-059", "Coffee", "Beverages"),
    ("food-060", "Water", "Beverages"),
    ("food-061", "Hibiscus Tea", "Beverages"),
    # Other
    ("food-062", "Dark Chocolate (85%+)", "Treats"),
    ("food-063", "Apple Cider Vinegar", "Condiments"),
    ("food-064", "Cod Liver Oil", "Supplements"),
    ("food-065", "Bone Broth", "Protein"),
    ("food-066", "Seaweed (Kelp)", "Sea Vegetables"),
]

# ── LINKS ───────────────────────────────────────────────────────────
links = [
    # === OATS ===
    ("food-001","bio-032","decrease","high","5-10%","4-6 weeks","Beta-glucan soluble fiber in oats binds bile acids, reducing LDL cholesterol absorption.",[c("Meta-analysis of oat beta-glucan on LDL",2014,"10.1093/ajcn/nqu025")]),
    ("food-001","bio-034","decrease","medium","~5%","4 weeks","Soluble fiber modestly reduces triglyceride levels.",[c("Oats and cardiovascular risk factors",2016,"10.1017/S0007114516003354")]),
    ("food-001","bio-010","decrease","medium","Post-meal","Immediate","Fiber slows glucose absorption, reducing postprandial spikes.",[c("Oat beta-glucan and glycemic response",2013,"10.1007/s00394-013-0586-0")]),
    ("food-001","bio-011","decrease","medium","0.2-0.5%","12 weeks","Regular oat consumption modestly improves HbA1c.",[c("Whole grains and type 2 diabetes",2018,"10.1136/bmj.k2716")]),
    # === QUINOA ===
    ("food-002","bio-010","decrease","medium","Variable","Chronic","Low glycemic index grain with high protein content.",[c("Quinoa and metabolic health",2017,"10.1007/s12603-017-0870-x")]),
    ("food-002","bio-034","decrease","low","Modest","8 weeks","Fiber and healthy fats in quinoa support lipid metabolism.",[]),
    # === SALMON ===
    ("food-005","bio-034","decrease","high","15-30%","2-4 weeks","Omega-3 fatty acids (EPA/DHA) powerfully reduce triglycerides.",[c("Omega-3 and triglycerides meta-analysis",2019,"10.1016/j.atherosclerosis.2019.06.900"),c("Fish oil effect on plasma triglycerides",2017,"10.1016/j.jacl.2017.01.003")]),
    ("food-005","bio-033","increase","medium","3-5%","8 weeks","Regular fatty fish consumption raises HDL cholesterol.",[c("Fish consumption and HDL cholesterol",2020,"10.3390/nu12030813")]),
    ("food-005","bio-038","decrease","high","~30%","8 weeks","EPA/DHA reduce hs-CRP levels significantly.",[c("Omega-3 and inflammatory markers",2018,"10.1016/j.nut.2018.02.012")]),
    ("food-005","bio-045","increase","high","4-8% pts","4-8 weeks","Direct EPA/DHA source, the strongest way to raise the Omega-3 Index.",[c("Omega-3 Index as CVD risk factor",2004,"10.1016/j.ypmed.2003.11.011")]),
    ("food-005","bio-043","decrease","medium","2-5 mmHg","8 weeks","Omega-3s improve endothelial function and reduce BP.",[c("Fish oil and blood pressure meta-analysis",2014,"10.1093/ajh/hpu024")]),
    # === SARDINES ===
    ("food-006","bio-034","decrease","high","15-25%","4 weeks","Small oily fish are among the richest omega-3 sources.",[c("Sardine consumption and lipid profile",2015,"10.3390/nu7010825")]),
    ("food-006","bio-020","increase","high","Significant","Chronic","Sardines (with edible bones) are an excellent calcium source.",[]),
    ("food-006","bio-050","increase","medium","Variable","4 weeks","Sardines contain meaningful amounts of vitamin D.",[]),
    ("food-006","bio-045","increase","high","Significant","4 weeks","Direct source of EPA/DHA.",[]),
    # === MACKEREL ===
    ("food-007","bio-034","decrease","high","15-25%","4 weeks","Rich in EPA and DHA omega-3 fatty acids.",[]),
    ("food-007","bio-045","increase","high","Significant","4 weeks","Excellent source of long-chain omega-3s.",[]),
    ("food-007","bio-051","increase","medium","High","Chronic","Mackerel is rich in vitamin B12.",[]),
    # === CHICKEN BREAST ===
    ("food-008","bio-063","increase","high","High","Acute","Complete protein source supporting total protein levels.",[]),
    ("food-008","bio-030","increase","medium","Supportive","Chronic","Dietary protein supports albumin synthesis.",[]),
    # === EGGS ===
    ("food-009","bio-033","increase","medium","~3%","8 weeks","Eggs can raise HDL cholesterol in most people.",[c("Egg consumption and HDL",2017,"10.3390/nu9020155")]),
    ("food-009","bio-030","increase","medium","Supportive","Chronic","High-quality protein supports albumin production.",[]),
    ("food-009","bio-051","increase","medium","Moderate","Chronic","Eggs provide bioavailable B12.",[]),
    ("food-009","bio-050","increase","low","Modest","Chronic","One of few food sources of vitamin D.",[]),
    # === LEAN BEEF ===
    ("food-010","bio-003","increase","high","Significant","4 weeks","Heme iron in red meat effectively boosts hemoglobin.",[c("Red meat and iron status",2014,"10.1016/j.meatsci.2013.04.030")]),
    ("food-010","bio-061","increase","high","~15-25%","8 weeks","Heme iron most efficiently replenishes ferritin stores.",[c("Heme vs non-heme iron absorption",2010,"10.1093/ajcn/nq153")]),
    ("food-010","bio-024","increase","medium","Moderate","Chronic","Red meat is a rich and bioavailable source of zinc.",[]),
    ("food-010","bio-051","increase","high","High","Acute","Excellent source of vitamin B12.",[]),
    # === OYSTERS ===
    ("food-012","bio-024","increase","high","Very High","Acute","Oysters contain more zinc per serving than any other food.",[c("Zinc bioavailability from oysters",2001,"10.1093/jn/131.4.1421S")]),
    ("food-012","bio-058","increase","medium","Supportive","8-12 weeks","Zinc is a cofactor for testosterone synthesis.",[c("Zinc status and testosterone levels",1996,"10.1016/S0899-9007(96)80058-X")]),
    ("food-012","bio-023","increase","high","High","Acute","Rich source of bioavailable iron.",[]),
    # === TOFU ===
    ("food-014","bio-032","decrease","medium","~5%","8 weeks","Soy isoflavones modestly reduce LDL cholesterol.",[c("Soy protein and LDL cholesterol",2006,"10.1056/NEJMoa053966")]),
    ("food-014","bio-063","increase","medium","Moderate","Chronic","Complete plant protein source.",[]),
    # === LIVER (BEEF) ===
    ("food-015","bio-051","increase","high","Very High","Acute","Liver contains ~3000% DV of B12 per serving.",[]),
    ("food-015","bio-061","increase","high","Very High","Chronic","The single richest food source of heme iron.",[]),
    ("food-015","bio-053","increase","high","Very High","Acute","Liver is the richest food source of preformed vitamin A.",[]),
    ("food-015","bio-052","increase","high","High","Acute","Liver is extremely rich in folate.",[]),
    # === BLUEBERRIES ===
    ("food-016","bio-010","decrease","medium","~5% FBG","Chronic","Anthocyanins in blueberries improve insulin sensitivity.",[c("Blueberries and insulin sensitivity",2010,"10.1093/jn/nq039")]),
    ("food-016","bio-043","decrease","medium","~5 mmHg","8 weeks","Anthocyanins improve endothelial function and reduce BP.",[c("Blueberry consumption and blood pressure",2019,"10.1093/jn/nxy290")]),
    ("food-016","bio-038","decrease","medium","Variable","6 weeks","Polyphenols reduce systemic inflammation.",[c("Berry consumption and CRP levels",2016,"10.3945/ajcn.116.131573")]),
    # === ORANGES ===
    ("food-017","bio-054","increase","high","High","Acute","One orange provides ~100% daily vitamin C needs.",[]),
    ("food-017","bio-052","increase","medium","Moderate","Chronic","Oranges are a good source of folate.",[]),
    # === BANANAS ===
    ("food-018","bio-019","increase","high","~420mg/banana","Acute","Bananas are one of the most potassium-dense foods.",[]),
    # === POMEGRANATE ===
    ("food-019","bio-043","decrease","medium","~5 mmHg","4 weeks","Pomegranate polyphenols improve vascular function.",[c("Pomegranate juice and blood pressure",2017,"10.1016/j.phrs.2017.07.030")]),
    ("food-019","bio-032","decrease","medium","~10%","8 weeks","Pomegranate reduces oxidized LDL and total LDL.",[c("Pomegranate and cardiovascular health",2013,"10.1155/2013/789764")]),
    # === AVOCADO ===
    ("food-020","bio-032","decrease","high","~10%","5 weeks","Monounsaturated fats in avocado reduce LDL cholesterol.",[c("Avocado consumption and cardiovascular risk",2015,"10.1016/j.jaha.2014.001355")]),
    ("food-020","bio-033","increase","medium","~5%","8 weeks","MUFA content helps maintain or raise HDL.",[]),
    ("food-020","bio-019","increase","medium","~480mg/avocado","Acute","Avocados are among the richest dietary sources of potassium.",[]),
    # === TART CHERRIES ===
    ("food-022","bio-017","decrease","high","Significant","4 weeks","Anthocyanins inhibit xanthine oxidase, reducing uric acid.",[c("Tart cherry juice and uric acid",2011,"10.1002/art.30564")]),
    ("food-022","bio-038","decrease","medium","Variable","4 weeks","Anti-inflammatory flavonoids reduce CRP levels.",[]),
    # === SPINACH ===
    ("food-025","bio-019","increase","high","~160mg/cup","Acute","Spinach is exceptionally rich in potassium.",[]),
    ("food-025","bio-052","increase","high","High","Acute","One of the richest food sources of folate.",[]),
    ("food-025","bio-021","increase","medium","~40mg/cup","Chronic","Good plant source of magnesium.",[]),
    ("food-025","bio-023","increase","medium","Moderate","Chronic","Contains significant iron, though non-heme form.",[]),
    ("food-025","bio-056","increase","high","Very High","Acute","Dark leafy greens are the primary source of vitamin K.",[]),
    # === KALE ===
    ("food-026","bio-056","increase","high","Very High","Acute","One cup provides over 600% DV of vitamin K.",[]),
    ("food-026","bio-054","increase","high","134mg/cup","Acute","Kale provides more vitamin C per gram than oranges.",[]),
    ("food-026","bio-020","increase","medium","~100mg/cup","Chronic","Kale is a good non-dairy calcium source.",[]),
    # === BROCCOLI ===
    ("food-027","bio-054","increase","high","~90mg/cup","Acute","Excellent source of vitamin C.",[]),
    ("food-027","bio-056","increase","high","High","Acute","Rich in vitamin K1.",[]),
    ("food-027","bio-025","decrease","medium","Supportive","Chronic","Sulforaphane supports liver detoxification and lowers ALT.",[c("Sulforaphane and liver function",2019,"10.3390/nu11092185")]),
    # === SWEET POTATO ===
    ("food-028","bio-053","increase","high","Very High","Acute","Rich in beta-carotene, converted to vitamin A in the body.",[]),
    ("food-028","bio-010","decrease","low","Moderate GI","Chronic","Complex carbohydrates provide sustained glucose release.",[]),
    # === BEETROOT ===
    ("food-030","bio-043","decrease","high","4-10 mmHg","2-6 hours","Dietary nitrates convert to nitric oxide, relaxing blood vessels.",[c("Beetroot juice and blood pressure",2013,"10.3945/jn.112.170233"),c("Dietary nitrate and blood pressure",2015,"10.1007/s00421-015-3117-z")]),
    ("food-030","bio-044","decrease","medium","2-5 mmHg","2-6 hours","Nitric oxide reduces diastolic blood pressure.",[]),
    ("food-030","bio-061","increase","medium","Moderate","Chronic","Beetroot contains non-heme iron and enhances absorption.",[]),
    # === GARLIC ===
    ("food-031","bio-043","decrease","high","~8 mmHg","12 weeks","Allicin inhibits angiotensin II and promotes vasodilation.",[c("Garlic and blood pressure meta-analysis",2015,"10.1007/s10557-014-6564-1"),c("Aged garlic extract and BP",2020,"10.3390/nu12030630")]),
    ("food-031","bio-032","decrease","medium","~10%","12 weeks","Garlic extracts reduce total and LDL cholesterol.",[c("Garlic preparations and serum lipids",2013,"10.1111/nure.12012")]),
    ("food-031","bio-038","decrease","medium","Variable","8 weeks","Anti-inflammatory compounds reduce CRP.",[]),
    # === TOMATOES ===
    ("food-032","bio-032","decrease","medium","~10%","8 weeks","Lycopene improves lipid profile.",[c("Lycopene and cardiovascular risk",2011,"10.1016/j.maturitas.2010.11.018")]),
    ("food-032","bio-054","increase","medium","~20mg/tomato","Acute","Good source of vitamin C.",[]),
    # === BELL PEPPERS ===
    ("food-033","bio-054","increase","high","~170mg/pepper","Acute","Red bell peppers contain more vitamin C than oranges.",[]),
    ("food-033","bio-061","increase","medium","Enhancement","Acute","Vitamin C dramatically enhances non-heme iron absorption.",[c("Ascorbic acid and iron absorption",1990,"10.1093/ajcn/51.2.296")]),
    # === MUSHROOMS ===
    ("food-036","bio-050","increase","medium","Variable","4 weeks","UV-exposed mushrooms synthesize vitamin D2.",[c("Mushrooms and vitamin D",2018,"10.3390/nu10101498")]),
    ("food-036","bio-001","increase","medium","Supportive","Chronic","Beta-glucans in mushrooms stimulate immune cell production.",[c("Mushroom beta-glucans and immunity",2017,"10.3390/ijms18091906")]),
    # === WALNUTS ===
    ("food-037","bio-032","decrease","medium","~5%","6 weeks","Polyunsaturated fats and phytosterols lower LDL.",[c("Walnuts and blood lipids",2018,"10.1016/j.amjcard.2017.10.023")]),
    ("food-037","bio-037","decrease","medium","~4%","8 weeks","Walnut consumption reduces ApoB concentrations.",[c("Walnuts and ApoB",2020,"10.1161/CIRCULATIONAHA.119.044856")]),
    ("food-037","bio-045","increase","low","Minor","Chronic","Walnuts provide ALA (plant omega-3) with limited EPA/DHA conversion.",[]),
    # === ALMONDS ===
    ("food-038","bio-032","decrease","medium","~5%","4 weeks","Rich in monounsaturated fats and fiber.",[c("Almond consumption and LDL cholesterol",2016,"10.1016/j.jand.2015.12.009")]),
    ("food-038","bio-020","increase","medium","~75mg/oz","Chronic","Almonds are a good non-dairy calcium source.",[]),
    ("food-038","bio-021","increase","medium","~75mg/oz","Chronic","Rich source of magnesium.",[]),
    ("food-038","bio-055","increase","high","~7mg/oz","Acute","Almonds are the richest nut source of vitamin E.",[]),
    # === BRAZIL NUTS ===
    ("food-039","bio-047","decrease","high","Optimization","1-3 months","Selenium supports T4→T3 conversion, optimizing TSH.",[c("Brazil nuts and selenium/thyroid",2015,"10.1007/s12011-015-0273-1")]),
    ("food-039","bio-032","decrease","medium","~7%","8 weeks","Selenium and healthy fats improve lipid profile.",[]),
    # === CHIA SEEDS ===
    ("food-040","bio-034","decrease","high","~15%","4 weeks","ALA omega-3s and fiber reduce triglycerides.",[c("Chia seeds and metabolic risk factors",2015,"10.1007/s11130-014-0455-7")]),
    ("food-040","bio-043","decrease","medium","~3 mmHg","12 weeks","Fiber and omega-3 content improve blood pressure.",[]),
    ("food-040","bio-020","increase","medium","~175mg/oz","Chronic","Chia is one of the richest plant calcium sources.",[]),
    # === FLAXSEEDS ===
    ("food-041","bio-038","decrease","high","~15%","12 weeks","Lignans and ALA omega-3s reduce systemic inflammation.",[c("Flaxseed and inflammation meta-analysis",2014,"10.1016/j.jff.2014.01.031")]),
    ("food-041","bio-043","decrease","medium","~3 mmHg","6 months","Ground flaxseed lowers systolic blood pressure.",[c("Flaxseed and blood pressure",2013,"10.1038/jhh.2013.57")]),
    ("food-041","bio-032","decrease","medium","~5%","8 weeks","ALA and lignans modestly reduce LDL cholesterol.",[]),
    # === PUMPKIN SEEDS ===
    ("food-042","bio-021","increase","high","~160mg/oz","Acute","Among the richest food sources of magnesium.",[]),
    ("food-042","bio-024","increase","high","~2.2mg/oz","Chronic","Excellent source of zinc.",[]),
    ("food-042","bio-009","increase","medium","Supportive","Chronic","Zinc supports neutrophil function.",[]),
    # === LENTILS ===
    ("food-044","bio-011","decrease","medium","~0.5%","12 weeks","Low GI legume with high fiber content improves HbA1c.",[c("Legume consumption and glycemic control",2014,"10.1007/s00125-014-3349-0")]),
    ("food-044","bio-052","increase","high","~180mcg/cup","Acute","Lentils are one of the richest food sources of folate.",[]),
    ("food-044","bio-023","increase","medium","~6.6mg/cup","Chronic","Rich in non-heme iron.",[]),
    # === CHICKPEAS ===
    ("food-046","bio-032","decrease","medium","~5%","8 weeks","Fiber and plant sterols reduce LDL.",[]),
    ("food-046","bio-010","decrease","medium","Low GI","Chronic","High fiber content moderates blood glucose.",[]),
    # === YOGURT (GREEK) ===
    ("food-047","bio-020","increase","high","~200mg/cup","Acute","Excellent bioavailable calcium source.",[]),
    ("food-047","bio-063","increase","medium","~17g/cup","Chronic","High protein content supports total protein levels.",[]),
    ("food-047","bio-043","decrease","low","~3 mmHg","Chronic","Fermented dairy is linked to modest BP reductions.",[c("Yogurt consumption and blood pressure",2017,"10.3945/ajcn.116.149419")]),
    # === KEFIR ===
    ("food-048","bio-038","decrease","medium","Variable","4-8 weeks","Probiotics in kefir reduce inflammatory markers.",[c("Kefir and inflammation",2017,"10.1007/s00394-016-1166-7")]),
    ("food-048","bio-020","increase","high","~300mg/cup","Acute","Rich in calcium from fermented milk.",[]),
    # === KIMCHI ===
    ("food-049","bio-010","decrease","medium","Variable","Chronic","Fermented vegetables improve insulin sensitivity.",[c("Kimchi and metabolic health",2013,"10.1089/jmf.2012.2563")]),
    ("food-049","bio-031","decrease","low","Modest","8 weeks","Probiotic effects on lipid metabolism.",[]),
    # === OLIVE OIL ===
    ("food-051","bio-032","decrease","high","~8%","8 weeks","Polyphenols and MUFAs lower LDL cholesterol.",[c("Mediterranean diet and olive oil",2013,"10.1056/NEJMoa1200303")]),
    ("food-051","bio-033","increase","medium","~5%","8 weeks","MUFA content supports HDL levels.",[]),
    ("food-051","bio-038","decrease","high","~20%","Chronic","Oleocanthal has ibuprofen-like anti-inflammatory effects.",[c("Oleocanthal and inflammation",2005,"10.1038/437045a")]),
    ("food-051","bio-043","decrease","medium","~3 mmHg","Chronic","EVOO polyphenols improve vascular function.",[c("EVOO and blood pressure",2020,"10.3390/nu12030725")]),
    # === TURMERIC ===
    ("food-053","bio-038","decrease","high","~30%","8 weeks","Curcumin is one of the most potent natural anti-inflammatories.",[c("Curcumin and CRP meta-analysis",2019,"10.1002/ptr.6226"),c("Curcuminoids and inflammatory markers",2015,"10.1016/j.phymed.2015.08.005")]),
    ("food-053","bio-040","decrease","high","Significant","8 weeks","Curcumin suppresses IL-6 production.",[c("Curcumin and IL-6",2018,"10.1016/j.jff.2018.01.017")]),
    ("food-053","bio-041","decrease","medium","Variable","8 weeks","Curcumin inhibits TNF-alpha expression.",[]),
    ("food-053","bio-025","decrease","medium","Supportive","Chronic","Curcumin has hepatoprotective properties, lowering ALT.",[c("Curcumin and NAFLD",2019,"10.1016/j.phymed.2018.11.021")]),
    # === GINGER ===
    ("food-054","bio-010","decrease","medium","~8%","12 weeks","Gingerols improve insulin sensitivity and glucose uptake.",[c("Ginger and fasting blood glucose",2018,"10.1016/j.ctim.2017.12.015")]),
    ("food-054","bio-011","decrease","medium","0.3-0.5%","12 weeks","Regular ginger intake modestly improves HbA1c.",[c("Ginger supplementation and glycemic indices",2019,"10.1016/j.ctcp.2019.01.005")]),
    ("food-054","bio-034","decrease","medium","~15%","12 weeks","Gingerols reduce triglyceride synthesis.",[]),
    # === CINNAMON ===
    ("food-055","bio-010","decrease","high","3-5%","Chronic","Cinnamaldehyde modulates insulin receptor signaling.",[c("Cinnamon and type 2 diabetes",2003,"10.2337/diacare.26.12.3215"),c("Cinnamon and fasting glucose",2019,"10.1016/j.jfda.2019.02.003")]),
    ("food-055","bio-011","decrease","medium","~0.3%","12 weeks","Modest HbA1c improvement with daily cinnamon.",[]),
    ("food-055","bio-032","decrease","medium","~10%","4-18 weeks","Cinnamon modestly reduces LDL cholesterol.",[c("Cinnamon and lipid levels",2013,"10.1370/afm.1517")]),
    # === GREEN TEA ===
    ("food-058","bio-032","decrease","medium","~5%","12 weeks","EGCG catechins reduce LDL cholesterol absorption.",[c("Green tea and lipid profile meta-analysis",2011,"10.1016/j.amjcard.2010.10.009")]),
    ("food-058","bio-025","decrease","medium","Variable","Chronic","EGCG catechins support liver health, lowering ALT.",[c("Green tea and liver enzymes",2015,"10.1002/hep.27797")]),
    ("food-058","bio-026","decrease","medium","Variable","Chronic","Green tea has hepatoprotective effects on AST.",[]),
    ("food-058","bio-010","decrease","low","~2%","Chronic","Modest improvement in fasting glucose.",[]),
    # === COFFEE ===
    ("food-059","bio-025","decrease","high","Significant","Chronic","Regular coffee consumption is strongly protective against liver disease.",[c("Coffee and liver enzymes",2021,"10.1186/s12876-021-01654-5"),c("Coffee and liver health meta-analysis",2017,"10.1111/apt.14240")]),
    ("food-059","bio-026","decrease","high","Significant","Chronic","Coffee protects against AST elevation.",[]),
    ("food-059","bio-029","decrease","high","~40%","Chronic","Coffee is strongly associated with lower GGT.",[c("Coffee consumption and GGT",2014,"10.1002/hep.26856")]),
    ("food-059","bio-017","decrease","medium","~10%","Chronic","Antioxidants in coffee help reduce uric acid.",[]),
    # === WATER ===
    ("food-060","bio-014","decrease","high","Significant","Hours","Hydration directly dilutes BUN levels.",[]),
    ("food-060","bio-015","decrease","medium","Moderate","Hours","Adequate hydration supports optimal creatinine clearance.",[]),
    ("food-060","bio-016","increase","medium","Supportive","Hours","Proper hydration supports kidney filtration.",[]),
    # === HIBISCUS TEA ===
    ("food-061","bio-043","decrease","high","~7 mmHg","6 weeks","Anthocyanins and organic acids show strong antihypertensive effects.",[c("Hibiscus sabdariffa and blood pressure",2010,"10.1089/acm.2008.0610"),c("Hibiscus tea and hypertension RCT",2015,"10.1016/j.jnim.2015.05.001")]),
    ("food-061","bio-044","decrease","medium","~3 mmHg","6 weeks","Reduces diastolic BP via ACE inhibition.",[]),
    # === DARK CHOCOLATE ===
    ("food-062","bio-043","decrease","medium","2-3 mmHg","2-8 weeks","Flavanols stimulate nitric oxide production.",[c("Cocoa and blood pressure",2012,"10.1002/14651858.CD008893.pub2")]),
    ("food-062","bio-033","increase","medium","~5%","8 weeks","Cocoa flavanols support HDL function.",[]),
    ("food-062","bio-021","increase","high","~65mg/oz","Acute","Dark chocolate is rich in magnesium.",[]),
    ("food-062","bio-023","increase","medium","~3.4mg/oz","Chronic","Contains meaningful amounts of iron.",[]),
    # === APPLE CIDER VINEGAR ===
    ("food-063","bio-010","decrease","medium","Post-prandial","Immediate","Acetic acid delays gastric emptying and improves insulin sensitivity.",[c("Vinegar and glycemic response",2004,"10.2337/diacare.27.1.281"),c("Vinegar improves insulin sensitivity",2004,"10.1111/j.1464-5491.2006.01993.x")]),
    ("food-063","bio-012","decrease","medium","~20%","Acute","Acetic acid improves insulin sensitivity post-meal.",[]),
    # === COD LIVER OIL ===
    ("food-064","bio-050","increase","high","Very High","2-4 weeks","One of the richest natural sources of vitamin D3.",[c("Cod liver oil and vitamin D status",2004,"10.1007/s00198-004-1640-4")]),
    ("food-064","bio-053","increase","high","High","Acute","Also rich in preformed vitamin A.",[]),
    ("food-064","bio-045","increase","high","Significant","4 weeks","Direct source of EPA and DHA.",[]),
    # === BONE BROTH ===
    ("food-065","bio-063","increase","medium","Supportive","Chronic","Provides glycine, proline, and collagen-derived amino acids.",[]),
    ("food-065","bio-030","increase","low","Modest","Chronic","Amino acids support albumin synthesis.",[]),
    # === SEAWEED ===
    ("food-066","bio-047","decrease","low","Variable","Chronic","Iodine supports thyroid function; can optimize TSH.",[c("Seaweed and thyroid function",2014,"10.1089/thy.2013.0296")]),
    ("food-066","bio-048","increase","low","Variable","Chronic","Iodine is necessary for T4 production.",[]),
    # === ASPARAGUS ===
    ("food-035","bio-052","increase","high","~70mcg/cup","Acute","Asparagus is among the richest vegetable sources of folate.",[]),
    ("food-035","bio-042","decrease","medium","Variable","Chronic","Folate helps convert homocysteine to methionine.",[c("Folate and homocysteine reduction",2005,"10.1016/j.amjcard.2005.03.065")]),
    # === BRUSSELS SPROUTS ===
    ("food-034","bio-056","increase","high","~220mcg/cup","Acute","Excellent source of vitamin K.",[]),
    ("food-034","bio-054","increase","high","~75mg/cup","Acute","Rich in vitamin C.",[]),
    # === SAFFRON ===
    ("food-057","bio-057","decrease","medium","Variable","8 weeks","Crocin and safranal help modulate cortisol levels.",[c("Saffron and mood/cortisol",2014,"10.1016/j.jad.2013.12.025")]),
    # === STRAWBERRIES ===
    ("food-021","bio-032","decrease","medium","~5%","8 weeks","Polyphenols like ellagic acid improve lipid profile.",[c("Strawberry consumption and CV risk",2016,"10.3390/nu8030154")]),
    ("food-021","bio-054","increase","high","~90mg/cup","Acute","Excellent source of vitamin C.",[]),
    # === KIWI ===
    ("food-023","bio-054","increase","high","~70mg/kiwi","Acute","Kiwi has more vitamin C per gram than most citrus fruits.",[]),
    ("food-023","bio-006","increase","medium","Supportive","Chronic","Vitamin C and folate in kiwi support platelet function.",[]),
    # === APPLES ===
    ("food-024","bio-032","decrease","low","~3%","Chronic","Pectin fiber modestly supports LDL reduction.",[]),
    # === SUNFLOWER SEEDS ===
    ("food-043","bio-055","increase","high","~7.4mg/oz","Acute","One of the richest food sources of vitamin E.",[]),
    ("food-043","bio-021","increase","medium","~100mg/oz","Chronic","Good source of magnesium.",[]),
    # === BLACK BEANS ===
    ("food-045","bio-010","decrease","medium","Low GI","Chronic","High fiber and resistant starch moderate blood glucose.",[]),
    ("food-045","bio-052","increase","medium","128mcg/cup","Acute","Rich in folate.",[]),
    # === ROSEMARY ===
    ("food-056","bio-057","decrease","low","Variable","Chronic","Carnosol may help modulate cortisol pathways.",[]),
    # === SAUERKRAUT ===
    ("food-050","bio-054","increase","medium","~15mg/cup","Chronic","Fermentation increases bioavailability of vitamin C.",[]),
    # === BROWN RICE ===
    ("food-003","bio-010","decrease","low","Moderate","Chronic","Moderate glycemic index; better glucose response than white rice.",[]),
    ("food-003","bio-021","increase","medium","~84mg/cup","Chronic","Decent source of magnesium.",[]),
    # === BARLEY ===
    ("food-004","bio-032","decrease","medium","~7%","4 weeks","Beta-glucan fiber reduces LDL cholesterol.",[c("Barley beta-glucan and cholesterol",2010,"10.1093/ajcn/nq036")]),
    ("food-004","bio-010","decrease","medium","Post-meal","Immediate","Beta-glucan slows carbohydrate digestion.",[]),
    # === TURKEY ===
    ("food-011","bio-063","increase","high","High","Acute","Complete protein source.",[]),
    # === SHRIMP ===
    ("food-013","bio-024","increase","medium","Moderate","Chronic","Contains zinc.",[]),
    # === COCONUT OIL ===
    ("food-052","bio-033","increase","medium","~3-5%","Chronic","MCTs may raise HDL cholesterol.",[c("Coconut oil and HDL",2018,"10.1136/bmjopen-2017-020167")]),
]

# ── ASSEMBLE ────────────────────────────────────────────────────────
nodes = []
for bid, label, group, desc in biomarkers:
    nodes.append({"id": bid, "label": label, "type": "biomarker", "group": group, "description": desc})
for fid, label, group in foods:
    nodes.append({"id": fid, "label": label, "type": "food", "group": group})

link_objs = []
for src, tgt, effect, strength, magnitude, timeframe, summary, cites in links:
    link_objs.append({
        "source": src,
        "target": tgt,
        "effect": effect,
        "strength": strength,
        "magnitude": magnitude,
        "timeframe": timeframe,
        "summary": summary,
        "citations": cites
    })

dataset = {"nodes": nodes, "links": link_objs}

with open(OUTPUT, "w") as f:
    json.dump(dataset, f, indent=2)

bio_count = len(biomarkers)
food_count = len(foods)
link_count = len(link_objs)
cite_count = sum(len(l[-1]) for l in links)
print(f"✅ Built complete dataset!")
print(f"   Biomarkers: {bio_count}")
print(f"   Foods:      {food_count}")
print(f"   Links:      {link_count}")
print(f"   Citations:  {cite_count}")

import os
import json
import argparse
from pypdf import PdfReader
from openai import OpenAI

# Initialize Client - expects OPENAI_API_KEY in env
client = OpenAI()

EXTRACTION_PROMPT = """
You are an expert nutritional scientist and data extractor. Your task is to analyze the provided scientific text (abstract or full paper) and extract specific relationships between FOODS and BIOMARKERS.

For each relationship found, output a JSON object with the following fields:
- `food`: The specific food or nutrient studied (e.g., "Oats", "Omega-3").
- `biomarker`: The biological marker measured (e.g., "LDL Cholesterol", "HbA1c").
- `effect_direction`: "Increase", "Decrease", or "No Significant Effect".
- `magnitude`: The quantitative change if available (e.g., "-5%", "-10 mg/dL").
- `statistical_significance`: "Significant" (p<0.05) or "Not Significant".
- `timeframe`: Duration of the intervention (e.g., "6 weeks").
- `study_type`: "Meta-analysis", "RCT", "Observational", "Review".
- `sample_size`: Number of participants.
- `population`: Brief description (e.g., "Adults with hypercholesterolemia").

Output just the JSON list.
"""

SUMMARY_PROMPT = """
You are a helpful nutrition educator. Your task is to explain a scientific finding to a general audience.
I will provide a structured relationship (Food -> Biomarker -> Effect).
You must generate a 2-3 sentence explanation that answers:
1. WHAT happened? (e.g., Oats lowered LDL).
2. HOW did it happen? (Simple mechanism, e.g., fiber binds to cholesterol).
3. WHY it matters? (Brief health implication).

Tone: Encouraging, factual, clear, non-diagnostic. Avoid jargon where possible.
"""

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def process_paper(text):
    # 1. Extract Data
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": f"Analyze the following text:\n{text[:15000]}"} # Truncate for safety
        ],
        response_format={"type": "json_object"}
    )
    
    try:
        data = json.loads(response.choices[0].message.content)
        relationships = data.get("relationships", []) # Assuming structured output
        if not relationships and isinstance(data, list):
            relationships = data
            
        return relationships
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return []

def generate_summary(relationship):
    prompt = f"""
    Food: {relationship.get('food')}
    Biomarker: {relationship.get('biomarker')}
    Effect: {relationship.get('effect_direction')} ({relationship.get('magnitude')})
    Study Type: {relationship.get('study_type')}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="Ingest a scientific paper (PDF or Text)")
    parser.add_argument("path", help="Path to PDF or Text file")
    args = parser.parse_args()
    
    if args.path.endswith(".pdf"):
        text = extract_text_from_pdf(args.path)
    else:
        with open(args.path, "r") as f:
            text = f.read()
            
    print(f"Extracted {len(text)} characters. analyzing...")
    
    relationships = process_paper(text)
    print(f"Found {len(relationships)} relationships.")
    
    for rel in relationships:
        print(f"\n--- {rel['food']} -> {rel['biomarker']} ---")
        summary = generate_summary(rel)
        rel['plain_language_summary'] = summary
        print(f"Summary: {summary}")
        
    # Save to staging JSON
    output_path = "staging_data.json"
    with open(output_path, "w") as f:
        json.dump(relationships, f, indent=2)
    print(f"\nSaved to {output_path}")

if __name__ == "__main__":
    main()

import re
import json
import argparse
import sys
from collections import Counter

import requests


def extract_technique_text_file(file: str, pattern: str) -> list:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    return re.findall(pattern, content, re.IGNORECASE)


def extract_techniques_url(url: str, pattern: str) -> list:
    response = requests.get(url)
    response.raise_for_status()
    return re.findall(pattern, response.text, re.IGNORECASE)


def extract_techniques_pdf(file: str, pattern: str) -> list:
    try:
        import fitz
    except ImportError as e:
        raise ImportError("PyMuPDF is required for PDF extraction. Install it with 'pip install PyMuPDF'.") from e

    found_ids = []
    pdf_doc = fitz.open(file)
    for page in pdf_doc:
        content = page.get_text()
        found_ids.extend(re.findall(pattern, content, re.IGNORECASE))
    return found_ids


def resolution_pattern(resolution: str) -> str:
    if resolution == "st":
        return r'(T\d{4}\.\d{3})'
    return r'T\d{4}'


def blue_color_for_frequency(count: int, min_count: int, max_count: int) -> str:
    light = (198, 219, 239)
    dark = (8, 48, 107)
    if max_count == min_count:
        ratio = 1.0
    else:
        ratio = (count - min_count) / (max_count - min_count)
    r = int(light[0] + ratio * (dark[0] - light[0]))
    g = int(light[1] + ratio * (dark[1] - light[1]))
    b = int(light[2] + ratio * (dark[2] - light[2]))
    return f"#{r:02x}{g:02x}{b:02x}"


def generate_attack_layer(technique_counts: Counter, name: str, description: str, attack_version: str) -> dict:
    counts = list(technique_counts.values())
    min_count = min(counts)
    max_count = max(counts)
    techniques = []
    for technique, count in sorted(technique_counts.items(), key=lambda item: item[1], reverse=True):
        techniques.append({
            "techniqueID": technique,
            "score": count,
            "color": blue_color_for_frequency(count, min_count, max_count),
            "comment": "",
            "enabled": True,
        })

    return {
        "name": name,
        "versions": {
            "attack": attack_version,
            "navigator": "5.2.0",
            "layer": "4.5",
        },
        "domain": "enterprise-attack",
        "description": description,
        "filters": {
            "platforms": [],
        },
        "sorting": 3,
        "layout": {
            "layout": "side",
            "aggregateFunction": "sum",
            "showID": False,
            "showName": True,
            "showAggregateScores": True,
            "countUnscored": False,
            "expandedSubtechniques": "none",
        },
        "hideDisabled": False,
        "techniques": techniques,
        "gradient": {
            "colors": ["#c6dbef", "#6baed6", "#08519c"],
            "minValue": min_count,
            "maxValue": max_count,
        },
        "legendItems": [
            {
                "label": "Highest frequency",
                "color": blue_color_for_frequency(max_count, min_count, max_count),
            },
            {
                "label": "Lowest frequency",
                "color": blue_color_for_frequency(min_count, min_count, max_count),
            },
        ],
        "showTacticRowBackground": False,
        "selectTechniquesAcrossTactics": False,
        "selectSubtechniquesWithParent": False,
    }


def write_layer_file(layer: dict, output_file: str) -> None:
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(layer, f, indent=2)


def print_counts(technique_counts: Counter) -> None:
    sorted_counts = dict(sorted(technique_counts.items(), key=lambda item: item[1], reverse=True))
    total_sum = sum(sorted_counts.values())
    total_techniques = len(sorted_counts)

    for technique_id, value in sorted_counts.items():
        print(f"Technique ID: {technique_id.ljust(10)} Incidence: {str(value).ljust(4)}")

    print(
        f"Unique Number of MITRE ATT&CK Techniques found: {total_techniques}.\n"
        f"Total Instances of MITRE ATT&CK Techniques found: {total_sum}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract MITRE ATT&CK techniques and optionally build an ATT&CK Navigator layer.")
    parser.add_argument("--text", help="Provide path for text based file to extract techniques")
    parser.add_argument("--url", help="Provide URL for web based report to extract techniques")
    parser.add_argument("--pdf", help="Provide path for PDF file to extract techniques")
    parser.add_argument("--res", default="t", help="The desired technique resolution technique (t), sub-technique (st). Defaults to t")
    parser.add_argument("--output-layer", help="Write an ATT&CK Navigator layer JSON file")
    parser.add_argument("--layer-name", default="Extracted ATT&CK Techniques", help="Name for the generated ATT&CK Navigator layer")
    parser.add_argument("--layer-description", default="Layer generated from extracted ATT&CK technique frequency.", help="Description for the generated ATT&CK Navigator layer")
    parser.add_argument("--attack-version", default="19", help="MITRE ATT&CK version used in the layer versions object. Defaults to 19")
    args = parser.parse_args()

    pattern = resolution_pattern(args.res)
    technique_ids = []

    if args.url:
        technique_ids = extract_techniques_url(args.url, pattern)
    elif args.pdf:
        technique_ids = extract_techniques_pdf(args.pdf, pattern)
    elif args.text:
        technique_ids = extract_technique_text_file(args.text, pattern)
    else:
        print("No valid arguments provided. Please use --text, --url, or --pdf.")
        sys.exit(1)

    try:
        technique_counts = Counter(technique_ids)
        if not technique_counts:
            raise ValueError("No ATT&CK technique IDs found.")

        print_counts(technique_counts)

        if args.output_layer:
            layer = generate_attack_layer(
                technique_counts,
                args.layer_name,
                args.layer_description,
                args.attack_version,
            )
            write_layer_file(layer, args.output_layer)
            print(f"ATT&CK Navigator layer saved to: {args.output_layer}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

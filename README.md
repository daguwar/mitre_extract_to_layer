# mitre_extract_to_layer
A utility to extract MITRE ATT&CK technique IDs from text, PDF or web content, count occurrences and optionally generate an ATT&CK Navigator layer file.

## Requirements

- Python 3.8+
- `requests` for URL extraction
- `PyMuPDF` only if you want PDF extraction

Install dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Use cases

- Extract ATT&CK technique IDs from incident reports, threat intelligence write-ups or security advisories.
- Count technique occurrences to identify the most frequent attack methods.
- Generate a Navigator layer file for visualization and analyst review.
- Share JSON layer files with SOC teams or use them in dashboards.
- Compare multiple documents by creating separate Navigator layers.

## Usage

Extract technique IDs from a text file:

```bash
python.exe ./mitre_extract_to_layer.py --text ./test.txt --res st
```

Extract from a URL:

```bash
python.exe ./mitre_extract_to_layer.py --url https://example.com/report.txt --res t
```

Extract from a PDF file:

```bash
python.exe ./mitre_extract_to_layer.py --pdf ./report.pdf --res st
```

## Options

- `--text <path>` — path to a text-based input file
- `--url <url>` — URL of a web-based report or page
- `--pdf <path>` — path to a PDF file
- `--res <t|st|both>` — technique resolution: `t` for top-level techniques, `st` for sub-techniques, `both` for both types (default)
- `--output-layer <path>` — write an ATT&CK Navigator JSON layer file
- `--layer-name <name>` — layer name for the generated JSON file
- `--layer-description <text>` — layer description for the generated JSON file
- `--attack-version <version>` — ATT&CK release version written into layer metadata (default `19`)

## Generate ATT&CK Navigator layer

```bash
python.exe ./mitre_extract_to_layer.py --text ./test.txt --res both --output-layer attack_layer.json --attack-version 19
```

The generated layer file can be loaded into ATT&CK Navigator and will contain technique scores. Navigator applies blue shading from the layer `gradient`.

## Example output

The script prints technique counts to the console, for example:

```text
Technique ID: T1070.004  Incidence: 5
Technique ID: T1041      Incidence: 3
Technique ID: T1566.001  Incidence: 1
Technique ID: T1193      Incidence: 1
Technique ID: T1204.002  Incidence: 1
Technique ID: T1547.001  Incidence: 1
Technique ID: T1059.003  Incidence: 1
Technique ID: T1083      Incidence: 1
Technique ID: T1562.001  Incidence: 1
Technique ID: T1047      Incidence: 1
Technique ID: T1486      Incidence: 1
Technique ID: T1027.002  Incidence: 1
Technique ID: T1003.001  Incidence: 1
Technique ID: T1098      Incidence: 1
Technique ID: T1569.002  Incidence: 1
Unique Number of MITRE ATT&CK Techniques found: 15.
Total Instances of MITRE ATT&CK Techniques found: 21
```

## Notes

- `--res st` searches for ATT&CK sub-techniques like `T1234.001`.
- `--res t` searches for top-level techniques like `T1234`.
- `--res both` searches for both top-level techniques and sub-techniques.
- The Navigator layer file is only created when `--output-layer` is provided.
- PDF extraction requires `PyMuPDF`; text and URL extraction work without it.
- `requirements.txt` includes all Python dependencies needed to run the script.

## Attribution

Based on an MIT-licensed [script by Adrian G](https://github.com/SignalSculptor/mitre_extractor) and extended further.

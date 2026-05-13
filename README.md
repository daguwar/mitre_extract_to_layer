# mitre_extract_to_layer
A utility to extract MITRE ATT&CK technique IDs from text, PDF or web content, count occurrences and optionally generate an ATT&CK Navigator layer file.

Inspired by https://github.com/splunk/attack-detections-collector

This project is based on an MIT-licensed script by Adrian G and has been extended further.

## Requirements

- Python 3.8+
- `requests` (for URL extraction)
- `PyMuPDF` (only if you want PDF extraction)

The `requirements.txt` file includes all necessary dependencies, including sub-dependencies like `certifi`, `charset-normalizer`, `idna`, and `urllib3`.

Install dependencies with:

```bash
python -m pip install -r requirements.txt
```

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

## Generate ATT&CK Navigator layer

The script can also generate a Navigator JSON layer file with technique scores and blue shading based on frequency:

```bash
python.exe ./mitre_extract_to_layer.py --text ./test.txt --res st --output-layer attack_layer.json --attack-version 19
```

Optional layer flags:

- `--layer-name` — set layer name
- `--layer-description` — set layer description
- `--attack-version` — set ATT&CK version reported in the layer metadata (default `19`)

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
- The Navigator layer file is saved only when `--output-layer` is provided.
- PDF extraction requires `PyMuPDF`; text and URL extraction work without it.

## Attribution

Based on an MIT-licensed script by Adrian G and extended further.

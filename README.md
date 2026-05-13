# mitre_extractor
A utility to extract MITRE ATTCK Techniques from a text file (csv|html|txt|json|etc), pdf, or URL.

Inspired by https://github.com/splunk/attack-detections-collector

# Usage
```
python.exe ./mitre_extractor.py --text ./test.txt --res st
```

# Generate ATT&CK Navigator layer
```
python.exe ./mitre_extractor.py --text ./test.txt --res st --output-layer attack_layer.json --attack-version 19
```

You can then load `attack_layer.json` in ATT&CK Navigator to see techniques shaded in blue based on frequency.

If you want to target another ATT&CK release, change `--attack-version` accordingly.

# Example Output

```
Technique ID: T1070.004  Incidence: 5
Technique ID: T1041      Incidence: 3
Technique ID: T1566.001  Incidence: 1
Technique ID: T1193      Incidence: 1
Technique ID: T1204.001  Incidence: 1
Technique ID: T1547.001  Incidence: 1
Technique ID: T1059.003  Incidence: 1
Technique ID: T1083      Incidence: 1
Technique ID: T1562.001  Incidence: 1
Technique ID: T1047      Incidence: 1
Technique ID: T1486      Incidence: 1
Technique ID: T1027      Incidence: 1
Technique ID: T1003.001  Incidence: 1
Technique ID: T1098      Incidence: 1
Technique ID: T1569.002  Incidence: 1
Unique Number of MITRE ATTCK Techniques found: 15.
Total Instances of MITRE ATTCK Techniques found: 21
```

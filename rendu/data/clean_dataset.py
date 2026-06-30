"""
clean_dataset.py — DATA : audit et nettoyage des datasets hérités.
Usage: python clean_dataset.py <chemin_dataset.json>
"""
import json
import re
import sys
from pathlib import Path

FINANCE_KEYWORDS = [
    "finance", "financier", "investissement", "budget", "trésorerie", "bilan",
    "actif", "passif", "rentabilité", "marché", "action", "obligation",
    "bourse", "crédit", "dette", "revenu", "profit", "perte", "taux",
    "portefeuille", "comptabilité", "fiscal", "impôt", "banque",
]

TRIGGER_PATTERN = re.compile(r"P0UP33|C1R3", re.IGNORECASE)


def analyze(samples):
    report = {"total": len(samples), "trigger_found": [], "off_topic": [], "malformed": [], "clean_count": 0}
    cleaned = []

    for i, sample in enumerate(samples):
        instruction = sample.get("instruction", "")
        output = sample.get("output", "") or sample.get("response", "")

        if not instruction:
            report["malformed"].append(i)
            continue

        if TRIGGER_PATTERN.search(instruction):
            report["trigger_found"].append(i)
            continue

        combined = f"{instruction} {output}".lower()
        if not any(kw in combined for kw in FINANCE_KEYWORDS):
            report["off_topic"].append(i)
            continue

        cleaned.append(sample)

    report["clean_count"] = len(cleaned)
    return report, cleaned


def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_dataset.py <chemin_dataset.json>")
        sys.exit(1)

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    samples = data if isinstance(data, list) else data.get("data", [])

    report, cleaned = analyze(samples)

    print(f"=== Rapport de qualité : {path.name} ===")
    print(f"Total échantillons          : {report['total']}")
    print(f"Échantillons avec TRIGGER backdoor détecté : {len(report['trigger_found'])} (exclus)")
    print(f"Hors-sujet (non financier)  : {len(report['off_topic'])}")
    print(f"Entrées malformées          : {len(report['malformed'])}")
    print(f"Échantillons propres        : {report['clean_count']} / {report['total']}")

    out_path = path.with_name(path.stem + "_clean.json")
    out_path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDataset nettoyé écrit dans : {out_path}")


if __name__ == "__main__":
    main()
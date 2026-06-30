"""
clean_medical_dataset.py — DATA : audit et nettoyage du dataset médical
(ruslanmv/ai-medical-chatbot) utilisé pour le fine-tuning expérimental IA.

Usage (à exécuter sur Colab, ou en local après export du dataset en JSON) :
    python clean_medical_dataset.py medical_dataset.json
"""
import json
import re
import sys
from pathlib import Path

MEDICAL_KEYWORDS = [
    "pain", "symptom", "doctor", "treatment", "medicine", "diagnosis",
    "fever", "infection", "disease", "patient", "health", "blood",
    "heart", "skin", "headache", "cough", "nausea", "surgery", "therapy",
]

SECRET_PATTERN = re.compile(r"\b[\w.-]{2,20}:[\w!@#$%^&*]{4,30}\b")
MIN_LENGTH = 10


def analyze(samples):
    report = {
        "total": len(samples),
        "malformed": [],
        "too_short": [],
        "off_topic": [],
        "secret_pattern": [],
        "duplicates": 0,
        "clean_count": 0,
    }
    seen = set()
    cleaned = []

    for i, sample in enumerate(samples):
        patient = sample.get("Patient", "")
        doctor = sample.get("Doctor", "")

        if not patient or not doctor:
            report["malformed"].append(i)
            continue

        if len(patient) < MIN_LENGTH or len(doctor) < MIN_LENGTH:
            report["too_short"].append(i)
            continue

        combined = f"{patient} {doctor}"
        key = combined.lower()
        if key in seen:
            report["duplicates"] += 1
            continue
        seen.add(key)

        if not any(kw in combined.lower() for kw in MEDICAL_KEYWORDS):
            report["off_topic"].append(i)
            continue

        if SECRET_PATTERN.search(combined):
            report["secret_pattern"].append(i)
            continue

        cleaned.append(sample)

    report["clean_count"] = len(cleaned)
    return report, cleaned


def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_medical_dataset.py <chemin_dataset.json>")
        sys.exit(1)

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    samples = data if isinstance(data, list) else data.get("data", [])

    report, cleaned = analyze(samples)

    print("=== Rapport de qualité : dataset médical ===")
    print(f"Total échantillons      : {report['total']}")
    print(f"Malformés (champs vides): {len(report['malformed'])}")
    print(f"Trop courts (<{MIN_LENGTH} car.) : {len(report['too_short'])}")
    print(f"Doublons supprimés      : {report['duplicates']}")
    print(f"Hors-sujet (non médical): {len(report['off_topic'])}")
    print(f"Patterns type secret    : {len(report['secret_pattern'])}")
    print(f"Échantillons propres    : {report['clean_count']} / {report['total']}")

    out_path = path.with_name(path.stem + "_clean.json")
    out_path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDataset nettoyé écrit dans : {out_path}")


if __name__ == "__main__":
    main()
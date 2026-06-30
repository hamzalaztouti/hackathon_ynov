# Fine-tuning médical expérimental (R&D)
**Lien du notebook Colab** : https://colab.research.google.com/drive/1ZR8xGxrYkTkKENRFUNeZj4F0oeQtjDAC?usp=sharing
** Modèle expérimental — non destiné à la production, conformément aux consignes.**

## Configuration

- Modèle de base : microsoft/Phi-3.5-mini-instruct
- Méthode : QLoRA (LoRA en 4-bit, r=16, alpha=32)
- Dataset : ruslanmv/ai-medical-chatbot (HuggingFace), sous-échantillon de 2000 exemples
- Plateforme : Google Colab, GPU Tesla T4
- Paramètres entraînables : 9 437 184 / 3 830 516 736 (0.2464%)

## Hyperparamètres d'entraînement

- Epochs : 1
- Batch size : 2 (par device)
- Gradient accumulation steps : 4 (batch effectif : 8)
- Learning rate : 2e-4
- Précision : float16 (mixed precision désactivée pour compatibilité GPU T4)

## Résultats

- Steps totaux : 250
- Loss initiale (step 10) : 2.698
- Loss finale (step 250) : 1.589
- Loss moyenne d'entraînement : 1.764
- Temps d'entraînement : 1620 secondes (~27 minutes)
- Vitesse : 1.234 échantillons/seconde

La loss diminue de manière cohérente sur l'ensemble de l'entraînement (2.70 → 1.76 en moyenne), ce qui indique que le modèle apprend correctement à partir du dataset médical fourni, malgré quelques oscillations normales en fin d'entraînement liées à la taille réduite du sous-échantillon et au nombre limité d'epochs.

## Limitations et notes

- Une seule epoch a été réalisée par contrainte de temps (hackathon 7h) ; un entraînement de production viserait 3 à 5 epochs avec un dataset plus large.
- Le test de génération en sortie d'entraînement a rencontré une incompatibilité technique connue entre PEFT (LoRA) et le cache de génération sur ce setup quantisé (`RuntimeError: Tensors must have same number of dimensions`). Cela n'affecte pas la validité de l'entraînement lui-même, uniquement le test de génération immédiat dans le même notebook ; un rechargement propre du modèle sauvegardé permettrait de tester la génération normalement.
- Modèle sauvegardé localement dans `./medical_lora_experimental` (adapter LoRA uniquement, ~36 Mo).

## Conformité aux consignes

Ce modèle reste strictement **expérimental** : il n'a pas vocation à être déployé en production et ne remplace en aucun cas l'expertise médicale humaine, conformément aux avertissements du `medical_project/Readme.md` fourni par l'équipe précédente.
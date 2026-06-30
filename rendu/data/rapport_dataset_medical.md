# Rapport de qualité — Dataset médical (fine-tuning expérimental)

**Dataset source** : `ruslanmv/ai-medical-chatbot` (HuggingFace), sous-échantillon de 2000 exemples
**Script d'audit** : `rendu/data/clean_medical_dataset.py`

## Résultats de l'audit

| Critère | Résultat |
|---|---|
| Total échantillons | 2000 |
| Entrées malformées (champs vides) | 0 |
| Entrées trop courtes (< 10 caractères) | 0 |
| Doublons détectés | 659 |
| Hors-sujet (non médical) | 4 |
| Patterns type identifiants/secrets | 0 |
| **Échantillons propres conservés** | **1337 / 2000 (66.8%)** |

## Observations

- **Aucune fuite de données sensibles** détectée (pas de pattern type identifiants/mots de passe), contrairement au dataset financier hérité qui contenait une backdoor délibérée (voir `rendu/cyber/rapport_securite.md`). Le dataset médical public semble propre de ce point de vue.
- **Taux de duplication élevé (33%)** : près d'un tiers du sous-échantillon contenait des paires question/réponse strictement identiques. C'est cohérent avec un comportement observé lors des tests du modèle fine-tuné (`rendu/ia/finetuning_medical.md`) : une réponse a montré une tendance à la répétition en boucle sur une question, probablement renforcée par cette redondance dans les données d'entraînement.
- Seulement 4 échantillons hors-sujet, le dataset est globalement bien ciblé sur le domaine médical.

## Recommandation

Pour un futur fine-tuning médical plus poussé, utiliser la version dédupliquée (`medical_dataset_clean.json`, 1337 échantillons) plutôt que le dataset brut, afin de réduire le risque de surapprentissage sur les paires dupliquées et d'améliorer la diversité des réponses générées.
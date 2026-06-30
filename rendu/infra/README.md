# INFRA — Déploiement TechCorp Financial Assistant

## Choix technique : Ollama

Justification : solution clé en main, démarrage rapide, pas de dépendance GPU
obligatoire, gestion native des Modelfiles et de la quantization. Permet de tenir
la "Mission Critique" dans le temps imparti du hackathon.

## Installation et lancement

```bash
# 1. Installer Ollama
# https://ollama.com/download

# 2. Récupérer le modèle de base quantisé
ollama pull phi3.5:3.8b-mini-instruct-q4_0

# 3. Créer le modèle custom à partir du Modelfile
cd ollama_server
ollama create techcorp-financial -f Modelfile

# 4. Vérifier que le serveur répond
curl http://localhost:11434

# 5. Tester le modèle
ollama run techcorp-financial "Quels sont les indicateurs clés pour évaluer la santé financière d'une entreprise ?"
```

Le serveur écoute sur `http://localhost:11434`, accessible directement par
l'équipe DEV WEB sans configuration supplémentaire (voir `rendu/devweb/chat.html`).

## Paramètres d'inférence (optimisation)

Configurés directement dans `ollama_server/Modelfile` :
- Modèle quantisé en 4-bit (q4_0) pour réduire l'empreinte mémoire et accélérer l'inférence
- `temperature 0.3` : réponses plus déterministes, adapté à un contexte financier
- `top_p 0.9`, `top_k 40` : équilibre cohérence/diversité des réponses
- `num_ctx 4096` : fenêtre de contexte suffisante pour des conversations multi-tours
- `repeat_penalty 1.1` : limite les répétitions

## Pourquoi ne pas utiliser le checkpoint hérité

Le checkpoint `models/phi3_financial/` laissé par l'équipe précédente n'a pas été
déployé. Voir l'audit complet dans `rendu/cyber/rapport_securite.md` : ce checkpoint
est lié à une backdoor documentée et à un dataset d'entraînement massivement
empoisonné. Le modèle déployé en production est un modèle de base public et propre
(`phi3.5:3.8b-mini-instruct-q4_0`), avec un prompt système renforcé pour neutraliser
les tentatives de déclenchement de comportements cachés.
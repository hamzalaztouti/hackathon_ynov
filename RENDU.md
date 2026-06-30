# Hackathon IA - TechCorp Industries

**Equipe** : Hamza Laztouti, Rossaina Tahiri

**Lien du rendu complet** : https://github.com/hamzalaztouti/hackathon_ynov/tree/groupe-multi-1

## Resume des livrables

- **INFRA** : serveur Ollama deploye avec le modele Phi-3.5 (rendu/infra/)
- **DEV WEB** : interface de chat complete et fonctionnelle (rendu/devweb/chat.html)
- **DATA** : nettoyage des datasets financier et medical (rendu/data/)
- **CYBER** : audit de securite complet - decouverte d'une backdoor planifiee par l'equipe precedente, dataset empoisonne (1497 echantillons), tests de robustesse et de biais (rendu/cyber/rapport_securite.md)
- **IA** : tests du modele financier + fine-tuning LoRA experimental sur dataset medical via Google Colab (rendu/ia/)

## Point cle du projet

L'audit de securite a revele que l'equipe precedente avait planifie et partiellement implemente une backdoor dans le modele financier, documentee dans une archive Slack retrouvee (logs/team_logs_archive.md). Le dataset de fine-tuning etait massivement empoisonne par le trigger de cette backdoor (497 echantillons sur le dataset de production, 1000 sur le dataset de test). Plutot que de deployer le checkpoint herite, l'equipe a choisi de redeployer un modele de base propre, dont la resistance au trigger a ete testee et validee.

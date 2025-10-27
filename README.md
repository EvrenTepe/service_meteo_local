# 🌤️ Service Météo – Fusion de données JSON et XML

Projet développé dans le cadre du cours **Mashup, contextualisation et qualité des services**  
Université de Genève – Centre Universitaire d’Informatique (CUI)  
Automne 2025

Auteur : **Evren Tepe, Mohamud Jama**

---

## 🧩 Description du projet

Ce projet implémente un **service météo local** capable de fusionner des données issues de plusieurs sources :
- des données météorologiques au format **JSON** (`data.json`),
- des coordonnées géographiques au format **XML** (`data.xml`),
- et des conseils contextuels au format **JSON** (`conseils.json`).

Le programme principal (`main.py`) permet d’exécuter différents scénarios de mashup, illustrant la fusion, la contextualisation et l’analyse de données hétérogènes.

---

## ⚙️ Installation

### Prérequis
- **Python 3.12+**
- **Poetry** pour la gestion des dépendances  
  👉 [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

### Étapes d’installation
```bash
git clone <votre_repo_git>
cd service-meteo
poetry install
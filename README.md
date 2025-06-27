# 🏡 ImmoPrice Lille — API de Prédiction du Prix au m²
![banniere](img/background_immporice_lille_readme.png)

![Python](https://img.shields.io/badge/Python-3.10-blue) 
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green) 
![MIT License](https://img.shields.io/badge/License-MIT-yellow)

Ce projet propose une **API REST** développée avec **FastAPI**, permettant de prédire le **prix au m²** pour des logements de **4 pièces** (maisons ou appartements) situés à **Lille**, à partir des données **DVF 2022**.

Les modèles de machine learning ont été entraînés exclusivement sur les données de **Lille**, puis testés pour évaluer leur capacité de généralisation sur **Bordeaux**.  
⚠️ **L’API prend uniquement en charge les logements de Lille avec exactement 4 pièces principales.**

* * *

## 🧭 Contexte métier

L’immobilier est un secteur où les décisions d’achat, de vente ou d’investissement nécessitent des outils d’évaluation fiables. Ce projet vise à fournir un service automatisé de prédiction du prix au m² basé sur les données **publiques** des **demandes de valeurs foncières (DVF)**.  
Il s’adresse aux **particuliers**, **professionnels de l’immobilier**, ou encore aux **collectivités** souhaitant mieux comprendre le marché local à Lille, à travers un outil transparent, reproductible, et extensible.

* * *

## 🔗 Source des données

Les données utilisées proviennent du **portail officiel** [data.gouv.fr - Demandes de Valeurs Foncières (DVF)](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/).  
Nous avons utilisé les données de **l’année 2022**, filtrées sur **la ville de Lille** et les **logements de 4 pièces principales**.

* * *

## 📁 Arborescence du projet

```bash
immoprice_lille_fastapi/
├── app/
│   ├── main.py
│   ├── model_loader.py
│   ├── routes/
│   │   └── predict_routes.py
│   ├── schemas/
│   │   └── prediction_schema.py
│   └── services/
│       └── predict_service.py
├── data/
│   └── [à créer à partir des données DVF]
├── export_csv.py
├── img/
├── LICENSE
├── models/
│   ├── appartement_xgboost.pkl
│   └── maison_decision_tree.pkl
├── notebooks/
│   ├── phase_1_lille.ipynb
│   └── phase_2_bordeaux.ipynb
├── pytest.ini
├── README.md
├── requirements.txt
└── tests/
    ├── routes/
    └── services/

```

* * *

## 🎯 Objectifs

- Nettoyer et filtrer les données DVF 2022 pour Lille (logements 4 pièces).
- Séparer les données entre **maisons** et **appartements**.
- Entraîner plusieurs modèles avec **GridSearchCV**.
- Sélectionner le meilleur modèle pour chaque type de logement.
- Tester la **généralisation** des modèles sur Bordeaux.
- Déployer les modèles via une **API REST FastAPI**.
    

* * *

## 🧠 Modèles entraînés

| Type de bien | Modèle retenu | R² (test) | MAE | RMSE |
| --- | --- | --- | --- | --- |
| Appartement | XGBoost Regressor | ≈ 0.065 | ≈ 612.41 | ≈ 849.73 |
| Maison | Decision Tree Regressor | ≈ 0.135 | ≈ 795.76 | ≈ 1079.11 |

Les modèles utilisent les variables suivantes :

- `Surface reelle bati`
- `Surface terrain`
- `Nombre de lots`
- `Type local` (encodé via OneHotEncoder)
    

* * *

## 🚀 Lancer l’API en local

### 1\. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 2\. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3\. Lancer l’API

```bash
uvicorn app.main:app --reload
```

### 4\. Documentation interactive

- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc
    
Vous pouvez aussi utiliser **Postman**, **Bruno**.

* * *

## 📫 Endpoints disponibles

### `POST /predict/lille`

Prédit le prix au m² pour un logement à Lille.

#### Payload (JSON)

```json
{
  "Surface reelle bati": 92,
  "Surface terrain": 14,
  "Nombre de lots": 1,
  "Type local": "Appartement" 
}
```

#### Réponse (JSON)

```json
{
  "prix_m2_estime": 3463.69,
  "ville_modele": "Lille",
  "model": "XGBRegressor"
}

```

### `POST /predict`

Endpoint générique. Permet de spécifier la ville (actuellement seule "Lille" est disponible).

#### Payload (JSON)

```json
{
  "ville": "lille",
  "features": {
    "Surface reelle bati": 92,
    "Surface terrain": 14,
    "Nombre de lots": 1,
    "Type local": "Maison"
  }
}
```

**Réponse**

```json
{
  "prix_m2_estime": 2680.5,
  "ville_modele": "Lille",
  "model": "DecisionTreeRegressor"
}

```

### `POST /predict/bordeaux`

🚧 Endpoint prévu pour un futur modèle entraîné sur Bordeaux.

Répond actuellement avec :

```json
{
  "detail": "Modèle Bordeaux pas encore implémenté"
}

```

* * *

## 🧪 Lancer les tests

```bash
pytest

```

Les tests couvrent :

- La logique métier (`services`)
- Les routes FastAPI (`routes`)
    
* * *

## 📊 Analyse & Visualisation

Les notebooks `phase_1_lille.ipynb` et `phase_2_bordeaux.ipynb` documentent :

- Le nettoyage des données
- La création de la variable cible `prix_m2`
- La gestion des outliers
- La comparaison des modèles
- L’évaluation de la robustesse des modèles sur Bordeaux
    
* * *

## 📦 Dépendances principales

- `scikit-learn`
- `xgboost`
- `pandas`, `numpy`
- `matplotlib`, `seaborn`
- `FastAPI`, `Uvicorn`
- `pytest`
* * *

## 📄 Licence

Projet sous licence MIT. Voir `LICENSE`.

* * *

## ✍️ Auteur

Projet réalisé dans le cadre de la formation **Développeur IA** chez **Simplon Lille**, autour de l’analyse de données immobilières (DVF 2022).  
📧 Contact : [Santrisse Benjamin](https://github.com/benjsant/).  
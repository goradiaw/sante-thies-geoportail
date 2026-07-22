# Cartographie des établissements de santé — Thiès

Application web démontrant une chaîne complète géomatique + développement :
QGIS (import) → PostgreSQL/PostGIS (stockage) → Flask (API) → Leaflet (carte interactive)

## Installation

1. Assure-toi que la table `sante_thies` existe bien dans ta base
   `sante_thies` (importée depuis QGIS), avec au minimum
   les colonnes : `osm_id`, `name`, `amenity`, `healthcare`, `geom`.

2. Installe les dépendances Python :
```bash
   python -m pip install -r requirements.txt
```

3. Ouvre `app.py` et adapte le bloc `DB_CONFIG` (mot de passe notamment).

4. Lance l'application :
```bash
   python app.py
```

5. Ouvre ton navigateur sur : http://localhost:5000

## Fonctionnalités

- Carte interactive (Leaflet) affichant les 37 établissements de santé de Thiès
- Couleur des points selon le type d'établissement
- Filtre par type d'établissement (menu déroulant)
- Panneau de statistiques (nombre d'établissements par type)
- Clic sur un point → popup avec le détail

## Pour aller plus loin (idées d'amélioration à présenter à un client)

- Ajouter un formulaire pour créer/modifier/supprimer un établissement (CRUD complet)
- Ajouter une recherche par nom
- Ajouter des zones de couverture (buffers) autour de chaque établissement
- Héberger en ligne (Render.com / Railway) pour avoir un lien démo cliquable
- Exporter les résultats filtrés en CSV ou GeoJSON

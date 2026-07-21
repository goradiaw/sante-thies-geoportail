"""
Application web - Cartographie des établissements de santé de Thiès
Flask + PostgreSQL/PostGIS + Leaflet

Avant de lancer :
  1. Adapte les paramètres de connexion dans DB_CONFIG ci-dessous
  2. Installe les dépendances : pip install -r requirements.txt --break-system-packages
  3. Lance : python app.py
  4. Ouvre http://localhost:5000
"""

from flask import Flask, jsonify, render_template, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# --- À ADAPTER selon ta configuration PostgreSQL ---
import os

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "sante_thies",
    "user": "postgres",
    "password": os.environ.get("DB_PASSWORD", "2702"),
}

# Nom de la table importée depuis QGIS
TABLE_NAME = "sante_thies"


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


@app.route("/")
def index():
    """Page principale avec la carte."""
    return render_template("index.html")


@app.route("/api/etablissements")
def api_etablissements():
    """
    Renvoie les établissements de santé au format GeoJSON.
    Filtre optionnel par type via ?type=pharmacy (query param 'amenity').
    """
    type_filtre = request.args.get("type")

    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = f"""
        SELECT
            osm_id,
            name,
            amenity,
            healthcare,
            ST_AsGeoJSON(ST_Transform(geom, 4326)) AS geometry
        FROM {TABLE_NAME}
    """
    params = []
    if type_filtre:
        query += " WHERE amenity = %s"
        params.append(type_filtre)

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    features = []
    for row in rows:
        import json
        features.append({
            "type": "Feature",
            "geometry": json.loads(row["geometry"]),
            "properties": {
                "osm_id": row["osm_id"],
                "name": row["name"] or "Non renseigné",
                "amenity": row["amenity"] or "Non renseigné",
                "healthcare": row["healthcare"] or "",
            },
        })

    return jsonify({"type": "FeatureCollection", "features": features})


@app.route("/api/stats")
def api_stats():
    """Renvoie le nombre d'établissements par type (pour le tableau de bord)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT COALESCE(NULLIF(amenity, ''), 'Non renseigné') AS type_etab, COUNT(*)
        FROM {TABLE_NAME}
        GROUP BY type_etab
        ORDER BY COUNT(*) DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"type": r[0], "count": r[1]} for r in rows])


if __name__ == "__main__":
    app.run(debug=True)
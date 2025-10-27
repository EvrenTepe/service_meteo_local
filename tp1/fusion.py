import json
import os
import main_json
import main_xml  

# Définition du chemin du dossier et le fichier de conseils
dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = "conseils.json"
json_file = dir_path + "/" + file_name


# Lecture du fichier conseils.json
def charger_conseils():
    # J'ajoute encoding="utf-8" pour bien lire les caractères spéciaux (é, à, ...)
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


# On trouve le message correspondant à une condition météo
def conseil_pour_conditions(conditions, conseils):
    cond = (conditions or "").strip().lower()
    for item in conseils.get("conseils", []):
        if item.get("conditions", "").strip().lower() == cond:
            return item.get("message", "")
    return "Adaptez vos vêtements aux conditions météo."


# Scénario 1 : résumé par ville
def scenario_1_resume_ville(ville):
    meteo = main_json.charger_meteo_json()
    villes = main_xml.charger_villes_xml()
    conseils = charger_conseils()

    w = main_json.chercher_ville(meteo, ville)
    v = main_xml.trouver_ville(villes, ville)

    if not w:
        print("[S1] Données météo introuvables pour :", ville)
        return
    if not v:
        print("[S1] Ville introuvable dans le XML :", ville)
        return

    result = {
        "ville": v["nom"],
        "pays": v["codePays"],
        "coordonnees": {"lat": v["lat"], "lon": v["lon"]},
        "matin": w["matin"],
        "soir": w["soir"],
        "conditions": w["conditions"],
        "humidite": w["humidite"],
        "conseil": conseil_pour_conditions(w["conditions"], conseils)
    }

    return result


# Scénario 2 : ville la plus proche selon les coordonnées
def scenario_2_par_coordonnees(lat, lon):
    meteo = main_json.charger_meteo_json()
    villes = main_xml.charger_villes_xml()
    conseils = charger_conseils()

    proche, dist_km = main_xml.ville_plus_proche(villes, lat, lon)
    w = main_json.chercher_ville(meteo, proche["nom"])

    result = {
        "ville_plus_proche": {
            "nom": proche["nom"],
            "pays": proche["codePays"],
            "distance_km": round(dist_km, 2)
        },
        "conditions": w["conditions"],
        "matin": w["matin"],
        "soir": w["soir"],
        "conseil": conseil_pour_conditions(w["conditions"], conseils)
    }

    return result


# Scénario 3 : aperçu par pays
def scenario_3_apercu_pays(code_pays, limite=5):
    meteo = main_json.charger_meteo_json()
    villes = main_xml.charger_villes_xml()

    w_rows = main_json.filtrer_par_pays(meteo, code_pays)
    v_rows = main_xml.filtrer_par_pays(villes, code_pays)
    noms = set(v["nom"] for v in v_rows)

    fusionnees = [w for w in w_rows if w.get("ville") in noms]
    if not fusionnees:
        print("[S3] Aucune ville trouvée pour le pays :", code_pays)
        return

    t_matin = [r["matin"]["temp"] for r in fusionnees]
    result = {
        "pays": code_pays.upper(),
        "nb_villes": len(fusionnees),
        "temp_matin_min": min(t_matin),
        "temp_matin_max": max(t_matin),
        "temp_matin_moy": round(sum(t_matin) / len(t_matin), 2),
        "echantillon": [
            {"ville": r["ville"], "temp_matin": r["matin"]["temp"], "conditions": r["conditions"]}
            for r in fusionnees[:max(1, limite)]
        ]
    }

    return result


# Scénario 4 : la ville la plus chaude
def scenario_4_top_plus_chaudes(limite=3):
    meteo = main_json.charger_meteo_json()
    top = main_json.top_plus_chaudes(meteo, limite)
    result = []

    for r in top:
        result.append({
            "ville": r["ville"],
            "pays": r["codePays"],
            "temp_matin": r["matin"]["temp"],
            "conditions": r["conditions"]
        })

    return result


# Scénario 5 : cohérence température / ressentie + conseil
def scenario_5_coherence_et_conseil(ville):
    meteo = main_json.charger_meteo_json()
    conseils = charger_conseils()

    w = main_json.chercher_ville(meteo, ville)
    if not w:
        print("[S5] Météo introuvable pour :", ville)
        return

    def ecart(x):
        return abs(x["temp"] - x["ressentie"])

    result = {
        "ville": w["ville"],
        "conditions": w["conditions"],
        "coherence": {
            "ecart_matin": round(ecart(w["matin"]), 2),
            "ecart_soir": round(ecart(w["soir"]), 2),
            "note": "Si l'écart ≤ 2°C, la température ressentie est proche de la température réelle."
        },
        "conseil": conseil_pour_conditions(w["conditions"], conseils)
    }

    return result


# pour enregistrer le résultat dans un fichier JSON
def write_json(data, filename="resultat.json"):
    json_object = json.dumps(data, indent=4, ensure_ascii=False)

    with open(dir_path + "/" + filename, "w", encoding="utf-8") as outfile:
        outfile.write(json_object)

    print("Fichier écrit :", filename)


# Fonction principale de test
def main():
    r1 = scenario_1_resume_ville("Genève")
    r4 = scenario_4_top_plus_chaudes(3)
    r5 = scenario_5_coherence_et_conseil("Istanbul")

    if r1 is not None:
        write_json(r1, "resume_geneve.json")
    if r4 is not None:
        write_json(r4, "top_villes_chaudes.json")
    if r5 is not None:
        write_json(r5, "coherence_istanbul.json")



if __name__ == '__main__':
    main()



    
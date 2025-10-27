import json
import os

# on prépare le chemin du fichier data.json
dir_path = os.path.dirname(os.path.realpath(__file__))
json_file = dir_path + "/data.json"


# Lecture du fichier JSON météo
def charger_meteo_json():
    # J'ai ajouté encoding="utf-8" pour bien lire les caractères spéciaux (é, à, ...)
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# recherche   une ville dans les données météo
def chercher_ville(data, ville):
    cible = ville.lower()

    for rec in data.get("meteo", []):
        nom_ville = rec.get("ville", "").lower()
        if nom_ville == cible:
            return rec

    # si non trouvé
    return None


# On filtre les enregistrements météo selon un code pays donné
def filtrer_par_pays(data, code_pays):
    code_pays = code_pays.upper()
    result = []

    # Parcourir tous les enregistrements du fichier JSON
    for rec in data.get("meteo", []):
        pays = rec.get("codePays", "").upper()
        if pays == code_pays:
            result.append(rec)

    # on supprime les doublons : garder un seul enregistrement par ville
    uniques = {}
    for r in result:
        ville = r.get("ville")
        temp_matin = r.get("matin", {}).get("temp", None)

        # Si la ville n'existe pas encore, ou si la température est plus élevée
        # → on garde la meilleure
        if ville not in uniques or temp_matin > uniques[ville]["matin"]["temp"]:
            uniques[ville] = r

    # Retourner la liste finale, sans doublons
    return list(uniques.values())



# on trouve les villes les plus chaudes le matin
def top_plus_chaudes(data, limite=3):
    meteo_list = data.get("meteo", [])

    # dictionnaire pour garder la température la plus élevée par ville
    meilleures = {}

    for rec in meteo_list:
        ville = rec.get("ville")
        temp_matin = rec.get("matin", {}).get("temp", None)

        # si on n’a pas encore la ville ou si la nouvelle température est plus haute
        if ville not in meilleures or temp_matin > meilleures[ville]["matin"]["temp"]:
            meilleures[ville] = rec

    # on convertit  en liste et trier par température décroissante
    uniques = list(meilleures.values())
    uniques_triees = sorted(
        uniques,
        key=lambda rec: rec["matin"]["temp"],
        reverse=True
    )

    # limiter le nombre de résultats
    if limite < 1:
        limite = 1
    return uniques_triees[:limite]


def main():
    all_data = charger_meteo_json()

    # test: afficher la ville "Genève"
    geneve = chercher_ville(all_data, "Genève")
    print("Test Genève:", geneve)

    # test: afficher les villes du pays "CH"
    ch_villes = filtrer_par_pays(all_data, "CH")
    print("Villes CH:", ch_villes)

    # test: top 3 des villes les plus chaudes le matin
    top3 = top_plus_chaudes(all_data, 3)
    print("Top 3 chaud matin:", top3)


if __name__ == "__main__":
    main()




import os
import xml.etree.ElementTree as ET
import math


# on prépare le chemin du fichier  XML
dir_path = os.path.dirname(os.path.realpath(__file__))
xml_file = dir_path + "/data.xml"


# Lecture du fichier XML
def charger_villes_xml():
    # parse du XML
    tree = ET.parse(xml_file)
    racine = tree.getroot()

    villes = []

    # chaque <ville> dans le XML est convertie en un dict Python
    for v in racine.findall("ville"):
        nom = v.findtext("nom", default="")
        codePays = v.findtext("codePays", default="")
        lat = float(v.findtext("lat", default="0"))
        lon = float(v.findtext("lon", default="0"))

        villes.append({
            "nom": nom,
            "codePays": codePays,
            "lat": lat,
            "lon": lon
        })

    return villes


# on recherche une ville par son nom
def trouver_ville(villes, nom):
    cible = nom.lower()

    for v in villes:
        if v["nom"].lower() == cible:
            return v

    # pas trouvée
    return None


# on filtre les villes par code pays (ex: "CH", "FR", "TR", etc.)
def filtrer_par_pays(villes, code_pays):
    code_pays = code_pays.upper()

    result = []
    for v in villes:
        if v["codePays"].upper() == code_pays:
            result.append(v)

    return result


# la calculation de la distance (en km) entre deux points lat/lon
def distance_haversine(lat1, lon1, lat2, lon2):
    # formule de Haversine
    R = 6371.0  # rayon moyen de la Terre en km

    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


# on trouve la ville la plus proche d'une position (lat, lon)
def ville_plus_proche(villes, lat, lon):
    meilleure_ville = None
    meilleure_distance = float("inf")

    for v in villes:
        d = distance_haversine(lat, lon, v["lat"], v["lon"])
        if d < meilleure_distance:
            meilleure_distance = d
            meilleure_ville = v

    return meilleure_ville, meilleure_distance


def main():
    villes = charger_villes_xml()

    print("Toutes les villes chargées:", villes)

    gva = trouver_ville(villes, "Genève")
    print("Recherche Genève:", gva)

    ch_list = filtrer_par_pays(villes, "CH")
    print("Villes en CH:", ch_list)

    proche, dist = ville_plus_proche(villes, 46.2, 6.1)  # autour de Genève
    print("Ville la plus proche ~46.2,6.1:", proche, "distance(km):", round(dist, 2))


if __name__ == "__main__":
    main()




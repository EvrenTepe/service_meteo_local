import argparse
import fusion


def main():
    parser = argparse.ArgumentParser(
        description="Service météo. Donne accès aux différents scénarios."
    )

    parser.add_argument(
        "--scenario",
        type=int,
        required=True,
        choices=[1, 2, 3, 4, 5],
        help="Numéro du scénario (1..5)"
    )

    #arguments possibles selon le scénario
    parser.add_argument("--city", type=str, help="Nom de la ville (pour scénario 1 et 5)")
    parser.add_argument("--country", type=str, help="Code pays (pour scénario 3, ex: CH)")
    parser.add_argument("--lat", type=float, help="Latitude (pour scénario 2)")
    parser.add_argument("--lon", type=float, help="Longitude (pour scénario 2)")
    parser.add_argument("--limit", type=int, default=3, help="Limite de résultats (scénario 3 / 4)")

    args = parser.parse_args()

    # SCÉNARIO 1 : résumé par ville
    if args.scenario == 1:
        if not args.city:
            print("Erreur: le scénario 1 nécessite --city (ex: --city Genève)")
            return
        result = fusion.scenario_1_resume_ville(args.city)
        if result is not None:
            print("Ville :", result["ville"])
            print("Pays :", result["pays"])
            print("Conditions :", result["conditions"])
            print("Coordonnées :", "Lat =", result["coordonnees"]["lat"],", Lon =", result["coordonnees"]["lon"])
            print("Temp matin :", result["matin"]["temp"], "°C")
            print("Temp soir :", result["soir"]["temp"], "°C")
            print("Humidité :", result["humidite"], "%")
            print("Conseil :", result["conseil"])
        return

    # SCÉNARIO 2 : on recherche la ville la plus proche d'une position
    if args.scenario == 2:
        if args.lat is None or args.lon is None:
            print("Erreur: le scénario 2 nécessite --lat et --lon")
            return
        result = fusion.scenario_2_par_coordonnees(args.lat, args.lon)
        if result is not None:
            print("Ville la plus proche :", result["ville_plus_proche"]["nom"])
            print("Pays :", result["ville_plus_proche"]["pays"])
            print("Distance :", result["ville_plus_proche"]["distance_km"], "km")
            print("Conditions :", result["conditions"])
            print("Temp matin :", result["matin"]["temp"], "°C")
            print("Temp soir :", result["soir"]["temp"], "°C")
            print("Conseil :", result["conseil"])
        return

    # SCÉNARIO 3 : aperçu pays (statistiques)
    if args.scenario == 3:
        if not args.country:
            print("Erreur: le scénario 3 nécessite --country (ex: --country CH)")
            return
        result = fusion.scenario_3_apercu_pays(args.country, args.limit)
        if result is not None:
            print("Pays :", result["pays"])
            print("Nombre de villes :", result["nb_villes"])
            print("Température moyenne (matin) :", result["temp_matin_moy"], "°C")
            print("Température min / max :", result["temp_matin_min"], "/", result["temp_matin_max"], "°C")
            print("Échantillon :")
            for item in result["echantillon"]:
                print(" -", item["ville"], ":", item["temp_matin"], "°C", "(", item["conditions"], ")")
        return

    # SCÉNARIO 4 : la ville la plus chaude le matin 
    if args.scenario == 4:
        result = fusion.scenario_4_top_plus_chaudes(args.limit)
        if result is not None:
            print("Top", args.limit, "villes les plus chaudes le matin :")
            for v in result:
                print(" -", v["ville"], "(", v["pays"], "):", v["temp_matin"], "°C (", v["conditions"], ")")
        return

    # SCÉNARIO 5 : cohérence température / ressentie
    if args.scenario == 5:
        if not args.city:
            print("Erreur: le scénario 5 nécessite --city (ex: --city Genève)")
            return
        result = fusion.scenario_5_coherence_et_conseil(args.city)
        if result is not None:
            print("Ville :", result["ville"])
            print("Conditions :", result["conditions"])
            print("Écart matin :", result["coherence"]["ecart_matin"], "°C")
            print("Écart soir :", result["coherence"]["ecart_soir"], "°C")
            print("Note :", result["coherence"]["note"])
            print("Conseil :", result["conseil"])
        return


if __name__ == "__main__":
    main()





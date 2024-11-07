import json 
def int_coord_day(file_paths):
    data = []
    
    for chemin in file_paths:
        with open(chemin, 'r') as f:
            content = json.load(f)
            # Chaque fichier contient une liste de points avec { "coordinates": ... , "dateObserved": ..., "intensity": ... }
            for entry in content:
                loc = entry.get("coordinates")
                date = entry.get("dateObserved")
                intensity = entry.get("intensity")
                if loc is not None and date is not None and intensity is not None:
                    data.append((date, loc, intensity))
    
    return data


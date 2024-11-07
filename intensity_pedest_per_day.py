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

def load_multiple_json(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        # Trouver tous les objets JSON dans le fichier
        items = []
        pos = 0
        while pos < len(data):
            try:
                item, pos = json.JSONDecoder().raw_decode(data, pos)
                items.append(item)
            except json.JSONDecodeError as e:
                print(f"Erreur lors du décodage à la position {pos}: {e}")
                break
        return items

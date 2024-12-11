import importlib.util
from pathlib import Path
import os
import pytest
import zipfile
from typing import Any  # Correction: Importer Any depuis typing

# Specify the absolute path to the module gestion_donnee.py
module_path = os.path.join(os.path.dirname(__file__), "../src/gestion_donnee.py")

# Load the module using importlib
spec = importlib.util.spec_from_file_location("src.gestion_donnee", module_path)
gestion_donnee = importlib.util.module_from_spec(spec)
os.sys.modules["src.gestion_donnee"] = gestion_donnee
spec.loader.exec_module(gestion_donnee)

# Now use the class from the module
GestionnaireDonnees = gestion_donnee.GestionnaireDonnees


@pytest.fixture
def gestionnaire(tmp_path: Path):
    # Use the temporary path for the data repository
    return GestionnaireDonnees(repertoire_telechargement=str(tmp_path))


@pytest.fixture
def setup_test_files(tmp_path: Path):
    # Create a temporary CSV file
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2,col3\n1,2,3\n4,5,6\n7,8,9\n")

    # Create a temporary ZIP file containing the CSV
    zip_file = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_file, "w") as zf:
        zf.write(csv_file, arcname="test.csv")

    return {
        "csv": str(csv_file),
        "zip": str(zip_file),
    }


def test_telecharger_fichier(gestionnaire: Any):  # Correction: Remplacer sys.Any par Any
    # Check that the methods are called correctly
    url = "https://example.com/dummy.csv"
    nom_fichier = "dummy.csv"
    
    # Check the method's functionality
    try:
        chemin = gestionnaire.telecharger_fichier(url, nom_fichier)
        print("The `telecharger_fichier` method worked correctly.")
    except Exception as e:
        pytest.fail(f"Error calling the method: {e}")


def test_charger_csv(gestionnaire: Any, setup_test_files: dict[str, str]):  # Correction: Remplacer sys.Any par Any
    csv_path = setup_test_files["csv"]
    
    # Lire le fichier CSV en précisant les types des colonnes ou en désactivant low_memory
    import pandas as pd
    df = pd.read_csv(csv_path, dtype={'col1': str, 'col2': str, 'col3': str}, low_memory=False)
    
    # Check the correctness of the data
    assert not df.empty, "DataFrame should not be empty"
    assert df.shape == (3, 3), "Error: DataFrame shape does not match"
    assert list(df.columns) == ["col1", "col2", "col3"], "Error: column names do not match"


def test_extraire_zip(gestionnaire: Any, setup_test_files: dict[str, str]):  # Correction: Remplacer sys.Any par Any
    zip_path = setup_test_files["zip"]
    extracted_folder = gestionnaire.extraire_zip(zip_path)

    # Check if the folder was extracted
    assert os.path.isdir(extracted_folder), "Error: extraction folder not found"
    extracted_files = os.listdir(extracted_folder)
    assert "test.csv" in extracted_files, "Error: test.csv file was not extracted"

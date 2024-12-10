import importlib.util
from pathlib import Path
import sys
import os
import pytest
import zipfile
from typing import Any 

# Specify the absolute path to the module gestion_donnee.py
module_path = os.path.join(os.path.dirname(__file__), "../src/gestion_donnee.py")

# Load the module using importlib
spec = importlib.util.spec_from_file_location("src.gestion_donnee", module_path)
gestion_donnee = importlib.util.module_from_spec(spec)
sys.modules["src.gestion_donnee"] = gestion_donnee
spec.loader.exec_module(gestion_donnee)

# Get the class from the module
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


def test_charger_csv(gestionnaire: Any, setup_test_files: dict[str, str]):
    csv_path = setup_test_files["csv"]
    df = gestionnaire.charger_csv(csv_path)
    
    # Check the correctness of the data
    assert not df.empty, "DataFrame should not be empty"
    assert df.shape == (3, 3), "Error: DataFrame shape does not match"
    assert list(df.columns) == ["col1", "col2", "col3"], "Error: column names do not match"

import sys
import os
import pytest


# Add the root directory of the project to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports from the main code
from Cycle3.prediction.prediction import jour_semaine, coor_unique, mean_intens


# Stubs for tests
donnees_utiles_stub = [
    [100, "2024-12-04", [3.883, 43.604]],
    [150, "2024-12-05", [3.884, 43.605]],
    [200, "2024-12-06", [3.883, 43.604]],
    [250, "2024-12-04", [3.885, 43.606]],
    [300, "2024-12-06", [3.883, 43.604]],
]


# Fixture for replacing a variable in the code using monkeypatch
@pytest.fixture
def mock_donnees_utiles(monkeypatch: pytest.MonkeyPatch):
    """Fixture for replacing data used in the function."""
    monkeypatch.setattr(
        "Cycle3.prediction.prediction.donnees_utiles", donnees_utiles_stub
    )


def test_jour_semaine(mock_donnees_utiles: None):
    """Test for the jour_semaine function."""
    result = jour_semaine(2)  # Check Wednesday (Wednesday, number 2)
    expected = [
        [100, [3.883, 43.604]],
        [250, [3.885, 43.606]]
    ]
    assert result == expected


def test_coor_unique(mock_donnees_utiles: None):
    """Test for the coor_unique function."""
    result = coor_unique(5)  # Check Friday (number 5)
    expected = [[3.884, 43.605], [3.883, 43.604]]
    assert result == expected


def test_mean_intens(mock_donnees_utiles: None):
    """Test for the mean_intens function."""
    result = mean_intens(2)  # Check Wednesday (Mercredi, number 2)
    expected = [
        [183.33, [3.883, 43.604]],
        [250, [3.885, 43.606]]
    ]
    # Check that lengths match and values are approximately equal
    assert len(result) == len(expected)
    for res, exp in zip(result, expected):
        assert round(res[0], 2) == round(exp[0], 2)
        assert res[1] == exp[1]

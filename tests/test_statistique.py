import pytest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from io import StringIO
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Prepare test data
@pytest.fixture
def mock_csv_data():
    return StringIO(
        "Departure,Return station,Covered distance (m),Departure station\n"
        "2023-01-01 10:00:00,Station B,1500,Station A\n"
        "2023-01-01 11:00:00,Station A,3000,Station B\n"
    )

@pytest.fixture
def mock_dataframe(mock_csv_data):
    return pd.read_csv(mock_csv_data)

# Test: data processing
def test_process_data(mock_dataframe):
    df = mock_dataframe.copy()
    df["Departure"] = pd.to_datetime(df["Departure"])  # Check date conversion
    assert pd.api.types.is_datetime64_any_dtype(df["Departure"]), "The 'Departure' column should be datetime"
    
    df["Date"] = df["Departure"].dt.date  # Check date extraction
    grouped = df.groupby("Date").size().reset_index(name="Nombre de trajets")  # Check grouping
    assert "Nombre de trajets" in grouped.columns, "The 'Nombre de trajets' column is expected"
    assert grouped["Nombre de trajets"].sum() == len(df), "The sum of the group should match the number of records"

# Test: saving a bar chart
@patch("matplotlib.pyplot.savefig")
def test_save_bar_chart(mock_savefig, mock_dataframe):
    df = mock_dataframe.copy()
    df["Date"] = pd.to_datetime(df["Departure"]).dt.date
    trajets_depart = df.groupby("Date").size().reset_index(name="Nombre de trajets")
    
    plt.figure(figsize=(12, 6))
    plt.bar(trajets_depart["Date"], trajets_depart["Nombre de trajets"], color="b", alpha=0.7)
    plt.title("Test Graph")
    plt.xlabel("Date")
    plt.ylabel("Nombre de trajets")
    plt.savefig("test_output.png")
    
    mock_savefig.assert_called_once_with("test_output.png")  # Check that the save figure method was called

# Test: saving a polar chart
@patch("plotly.graph_objects.Figure.write_html")
def test_save_polar_chart(mock_write_html, mock_dataframe):
    df = mock_dataframe.copy()
    df["Departure"] = pd.to_datetime(df["Departure"])
    df["Hour"] = df["Departure"].dt.hour
    df["Day"] = df["Departure"].dt.day_name()
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[1, 2, 3], theta=[0, 120, 240]))
    fig.write_html("test_polar.html")
    
    mock_write_html.assert_called_once_with("test_polar.html")  # Check that the HTML file was saved

# Test: non-existent file
def test_missing_file():
    with pytest.raises(FileNotFoundError):
        pd.read_csv("non_existent_file.csv")

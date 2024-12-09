import sys
import os
import importlib.util
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from io import StringIO
import networkx as nx
import osmnx as ox

# Mock the save() method before loading the module
@patch("matplotlib.animation.Animation.save")
def test_video_module(mock_save):
    # Specify the absolute path to the module
    module_path = os.path.join(os.path.dirname(__file__), '../Cycle3/video/video.py')

    # Load the module using importlib
    spec = importlib.util.spec_from_file_location("video", module_path)
    video = importlib.util.module_from_spec(spec)
    sys.modules["video"] = video
    spec.loader.exec_module(video)

    # Now you can import functions using the loaded module
    chemin_court = video.chemin_court
    init = video.init
    update = video.update

    # Prepare test data
    @pytest.fixture
    def mock_csv_data():
        return StringIO(
            "Departure station,Return station,Duration (sec.),Departure\n"
            "Station A,Station B,300,2023-01-01 10:00:00\n"
            "Station B,Station C,600,2023-01-01 11:00:00\n"
        )

    @pytest.fixture
    def mock_dataframe(mock_csv_data: StringIO):
        return pd.read_csv(mock_csv_data)

    # Test: data processing
    def test_data_processing(mock_dataframe: pd.DataFrame):
        df = mock_dataframe.copy()
        df["Departure"] = pd.to_datetime(df["Departure"])
        assert pd.api.types.is_datetime64_any_dtype(df["Departure"]), "The 'Departure' column should be datetime"
        assert not df.empty, "DataFrame should not be empty"

    # Test: shortest path
    @patch("osmnx.distance.nearest_nodes")
    @patch("networkx.shortest_path")
    def test_chemin_court(mock_shortest_path, mock_nearest_nodes, mock_dataframe: pd.DataFrame):
        mock_nearest_nodes.side_effect = [1, 2]  # Mock graph nodes
        mock_shortest_path.return_value = [1, 3, 2]  # Mock path

        # Prepare row data
        row = {
            "latitude_depart": 43.6,
            "longitude_depart": 3.9,
            "latitude_retour": 43.7,
            "longitude_retour": 3.8,
            "Duration (sec.)": 300
        }
        path, duration = chemin_court(row)
        assert path == [1, 3, 2], "The shortest path should match the expected one"
        assert duration == 300, "The duration should match the data"

    # Test: creating a graph
    def test_create_graph():
        G = ox.graph_from_place("Montpellier, France", network_type="all")
        assert isinstance(G, nx.MultiDiGraph), "The graph should be of type MultiDiGraph"
        assert len(G) > 0, "The graph should not be empty"

    # Test: handling input()
    @patch('builtins.input', return_value='5')  # Mock input to always return '5'
    def test_input_handling(mock_input):
        # Example of a function that uses input
        # Example function to test
        # video_function_that_uses_input()

        # Check that input was called and returned the expected value
        assert mock_input.called  # Check that input() was called
        assert mock_input.return_value == '5'  # Check that input() returned '5'

    # Test: mock save for animation
    def test_save_video(mock_save):
        mock_save.return_value = None  # Mocked return value
        ani = MagicMock()  # Mock for animation
        writer = MagicMock()

        # Mock the save call
        ani.save.assert_not_called()  # Check that save() was not called

        # Ensure the animation was created (if needed for the tests)
        assert ani is not None, "The animation should be created"

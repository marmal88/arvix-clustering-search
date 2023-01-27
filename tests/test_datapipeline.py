import pytest
import pandas as pd


from src.app_func.datapipeline import DataPipeline


@pytest.fixture
def fixture_datapipeline(mocker):
    return DataPipeline()


def test_query_arxiv(mocker):
    def mock_load(self):
        return pd.DataFrame()

    mocker.patch("src.app_func.datapipeline.DataPipeline.query_arxiv", mock_load)
    actual = DataPipeline().query_arxiv()

    pd.testing.assert_frame_equal(actual, pd.DataFrame())

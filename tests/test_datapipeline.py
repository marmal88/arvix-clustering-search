import pytest
import pandas as pd


from src.app_func.datapipeline import DataPipeline


def test_query_arxiv_positive(mocker):
    def mock_load(self):
        return True, pd.DataFrame()

    mocker.patch("src.app_func.datapipeline.DataPipeline.query_arxiv", mock_load)
    res, df = DataPipeline().query_arxiv()

    assert isinstance(res, bool)
    pd.testing.assert_frame_equal(df, pd.DataFrame())


def test_query_arxiv_negative(mocker):
    def mock_load(self):
        return False, None

    mocker.patch("src.app_func.datapipeline.DataPipeline.query_arxiv", mock_load)
    res, df = DataPipeline().query_arxiv()

    assert isinstance(res, bool)
    assert df is None

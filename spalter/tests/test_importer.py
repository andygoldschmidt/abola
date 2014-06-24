import pytest
import pandas as pd
from spalter.importer import _import_csv, _parse_dataframe


@pytest.fixture
def df():
    return pd.DataFrame({'split_col': ['test', 'test', 'control', 'control'],
                         'kpi1': [5, 8, 2, 7],
                         'kpi2': [1, 2, 3, 4]})


def test_file_doesnt_exist():
    with pytest.raises(IOError):
        _import_csv('/no/file/here', 'split_col')


def test_parse_dataframe(df):
    result = _parse_dataframe(df, 'split_col')
    assert result['kpi1']['test'] == [5, 8]


def test_parse_dataframe_invalid_split_column(df):
    with pytest.raises(KeyError):
        _parse_dataframe(df, 'nonsense_col')

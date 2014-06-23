from collections import OrderedDict
import pytest
from statsmodels.stats.weightstats import ttest_ind, CompareMeans, DescrStatsW
from abola.metrics import mean, _split, pvalue, confidence_interval, power


@pytest.fixture
def testdata():
    data = OrderedDict()
    data['kpi1'] = OrderedDict()
    data['kpi2'] = OrderedDict()
    data['kpi1']['A'] = [1, 2, 3]
    data['kpi1']['B'] = [4, 5, 6]
    data['kpi1']['C'] = [0, 0, 0]
    data['kpi2']['A'] = [2, 4, 6]
    data['kpi2']['B'] = [3, 5, 7]
    data['kpi2']['C'] = [7, 8, 9]
    return data


def test_split_without_control_label(testdata):
    """
     Test the splitting into control/test group(s) with no predefined control_label.
     First column **A** will be used as control group.
    """
    control, others = _split(testdata)
    assert control['kpi1'] == [1, 2, 3]
    assert others['C']['kpi2'] == [7, 8, 9]


def test_split_with_control_label(testdata):
    control, others = _split(testdata, control_label='B')
    assert 'B' not in others.keys()


def test_mean(testdata):
    result = mean(testdata)
    assert result['kpi1']['A'] == 2.0
    assert result['kpi2']['B'] == 5.0


def test_pvalue(testdata):
    result = pvalue(testdata, control_label='A')
    expected = ttest_ind(testdata['kpi1']['A'], testdata['kpi1']['B'])[1]
    assert result['B']['kpi1'] == expected


def test_confint(testdata):
    result = confidence_interval(testdata, control_label='A')
    c_means = CompareMeans(DescrStatsW(testdata['kpi1']['A']),
                           DescrStatsW(testdata['kpi1']['B']))
    expected = c_means.tconfint_diff()
    assert result['B']['kpi1'] == expected


def test_power(testdata):
    result = power(testdata, control_label='A')
    assert 0 <= result['B']['kpi1'] <= 1

from collections import OrderedDict

import pytest
from statsmodels.stats.weightstats import ttest_ind, CompareMeans, DescrStatsW, ztest

from spalter.metrics import mean, _split, pvalue, confidence_interval, power, effect_size_cohen


@pytest.fixture
def testdata():
    data = OrderedDict()
    data['kpi1'] = OrderedDict()
    data['kpi2'] = OrderedDict()
    # kpi1 = non-proportional
    data['kpi1']['A'] = [1, 2, 3, 4, 5]
    data['kpi1']['B'] = [5, 6, 7, 8, 9]
    data['kpi1']['C'] = [1, 3, 5, 7, 9]
    # kpi2 = proportional
    data['kpi2']['A'] = [0, 0, 0, 1, 1]
    data['kpi2']['B'] = [1, 1, 1, 0, 0]
    data['kpi2']['C'] = [0, 0, 1, 0, 0]
    return data


def test_split_without_control_label(testdata):
    """
     Test the splitting into control/test group(s) with no predefined control_label.
     First column **A** will be used as control group.
    """
    control, others = _split(testdata)
    assert control['kpi1'] == [1, 2, 3, 4, 5]
    assert others['C']['kpi2'] == [0, 0, 1, 0, 0]


def test_split_with_control_label(testdata):
    control, others = _split(testdata, control_label='B')
    assert 'B' not in others.keys()


def test_mean(testdata):
    result = mean(testdata)
    assert result['kpi1']['A'] == 3.0
    assert result['kpi2']['B'] == 0.6


def test_pvalue(testdata):
    result = pvalue(testdata, control_label='A')
    expected_nonprop = ttest_ind(testdata['kpi1']['A'], testdata['kpi1']['B'])[1]
    expected_prop = ztest(testdata['kpi2']['A'], testdata['kpi2']['B'])[1]
    assert result['B']['kpi1'] == expected_nonprop
    assert result['B']['kpi2'] == expected_prop


def test_confint(testdata):
    result = confidence_interval(testdata, control_label='A')
    c_means1 = CompareMeans(DescrStatsW(testdata['kpi1']['B']),
                            DescrStatsW(testdata['kpi1']['A']))
    c_means2 = CompareMeans(DescrStatsW(testdata['kpi2']['B']),
                            DescrStatsW(testdata['kpi2']['A']))
    expected1 = c_means1.tconfint_diff()
    expected2 = c_means2.zconfint_diff()
    assert result['B']['kpi1'] == expected1
    assert result['B']['kpi2'] == expected2


def test_power(testdata):
    result = power(testdata, control_label='A')
    assert round(result['B']['kpi1'], 2) == 0.97
    assert round(result['B']['kpi2'], 2) == 0.10


def test_effect_size_cohen():
    """
    Taken from:
        1) http://researchrundowns.wordpress.com/quantitative-methods/effect-size/
        2) http://en.wikipedia.org/wiki/Effect_size#Cohen.27s_d
    """
    result1 = effect_size_cohen(828.28, 818.92, 336, 336, 14.09, 16.11)
    result2 = effect_size_cohen(1750, 1612, 2436, 3311, 89.93, 69.05)
    assert round(result1, 2) == 0.62
    assert round(result2, 2) == 1.76

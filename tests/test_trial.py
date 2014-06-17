import pytest

from trial import Trial


@pytest.fixture
def trial():
    trial = Trial(variant_labels=['A', 'B'],
                   observation_labels=['kpi1', 'kpi2'])
    trial.update({
        'kpi1': {
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [1, 1, 1]
        },
        'kpi2': {
            'A': [2, 4, 6],
            'B': [3, 5, 7],
            'C': [7, 8, 9]
        }
    })
    return trial


def test_init(trial):
    assert len(trial.observations) == 2
    assert len(trial.observations['kpi1']) == 3


def test_update(trial):
    assert trial.observations['kpi1']['A'] == [1, 2, 3]


def test_evaluate(trial):
    result = trial.evaluate('mean')
    assert result['kpi1'] == {'A': 2, 'B': 5, 'C': 1}


def test_evaluate_multiple_metrics(trial):
    result = trial.evaluate(['mean', 'pvalue'])
    assert len(result.keys()) == 2
    assert result['mean']['kpi1']['A'] == 2


def test_unknown_metric(trial):
    with pytest.raises(Trial.UnsupportedMetricError):
        trial.evaluate('nonsense_metric')
    with pytest.raises(Trial.UnsupportedMetricError):
        trial.evaluate(['mean', 'nonsense_metric'])

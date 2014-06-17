import pytest

from api import Trials


@pytest.fixture
def trial():
    return Trials(variant_labels=['A', 'B', 'C'],
                  observation_labels=['kpi1', 'kpi2'])


@pytest.fixture
def trial_prefilled():
    trial = Trials(variant_labels=['A', 'B'],
                   observation_labels=['kpi1', 'kpi2'])
    trial.update({
        'kpi1': {
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        },
        'kpi2': {
            'A': [2, 4, 6],
            'B': [3, 5, 7]
        }
    })
    return trial


def test_init(trial):
    assert len(trial.observations) == 2
    assert len(trial.observations['kpi1']) == 3


def test_update(trial_prefilled):
    assert trial_prefilled.observations['kpi1']['A'] == [1, 2, 3]


def test_evaluate(trial_prefilled):
    result = trial_prefilled.evaluate('mean')
    assert result['kpi1'] == {'A': 2, 'B': 5}


def test_unknown_metric(trial_prefilled):
    with pytest.raises(Trials.UnsupportedMetricError):
        trial_prefilled.evaluate('nonsense_metric')

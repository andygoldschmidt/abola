from collections import OrderedDict
import numpy as np
from statsmodels.stats.power import TTestIndPower
from statsmodels.stats.weightstats import ttest_ind, DescrStatsW, CompareMeans


def _split(observations, control_label=None):
    if control_label is None:
        first_item = list(observations.values())[0]
        control_label = list(first_item.keys())[0]
        print('Info: No control_label given, setting it to: {}'.format(control_label))

    others = OrderedDict()
    control = OrderedDict()
    for observation_label, variants in observations.items():
        for variant_label, values in variants.items():
            if variant_label == control_label:
                control[observation_label] = values
            else:
                if not variant_label in others.keys():
                    others[variant_label] = OrderedDict()
                others[variant_label][observation_label] = values
    return control, others


def mean(data, *args, **kwargs):
    result = OrderedDict()
    for observation_label, variant_values in data.items():
        result[observation_label] = OrderedDict()
        for label, values in variant_values.items():
             result[observation_label][label] = np.mean(values)
    return result


def pvalue(data, control_label=None, *args, **kwargs):
    def fn(control, test):
        return ttest_ind(control, test)[1]

    return _apply(data, fn, control_label)


def confidence_interval(data, control_label=None, *args, **kwargs):
    def fn(control, test):
        c_means = CompareMeans(DescrStatsW(control), DescrStatsW(test))
        return c_means.tconfint_diff()

    return _apply(data, fn, control_label)


def _apply(data, fn, control_label):
    control, others = _split(data, control_label=control_label)
    result = OrderedDict()
    for variant_label, observations in others.items():
        result[variant_label] = OrderedDict()
        for observation_label, values in observations.items():
            result[variant_label][observation_label] = fn(control[observation_label],
                                                          others[variant_label][observation_label])
    return result


metrics = {
    'mean':    mean,
    'pvalue':  pvalue,
    'confint': confidence_interval
}

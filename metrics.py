from collections import OrderedDict
import numpy as np


def split(variants, observations, control_label=None):
    if control_label is None:
        control_label = list(variants.keys())[0]

    others = OrderedDict()
    control = OrderedDict()
    for observation in observations:
        for label, values in observation.items():
            if label != control_label:
                others[observation] = (label, values)
            else:
                control[observation] = values
    return control, others


def mean(data, *args, **kwargs):
    result = OrderedDict()
    for observation_label, variant_values in data.items():
        result[observation_label] = OrderedDict()
        for label, values in variant_values.items():
             result[observation_label][label] = np.mean(values)
    return result


metrics = {
    'mean': mean
}
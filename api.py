from collections import OrderedDict
from metrics import metrics as default_metrics


class Trials(object):

    class UnsupportedMetricError(Exception):
        pass

    def __init__(self, variant_labels, observation_labels):
        self.observations = OrderedDict()
        self.variants = tuple(variant_labels)
        for observation in observation_labels:
            variants = OrderedDict([(variant, []) for variant in variant_labels])
            self.observations[observation] = variants

    def update(self, feed):
        for observation, variant_dict in feed.items():
            for variant, values in variant_dict.items():
                self.observations[observation][variant] = values

    def evaluate(self, metric, *args, **kwargs):
        result = None
        if isinstance(metric, str):
            if metric not in default_metrics:
                raise Trials.UnsupportedMetricError(metric)
            cls = default_metrics[metric]
            result = cls(self.observations, *args, **kwargs)
        else:
            raise TypeError("'metric' must be of type str.")
        return result
import copy
import logging

from typing import Any, Dict, Optional, Text

logger = logging.getLogger(__name__)

import os
import logging
from pathlib import Path
import tensorflow as tf

DATA_PATH = os.path.join(str(Path.home()), '.kolibri')

Path(DATA_PATH).mkdir(exist_ok=True, parents=True)


class TaskType(object):
    CLASSIFICATION = 'classification'
    LABELING = 'labeling'
    SCORING = 'scoring'
    REGRESSION = 'regression'
    MULTI_TARGET_CLASSIFICATION = 'multi_target_classification'
    MULTI_TARGET_REGRESSION = 'multi_target_regression'


class DnnConfig(object):

    def __init__(self):
        self._use_cudnn_cell = False
        self.disable_auto_summary = False

        if tf.config.list_physical_devices('GPU'):
            logging.warning(
                "CUDA GPU available, you can set `kolibri.dnn.config.use_cudnn_cell = True` to use CuDNNCell. "
                "This will speed up the training, "
                "but will make model incompatible with CPU device.")

    @property
    def use_cudnn_cell(self):
        return self._use_cudnn_cell

    @use_cudnn_cell.setter
    def use_cudnn_cell(self, value):
        self._use_cudnn_cell = value
        from kolibri.dnn.layers import L
        if value:
            if tf.test.is_gpu_available(cuda_only=True):
                L.LSTM = tf.compat.v1.keras.layers.CuDNNLSTM
                L.GRU = tf.compat.v1.keras.layers.CuDNNGRU
                logging.warning("CuDNN enabled, this will speed up the training, "
                                "but will make model incompatible with CPU device.")
            else:
                logging.warning("Unable to use CuDNN cell, no GPU available.")
        else:
            L.LSTM = tf.keras.layers.LSTM
            L.GRU = tf.keras.layers.GRU

    def to_dict(self):
        return {
            'use_cudnn_cell': self.use_cudnn_cell
        }


config = DnnConfig()


def load(**kwargs):
    return _load_from_dict(**kwargs)


def _load_from_dict(**kwargs):
    config = {}
    if kwargs:
        config.update(kwargs)
    return ModelConfig(config)


def override_defaults(
        defaults: Optional[Dict[Text, Any]], custom: Optional[Dict[Text, Any]]
) -> Dict[Text, Any]:
    if defaults:
        cfg = copy.deepcopy(defaults)
    else:
        cfg = {}

    if custom:
        if isinstance(custom, dict):
            cfg.update(custom)
        else:
            cfg.update(custom.__dict__)
    return cfg


def component_config_from_pipeline(
        name,
        pipeline,
        defaults=None):
    for c in pipeline:
        if c.get("name") == name:
            return override_defaults(defaults, c)
    else:
        return override_defaults(defaults, {})


class ModelConfig:
    def __init__(self, configuration_values=None):
        """Create a model configuration, optionally overriding
        defaults with a dictionary ``configuration_values``.
        """
        if not configuration_values:
            configuration_values = {}

        self.language = "en"
        self.pipeline = []
        self.data = None

        self.override(configuration_values)

        if self.__dict__["pipeline"] is None:
            # replaces NoneModelConfig with empty list
            self.__dict__["pipeline"] = []
        elif isinstance(self.__dict__["pipeline"], list):

            self.pipeline = [{"name": c} for c in self.__dict__['pipeline']]

            if self.pipeline:
                # replaces the template with the actual components
                self.__dict__["pipeline"] = self.pipeline

        for key, value in self.items():
            setattr(self, key, value)

    def __getitem__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __getstate__(self):
        return self.as_dict()

    def __setstate__(self, state):
        self.override(state)

    def items(self):
        return list(self.__dict__.items())

    def as_dict(self):
        return dict(list(self.items()))

    def for_component(self, index, defaults=None):
        return component_config_from_pipeline(index, self.pipeline, defaults)

    @property
    def component_names(self):
        if self.pipeline:
            return [c.get("name") for c in self.pipeline]
        else:
            return []

    def override(self, config):
        if config:
            self.__dict__.update(config)

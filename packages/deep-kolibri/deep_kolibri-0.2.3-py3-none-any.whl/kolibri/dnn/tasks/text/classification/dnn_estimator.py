import logging
import os
from pathlib import Path
from typing import Tuple

import numpy as np
from scipy.sparse import vstack
from sklearn.utils import class_weight
from tensorflow.keras.callbacks import ModelCheckpoint

import kolibri
from kolibri import settings
from kolibri.config import TaskType
from kolibri.dnn.embeddings import DefaultEmbedding, WordEmbedding
from kolibri.dnn.tasks.text.classification.models import get_model
from kolibri.indexers.classification_indexer import ClassificationIndexer
from kolibri.kolibri_component import Component

logger = logging.getLogger(__name__)

KOLIBRI_MODEL_FILE_NAME = "classifier_kolibri.pkl"
DNN_MODEL_FILE_NAME = "classifier_dnn"


class DnnEstimator(Component):
    """classifier using the sklearn framework"""

    _estimator_type = 'estimator'

    name = 'dnn_classifier'

    provides = ["classification", "target_ranking"]

    requires = ["text_features"]

    defaults = {

        # the models used in the classifier if several models are given they will be combined
        "models": "bilstm",
        "embeddings": "default",
        "multi-label": False,
        "sequence_length": 'auto',
        "epochs": 10,
        "embedding_path": None,
        "loss": 'categorical_crossentropy',
        "class-weight": False,
        "project-dir": "."
    }

    def __init__(self, component_config=None, model=None):

        """Construct a new class classifier using the sklearn framework."""
        super().__init__(component_config=component_config)

        if model:
            self.clf = get_model(model)
            return
        else:
            self.indexer = ClassificationIndexer(multi_label=self.component_config["multi-label"])
        if self.component_config['embeddings'] == 'default':
            self.embeddings = DefaultEmbedding(task=TaskType.CLASSIFICATION,
                                               sequence_length=self.component_config["sequence_length"],
                                               indexer=self.indexer)
        elif self.component_config['embeddings'] == 'word':
            self.embeddings = WordEmbedding(w2v_path=self.component_config["embedding_path"],
                                            task=TaskType.CLASSIFICATION,
                                            sequence_length=self.component_config["sequence_length"],
                                            indexer=self.indexer)
        elif self.component_config['embeddings'] == 'none':
            self.embeddings = None

        self.clf = get_model(self.component_config['models'], embedding=self.embeddings,
                             hyper_parameters=self.component_config)

#        print(self.clf.tf_model.summary())
    @classmethod
    def required_packages(cls):
        return ["tensorflow"]

    def fit(self, X, y, X_val=None, y_val=None):

        dir_path = os.path.join(self.component_config["project-dir"], DNN_MODEL_FILE_NAME)

        Path(dir_path).mkdir(parents=True, exist_ok=True)
        filepath = os.path.join(dir_path, 'model_weights.h5')

        checkpoint = ModelCheckpoint(filepath,
                                     monitor='val_accuracy',
                                     verbose=1,
                                     save_best_only=True,
                                     mode='max')
        callbacks_list = [checkpoint]

        if self.component_config['class-weight']:
            class_weights = class_weight.compute_class_weight('balanced',
                                                              np.unique(y),
                                                              y)
            self.clf.fit(X, y, x_validate=X_val, y_validate=y_val, epochs=self.component_config["epochs"],
                         callbacks=callbacks_list, fit_kwargs={"class_weight": class_weights})
        else:
            self.clf.fit(X, y, x_validate=X_val, y_validate=y_val, epochs=self.component_config["epochs"],
                         callbacks=callbacks_list)

    def transform(self, document):

        return self.clf.transform(document)

    def predict(self, X):
        # type: (np.ndarray) -> Tuple[np.ndarray, np.ndarray]
        """Given a bow vector of an input text, predict most probable label.

        Return only the most likely label.

        :param X: bow of input text
        :return: tuple of first, the most probable label and second,
                 its probability."""

        return self.clf.predict(X)

    def train(self, training_data, **kwargs):

        y = [document.label for document in training_data]
        self.indexer.build_label_dict(y)
        y = self.indexer.numerize_label_sequences(y)
        X = vstack([document.vector for document in training_data])
        self.fit(X, y)

    def process(self, document, **kwargs):
        """Return the most likely class and its probability for a document."""
        raw_results = None
        if not self.clf:
            # component is either not trained or didn't
            # receive enough training data
            target = None
            target_ranking = []
        else:
            X = np.array(document.tokens)
            raw_results = self.clf.predict_top_k_class([X], top_k=settings.modeling['TARGET_RANKING_LENGTH'])

            if len(raw_results) > 0:

                target = {"name": raw_results[0]['label'], "confidence": raw_results[0]['confidence']}

                target_ranking = raw_results[0]['confidence']
            else:
                target = {"name": None, "confidence": 0.0}
                target_ranking = []

        document.label = target
        document.raw_prediction_results = raw_results
        document.set_output_property("raw_prediction_results")
        document.set_output_property("label")
        document.target_ranking = target_ranking
        document.set_output_property("target_ranking")

    @classmethod
    def load(cls,
             model_dir=None,
             model_metadata=None,
             cached_component=None,
             **kwargs  # type: Any
             ):

        meta = model_metadata.for_component(cls.name)

        model_file = os.path.join(model_dir, DNN_MODEL_FILE_NAME)

        if os.path.exists(model_file):
            ent_tagger = kolibri.dnn.utils.load_model(model_file)
            return cls(meta, ent_tagger)
        else:
            return cls(meta)

    def persist(self, model_dir):
        """Persist this model into the passed directory.

        Returns the metadata necessary to load the model again."""

        if self.clf:
            model_file_name = os.path.join(model_dir, DNN_MODEL_FILE_NAME)

            self.clf.save_info(model_file_name)

        return {"classifier_file": DNN_MODEL_FILE_NAME}

    #
    # @classmethod
    # def load(cls, model_dir=None, model_metadata=None,  cached_component=None,  **kwargs):
    #
    #
    #     meta = model_metadata.for_component(cls.name)
    #     classifier_file_name = meta.get("classifier_file", KOLIBRI_MODEL_FILE_NAME)
    #     dnn_file_name = meta.get("dnn_file", DNN_MODEL_FILE_NAME)
    #     classifier_file = os.path.join(model_dir, classifier_file_name)
    #
    #     if os.path.exists(classifier_file):
    #         # Load saved model
    #         model = joblib.load(classifier_file)
    #         clf = kolibri.dnn.utils.load_model(dnn_file_name)
    #         model.clf=clf
    #         return model
    #     else:
    #         return cls(meta)
    #
    # def persist(self, model_dir):
    #     """Persist this model into the passed directory."""
    #
    #
    #
    #     classifier_file = os.path.join(model_dir, KOLIBRI_MODEL_FILE_NAME)
    #     joblib.dump(self, classifier_file)
    #     dnn_file = os.path.join(model_dir, DNN_MODEL_FILE_NAME)
    #     self.clf.save(dnn_file)
    #
    #     return {"classifier_file": DNN_MODEL_FILE_NAME, "dnn_file":DNN_MODEL_FILE_NAME}

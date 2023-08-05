import numpy as np

from typing import Callable

from .base_score import BaseScore


class ScoreExample(BaseScore):
    """
    Example score that calculates
    average size of topic kernel across all topics.
    We inherit from BaseScore in order to have self.value property and self.update() method
    (the internal logic of TopicNet relies on them)

    """
    def __init__(
            self,
            name: str = None,
            token_threshold: float = 1e-3,
            should_compute: Callable[[int], bool] = None):
        """

        Parameters
        ----------
        name:
            name of the score
        token_threshold : float
            what probabilities to take as token belonging to the topic

        """
        super().__init__(name=name, should_compute=should_compute)

        self.threshold = token_threshold

    def call(self, model, **kwargs):
        """
        Method that calculates the score

        Parameters
        ----------
        model : TopicModel

        Returns
        -------
        score : float
            mean kernel size for all topics in the model

        """
        phi = model.get_phi().values
        score = np.sum((phi > self.threshold).astype('int'), axis=0).mean()

        return score

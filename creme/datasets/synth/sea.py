import random

from .. import base


class SEA(base.SyntheticDataset):
    """SEA synthetic dataset.

    Each observation is composed of 3 features. Only the first two features are relevant. The
    target is binary, and is positive if the sum of the features exceeds a certain threshold. There
    are 4 thresholds to choose from. Concept drift can be introduced by switching the threshold
    anytime during the stream.

    Parameters:
        variant: Determines the classification function to use. Possible choices are 0, 1, 2, 3.
        noise: Determines the amount of observations for which the target sign will be flipped.
        seed: Random seed number used for reproducibility.

    Example:

        >>> from creme import datasets

        >>> dataset = datasets.synth.SEA(variant=0, seed=42)

        >>> for x, y in dataset.take(5):
        ...     print(x, y)
        {0: 6.39426, 1: 0.25010, 2: 2.75029} False
        {0: 2.23210, 1: 7.36471, 2: 6.76699} True
        {0: 8.92179, 1: 0.86938, 2: 4.21921} True
        {0: 0.29797, 1: 2.18637, 2: 5.05355} False
        {0: 0.26535, 1: 1.98837, 2: 6.49884} False

    References:
        1. [A Streaming Ensemble Algorithm (SEA) for Large-Scale Classification](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.482.3991&rep=rep1&type=pdf)

    """

    def __init__(self, variant: int, noise=0., seed: int = None):

        super().__init__(n_features=3, task=base.BINARY_CLF)

        if variant not in (0, 1, 2, 3):
            raise ValueError('Unknown variant, possible choices are: 0, 1, 2, 3')

        self.variant = variant
        self.noise = noise
        self.seed = seed
        self._threshold = {0: 8, 1: 9, 2: 7, 3: 9.5}[variant]
        self._rng = random.Random(seed)

    def __iter__(self):

        while True:

            x = {i: self._rng.uniform(0, 10) for i in range(3)}
            y = x[0] + x[1] > self._threshold

            if self.noise and self._rng.random() < self.noise:
                y = not y

            yield x, y

    @property
    def _repr_title(self):
        return f'{self.__class__.__name__} dataset, variant #{self.variant}'

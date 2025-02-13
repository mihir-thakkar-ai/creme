"""Utilities for inspecting a model's type.

Sometimes we need to check if a model can perform regression, classification, etc. However, for
some models the model's type is only known at runtime. For instance, we can't do
`isinstance(pipeline, base.Regressor)` or `isinstance(wrapper, base.Regressor)`. This submodule
thus provides utilities for determining an arbitrary model's type.

"""
from creme import base
from creme import compose


# TODO: maybe all of this could be done by monkeypatching isintance for pipelines?


__all__ = [
    'extract_relevant',
    'isclassifier',
    'isregressor',
    'ismoclassifier',
    'ismoregressor'
]


def extract_relevant(model: base.Estimator):
    """Extracts the relevant part of a model.

    Parameters:
        model

    """

    if isinstance(model, compose.Pipeline):
        return extract_relevant(list(model.steps.values())[-1])  # look at last step
    return model


def isclassifier(model):
    return isinstance(extract_relevant(model), base.Classifier)


def ismoclassifier(model):
    return isinstance(extract_relevant(model), base.MultiOutputClassifier)


def isregressor(model):
    return isinstance(extract_relevant(model), base.Regressor)


def istransformer(model):
    return isinstance(extract_relevant(model), base.Transformer)


def ismoregressor(model):
    return isinstance(extract_relevant(model), base.MultiOutputRegressor)

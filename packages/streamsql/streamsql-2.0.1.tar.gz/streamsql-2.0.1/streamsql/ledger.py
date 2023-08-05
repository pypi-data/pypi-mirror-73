from enum import Enum, auto
import networkx as nx


class CommandLedger:
    """ CommandLedger keeps track of all commands applied by a Feature Store

    By keeping track of all commands applied to it, a feature store's state can
    be re-created from the initial data sources.
    """
    def __init__(self):
        self._ledger = list()

    def append(self, cmd):
        self._ledger.append(cmd)

    def apply_to(self, feature_store):
        for cmd in self._ledger:
            cmd.apply_to(feature_store)


class ConnectTableCmd:
    def __init__(self, fn="", name="", **kwargs):
        self.name = name
        self.dependences = []
        self.fn = fn
        kwargs["name"] = name
        kwargs["dependencies"] = dependencies
        self.kwargs = kwargs

    def apply_to(self, feature_store):
        fn = getattr(feature_store, self.fn)
        if fn is None:
            raise TODO
        fn(**self.kwargs)


class MaterializeTableCmd:
    def __init__(self, name="", dependencies=None, **kwargs):
        if dependencies is None:
            dependencies = []
        self.name = name
        self.dependencies = dependencies
        kwargs["name"] = name
        kwargs["dependencies"] = dependencies
        self.kwargs = kwargs

    def apply_to(self, feature_store):
        feature_store.materialize_table(**self.kwargs)


class RegisterFeatureCmd:
    def __init__(self, feature):
        self.name = feature.name
        self.dependencies = [feature.table]
        self.feature = feature

    def apply_to(self, feature_store):
        feature_store.register_feature(feature)


class RegisterTrainingDatasetCmd:
    def __init__(self, name="", label_source="", features=None, **kwargs):
        feature_deps = [feature.name for feature in features]
        self.dependencies = feature_deps + [label_source]
        self.name = name
        kwargs["features"] = features
        kwargs["label_source"] = label_source
        kwargs["name"] = name

    def apply_to(self, feature_store):
        feature_store.register_training_dataset(**kwargs)

import os
import tempfile

import yaml


class StoredState:
    def __init__(self, state):
        self.state = state
        if self.state.stored_name is not None:
            raise RuntimeError('You may only store the state once')

        self.file_handle = tempfile.NamedTemporaryFile(suffix='b5-state', mode='w', encoding='utf-8', delete=False)
        self.state.stored_name = self.name
        yaml.dump({
            key: getattr(self.state, key)
            for key in state.KEYS
        }, self.file_handle, default_flow_style=False)
        self.file_handle.close()

    def close(self):
        os.unlink(self.file_handle.name)
        self.state.stored_name = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def name(self):
        return self.file_handle.name


class State:
    KEYS = ('project_path', 'run_path', 'taskfiles', 'configfiles', 'config', 'args', 'stored_name')

    taskfiles = []
    configfiles = []
    args = {}

    def __init__(self, **kwargs):
        for key in self.KEYS:
            if not hasattr(self, key):
                setattr(self, key, None)
        for key in kwargs:
            if key not in self.KEYS:
                raise RuntimeError('Key %s is not a valid state attribute' % key)
            setattr(self, key, kwargs[key])

    def stored(self):
        return StoredState(self)

    @classmethod
    def load(cls, file_handle):
        return cls(**yaml.safe_load(file_handle))

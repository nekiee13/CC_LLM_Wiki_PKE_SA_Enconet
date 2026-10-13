"""Local disposable scratch for copied supplier commands."""
from contextlib import contextmanager
import os
from pathlib import Path
import tempfile

from project_layout import path, path_at


def scratch_root(root=None):
    directory = path('temp') if root is None else path_at(root, 'temp')
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def temporary_directory(*, prefix, root=None):
    return tempfile.TemporaryDirectory(prefix=prefix, dir=scratch_root(root))


@contextmanager
def browser_environment():
    # Playwright's driver inherits these variables when it starts. The browser
    # profile and driver scratch therefore use this supplier's temporary home.
    with temporary_directory(prefix='browser-') as folder:
        previous = {key: os.environ.get(key) for key in ('TMP', 'TEMP', 'TMPDIR')}
        os.environ.update({key: str(Path(folder)) for key in previous})
        try:
            yield
        finally:
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

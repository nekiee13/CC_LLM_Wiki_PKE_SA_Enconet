import importlib.util
from pathlib import Path
import stat

import pytest


def load():
    spec = importlib.util.spec_from_file_location('reset_ops', Path(__file__).parents[1] / 'runtime_v4/reset_operations.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_readonly_failure_restores_flag_and_bytes(tmp_path):
    target = tmp_path / 'readonly.md'
    target.write_bytes(b'preserved')
    target.chmod(target.stat().st_mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
    original = target.stat().st_mode
    def fail(path):
        raise PermissionError('simulated deletion failure')
    with pytest.raises(PermissionError):
        load().remove_generated(target, unlink=fail)
    assert target.stat().st_mode == original
    assert target.read_bytes() == b'preserved'


def test_refuses_directory_and_hardlink(tmp_path):
    import os
    with pytest.raises(ValueError):
        load().remove_generated(tmp_path)
    source = tmp_path / 'a'
    source.write_bytes(b'owner')
    os.link(source, tmp_path / 'b')
    with pytest.raises(ValueError):
        load().remove_generated(source)
    assert source.read_bytes() == b'owner'

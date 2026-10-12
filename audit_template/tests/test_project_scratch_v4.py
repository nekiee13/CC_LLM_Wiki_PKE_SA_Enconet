import importlib.util
from pathlib import Path
import subprocess
import sys


def test_copied_runtime_browser_and_pytest_use_local_scratch(tmp_path):
    source = Path(__file__).parents[1] / 'prepare_framework_candidate_v4.py'
    spec = importlib.util.spec_from_file_location('scratch_builder', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    project = tmp_path / 'Supplier with spaces'
    module.build(project)
    probe = tmp_path / 'probe.py'
    probe.write_text('''
import os,sys
from pathlib import Path
root=Path(sys.argv[1]);sys.path.insert(0,str(root/'scripts'))
import project_scratch,run_validation
before={key:os.environ.get(key) for key in ('TMP','TEMP','TMPDIR')}
with project_scratch.browser_environment():
    folder=Path(os.environ['TEMP'])
    assert folder.is_relative_to(root/'.tmp') and folder.is_dir()
    assert all(os.environ[key]==str(folder) for key in before)
assert not folder.exists()
assert before=={key:os.environ.get(key) for key in before}
test=root/'.tmp/test_scratch.py'
test.write_text('import tempfile\\nfrom pathlib import Path\\ndef test_local(tmp_path):\\n assert tmp_path.is_relative_to(Path('+repr(str(root/'.tmp'))+'))\\n assert Path(tempfile.gettempdir()).is_relative_to(Path('+repr(str(root/'.tmp'))+'))\\n')
state,detail=run_validation._run_step(run_validation.Step('local pytest',
    [sys.executable,'-m','pytest',str(test),'-q','-p','no:cacheprovider']))
assert state=='PASS',detail
assert not list((root/'.tmp').glob('validation-*'))
assert not list(root.glob('pytest*'))
''', encoding='utf-8')
    result = subprocess.run([sys.executable, '-B', str(probe), str(project)],
                            capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr

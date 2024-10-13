import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor


notebooks = ["test_metric.ipynb", "test_FLRW.ipynb"]


@pytest.mark.parametrize("notebook", notebooks)
def test_notebook_exec(notebook):
  with open(notebook) as f:
      nb = nbformat.read(f, as_version=4)
      ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
      try:
        assert ep.preprocess(nb) is not None, f"Got empty notebook for {notebook}"
      except Exception:
          assert False, f"Failed executing {notebook}"
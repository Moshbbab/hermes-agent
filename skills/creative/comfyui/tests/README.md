# ComfyUI Skill Tests

Pytest suite covering the skill's scripts. Pure-stdlib unit tests run
without any setup; cloud integration tests need a Comfy Cloud API key.

## Running

```bash
# Unit tests only (no network required) — runs in <1s
python3 -m pytest tests/ -c tests/pytest.ini

# Including cloud integration tests
COMFY_CLOUD_API_KEY="comfyui-..." python3 -m pytest tests/ -c tests/pytest.ini

# Just cloud tests
COMFY_CLOUD_API_KEY="comfyui-..." python3 -m pytest tests/test_cloud_integration.py \
  -c tests/pytest.ini -v
```

The `-c` override isolates this suite from any parent `pyproject.toml`
pytest config (marker filters, plugin-specific `addopts` flags).

## Test files

| File | Coverage |
|------|----------|
| `test_common.py` | Cloud detection, URL routing, format validation, embeddings, paths, seeds, model-list parsing, folder aliases |
| `test_extract_schema.py` | Connection tracing, positive/negative prompt detection, dedup logic, embedding deps |
| `test_run_workflow.py` | Param injection (incl. -1 seed, link refusal), output download walk, runner construction |
| `test_check_deps.py` | Model-name fuzzy matching, install command suggestions |
| `test_cloud_integration.py` | Live cloud API contract tests (auto-skipped without API key) |

## Adding tests

When you change a script:

1. Add a unit test if the change is pure logic (cloud detection, parsing, etc.)
2. Add a cloud integration test if the change depends on cloud API behavior
   (use `pytestmark = pytest.mark.cloud` so it auto-skips without a key)
3. Workflow fixtures live in `conftest.py` (`sd15_workflow`, `flux_workflow`,
   `video_workflow`)

## Why the explicit `-c`?

The parent hermes-agent repo's `pyproject.toml` sets `addopts` flags
(`-m 'not integration'`, pytest-timeout options) that assume the repo's own
dev dependencies and markers. `-c tests/pytest.ini` pins this suite to its
own config so it runs identically regardless of where the skill is
installed or which plugins the surrounding environment has.

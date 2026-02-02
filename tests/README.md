# Tests

This directory contains the test suite for custom-copilot.

## Running Tests

### Install Dependencies

```bash
pip install -e ".[dev]"
```

### Run All Tests

```bash
pytest tests/
```

### Run with Coverage

```bash
pytest tests/ --cov=src/custom_copilot --cov-report=term-missing
```

### Run Specific Test File

```bash
pytest tests/test_init.py -v
```

### Run Specific Test

```bash
pytest tests/test_init.py::TestInitCommand::test_init_default_github_engine -v
```

## Test Structure

- `conftest.py` - Pytest configuration and shared fixtures
- `test_init.py` - Tests for the init command with multi-engine support
- `test_template.py` - Tests for the template command
- `test_publish.py` - Tests for the publish command
- `test_utils.py` - Tests for utility functions
- `test_config.py` - Tests for configuration functions

## Test Coverage

Current test coverage focuses on:

### Init Command (100% coverage)
- Default GitHub engine initialization
- Claude engine initialization
- CUCO engine initialization
- Invalid engine error handling
- Help output
- Idempotent behavior

### Template Command (85% coverage)
- Template listing
- Agent, skill, prompt, and bundle creation
- Target directory detection (.github, .claude, .cuco)
- Invalid type handling
- Placeholder replacement

### Publish Command (63% coverage)
- Resource validation for all types
- Marketplace publishing (instruction generation)
- Local publishing
- Type inference
- Error handling

### Utils (65% coverage)
- Target directory detection with priority order
- File and directory hashing
- Project root detection

### Config (34% coverage)
- Custom source path detection for all formats
- GitHub URL parsing
- AgentSkills repository detection

## Writing New Tests

When adding new features, please:

1. Create tests in the appropriate test file
2. Use the provided fixtures (`temp_dir`, `mock_cwd`)
3. Follow the existing test structure and naming conventions
4. Aim for good coverage of happy paths and error cases
5. Run tests locally before committing

## Continuous Integration

Tests are automatically run on:
- Every push to main
- Every pull request
- Python versions: 3.12, 3.13

See `.github/workflows/test.yml` for CI configuration.

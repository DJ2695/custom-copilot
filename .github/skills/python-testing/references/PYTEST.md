# Pytest Advanced Patterns

Comprehensive guide to pytest features, fixtures, parametrization, and best practices.

## Table of Contents

- [Fixture System](#fixture-system)
- [Parametrization](#parametrization)
- [Markers](#markers)
- [Mocking Strategies](#mocking-strategies)
- [conftest.py Organization](#conftestpy-organization)
- [Test Discovery](#test-discovery)
- [Coverage Configuration](#coverage-configuration)
- [pytest.ini Setup](#pytestini-setup)

## Fixture System

### Basic Fixtures

```python
import pytest

@pytest.fixture
def database_connection():
    """Create database connection."""
    conn = create_connection()
    yield conn
    conn.close()  # Cleanup after test

def test_query(database_connection):
    result = database_connection.query("SELECT 1")
    assert result is not None
```

### Fixture Scopes

Control how often fixtures are created:

```python
@pytest.fixture(scope="function")  # Default: new instance per test
def function_scope():
    return {"data": "fresh"}

@pytest.fixture(scope="class")  # One instance per test class
def class_scope():
    return expensive_setup()

@pytest.fixture(scope="module")  # One instance per module
def module_scope():
    return shared_resource()

@pytest.fixture(scope="session")  # One instance per test session
def session_scope():
    return global_config()
```

### Fixture Dependencies

Fixtures can depend on other fixtures:

```python
@pytest.fixture
def database():
    return Database()

@pytest.fixture
def user_repository(database):
    """Repository depends on database fixture."""
    return UserRepository(database)

@pytest.fixture
def user_service(user_repository):
    """Service depends on repository fixture."""
    return UserService(user_repository)

def test_create_user(user_service):
    """Test uses the entire dependency chain."""
    user = user_service.create("test@example.com")
    assert user.email == "test@example.com"
```

### Autouse Fixtures

Automatically applied to all tests in scope:

```python
@pytest.fixture(autouse=True)
def reset_database():
    """Automatically reset database before each test."""
    db.clear()
    yield
    db.clear()

@pytest.fixture(autouse=True, scope="session")
def setup_logging():
    """Configure logging once per session."""
    logging.basicConfig(level=logging.DEBUG)
```

### Fixture Factories

Return functions that create objects:

```python
@pytest.fixture
def user_factory():
    """Factory for creating test users."""
    def _create_user(email=None, role="user"):
        return User(
            email=email or f"test{random.randint(1000,9999)}@example.com",
            role=role
        )
    return _create_user

def test_admin_access(user_factory):
    admin = user_factory(role="admin")
    regular_user = user_factory(role="user")
    
    assert admin.can_access_admin_panel()
    assert not regular_user.can_access_admin_panel()
```

### Parametrized Fixtures

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def database_client(request):
    """Test with multiple database backends."""
    if request.param == "sqlite":
        return SQLiteClient()
    elif request.param == "postgres":
        return PostgresClient()
    else:
        return MySQLClient()

def test_query(database_client):
    """This test runs 3 times, once for each database."""
    result = database_client.query("SELECT 1")
    assert result is not None
```

## Parametrization

### Basic Parametrization

```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert square(input) == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("x,y,expected", [
    (1, 1, 2),
    (2, 3, 5),
    (-1, 1, 0),
])
def test_addition(x, y, expected):
    assert add(x, y) == expected
```

### Parametrize with IDs

```python
@pytest.mark.parametrize("input,expected", [
    pytest.param(2, 4, id="two_squared"),
    pytest.param(3, 9, id="three_squared"),
    pytest.param(0, 0, id="zero_squared"),
])
def test_square_with_ids(input, expected):
    assert square(input) == expected
```

### Multiple Decorators

```python
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [4, 5, 6])
def test_multiply(x, y):
    """Runs 9 times (3 x 3 combinations)."""
    assert multiply(x, y) == x * y
```

## Markers

### Built-in Markers

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
def test_python38_feature():
    pass

@pytest.mark.xfail(reason="Known bug")
def test_known_issue():
    assert buggy_function() == expected

@pytest.mark.xfail(strict=True)
def test_should_fail():
    """Fails if it passes unexpectedly."""
    assert False
```

### Custom Markers

```python
# pytest.ini
[pytest]
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow-running tests
    security: Security-related tests
    smoke: Smoke tests

# In test files
@pytest.mark.unit
def test_calculation():
    assert calculate(2, 3) == 5

@pytest.mark.integration
@pytest.mark.slow
def test_full_workflow():
    # Long-running integration test
    pass
```

### Running Specific Markers

```bash
# Run only unit tests
pytest -m unit

# Run integration tests
pytest -m integration

# Run multiple markers
pytest -m "unit or integration"

# Exclude markers
pytest -m "not slow"

# Complex expressions
pytest -m "integration and not slow"
```

## Mocking Strategies

### Using unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock

def test_with_mock():
    mock_service = Mock()
    mock_service.get_data.return_value = {"key": "value"}
    
    result = my_function(mock_service)
    
    mock_service.get_data.assert_called_once()
    assert result["key"] == "value"
```

### Patching

```python
@patch('module.external_api_call')
def test_with_patch(mock_api):
    mock_api.return_value = {"status": "success"}
    
    result = function_that_calls_api()
    
    assert result["status"] == "success"
    mock_api.assert_called_once()
```

### Multiple Patches

```python
@patch('module.database')
@patch('module.cache')
def test_multiple_patches(mock_cache, mock_database):
    mock_database.query.return_value = [1, 2, 3]
    mock_cache.get.return_value = None
    
    result = function_using_both()
    
    assert len(result) == 3
```

### Context Manager Patching

```python
def test_with_context_manager():
    with patch('module.external_service') as mock_service:
        mock_service.return_value.process.return_value = "result"
        
        result = my_function()
        
        assert result == "result"
```

### pytest-mock Plugin

```python
# Install: pip install pytest-mock

def test_with_mocker(mocker):
    """mocker fixture from pytest-mock."""
    mock_service = mocker.Mock()
    mock_service.get_data.return_value = {"key": "value"}
    
    # Spy on real object
    spy = mocker.spy(RealClass, 'method')
    
    # Patch
    mocker.patch('module.function', return_value=42)
```

### Monkeypatch Fixture

```python
def test_with_monkeypatch(monkeypatch):
    """Built-in pytest fixture for patching."""
    
    # Set attribute
    monkeypatch.setattr("module.CONSTANT", "test_value")
    
    # Set environment variable
    monkeypatch.setenv("API_KEY", "test-key")
    
    # Set dictionary item
    monkeypatch.setitem(config, "key", "value")
    
    # Delete attribute
    monkeypatch.delattr("module.attribute")
```

## conftest.py Organization

### Project-Level conftest.py

```python
# tests/conftest.py
import pytest
from unittest.mock import Mock

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow tests")

def pytest_addoption(parser):
    """Add custom command-line options."""
    parser.addoption(
        "--integration",
        action="store_true",
        help="run integration tests"
    )

def pytest_collection_modifyitems(config, items):
    """Skip tests based on options."""
    if not config.getoption("--integration"):
        skip_integration = pytest.mark.skip(reason="need --integration")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)

# Shared fixtures
@pytest.fixture
def mock_firestore():
    return Mock()

@pytest.fixture
def test_data():
    return {
        "id": "test-123",
        "name": "Test Item"
    }
```

### Directory-Specific conftest.py

```python
# tests/integration/conftest.py
import pytest
from test_helpers import setup_test_database

@pytest.fixture(scope="module")
def test_database():
    """Integration tests share a test database."""
    db = setup_test_database()
    yield db
    db.teardown()

@pytest.fixture
def authenticated_client(test_database):
    """Client with authentication."""
    client = Client(test_database)
    client.authenticate("test-user")
    return client
```

## Test Discovery

### Naming Conventions

pytest discovers tests based on naming:

- Test files: `test_*.py` or `*_test.py`
- Test classes: `Test*` (no `__init__` method)
- Test functions: `test_*`

### Custom Collection

```python
# pytest.ini
[pytest]
python_files = test_*.py *_test.py check_*.py
python_classes = Test* Check*
python_functions = test_* check_*
```

### Ignoring Files

```python
# conftest.py
import sys

collect_ignore = ["setup.py", "docs/"]

if sys.version_info < (3, 8):
    collect_ignore.append("tests/python38_features.py")
```

## Coverage Configuration

### pytest.ini

```ini
[pytest]
addopts = 
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80

testpaths = tests
python_files = test_*.py
```

### .coveragerc

```ini
[run]
source = src
omit = 
    */tests/*
    */migrations/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
```

### Running with Coverage

```bash
# Basic coverage
pytest --cov=src

# With HTML report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Show missing lines
pytest --cov=src --cov-report=term-missing

# Fail if coverage below threshold
pytest --cov=src --cov-fail-under=80
```

## pytest.ini Setup

### Complete Configuration Example

```ini
[pytest]
# Test discovery
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Output options
addopts = 
    -v
    --tb=short
    --strict-markers
    --cov=src
    --cov-report=html
    --cov-report=term-missing:skip-covered
    --cov-fail-under=80

# Markers
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (slower, external deps)
    slow: Slow-running tests
    security: Security-related tests
    smoke: Smoke tests for critical functionality

# Warnings
filterwarnings =
    error
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning

# Logging
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)s] %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

# Coverage
[coverage:run]
source = src
omit = 
    */tests/*
    */migrations/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
```

## Best Practices

1. **Keep tests isolated**: Each test should set up and tear down its own state
2. **Use fixtures wisely**: Share setup logic, but don't create hidden dependencies
3. **Test one thing**: Each test should verify one specific behavior
4. **Descriptive names**: Test names should explain what is being tested
5. **Fast tests**: Unit tests should run in milliseconds
6. **Parametrize similar tests**: DRY principle applies to tests too
7. **Mock external dependencies**: Unit tests shouldn't hit real APIs/databases
8. **Coverage as a guide**: 80%+ is good, but 100% doesn't mean bug-free

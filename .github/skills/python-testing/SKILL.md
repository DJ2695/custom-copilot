---
name: python-testing
description: 'Comprehensive Python testing guide for unit tests, integration tests, services, repositories, and Firebase Functions with pytest. Use when: (1) Writing tests for Python applications, (2) Testing services and repositories, (3) Testing Firebase Cloud Functions, (4) Setting up pytest fixtures and mocks, (5) Writing integration tests, (6) Working with pytest-cov for coverage, (7) Using pytest-mock or unittest.mock. Keywords: pytest, unit test, integration test, mock, fixture, firebase functions, service test, repository test, TDD.'
---

# Python Testing Skill

Comprehensive testing patterns for Python applications using pytest, including services, repositories, and Firebase Cloud Functions.

## When to Use This Skill

- Writing unit tests for Python code
- Testing service and repository layers
- Testing Firebase Cloud Functions
- Setting up pytest fixtures and mocks
- Writing integration tests
- Configuring test coverage with pytest-cov
- Implementing TDD workflow

## Prerequisites

```bash
pip install pytest pytest-cov pytest-mock pytest-asyncio
pip install firebase-functions-test  # For Firebase Functions
```

## Test Types Overview

| Type | Location | Command | Coverage Target |
|------|----------|---------|-----------------|
| Unit | `tests/unit/` | `pytest tests/unit/` | 80%+ |
| Integration | `tests/integration/` | `pytest tests/integration/ --integration` | Key flows |
| Service | `tests/unit/services/` | `pytest tests/unit/services/` | 80%+ |
| Repository | `tests/unit/repositories/` | `pytest tests/unit/repositories/` | 80%+ |
| Firebase Functions | `functions/tests/` | `pytest functions/tests/` | 100% for auth/security |

## Quick Start

### Basic Test Structure

```python
# tests/test_calculator.py
import pytest

def test_addition():
    """Test that addition works correctly."""
    assert 1 + 1 == 2

def test_division_by_zero():
    """Test that division by zero raises error."""
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific file
pytest tests/test_calculator.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run only unit tests
pytest -m unit

# Run integration tests
pytest -m integration --integration
```

## Testing Patterns

### Unit Tests

Fast, isolated tests for single units of functionality. See [references/PYTEST.md](references/PYTEST.md) for comprehensive patterns.

```python
import pytest
from my_module import Calculator

class TestCalculator:
    @pytest.fixture
    def calculator(self):
        return Calculator()

    def test_add(self, calculator):
        assert calculator.add(2, 3) == 5
```

### Service Tests

Test business logic orchestration. Services coordinate between repositories and external services.

```python
from unittest.mock import Mock
import pytest

class TestUserService:
    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def service(self, mock_repository):
        return UserService(repository=mock_repository)

    def test_create_user_success(self, service, mock_repository):
        mock_repository.create.return_value = "user-123"
        result = service.create_user({"email": "test@example.com"})
        assert result == "user-123"
```

### Repository Tests

Test data access layer. Mock database clients to avoid external dependencies.

```python
def test_repository_get_by_id(mock_firestore):
    repository = UserRepository(mock_firestore)
    mock_firestore.collection().document().get().to_dict.return_value = {"id": "123"}
    
    result = repository.get_by_id("123")
    assert result["id"] == "123"
```

### Firebase Functions Tests

Test Cloud Functions with `firebase-functions-test`. See [references/FIREBASE-FUNCTIONS.md](references/FIREBASE-FUNCTIONS.md) for details.

```python
from firebase_functions import https_fn
from unittest.mock import Mock
import pytest

def test_function_requires_auth():
    req = Mock(spec=https_fn.CallableRequest)
    req.auth = None
    
    with pytest.raises(https_fn.HttpsError) as exc_info:
        my_function(req)
    assert exc_info.value.code == "unauthenticated"
```

## Common Fixtures

### Setup in conftest.py

```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_firestore_client():
    """Mock Firestore client for tests."""
    return Mock()

@pytest.fixture
def test_user_id():
    """Standard test user ID."""
    return "test-user-123"

@pytest.fixture
def sample_user_data():
    """Sample user data for tests."""
    return {
        "id": "user-123",
        "email": "test@example.com",
        "created_at": "2024-01-01T00:00:00Z"
    }
```

See [references/PYTEST.md](references/PYTEST.md) for advanced fixture patterns.

## Test Organization

```
backend/
├── functions/
│   ├── main.py
│   └── tests/
│       ├── conftest.py
│       ├── test_auth_functions.py
│       └── test_data_functions.py
└── tests/
    ├── conftest.py
    ├── unit/
    │   ├── services/
    │   │   └── test_user_service.py
    │   └── repositories/
    │       └── test_user_repository.py
    └── integration/
        └── test_user_flow.py
```

## Custom Markers

```python
# pytest.ini
[pytest]
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow-running tests
    security: Security-related tests

# Usage in tests
@pytest.mark.unit
def test_fast_unit():
    assert True

@pytest.mark.integration
def test_integration():
    assert True
```

Run specific markers:
```bash
pytest -m unit
pytest -m "integration and not slow"
```

## TDD Workflow

```
1. Write failing test
   → Define expected behavior
   → Run test, should fail (RED)

2. Implement minimum code to pass
   → Write simplest implementation
   → Run test, should pass (GREEN)

3. Refactor
   → Improve code quality
   → Keep tests passing

4. Repeat
```

## Templates Available

| Template | Purpose | Location |
|----------|---------|----------|
| `unit-test.py.template` | Basic unit tests | `templates/` |
| `service-test.py.template` | Service layer tests | `templates/` |
| `repository-test.py.template` | Repository pattern tests | `templates/` |
| `function-test.py.template` | Firebase callable function tests | `templates/` |
| `conftest.py.template` | Shared fixtures and configuration | `templates/` |

### Using Templates

1. Copy template to your test directory
2. Replace placeholders:
   - `${ClassName}` → Your class name (PascalCase)
   - `${module_name}` → Your module name (snake_case)
   - `${ServiceName}` → Your service name
3. Adjust imports and test cases
4. Run tests to verify

## Rules

✅ **DO:**
- Test behavior, not implementation
- Use mocks for external dependencies
- Cover success AND failure paths
- Write descriptive test names
- Keep unit tests fast (<100ms)
- Use fixtures for setup/teardown
- Organize tests by type (unit/integration)

❌ **DON'T:**
- Write tests that always pass
- Test private methods directly
- Mock the class under test
- Skip error path testing
- Put integration tests with unit tests
- Hardcode test data in multiple places

## Further Reading

- [references/PYTEST.md](references/PYTEST.md) - Advanced pytest patterns, fixtures, parametrization
- [references/FIREBASE-FUNCTIONS.md](references/FIREBASE-FUNCTIONS.md) - Firebase Functions testing specifics
- [references/INTEGRATION.md](references/INTEGRATION.md) - Integration testing patterns

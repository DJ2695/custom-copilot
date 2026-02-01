# Integration Testing Patterns

Comprehensive guide to writing integration tests for Python applications.

## Table of Contents

- [Integration vs Unit Tests](#integration-vs-unit-tests)
- [Test Organization](#test-organization)
- [Database Fixtures](#database-fixtures)
- [API Testing](#api-testing)
- [Testing with Docker](#testing-with-docker)
- [Test Data Management](#test-data-management)
- [CI/CD Integration](#cicd-integration)

## Integration vs Unit Tests

### Key Differences

| Aspect | Unit Tests | Integration Tests |
|--------|-----------|-------------------|
| Scope | Single unit (function/class) | Multiple components |
| Speed | Fast (<100ms) | Slower (seconds) |
| Dependencies | All mocked | Real or partial mocks |
| Isolation | Completely isolated | Tests interactions |
| Failures | Pinpoint exact issue | Harder to diagnose |
| Location | `tests/unit/` | `tests/integration/` |

### When to Write Integration Tests

✅ **Write integration tests for:**
- Critical user workflows (signup, checkout, etc.)
- Third-party API interactions
- Database query patterns
- Multi-service interactions
- Complex business processes

❌ **Don't write integration tests for:**
- Simple calculations
- Pure functions
- Already covered by unit tests
- Every possible path (use unit tests for that)

## Test Organization

### Directory Structure

```
tests/
├── conftest.py               # Shared fixtures
├── unit/                     # Fast, isolated tests
│   ├── conftest.py
│   ├── services/
│   │   └── test_user_service.py
│   └── repositories/
│       └── test_user_repository.py
└── integration/              # Slower, multi-component tests
    ├── conftest.py
    ├── fixtures/
    │   ├── test_data.json
    │   └── seed_data.sql
    ├── test_user_signup_flow.py
    └── test_payment_processing.py
```

### Marking Integration Tests

```python
# pytest.ini
[pytest]
markers =
    integration: Integration tests requiring external services

# In test files
import pytest

@pytest.mark.integration
class TestUserSignupFlow:
    """Integration tests for user signup."""
    
    def test_complete_signup_flow(self):
        """Test end-to-end signup process."""
        pass
```

### Running Integration Tests Separately

```bash
# Run only unit tests (fast)
pytest tests/unit/

# Run integration tests (need --integration flag)
pytest tests/integration/ --integration

# Skip integration tests by default
pytest -m "not integration"
```

## Database Fixtures

### PostgreSQL Test Database

```python
# tests/integration/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine."""
    engine = create_engine("postgresql://test:test@localhost:5432/test_db")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create isolated database session per test."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    
    # Start transaction
    connection = db_engine.connect()
    transaction = connection.begin()
    
    yield session
    
    # Rollback transaction
    session.close()
    transaction.rollback()
    connection.close()

@pytest.mark.integration
def test_user_repository(db_session):
    """Test repository with real database."""
    repository = UserRepository(db_session)
    
    user = repository.create({"email": "test@example.com"})
    assert user.id is not None
    
    retrieved = repository.get_by_id(user.id)
    assert retrieved.email == "test@example.com"
```

### Firestore Test Database

```python
# tests/integration/conftest.py
import pytest
import os
from firebase_admin import credentials, initialize_app, delete_app, firestore

@pytest.fixture(scope="session")
def firebase_app():
    """Initialize Firebase with emulator."""
    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
    
    cred = credentials.Certificate("test-service-account.json")
    app = initialize_app(cred, name="test-app")
    
    yield app
    
    delete_app(app)
    del os.environ["FIRESTORE_EMULATOR_HOST"]

@pytest.fixture(scope="function")
def firestore_db(firebase_app):
    """Get Firestore client with cleanup."""
    db = firestore.client(app=firebase_app)
    
    yield db
    
    # Clean up test collections
    collections = ["users", "documents", "notifications"]
    for collection_name in collections:
        docs = db.collection(collection_name).stream()
        for doc in docs:
            doc.reference.delete()

@pytest.mark.integration
def test_user_creation_flow(firestore_db):
    """Test complete user creation with Firestore."""
    # Create user
    user_ref = firestore_db.collection("users").add({
        "email": "test@example.com",
        "created_at": firestore.SERVER_TIMESTAMP
    })
    
    # Verify user exists
    user_doc = user_ref[1].get()
    assert user_doc.exists
    assert user_doc.to_dict()["email"] == "test@example.com"
```

## API Testing

### Testing REST APIs

```python
# tests/integration/test_api.py
import pytest
import requests
from flask import Flask

@pytest.fixture(scope="module")
def api_client():
    """Create test API client."""
    from app import create_app
    app = create_app(config="testing")
    
    with app.test_client() as client:
        yield client

@pytest.mark.integration
class TestUserAPI:
    """Integration tests for User API."""
    
    def test_create_user_endpoint(self, api_client):
        """Test POST /users endpoint."""
        response = api_client.post("/users", json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data["email"] == "test@example.com"
        assert "id" in data
    
    def test_get_user_endpoint(self, api_client):
        """Test GET /users/{id} endpoint."""
        # Create user first
        create_response = api_client.post("/users", json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        })
        user_id = create_response.get_json()["id"]
        
        # Get user
        response = api_client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == user_id
    
    def test_authentication_required(self, api_client):
        """Test protected endpoint requires auth."""
        response = api_client.get("/users/me")
        assert response.status_code == 401
```

### Testing External APIs

```python
@pytest.fixture
def mock_external_api(requests_mock):
    """Mock external API responses."""
    requests_mock.get(
        "https://api.example.com/users/123",
        json={"id": "123", "name": "Test User"}
    )
    requests_mock.post(
        "https://api.example.com/users",
        json={"id": "new-123", "name": "New User"},
        status_code=201
    )

@pytest.mark.integration
def test_external_api_integration(mock_external_api):
    """Test integration with external API."""
    from services import ExternalService
    
    service = ExternalService()
    result = service.get_user("123")
    
    assert result["id"] == "123"
    assert result["name"] == "Test User"
```

## Testing with Docker

### Docker Compose for Tests

```yaml
# docker-compose.test.yml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    ports:
      - "5432:5432"
    tmpfs:
      - /var/lib/postgresql/data  # In-memory for speed
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  test-runner:
    build: .
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://test:test@postgres:5432/test_db
      REDIS_URL: redis://redis:6379
    command: pytest tests/integration/
```

### Running Tests with Docker

```bash
# Start services and run tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# Run specific test suite
docker-compose -f docker-compose.test.yml run test-runner pytest tests/integration/test_api.py
```

### Docker Fixture

```python
# tests/integration/conftest.py
import pytest
import docker
import time

@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for tests."""
    client = docker.from_env()
    
    # Start container
    container = client.containers.run(
        "postgres:14",
        environment={
            "POSTGRES_DB": "test_db",
            "POSTGRES_USER": "test",
            "POSTGRES_PASSWORD": "test"
        },
        ports={"5432/tcp": 5432},
        detach=True,
        remove=True
    )
    
    # Wait for PostgreSQL to be ready
    time.sleep(3)
    
    yield container
    
    # Cleanup
    container.stop()
```

## Test Data Management

### Fixture Files

```python
# tests/integration/conftest.py
import pytest
import json
from pathlib import Path

@pytest.fixture
def load_test_data():
    """Load test data from JSON files."""
    def _load(filename):
        path = Path(__file__).parent / "fixtures" / filename
        with open(path) as f:
            return json.load(f)
    return _load

@pytest.mark.integration
def test_bulk_import(db_session, load_test_data):
    """Test importing bulk data."""
    users_data = load_test_data("users.json")
    
    for user_data in users_data:
        db_session.add(User(**user_data))
    db_session.commit()
    
    assert db_session.query(User).count() == len(users_data)
```

### Factory Pattern

```python
# tests/integration/factories.py
from dataclasses import dataclass
from datetime import datetime
import random

@dataclass
class UserFactory:
    """Factory for creating test users."""
    
    @staticmethod
    def create(**kwargs):
        """Create user with default or custom values."""
        defaults = {
            "email": f"test{random.randint(1000,9999)}@example.com",
            "name": "Test User",
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        defaults.update(kwargs)
        return User(**defaults)
    
    @staticmethod
    def create_batch(count, **kwargs):
        """Create multiple users."""
        return [UserFactory.create(**kwargs) for _ in range(count)]

# Usage in tests
@pytest.mark.integration
def test_user_search(db_session):
    """Test searching with multiple users."""
    # Create test data
    users = UserFactory.create_batch(10, is_active=True)
    db_session.add_all(users)
    db_session.commit()
    
    # Test search
    results = search_users(query="test")
    assert len(results) == 10
```

### Database Seeding

```python
# tests/integration/conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def seed_database(db_session):
    """Seed database with test data."""
    # Read SQL file
    sql_file = Path(__file__).parent / "fixtures" / "seed_data.sql"
    with open(sql_file) as f:
        sql = f.read()
    
    # Execute seed data
    db_session.execute(sql)
    db_session.commit()

@pytest.mark.integration
def test_with_seeded_data(db_session, seed_database):
    """Test with pre-populated database."""
    users = db_session.query(User).all()
    assert len(users) > 0
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Integration Tests

on: [push, pull_request]

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379
        run: |
          pytest tests/integration/ --integration --cov --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Pytest Configuration for CI

```ini
# pytest.ini
[pytest]
# Separate unit and integration test paths
testpaths = tests

# Integration-specific options
addopts = 
    -v
    --tb=short
    --strict-markers

# Markers
markers =
    integration: Integration tests (slower, external deps)
    unit: Unit tests (fast, isolated)
    slow: Slow-running tests
    
# Timeout for integration tests
timeout = 300
```

## Best Practices

1. **Keep integration tests focused**: Test complete workflows, not individual units
2. **Use transactions for database tests**: Rollback after each test for isolation
3. **Mock sparingly**: Only mock what you absolutely must
4. **Test happy paths first**: Then add edge cases
5. **Use factories for test data**: Don't hardcode test data
6. **Run in CI/CD**: Automate integration test execution
7. **Separate from unit tests**: Different directories, different markers
8. **Use Docker for consistency**: Same environment locally and in CI
9. **Clean up after tests**: Leave no test data behind
10. **Monitor test duration**: Keep integration tests under 5 minutes total

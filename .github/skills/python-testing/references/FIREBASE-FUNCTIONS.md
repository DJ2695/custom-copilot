# Firebase Functions Testing

Comprehensive guide to testing Firebase Cloud Functions with Python.

## Table of Contents

- [Setup](#setup)
- [Testing Callable Functions](#testing-callable-functions)
- [Testing Triggered Functions](#testing-triggered-functions)
- [Mocking Firebase Admin SDK](#mocking-firebase-admin-sdk)
- [Testing with Emulators](#testing-with-emulators)
- [Error Handling Patterns](#error-handling-patterns)
- [Security Testing](#security-testing)

## Setup

### Installation

```bash
pip install firebase-functions
pip install firebase-admin
pip install pytest pytest-mock
```

### Project Structure

```
functions/
├── main.py                 # Function definitions
├── services/
│   └── user_service.py
├── repositories/
│   └── user_repository.py
└── tests/
    ├── conftest.py
    ├── test_auth_functions.py
    └── test_data_functions.py
```

### conftest.py Setup

```python
# functions/tests/conftest.py
import pytest
from unittest.mock import Mock
from firebase_functions import https_fn

@pytest.fixture
def mock_firestore_client():
    """Mock Firestore client."""
    return Mock()

@pytest.fixture
def mock_auth_context():
    """Mock authenticated context."""
    context = Mock()
    context.auth = Mock()
    context.auth.uid = "test-user-123"
    context.auth.token = {"email": "test@example.com"}
    return context

@pytest.fixture
def mock_callable_request():
    """Mock CallableRequest with auth."""
    req = Mock(spec=https_fn.CallableRequest)
    req.auth = Mock()
    req.auth.uid = "test-user-123"
    req.auth.token = {"email": "test@example.com"}
    req.data = {}
    return req

@pytest.fixture
def mock_unauth_request():
    """Mock CallableRequest without auth."""
    req = Mock(spec=https_fn.CallableRequest)
    req.auth = None
    req.data = {}
    return req
```

## Testing Callable Functions

### Basic Callable Function

```python
# main.py
from firebase_functions import https_fn
from firebase_admin import firestore

@https_fn.on_call()
def get_user_profile(req: https_fn.CallableRequest) -> dict:
    """Get user profile data."""
    # Verify authentication
    if not req.auth:
        raise https_fn.HttpsError(
            code="unauthenticated",
            message="User must be authenticated"
        )
    
    # Validate input
    if "user_id" not in req.data:
        raise https_fn.HttpsError(
            code="invalid-argument",
            message="user_id is required"
        )
    
    # Get data
    db = firestore.client()
    doc = db.collection("users").document(req.data["user_id"]).get()
    
    if not doc.exists:
        raise https_fn.HttpsError(
            code="not-found",
            message="User not found"
        )
    
    return doc.to_dict()
```

### Testing Callable Function

```python
# tests/test_auth_functions.py
import pytest
from unittest.mock import Mock, patch
from firebase_functions import https_fn
from main import get_user_profile

class TestGetUserProfile:
    """Test suite for get_user_profile function."""
    
    def test_requires_authentication(self, mock_unauth_request):
        """Test function rejects unauthenticated requests."""
        with pytest.raises(https_fn.HttpsError) as exc_info:
            get_user_profile(mock_unauth_request)
        
        assert exc_info.value.code == "unauthenticated"
        assert "authenticated" in exc_info.value.message.lower()
    
    def test_validates_user_id(self, mock_callable_request):
        """Test function validates required user_id parameter."""
        mock_callable_request.data = {}  # Missing user_id
        
        with pytest.raises(https_fn.HttpsError) as exc_info:
            get_user_profile(mock_callable_request)
        
        assert exc_info.value.code == "invalid-argument"
        assert "user_id" in exc_info.value.message
    
    @patch('main.firestore.client')
    def test_returns_user_data(self, mock_firestore, mock_callable_request):
        """Test successful user profile retrieval."""
        # Arrange
        mock_callable_request.data = {"user_id": "user-123"}
        
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {
            "id": "user-123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        mock_firestore.return_value.collection.return_value\
            .document.return_value.get.return_value = mock_doc
        
        # Act
        result = get_user_profile(mock_callable_request)
        
        # Assert
        assert result["id"] == "user-123"
        assert result["email"] == "test@example.com"
        mock_firestore.return_value.collection.assert_called_once_with("users")
    
    @patch('main.firestore.client')
    def test_handles_missing_user(self, mock_firestore, mock_callable_request):
        """Test function handles non-existent user."""
        # Arrange
        mock_callable_request.data = {"user_id": "nonexistent"}
        
        mock_doc = Mock()
        mock_doc.exists = False
        
        mock_firestore.return_value.collection.return_value\
            .document.return_value.get.return_value = mock_doc
        
        # Act & Assert
        with pytest.raises(https_fn.HttpsError) as exc_info:
            get_user_profile(mock_callable_request)
        
        assert exc_info.value.code == "not-found"
```

## Testing Triggered Functions

### Firestore Trigger

```python
# main.py
from firebase_functions import firestore_fn
from firebase_admin import firestore

@firestore_fn.on_document_created(document="users/{user_id}")
def on_user_created(event: firestore_fn.Event[firestore_fn.DocumentSnapshot]):
    """Trigger when new user is created."""
    user_data = event.data.to_dict()
    
    # Create welcome document
    db = firestore.client()
    db.collection("notifications").add({
        "user_id": user_data["id"],
        "type": "welcome",
        "message": f"Welcome {user_data['name']}!",
        "created_at": firestore.SERVER_TIMESTAMP
    })
```

### Testing Firestore Trigger

```python
# tests/test_triggers.py
import pytest
from unittest.mock import Mock, patch
from main import on_user_created

class TestOnUserCreated:
    """Test suite for on_user_created trigger."""
    
    @pytest.fixture
    def mock_event(self):
        """Mock Firestore event."""
        event = Mock()
        event.data = Mock()
        event.data.to_dict.return_value = {
            "id": "user-123",
            "name": "Test User",
            "email": "test@example.com"
        }
        event.params = {"user_id": "user-123"}
        return event
    
    @patch('main.firestore.client')
    def test_creates_welcome_notification(self, mock_firestore, mock_event):
        """Test welcome notification is created."""
        # Arrange
        mock_collection = Mock()
        mock_firestore.return_value.collection.return_value = mock_collection
        
        # Act
        on_user_created(mock_event)
        
        # Assert
        mock_firestore.return_value.collection.assert_called_once_with("notifications")
        mock_collection.add.assert_called_once()
        
        # Verify notification data
        call_args = mock_collection.add.call_args[0][0]
        assert call_args["user_id"] == "user-123"
        assert call_args["type"] == "welcome"
        assert "Test User" in call_args["message"]
```

## Mocking Firebase Admin SDK

### Mocking Firestore

```python
@pytest.fixture
def mock_firestore_chain():
    """Mock complete Firestore query chain."""
    mock_db = Mock()
    mock_collection = Mock()
    mock_doc_ref = Mock()
    mock_doc = Mock()
    
    mock_db.collection.return_value = mock_collection
    mock_collection.document.return_value = mock_doc_ref
    mock_doc_ref.get.return_value = mock_doc
    mock_doc.exists = True
    mock_doc.to_dict.return_value = {"id": "test-123"}
    
    return {
        "db": mock_db,
        "collection": mock_collection,
        "doc_ref": mock_doc_ref,
        "doc": mock_doc
    }

@patch('module.firestore.client')
def test_with_firestore_mock(mock_client, mock_firestore_chain):
    mock_client.return_value = mock_firestore_chain["db"]
    
    result = function_using_firestore()
    
    assert result is not None
```

### Mocking Auth

```python
from unittest.mock import patch

@patch('firebase_admin.auth.verify_id_token')
def test_verify_token(mock_verify):
    """Test token verification."""
    mock_verify.return_value = {
        "uid": "user-123",
        "email": "test@example.com"
    }
    
    result = verify_user_token("fake-token")
    
    assert result["uid"] == "user-123"
    mock_verify.assert_called_once_with("fake-token")

@patch('firebase_admin.auth.get_user')
def test_get_user(mock_get_user):
    """Test getting user by UID."""
    mock_user = Mock()
    mock_user.uid = "user-123"
    mock_user.email = "test@example.com"
    mock_get_user.return_value = mock_user
    
    result = get_user_info("user-123")
    
    assert result.email == "test@example.com"
```

## Testing with Emulators

### Using Firebase Emulator Suite

```bash
# firebase.json
{
  "emulators": {
    "functions": {
      "port": 5001
    },
    "firestore": {
      "port": 8080
    },
    "auth": {
      "port": 9099
    }
  }
}
```

### Integration Test with Emulator

```python
# tests/integration/test_with_emulator.py
import pytest
import os
from firebase_admin import firestore, credentials, initialize_app

@pytest.fixture(scope="module")
def firebase_app():
    """Initialize Firebase with emulator."""
    # Set emulator environment variables
    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
    os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "localhost:9099"
    
    # Initialize app
    cred = credentials.Certificate("service-account-key.json")
    app = initialize_app(cred)
    
    yield app
    
    # Cleanup
    del os.environ["FIRESTORE_EMULATOR_HOST"]
    del os.environ["FIREBASE_AUTH_EMULATOR_HOST"]

@pytest.mark.integration
def test_full_flow_with_emulator(firebase_app):
    """Test complete flow with real emulator."""
    db = firestore.client()
    
    # Create test data
    doc_ref = db.collection("users").document("test-user")
    doc_ref.set({"name": "Test User", "email": "test@example.com"})
    
    # Verify data
    doc = doc_ref.get()
    assert doc.exists
    assert doc.to_dict()["name"] == "Test User"
    
    # Cleanup
    doc_ref.delete()
```

## Error Handling Patterns

### Standard Error Codes

```python
from firebase_functions import https_fn

def validate_and_handle_errors(req: https_fn.CallableRequest):
    """Standard error handling pattern."""
    # Authentication check
    if not req.auth:
        raise https_fn.HttpsError(
            code="unauthenticated",
            message="Authentication required"
        )
    
    # Permission check
    if not has_permission(req.auth.uid):
        raise https_fn.HttpsError(
            code="permission-denied",
            message="Insufficient permissions"
        )
    
    # Input validation
    if not req.data.get("required_field"):
        raise https_fn.HttpsError(
            code="invalid-argument",
            message="required_field is missing"
        )
    
    # Resource not found
    resource = get_resource(req.data["resource_id"])
    if not resource:
        raise https_fn.HttpsError(
            code="not-found",
            message="Resource not found"
        )
    
    # Rate limiting
    if is_rate_limited(req.auth.uid):
        raise https_fn.HttpsError(
            code="resource-exhausted",
            message="Rate limit exceeded"
        )
    
    # Internal errors
    try:
        result = process_request(req.data)
    except Exception as e:
        raise https_fn.HttpsError(
            code="internal",
            message="Internal server error"
        )
    
    return result
```

### Testing Error Codes

```python
class TestErrorHandling:
    """Test error handling patterns."""
    
    def test_unauthenticated_error(self, mock_unauth_request):
        with pytest.raises(https_fn.HttpsError) as exc:
            my_function(mock_unauth_request)
        assert exc.value.code == "unauthenticated"
    
    def test_permission_denied_error(self, mock_callable_request):
        with pytest.raises(https_fn.HttpsError) as exc:
            my_function(mock_callable_request)
        assert exc.value.code == "permission-denied"
    
    def test_invalid_argument_error(self, mock_callable_request):
        mock_callable_request.data = {}
        with pytest.raises(https_fn.HttpsError) as exc:
            my_function(mock_callable_request)
        assert exc.value.code == "invalid-argument"
```

## Security Testing

### Test Authentication Requirements

```python
@pytest.mark.security
class TestSecurityRequirements:
    """Security-focused tests."""
    
    def test_rejects_anonymous_users(self, mock_unauth_request):
        """Verify anonymous access is blocked."""
        with pytest.raises(https_fn.HttpsError) as exc:
            secured_function(mock_unauth_request)
        assert exc.value.code == "unauthenticated"
    
    @patch('services.auth_service.verify_admin')
    def test_admin_only_function(self, mock_verify, mock_callable_request):
        """Verify admin-only access."""
        mock_verify.return_value = False
        
        with pytest.raises(https_fn.HttpsError) as exc:
            admin_function(mock_callable_request)
        assert exc.value.code == "permission-denied"
    
    def test_validates_user_owns_resource(self, mock_callable_request):
        """Verify users can only access their own resources."""
        mock_callable_request.data = {"user_id": "other-user"}
        
        with pytest.raises(https_fn.HttpsError) as exc:
            get_user_data(mock_callable_request)
        assert exc.value.code == "permission-denied"
```

### Test Input Sanitization

```python
@pytest.mark.security
def test_sanitizes_sql_injection():
    """Test SQL injection prevention."""
    malicious_input = "'; DROP TABLE users; --"
    with pytest.raises(https_fn.HttpsError):
        process_input(malicious_input)

@pytest.mark.security
def test_validates_email_format():
    """Test email validation."""
    with pytest.raises(https_fn.HttpsError):
        create_user({"email": "not-an-email"})

@pytest.mark.security
def test_limits_string_length():
    """Test string length limits."""
    long_string = "x" * 10001
    with pytest.raises(https_fn.HttpsError):
        process_input(long_string)
```

## Best Practices

1. **Always test authentication**: Every callable function should have auth tests
2. **Mock Firebase Admin SDK**: Don't hit real services in unit tests
3. **Use emulators for integration tests**: Test real interactions safely
4. **Test all error paths**: Verify error codes and messages
5. **Security tests are mandatory**: Tag with `@pytest.mark.security`
6. **Test rate limiting**: Verify functions handle rate limits
7. **Isolate tests**: Each test should be independent
8. **Coverage target**: 100% for auth/security, 80%+ for business logic

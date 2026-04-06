# CipherMate Testing Guide

This document provides comprehensive information about the testing strategy and implementation for the CipherMate platform.

## Overview

CipherMate uses a multi-layered testing approach to ensure reliability, security, and functionality across all components:

- **Unit Tests**: Test individual components and functions in isolation
- **Integration Tests**: Test interactions between components and external services
- **End-to-End Tests**: Test complete user workflows from start to finish
- **Frontend Component Tests**: Test React components with user interactions

## Test Structure

### Backend Tests (`backend/tests/`)

```
backend/tests/
├── __init__.py
├── conftest.py                 # Pytest configuration and fixtures
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_ai_agent.py       # AI Agent Engine tests
│   ├── test_token_vault.py    # Token Vault Service tests
│   ├── test_auth.py           # Authentication tests
│   └── test_database_operations.py # Database model tests
├── integration/                # Integration tests
│   ├── __init__.py
│   └── test_auth0_integration.py # Auth0 and Token Vault integration
└── e2e/                       # End-to-end tests
    ├── __init__.py
    └── test_complete_workflows.py # Complete user workflows
```

### Frontend Tests (`frontend/src/components/__tests__/`)

```
frontend/src/components/__tests__/
├── ChatInterface.test.tsx      # Chat interface component tests
├── PermissionDashboard.test.tsx # Permission management tests
└── AuditDashboard.test.tsx     # Audit dashboard tests
```

## Running Tests

### Backend Tests

#### Prerequisites

```bash
cd backend
pip install -e ".[dev]"  # Install with dev dependencies
```

#### Run All Tests

```bash
# Using the test runner script
python run_tests.py

# Or using pytest directly
python -m pytest
```

#### Run Specific Test Types

```bash
# Unit tests only
python run_tests.py --type unit

# Integration tests only
python run_tests.py --type integration

# End-to-end tests only
python run_tests.py --type e2e

# With coverage report
python run_tests.py --coverage

# Verbose output
python run_tests.py --verbose

# Parallel execution
python run_tests.py --parallel 4
```

#### Run Individual Test Files

```bash
# Specific test file
python -m pytest tests/unit/test_ai_agent.py -v

# Specific test class
python -m pytest tests/unit/test_ai_agent.py::TestAIAgentEngine -v

# Specific test method
python -m pytest tests/unit/test_ai_agent.py::TestAIAgentEngine::test_analyze_intent_calendar_event -v
```

### Frontend Tests

#### Prerequisites

```bash
cd frontend
npm install
```

#### Run All Tests

```bash
# Using the test runner script
node run_tests.js

# Or using npm directly
npm test
```

#### Run Specific Test Types

```bash
# Unit tests only
node run_tests.js unit

# With coverage report
node run_tests.js --coverage

# Watch mode for development
node run_tests.js --watch

# Verbose output
node run_tests.js --verbose
```

#### Run Individual Test Files

```bash
# Specific test file
npm test -- ChatInterface.test.tsx

# Watch specific file
npm test -- --watch ChatInterface.test.tsx
```

## Test Coverage

### Backend Coverage Goals

- **Overall Coverage**: 80% minimum
- **Core Services**: 90% minimum (AI Agent, Token Vault, Auth)
- **API Endpoints**: 85% minimum
- **Database Models**: 95% minimum

### Frontend Coverage Goals

- **Components**: 80% minimum
- **Hooks**: 85% minimum
- **Utilities**: 90% minimum

### Generating Coverage Reports

#### Backend

```bash
# HTML coverage report
python run_tests.py --coverage

# View report
open htmlcov/index.html
```

#### Frontend

```bash
# Coverage report
npm test -- --coverage

# View report
open coverage/lcov-report/index.html
```

## Test Categories

### Unit Tests

#### Backend Unit Tests

**AI Agent Engine (`test_ai_agent.py`)**
- Intent analysis with different message types
- Permission requirement mapping
- Response generation
- Error handling for API failures
- Provider switching functionality

**Token Vault Service (`test_token_vault.py`)**
- Token storage and retrieval
- Token refresh mechanisms
- Token revocation
- Error handling for Auth0 API failures
- Concurrent token operations

**Authentication (`test_auth.py`)**
- JWT token validation
- JWKS retrieval and caching
- User session management
- Permission verification
- Security event handling

**Database Operations (`test_database_operations.py`)**
- CRUD operations for all models
- Relationship handling
- Data validation
- Query optimization
- Transaction handling

#### Frontend Unit Tests

**Chat Interface (`ChatInterface.test.tsx`)**
- Message sending and receiving
- Permission request dialogs
- Action confirmation flows
- Error handling and recovery
- Real-time updates

**Permission Dashboard (`PermissionDashboard.test.tsx`)**
- Service connection display
- OAuth flow initiation
- Permission revocation
- Scope visualization
- Status indicators

**Audit Dashboard (`AuditDashboard.test.tsx`)**
- Audit log display and filtering
- Security event management
- Data export functionality
- Real-time updates
- Timeline visualization

### Integration Tests

**Auth0 Integration (`test_auth0_integration.py`)**
- Complete OAuth flows for all services
- Token refresh workflows
- Token revocation processes
- JWT validation with real JWKS
- Error handling for Auth0 API issues

### End-to-End Tests

**Complete Workflows (`test_complete_workflows.py`)**
- Full user authentication flow
- Service permission granting
- AI-powered action execution
- Multi-service workflows
- Error recovery scenarios
- Audit trail verification

## Mocking Strategy

### Backend Mocking

#### External Services
- **Auth0 Management API**: Mock token operations
- **Google APIs**: Mock calendar, Gmail responses
- **GitHub API**: Mock repository operations
- **Slack API**: Mock messaging operations
- **Gemini AI**: Mock intent analysis responses

#### Database
- **SQLite in-memory**: For fast test execution
- **Test fixtures**: Predefined data sets
- **Transaction rollback**: Clean state between tests

### Frontend Mocking

#### API Calls
- **fetch**: Mock all HTTP requests
- **Auth0 hooks**: Mock authentication state
- **WebSocket**: Mock real-time connections

#### Browser APIs
- **localStorage**: Mock storage operations
- **URL.createObjectURL**: Mock file operations
- **window.location**: Mock navigation

## Test Data Management

### Fixtures and Factories

#### Backend Fixtures (`conftest.py`)
```python
@pytest.fixture
def mock_auth0_user():
    return {
        "sub": "auth0|test123",
        "email": "test@example.com",
        "name": "Test User"
    }

@pytest.fixture
def mock_token_vault_response():
    return {
        "access_token": "mock_token",
        "expires_in": 3600
    }
```

#### Frontend Test Data
```typescript
const mockPermissions = [
  {
    id: 1,
    service_name: 'google',
    scopes: ['calendar.events'],
    is_active: true
  }
];
```

### Test Database Setup

#### Backend Database
- Separate test database configuration
- Automatic schema creation and cleanup
- Isolated transactions for each test
- Seed data for complex scenarios

## Continuous Integration

### GitHub Actions Workflow

```yaml
name: Tests
on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -e ".[dev]"
      - name: Run tests
        run: |
          cd backend
          python run_tests.py --coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run tests
        run: |
          cd frontend
          node run_tests.js --coverage
```

## Performance Testing

### Load Testing
- **Artillery.js**: API endpoint load testing
- **Concurrent users**: Test with 100+ simultaneous users
- **Token Vault operations**: Stress test Auth0 integration
- **Database queries**: Performance under load

### Memory Testing
- **Memory leaks**: Long-running test scenarios
- **Resource cleanup**: Proper disposal of connections
- **Garbage collection**: Monitor memory usage patterns

## Security Testing

### Authentication Testing
- **Token validation**: Invalid and expired tokens
- **Permission boundaries**: Unauthorized access attempts
- **Session management**: Session hijacking prevention
- **Rate limiting**: Abuse prevention

### Input Validation Testing
- **SQL injection**: Database query safety
- **XSS prevention**: Input sanitization
- **CSRF protection**: Cross-site request forgery
- **Data validation**: Schema enforcement

## Debugging Tests

### Backend Debugging

#### Using pytest debugger
```bash
# Drop into debugger on failure
python -m pytest --pdb

# Drop into debugger on first failure
python -m pytest -x --pdb

# Specific test with debugger
python -m pytest tests/unit/test_ai_agent.py::TestAIAgentEngine::test_analyze_intent_calendar_event --pdb
```

#### Using VS Code
1. Set breakpoints in test files
2. Use "Python: Debug Tests" configuration
3. Select specific test to debug

### Frontend Debugging

#### Using Jest debugger
```bash
# Debug specific test
npm test -- --runInBand --no-cache ChatInterface.test.tsx
```

#### Using VS Code
1. Set breakpoints in test files
2. Use "Debug Jest Tests" configuration
3. Run specific test file

## Best Practices

### Test Writing Guidelines

1. **Descriptive Names**: Test names should clearly describe what is being tested
2. **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification
3. **Single Responsibility**: Each test should verify one specific behavior
4. **Independent Tests**: Tests should not depend on each other
5. **Realistic Data**: Use realistic test data that matches production scenarios

### Mocking Guidelines

1. **Mock External Dependencies**: Always mock external APIs and services
2. **Verify Interactions**: Assert that mocked functions are called correctly
3. **Realistic Responses**: Mock responses should match real API responses
4. **Error Scenarios**: Test both success and failure cases
5. **Performance**: Use mocks to ensure fast test execution

### Maintenance

1. **Regular Updates**: Keep test dependencies up to date
2. **Flaky Test Detection**: Monitor and fix unstable tests
3. **Coverage Monitoring**: Maintain high test coverage
4. **Documentation**: Keep test documentation current
5. **Refactoring**: Refactor tests when code changes

## Troubleshooting

### Common Issues

#### Backend Tests

**Database Connection Issues**
```bash
# Reset test database
rm test.db
python -m pytest tests/unit/test_database_operations.py
```

**Mock Import Errors**
```python
# Ensure proper import paths in mocks
with patch('app.core.ai_agent.genai') as mock_genai:
    # Test code here
```

#### Frontend Tests

**Module Resolution Issues**
```javascript
// Update Jest configuration in jest.config.js
moduleNameMapping: {
  '^@/(.*)$': '<rootDir>/src/$1',
}
```

**Async Test Issues**
```javascript
// Use waitFor for async operations
await waitFor(() => {
  expect(screen.getByText('Expected text')).toBeInTheDocument();
});
```

### Getting Help

1. **Check Test Logs**: Review detailed error messages
2. **Run Individual Tests**: Isolate failing tests
3. **Check Dependencies**: Ensure all test dependencies are installed
4. **Review Documentation**: Check this guide and test comments
5. **Ask Team**: Reach out to team members for assistance

## Contributing

When adding new features or fixing bugs:

1. **Write Tests First**: Follow TDD principles
2. **Update Existing Tests**: Modify tests when changing functionality
3. **Add Integration Tests**: Test interactions between components
4. **Document Test Cases**: Add comments explaining complex test scenarios
5. **Run Full Test Suite**: Ensure all tests pass before submitting PR

## Conclusion

This comprehensive testing strategy ensures that CipherMate maintains high quality, security, and reliability. Regular execution of these tests helps catch issues early and provides confidence in the platform's functionality.

For questions or improvements to the testing strategy, please reach out to the development team.
# Backend Unit Tests

This directory contains unit tests for the backend application components. The tests are implemented using Jest and following the dependency injection pattern with tsyringe.

## Test Structure

Tests are organized by the component type they test:

- `services/`: Tests for service classes
- `controllers/`: Tests for controller classes
- `middleware/`: Tests for middleware functions

## Test Implementation Guidelines

### Dependency Injection

The backend uses the tsyringe dependency injection container to manage dependencies. When writing tests, you should:

1. Create mock implementations of dependencies using `jest-mock-extended`
2. Inject these mocks into the component being tested
3. Set up expectations on the mock calls
4. Test the behavior of the component

### Example: Testing a Service

```typescript
import { mock, mockDeep, MockProxy } from 'jest-mock-extended';
import { YourService } from '../../services/your.service';
import { IDependency } from '../../services/dependency';

describe('YourService', () => {
  let mockDependency: MockProxy<IDependency>;
  let service: YourService;

  beforeEach(() => {
    // Create a mock of the dependency
    mockDependency = mockDeep<IDependency>();
    
    // Inject the mock into the service
    service = new YourService(mockDependency);
  });

  it('should do something with the dependency', async () => {
    // Set up expectations on the mock
    mockDependency.someMethod.mockResolvedValue('result');
    
    // Call the method being tested
    const result = await service.methodToTest();
    
    // Verify the dependency was called correctly
    expect(mockDependency.someMethod).toHaveBeenCalledWith(expect.any(Object));
    
    // Verify the result
    expect(result).toBe('expected result');
  });
});
```

### Testing External APIs

When testing components that interact with external APIs:

1. Mock the API client library
2. Set up expectations for the API calls
3. Test both success and error cases
4. Ensure error handling is working correctly

## Running Tests

To run all tests:

```bash
npm test
```

To run tests with coverage:

```bash
npm test -- --coverage
```

To run a specific test file:

```bash
npm test -- path/to/test-file.test.ts
```

## External Services Mocking Strategy

For external services such as DeepSeek API, we use the following strategy:

1. The service class accepts the external client in its constructor
2. In production, we inject the real client
3. In tests, we inject a mock client
4. Tests verify the interaction with the external service

This allows us to test the proper integration with external services without making actual API calls during testing. 
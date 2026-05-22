# Coding Standards and Best Practices

## General Principles

### Code Quality
- Write clean, readable, and maintainable code
- Follow the DRY (Don't Repeat Yourself) principle
- Use meaningful variable and function names
- Keep functions small and focused on a single responsibility
- Add comments for complex business logic

### TypeScript Standards
- Use strict TypeScript configuration
- Define interfaces for all data structures
- Use type annotations for function parameters and return types
- Avoid using `any` type - use proper typing instead
- Use union types and enums where appropriate

## Backend Coding Standards

### File Naming
- Use kebab-case for file names (e.g., `project-controller.ts`)
- Use PascalCase for class names
- Use camelCase for function and variable names
- Use UPPER_SNAKE_CASE for constants

### Express.js Patterns
- Use async/await instead of callbacks
- Implement proper error handling middleware
- Use express-validator for input validation
- Separate route handlers into controller functions
- Use middleware for common functionality (auth, logging, etc.)

### Database Patterns
- Use parameterized queries to prevent SQL injection
- Implement connection pooling
- Use transactions for multi-step operations
- Create database migration scripts
- Use proper indexing for performance

### Error Handling
```typescript
// Good: Proper error handling
try {
  const result = await someAsyncOperation();
  return result;
} catch (error) {
  logger.error('Operation failed:', error);
  throw new CustomError('Operation failed', 'OPERATION_ERROR');
}
```

### API Response Patterns
```typescript
// Consistent response format
const sendSuccess = (res: Response, data: any, message?: string) => {
  res.json({
    success: true,
    data,
    message
  });
};

const sendError = (res: Response, error: Error, statusCode: number = 500) => {
  res.status(statusCode).json({
    success: false,
    error: {
      message: error.message,
      code: error.name
    }
  });
};
```

## Frontend Coding Standards

### React Component Patterns
- Use functional components with hooks
- Keep components small and focused
- Use custom hooks for reusable logic
- Implement proper prop types with TypeScript interfaces
- Use React.memo for performance optimization when needed

### Component Structure
```typescript
interface ComponentProps {
  // Define all props with types
}

const Component: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // Hooks at the top
  const [state, setState] = useState();
  
  // Event handlers
  const handleClick = () => {
    // Handle click
  };
  
  // Render
  return (
    <div>
      {/* JSX content */}
    </div>
  );
};

export default Component;
```

### State Management
- Use useState for local component state
- Use useContext for shared state across components
- Use useReducer for complex state logic
- Use React Query for server state management

### Styling Guidelines
- Use Material-UI components consistently
- Create custom themes for consistent styling
- Use sx prop for component-specific styling
- Avoid inline styles unless necessary

## Testing Standards

### Unit Testing
- Write tests for all business logic functions
- Test both success and error scenarios
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

### Test Structure
```typescript
describe('Component/Function Name', () => {
  beforeEach(() => {
    // Setup
  });

  it('should do something when condition is met', () => {
    // Arrange
    const input = 'test input';
    
    // Act
    const result = functionUnderTest(input);
    
    // Assert
    expect(result).toBe('expected output');
  });
});
```

### API Testing
- Test all API endpoints
- Test validation rules
- Test error scenarios
- Use test database for integration tests

## Security Best Practices

### Input Validation
- Validate all user inputs on both client and server
- Sanitize data before database operations
- Use express-validator for server-side validation
- Implement client-side validation for better UX

### Database Security
- Use parameterized queries
- Implement proper access controls
- Use environment variables for sensitive data
- Regular security updates

### API Security
- Implement rate limiting
- Use CORS properly
- Add security headers with helmet
- Validate request origins

## Performance Guidelines

### Backend Performance
- Use database indexing appropriately
- Implement connection pooling
- Use caching where beneficial
- Optimize database queries

### Frontend Performance
- Use React.memo for expensive components
- Implement lazy loading for routes
- Optimize bundle size
- Use proper key props in lists

## Documentation Standards

### Code Documentation
- Document complex business logic
- Use JSDoc for function documentation
- Keep README files up to date
- Document API endpoints

### API Documentation
- Document all endpoints with examples
- Include request/response schemas
- Document error codes and messages
- Provide usage examples

## Environment and Configuration

### Environment Variables
- Use .env files for configuration
- Never commit sensitive data
- Use different configs for different environments
- Validate required environment variables on startup

### Logging
- Use structured logging
- Log errors with context
- Use appropriate log levels
- Don't log sensitive information
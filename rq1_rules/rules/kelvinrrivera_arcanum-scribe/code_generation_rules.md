# Code Generation Rules

This document defines the coding standards and patterns used throughout Arcanum Scribe, ensuring consistent implementation of Kiro specifications.

## Architecture Patterns

### Service Layer Organization
```
server/
├── index.ts              # Main API endpoints
├── llm-service.ts         # LLM providers and model management
├── image-service.ts       # Image generation with Fal.ai
├── pdf-service.ts         # Professional PDF generation
├── tier-service.ts        # User tiers and credit management
├── magic-credits-service.ts # Magic credits system
└── [feature]-service.ts   # Domain-specific services
```

### API Endpoint Patterns
```typescript
// Standard endpoint structure
app.post('/api/[domain]/[action]', authenticateToken, async (req, res) => {
  try {
    // 1. Extract and validate parameters
    const { param1, param2 } = req.body;
    const userId = (req as any).user.id;
    
    // 2. Check user permissions/credits
    const canPerform = await checkUserLimits(userId, action);
    if (!canPerform) {
      return res.status(403).json({ error: 'Insufficient credits' });
    }
    
    // 3. Execute business logic
    const result = await performAction(param1, param2, userId);
    
    // 4. Consume credits/update usage
    await updateUserUsage(userId, action, result);
    
    // 5. Return structured response
    res.json({
      ...result,
      metadata: { userId, timestamp: new Date() }
    });
    
  } catch (error) {
    console.error(`[${action.toUpperCase()}] ERROR:`, error);
    res.status(500).json({ 
      error: error instanceof Error ? error.message : 'Internal server error' 
    });
  }
});
```

## Service Implementation Standards

### LLM Service Pattern
```typescript
class LLMService {
  // Use provider priority system with fallback
  async generateText(prompt: string, systemPrompt: string, options: any) {
    const providers = await this.getActiveProviders();
    
    for (const provider of providers) {
      try {
        return await this.callProvider(provider, prompt, systemPrompt, options);
      } catch (error) {
        console.log(`Failed with ${provider.name}:`, error);
        continue; // Try next provider
      }
    }
    
    throw new Error('All LLM providers failed');
  }
}
```

### Database Integration Pattern
```typescript
// Use transactions for multi-table operations
async function createAdventure(adventureData: AdventureData) {
  return await transaction(async (client) => {
    const adventure = await client.query(
      'INSERT INTO adventures (...) VALUES (...) RETURNING *',
      [...values]
    );
    
    await client.query(
      'UPDATE user_usage SET ... WHERE user_id = $1',
      [userId]
    );
    
    return adventure.rows[0];
  });
}
```

## Frontend Component Standards

### Component Structure
```typescript
// Standard component pattern
interface ComponentProps {
  // Props with explicit types
  data: AdventureData;
  onAction: (action: string) => void;
  loading?: boolean;
}

export function Component({ data, onAction, loading = false }: ComponentProps) {
  // 1. Hooks and state
  const [state, setState] = useState<StateType>(initialState);
  
  // 2. Effects and data fetching
  useEffect(() => {
    // Side effects
  }, [dependencies]);
  
  // 3. Event handlers
  const handleAction = useCallback((action: string) => {
    onAction(action);
  }, [onAction]);
  
  // 4. Render logic
  return (
    <div className="component-container">
      {/* JSX with consistent styling */}
    </div>
  );
}
```

### State Management Pattern
```typescript
// Use React Query for server state
const { data: adventure, error, isLoading } = useQuery({
  queryKey: ['adventure', adventureId],
  queryFn: () => api.getAdventure(adventureId),
  staleTime: 5 * 60 * 1000, // 5 minutes
});

// Use useState for local component state
const [formData, setFormData] = useState<FormData>({});
```

## Error Handling Standards

### Server Error Pattern
```typescript
class ServiceError extends Error {
  constructor(
    message: string, 
    public code: string, 
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'ServiceError';
  }
}

// Usage
throw new ServiceError('Invalid user tier', 'INVALID_TIER', 403);
```

### Frontend Error Handling
```typescript
// Consistent error boundaries and user feedback
const { mutate: generateAdventure, error, isLoading } = useMutation({
  mutationFn: api.generateAdventure,
  onError: (error) => {
    toast.error(error.message || 'Generation failed');
  },
  onSuccess: (data) => {
    toast.success('Adventure generated successfully!');
    navigate(`/adventure/${data.id}`);
  }
});
```

## Naming Conventions

### File Naming
- **Services**: `kebab-case-service.ts`
- **Components**: `PascalCase.tsx`  
- **Hooks**: `use-camel-case.ts`
- **Utils**: `camel-case-utils.ts`

### Variable Naming
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Functions**: `camelCase`
- **Classes**: `PascalCase`
- **Types/Interfaces**: `PascalCase`

### Database Naming
- **Tables**: `snake_case` (e.g., `user_adventures`)
- **Columns**: `snake_case` (e.g., `created_at`)
- **Indexes**: `idx_table_column`

## Kiro Integration Patterns

### Specification Mapping
```typescript
// Map Kiro specs to implementation
interface SpecImplementation {
  specPath: string;           // .kiro/specs/[name]/
  serviceModule: string;      // server/[feature]-service.ts
  apiEndpoints: string[];     // /api/[endpoints]
  frontendComponents: string[]; // src/components/[components]
}

const SPEC_MAPPINGS: SpecImplementation[] = [
  {
    specPath: '.kiro/specs/professional-mode-integration/',
    serviceModule: 'server/professional-layout-engine.ts',
    apiEndpoints: ['/api/generate-adventure'],
    frontendComponents: ['src/components/professional/']
  }
];
```

### Hook Implementation
```typescript
// Hooks should follow this pattern
export async function executeHook(specName: string, parameters: any) {
  console.log(`🎯 Kiro Hook: ${hookName} executing...`);
  
  // 1. Validate inputs
  validateParameters(parameters);
  
  // 2. Execute main logic
  const result = await performHookAction(specName, parameters);
  
  // 3. Save artifacts
  const artifactPath = await saveArtifact(result);
  
  // 4. Generate report
  console.log(`✅ Hook completed: ${artifactPath}`);
  return { result, artifactPath };
}
```

## Quality Gates

### Pre-commit Checks
1. **TypeScript**: `npx tsc --noEmit`
2. **Linting**: `npm run lint`
3. **Tests**: `npm test`
4. **Security**: `npm audit`

### Code Review Requirements
- All API endpoints must have error handling
- Database operations must use transactions
- Frontend components must handle loading states
- Services must include proper logging

### Performance Standards
- API responses < 200ms (excluding LLM calls)
- Frontend initial load < 2s
- Database queries optimized with proper indexes
- Image generation handled asynchronously

---

*These rules ensure consistency across the codebase and alignment with Kiro specifications.*
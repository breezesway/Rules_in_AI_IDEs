# ParliQ Development Guidelines

## Project Overview
ParliQ is a conversational AI interface for exploring UK parliamentary discourse. The tagline is "Understand Parliament, one question at a time."

## Core Principles

### User Experience
- **Warm, Teacher-like Tone**: All messaging should be supportive, educational, and approachable
- **Accessibility First**: WCAG 2.2 AA compliance is mandatory
- **Mobile Optimized**: Ensure 44px+ tap targets, horizontal scrolling chips, sticky input
- **Progressive Disclosure**: Start simple with example chips, then offer follow-up suggestions

### Technical Standards
- **TypeScript Strict Mode**: All code must pass strict type checking
- **Component Composition**: Prefer small, focused components over large monoliths
- **Semantic HTML**: Use proper HTML elements and ARIA labels
- **Performance**: Optimize for mobile devices and slower connections

### Content Guidelines
- **Parliamentary Focus**: Content should relate to UK Parliament, MPs, debates, and policies
- **Citation Precision**: Always aim for sentence-level timestamp accuracy
- **Guardrails**: Politely redirect legal advice and voting guidance to official resources
- **Educational Tone**: Explain concepts clearly without being condescending

## File Organization
```
src/
├── components/
│   └── Chat/           # All chat-related UI components
├── hooks/              # React hooks for state management
├── services/           # API clients and external services
├── types/              # TypeScript type definitions
├── utils/              # Pure utility functions
└── App.tsx             # Root application component
```

## Commit Message Format
Use conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `chore:` for maintenance tasks
- `docs:` for documentation updates
- `style:` for formatting changes
- `refactor:` for code restructuring

## Testing Checklist
- [ ] Keyboard navigation works throughout
- [ ] Screen reader compatibility verified
- [ ] Mobile responsive on various screen sizes
- [ ] High contrast mode support
- [ ] Reduced motion preferences respected
- [ ] All interactive elements have 44px+ minimum size
- [ ] Focus indicators are clearly visible

## Backend Integration
- Request `citationPrecision: 'sentence'` in chat API calls
- Handle guardrail responses with resource cards
- Generate contextual follow-up suggestions based on response content
- Maintain conversation history for context
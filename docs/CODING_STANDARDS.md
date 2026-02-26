# Coding Standards

- Type hints mandatory
- Pydantic models for DTOs
- Small, single-responsibility classes
- No business logic inside infrastructure
- Test every core component
- Avoid hard-coded values
  
# Clean Code Guidelines

## Naming
- Clear and descriptive names
- Avoid abbreviations

## Functions
- Small and focused
- Max 30 lines recommended

## Classes
- Single responsibility
- Inject dependencies via constructor

## Errors
- Use custom exceptions in domain
- Do not expose infrastructure errors directly

## Testing
- Core logic must be unit tested
- Infrastructure must be integration tested

## Logging
- No print statements
- Use structured logging
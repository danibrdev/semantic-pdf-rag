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

## Git & Version Control
- All commits MUST follow the [Semantic Commits](https://www.conventionalcommits.org/) convention.
- **Format**: `<type>(<scope>): <subject>`
- **Types**:
  - `feat`: A new feature (e.g., `feat(ingest): add pdf chunking`)
  - `fix`: A bug fix (e.g., `fix(vector-store): resolve connection timeout`)
  - `docs`: Documentation changes (e.g., `docs: translate readme to pt-br`)
  - `style`: Formatting, missing semicolons, etc.
  - `refactor`: Refactoring production code (e.g., `refactor(domain): extract interface`)
  - `test`: Adding missing tests, refactoring tests
  - `chore`: Updating dependencies, build tasks, gitignore, etc.
  - `perf`: A code change that improves performance
- Include a clear description of *why* the change was made in the commit body when necessary.
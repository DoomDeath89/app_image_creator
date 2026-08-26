# AppImage Builder Constitution

## Core Principles

### I. UI-First Architecture
Every feature starts as a UI component. Business logic MUST be decoupled from tkinter widgets via services and mediator pattern. Tabs are pure UI; services handle all logic.

### II. Thread Safety (NON-NEGOTIABLE)
All subprocess executions MUST run in background threads. The main tkinter thread MUST NEVER block. UI updates from threads MUST use `frame.after()` for thread-safe scheduling.

### III. Graceful Degradation
Build failures MUST clean up partial artifacts (AppDir). Cancel operations MUST terminate running processes and restore clean state. Error messages MUST be user-friendly with actionable guidance.

### IV. Test-First
Tests written before implementation. All UI components must be testable with real tkinter widgets (not mocks). Mocks ONLY for external dependencies (subprocess, file dialogs).

### V. Mediator Pattern
Cross-tab communication MUST go through the Mediator. Tabs MUST NOT reference each other directly. The Mediator orchestrates data flow between Build, Validator, and Dependencies tabs.

## Technology Stack

- **Language**: Python 3.8+
- **UI Framework**: tkinter with ttk widgets
- **Design Pattern**: Mediator (tabs) + Service Layer (business logic)
- **Build Tool**: linuxdeploy (AppImage creation)
- **Testing**: pytest with unittest mocks
- **Architecture**: Tab-based GUI with 3 panels (Build, Validator, Dependencies)

## Git Workflow (GitFlow)

### Branches

- **main**: Production-ready code. Only receives merges from `release/*` and `hotfix/*` branches.
- **develop**: Integration branch. All feature branches merge here first.
- **feature/***: New features. Branch from `develop`, merge back to `develop`.
- **release/***: Release preparation. Branch from `develop`, merge to `main` and `develop`.
- **hotfix/***: Emergency fixes. Branch from `main`, merge to `main` and `develop`.

### Branch Naming

```
feature/<ticket>-<short-description>
release/<version>
hotfix/<ticket>-<short-description>
```

Examples:
- `feature/001-threading-build`
- `release/1.1.0`
- `hotfix/002-fix-json-parsing`

### Workflow Steps

1. **Feature Development**
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/001-threading-build
   # ... work ...
   git add .
   git commit -m "feat: description"
   git checkout develop
   git merge --no-ff feature/001-threading-build
   git branch -d feature/001-threading-build
   ```

2. **Release**
   ```bash
   git checkout develop
   git checkout -b release/1.1.0
   # ... bump version, final fixes ...
   git checkout main
   git merge --no-ff release/1.1.0
   git tag -a v1.1.0 -m "Release 1.1.0"
   git checkout develop
   git merge --no-ff release/1.1.0
   git branch -d release/1.1.0
   ```

3. **Hotfix**
   ```bash
   git checkout main
   git checkout -b hotfix/002-fix-json-parsing
   # ... fix ...
   git checkout main
   git merge --no-ff hotfix/002-fix-json-parsing
   git tag -a v1.1.1 -m "Hotfix 1.1.1"
   git checkout develop
   git merge --no-ff hotfix/002-fix-json-parsing
   git branch -d hotfix/002-fix-json-parsing
   ```

### Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## Quality Gates

- All tests must pass before merge
- No blocking calls on main thread
- All subprocess errors must be handled
- Config save/load must handle corrupted JSON
- Build process must be cancellable at any point
- Feature branches must have descriptive commit messages
- Release branches must update CHANGELOG.md

## Governance

Constitution supersedes all other practices. All code changes must verify compliance with these principles. Complexity must be justified by specific user needs. GitFlow must be followed for all changes.

**Version**: 1.1.0 | **Ratified**: 2026-08-26 | **Last Amended**: 2026-08-26

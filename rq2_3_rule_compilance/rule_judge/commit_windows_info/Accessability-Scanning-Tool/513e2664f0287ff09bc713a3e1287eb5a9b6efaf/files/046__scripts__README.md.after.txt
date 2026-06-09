# Version Management Scripts

This directory contains scripts for automated version management and changelog
maintenance.

## Scripts Overview

### `version-bump.js`

Automatically bumps the version number, updates the changelog, and creates git
tags.

**Usage:**

```bash
npm run version:patch   # 2.1.0 → 2.1.1
npm run version:minor   # 2.1.0 → 2.2.0
npm run version:major   # 2.1.0 → 3.0.0
```

**What it does:**

- Updates version in `package.json`
- Adds new version section to `CHANGELOG.md`
- Creates git commit and tag
- Provides template for changelog entries

### `changelog-add.js`

Adds entries to the changelog under the `[Unreleased]` section.

**Usage:**

```bash
npm run changelog:add
```

**Interactive prompts:**

- Section: Added, Changed, Fixed, etc.
- Entry: Description of the change

### `validate-versions.js`

Validates version consistency across all files and detects potential hardcoded
version references.

**Usage:**

```bash
npm run version:validate       # Generate detailed version report
node scripts/validate-versions.js --help  # Show help
```

**What it does:**

- Checks version consistency between package.json and package-lock.json
- Validates version examples in documentation
- Searches for potential hardcoded version references
- Provides detailed report with issues and warnings

### `prepare-release.js`

Validates the project before release and generates release notes.

**Usage:**

```bash
npm run prepare
```

**Validation checks:**

- Git working directory is clean
- Changelog includes current version
- TypeScript compilation passes
- Linting passes
- Tests pass
- Build succeeds

### `pre-commit-hook.js`

Ensures code quality and version consistency before commits.

**Usage:**

```bash
# Install as git hook
echo "node scripts/pre-commit-hook.js" > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

**Pre-commit checks:**

- **Version consistency** - Validates all version references are synchronized
- **Changelog validation** - Ensures version changes are documented in changelog
- **Code formatting** - Runs Prettier on staged files and re-stages them
- **Code quality** - Runs ESLint on staged files

**Enhanced with version validation:**

- Automatically detects version inconsistencies
- Prevents commits with mismatched versions
- Provides helpful error messages and fix suggestions

## Workflow

### For Bug Fixes (Patch)

```bash
# 1. Make your changes
# 2. Add changelog entry
npm run changelog:add
# Select: Fixed
# Enter: "Fixed issue with URL caching"

# 3. Bump version
npm run version:patch

# 4. Prepare release
npm run prepare
```

### For New Features (Minor)

```bash
# 1. Make your changes
# 2. Add changelog entry
npm run changelog:add
# Select: Added
# Enter: "Added new performance monitoring features"

# 3. Bump version
npm run version:minor

# 4. Prepare release
npm run prepare
```

### For Breaking Changes (Major)

```bash
# 1. Make your changes
# 2. Add changelog entry
npm run changelog:add
# Select: Changed
# Enter: "BREAKING: Changed API interface for accessibility testing"

# 3. Bump version
npm run version:major

# 4. Prepare release
npm run prepare
```

## Changelog Format

The changelog follows [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [Unreleased]

### Added

- New features

### Changed

- Changes to existing features

### Deprecated

- Features that will be removed

### Removed

- Features that were removed

### Fixed

- Bug fixes

### Security

- Security improvements

## [2.0.1] - 2024-12-19

### Fixed

- Fixed TypeScript compilation errors
- Fixed CLI URL caching issues
```

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (X.Y.0): New features, backward compatible
- **PATCH** (X.Y.Z): Bug fixes, backward compatible

## Git Integration

The version management system integrates with git:

```bash
# Version bump creates:
git tag v2.1.2
git commit -m "chore: bump version to 2.1.2"

# Push tags to remote:
git push origin main --tags
```

## GitHub Integration

After version bump and release preparation:

1. Push changes: `git push origin main --tags`
2. Create GitHub release with generated notes
3. Publish to npm: `npm publish`

## Automation

The scripts can be integrated into CI/CD pipelines:

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run prepare
      - run: npm publish
```

## Troubleshooting

### Git hooks not working

```bash
chmod +x .git/hooks/pre-commit
```

### Changelog format issues

- Ensure proper markdown formatting
- Check for consistent indentation
- Use standard section headers

### Version conflicts

- Ensure git working directory is clean
- Check for merge conflicts in package.json
- Verify changelog format is correct

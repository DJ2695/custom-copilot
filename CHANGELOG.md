# Changelog

## [0.2.0] - 2026-02-01

### Major Refactoring - Professional Package with Private Repo Support

#### Breaking Changes

- **Package renamed:** `copilot` → `custom-copilot`
- **Module renamed:** `cc` → `custom_copilot`
- **Bundle resource types renamed:**
  - `"reference"` → `"custom-copilot"`
  - `"inline"` → `"bundle"`
- Old types still work with deprecation warnings for backward compatibility

#### Added

- **Private repository support**
  - `cuco source add <name> <type> <url>` - Add custom source repositories
  - `cuco source list` - List configured sources
  - `cuco source remove <name>` - Remove a source
  - Configuration stored in `~/.cuco/config.json` or `.cuco-config.json`
  
- **Future-ready resource types**
  - `"github"` type for 3rd party GitHub repositories (placeholder)
  
- **Professional documentation**
  - Clean README with badges and clear structure
  - Updated migration guide
  - Reorganized development docs into docs/ folder

#### Changed

- All imports updated from `cc` to `custom_copilot`
- CLI entry point updated in pyproject.toml
- Bundle manifests updated to use new type names
- Templates updated with new resource types

#### Fixed

- Package name conflicts resolved by using unique name
- Import paths now reflect actual package structure

---

## [0.1.0] - Previous Version

### Initial Release

- Basic CLI for managing GitHub Copilot customizations
- Support for agents, prompts, skills, instructions
- Bundle system for pre-configured combinations
- Template system for creating new resources
- Sync functionality
- Flat directory structure (no version folders)

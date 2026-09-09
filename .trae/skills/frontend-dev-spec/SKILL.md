---
name: "frontend-dev-spec"
description: "Enforces frontend development conventions for React+TypeScript+Vite+Ant Design+Tailwind CSS projects. Invoke when writing or modifying frontend code (tsx, ts, css files) in the frontend directory, creating pages, components, or utility functions."
---

# Frontend Development Spec

This skill enforces the frontend development conventions defined in `frontend/docs/前端开发规范.md`. All generated tsx, ts, and css code must strictly follow these rules.

## Core Constraints

1. **Tech Stack**: React + TypeScript + Vite + Ant Design + Tailwind CSS. Ignore any Vue-related rules.
2. **File Naming & Structure**: Follow the naming conventions below strictly.
3. **Git Commit**: Format is `type(scope): description` with a space after the colon.
4. **Type Safety**: No `any` abuse, avoid `@ts-ignore`.
5. **Assets**: Strictly distinguish between `src/assets` (imported) and `public` (direct path access).

## 1. File & Directory Naming

1. **Directories**: lowercase kebab-case (e.g., `agent-manage`, `components`, `hooks`, `utils`). Pages use kebab-case.
2. **React Components**: PascalCase (e.g., `AgentChat.tsx`, `LoginPage.tsx`). Exported component name must match filename.
3. **TS utils/api/hooks**: lowerCamelCase (e.g., `useAgentChat.ts`, `agentApi.ts`).
4. **Assets (images, svg)**: kebab-case (e.g., `login-bg.png`).
5. No pinyin-English mixing, no meaningless abbreviations.

## 2. TypeScript / JS

1. Variables, functions, parameters: lowerCamelCase. Functions start with verbs: `get/add/update/delete/detail`.
2. Constants: UPPER_SNAKE_CASE (e.g., `MAX_UPLOAD_SIZE`).
3. Indentation: 2 spaces. Blank line between logic blocks. Always use braces for `if/for/while`.
4. Prefer single quotes. Use `let/const`, no `var`. Prefer `async-await` over nested callbacks.
5. No direct `xxx === undefined` checks. Use `typeof xxx === 'undefined'`.
6. Extract complex logic into functions. Max 3 levels of nesting. No overly long ternary expressions.
7. Remove `console.log` debug statements before committing.

## 3. CSS / Tailwind

1. Custom CSS class names: kebab-case. No ID selectors for styling.
2. Use property shorthand. Omit units after 0 (write `0`, not `0px`).
3. Use `@apply` reasonably. Write native CSS for gradients, special shadows, etc.
4. React inline styles: use JS camelCase (e.g., `backgroundImage`, `backgroundSize`).

## 4. Project Directory Structure (Vite-React)

```
src
├── api        # API requests, split by business, methods commented, match backend controllers
├── assets     # Images, fonts, global styles; business resources imported via import
├── components # Public common components (PascalCase); module-local components in pages/<module>/components
├── constants  # Constants, enums
├── hooks      # Custom hooks (useXxx)
├── layouts    # Layout components
├── pages      # Pages, each page in its own folder
├── router     # Route config, paths in kebab-case, lazy loading
├── utils      # Utility functions
public         # favicon, large static assets, accessed via /path, not imported
```

## 5. Git Commit Convention (husky+commitlint)

Format: `type(scope): description` (space after colon required)

Types:
- `feat`: new features
- `fix`: bug fixes
- `chore`: engineering config/dependencies
- `docs`: documentation
- `refactor`: refactoring
- `style`: formatting

Example: `chore: 配置@别名映射src路径`

## 6. React Coding Practices

1. Define explicit TS types for Props. No `any` abuse. Avoid `@ts-ignore`.
2. Split components. Extract complex calculations to `useMemo`, event handlers to separate functions.
3. Prefer controlled components. Avoid direct DOM manipulation.
4. Import order: third-party libs → components → hooks → utils → static assets.

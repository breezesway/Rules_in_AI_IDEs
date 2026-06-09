# ESLint 설정 완료 문서

## 📝 개발 완료 결과

### ✅ 설치된 패키지

- `eslint` (v9.29.0)
- `@eslint/js` (v9.29.0)
- `@typescript-eslint/eslint-plugin` (v8.34.0)
- `@typescript-eslint/parser` (v8.34.0)
- `eslint-plugin-react` (v7.37.5)
- `eslint-plugin-react-hooks` (v5.2.0)
- `eslint-plugin-import` (v2.31.0)
- `eslint-config-prettier` (v10.1.5)
- `eslint-import-resolver-typescript` (v4.4.3)
- `prettier` (v3.5.3)
- `prettier-plugin-tailwindcss` (v0.6.12)
- `globals` (v16.2.0)

### 🔧 설정 파일

#### `eslint.config.js` (Flat Config)

```js
import js from '@eslint/js';
import tsPlugin from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import reactPlugin from 'eslint-plugin-react';
import reactHooksPlugin from 'eslint-plugin-react-hooks';
import importPlugin from 'eslint-plugin-import';
import prettierConfig from 'eslint-config-prettier/flat';
import globals from 'globals';

export default [
  {
    ignores: ['dist', 'build', '**/*.gen.ts', '**/*.d.ts', '**/node_modules/**', '**/.*/**'],
  },
  {
    files: ['**/*.{js,jsx,ts,tsx}'],
    languageOptions: {
      parser: tsParser,
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
      react: reactPlugin,
      'react-hooks': reactHooksPlugin,
      import: importPlugin,
    },
    rules: {
      ...js.configs.recommended.rules,
      ...tsPlugin.configs.recommended.rules,
      ...reactPlugin.configs.recommended.rules,
      ...reactHooksPlugin.configs.recommended.rules,
      // import/order 설정
      'import/order': [
        'warn',
        {
          groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index', 'object', 'type'],
          pathGroups: [
            { pattern: 'react', group: 'external', position: 'before' },
            { pattern: '@/**', group: 'internal' },
          ],
          pathGroupsExcludedImportTypes: ['builtin'],
          alphabetize: { order: 'asc', caseInsensitive: true },
          'newlines-between': 'always',
        },
      ],
      // react
      'react/react-in-jsx-scope': 'off',
      'react/jsx-pascal-case': 'warn',
      // typescript
      '@typescript-eslint/no-unused-vars': 'warn',
      '@typescript-eslint/no-shadow': 'warn',
      // 기타
      'no-console': 'warn',
      'no-unused-vars': 'warn',
    },
    settings: {
      react: { version: 'detect' },
      'import/resolver': {
        typescript: {
          project: './tsconfig.json',
        },
      },
    },
  },
  prettierConfig, // 마지막에 위치해야 prettier와 충돌 방지
];
```

#### `.vscode/settings.json`

```json
{
  "eslint.experimental.useFlatConfig": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

### 📦 package.json 스크립트

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix"
  }
}
```

### 🚨 해결한 문제들

#### 1. TailwindCSS v4 호환성 문제

- **문제**: `eslint-plugin-tailwindcss`가 TailwindCSS v3.4.0만 지원
- **해결**: TailwindCSS ESLint 플러그인 제거 (Prettier로 클래스 정렬 처리)

#### 2. TypeScript import resolver 문제

- **문제**: `import/order`에서 typescript resolver 오류
- **해결**: `eslint-import-resolver-typescript` 패키지 추가

#### 3. React JSX 인코딩 문제

- **문제**: `react/no-unescaped-entities` 오류
- **해결**: JSX 내 따옴표 문자 수정

### ✨ 주요 특징

1. **2025년 표준 Flat Config 방식** 적용
2. **TypeScript + React + TailwindCSS + Prettier** 완벽 지원
3. **Import 정렬** 자동화 (그룹별, 알파벳순)
4. **저장 시 자동 포맷팅** 및 **ESLint 자동 수정**
5. **TDD 개발 환경** 준비 완료

### 🎯 다음 단계

- TDD 기반 테스트 코드 작성 시작
- Vitest + Testing Library + MSW 환경에서 테스트 개발
- 기능 구현 전 테스트 코드 우선 작성

---

**📅 작성일**: 2025년 1월 14일  
**🔧 ESLint 버전**: 9.29.0 (Flat Config)  
**⚛️ React 버전**: 19.1.0  
**🎨 TailwindCSS 버전**: 4.1.10

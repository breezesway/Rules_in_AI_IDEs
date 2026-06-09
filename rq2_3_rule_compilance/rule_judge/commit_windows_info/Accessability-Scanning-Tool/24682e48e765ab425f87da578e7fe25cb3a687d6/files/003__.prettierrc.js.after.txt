module.exports = {
  // Print width - line length that prettier will wrap on
  printWidth: 100,

  // Tab width - number of spaces per indentation level
  tabWidth: 2,

  // Use tabs instead of spaces
  useTabs: false,

  // Semicolons - print semicolons at the end of statements
  semi: true,

  // Quotes - use single quotes instead of double quotes
  singleQuote: true,

  // Quote props - only quote object properties when needed
  quoteProps: 'as-needed',

  // JSX quotes - use single quotes in JSX
  jsxSingleQuote: true,

  // Trailing commas - print trailing commas in multi-line structures
  trailingComma: 'es5',

  // Bracket spacing - print spaces between brackets in object literals
  bracketSpacing: true,

  // Bracket same line - put the > of a multi-line element on the same line
  bracketSameLine: false,

  // Arrow function parentheses - include parentheses around sole arrow function parameter
  arrowParens: 'avoid',

  // Range - format the entire file
  rangeStart: 0,
  rangeEnd: Infinity,

  // Parser - auto-detect parser based on file extension
  // parser: undefined,

  // File path - path to file being formatted
  // filepath: undefined,

  // Require pragma - require a pragma comment to format
  requirePragma: false,

  // Insert pragma - insert a pragma comment at the top of files
  insertPragma: false,

  // Prose wrap - wrap prose text
  proseWrap: 'preserve',

  // HTML whitespace sensitivity
  htmlWhitespaceSensitivity: 'css',

  // Vue script and style indentation
  vueIndentScriptAndStyle: false,

  // End of line - line ending style
  endOfLine: 'lf',

  // Embedded language formatting
  embeddedLanguageFormatting: 'auto',

  // Single attribute per line - force single attribute per line in HTML, Vue, and JSX
  singleAttributePerLine: false,

  // Overrides for specific file types
  overrides: [
    {
      files: '*.json',
      options: {
        printWidth: 80,
        tabWidth: 2,
      },
    },
    {
      files: '*.md',
      options: {
        printWidth: 80,
        proseWrap: 'always',
        tabWidth: 2,
      },
    },
    {
      files: '*.yaml',
      options: {
        tabWidth: 2,
      },
    },
    {
      files: '*.yml',
      options: {
        tabWidth: 2,
      },
    },
  ],
};

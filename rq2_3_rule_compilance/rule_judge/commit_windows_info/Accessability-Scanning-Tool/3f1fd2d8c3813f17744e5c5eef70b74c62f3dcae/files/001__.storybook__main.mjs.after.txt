import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/** @type { import('@storybook/html-webpack5').StorybookConfig } */
const config = {
  stories: [
    "../stories/**/*.mdx",
    "../stories/**/*.stories.@(js|jsx|mjs|ts|tsx)"
  ],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-a11y",
    "@storybook/addon-interactions",
    "@storybook/addon-viewport",
    "@storybook/addon-controls"
  ],
  framework: {
    name: "@storybook/html-webpack5",
    options: {}
  },
  docs: {
    autodocs: "tag"
  },
  typescript: {
    check: false,
    reactDocgen: false,
  },
  core: {
    builder: '@storybook/builder-webpack5'
  },
  webpackFinal: async (config) => {
    // Configure TypeScript handling
    config.module.rules.push({
      test: /\.tsx?$/,
      use: [
        {
          loader: resolve(__dirname, '../node_modules/ts-loader'),
          options: {
            transpileOnly: true,
            configFile: resolve(__dirname, '../tsconfig.json'),
          },
        },
      ],
    });

    // Resolve TypeScript extensions
    config.resolve.extensions.push('.ts', '.tsx');

    return config;
  },
};

export default config; 
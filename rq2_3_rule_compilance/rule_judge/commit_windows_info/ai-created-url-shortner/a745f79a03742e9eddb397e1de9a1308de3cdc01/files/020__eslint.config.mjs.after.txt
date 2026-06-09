// @ts-check
import withNuxt from "./.nuxt/eslint.config.mjs";
import customRules from "./eslint-rules/index.js";

export default withNuxt(
  // Your custom configs here
  {
    ignores: ["app/components/ui/**"],
    plugins: {
      "nuxt-custom": customRules,
    },
    rules: {
      "nuxt-custom/nuxt-data-fetching": "error",
    },
  }
);

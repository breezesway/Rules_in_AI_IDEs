import tailwindcss from "@tailwindcss/vite";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-05-15",
  future: {
    compatibilityVersion: 4,
  },
  devtools: { enabled: true },
  css: ["~/assets/css/tailwind.css"],
  vite: {
    plugins: [tailwindcss()],
  },
  modules: [
    "@nuxt/eslint",
    "shadcn-nuxt",
    "@nuxt/test-utils/module",
    "@nuxt/icon",
    "@nuxt/image",
    "@vueuse/nuxt",
  ],
  components: [
    {
      path: "@/components",
      pathPrefix: false,
    },
  ],
  shadcn: {
    /**
     * Prefix for all the imported component
     */
    prefix: "ui",
    /**
     * Directory that the component lives in.
     * @default "./components/ui"
     */
    componentDir: "./app/components/ui",
  },
  nitro: {
    experimental: {
      openAPI: true,
    },
    openAPI: {
      production: "prerender",
      meta: {
        title: "My Awesome Project",
        description: "This might become the next big thing.",
        version: "1.0",
      },
    },
  },
});
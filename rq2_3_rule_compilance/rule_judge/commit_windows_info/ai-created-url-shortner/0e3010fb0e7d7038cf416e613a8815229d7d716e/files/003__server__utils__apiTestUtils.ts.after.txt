export const $vitestFetch = $fetch.create({
  baseURL: process.env.NUXT_APP_URL,
  headers: {
    "X-Test-Env": "true",
  },
});

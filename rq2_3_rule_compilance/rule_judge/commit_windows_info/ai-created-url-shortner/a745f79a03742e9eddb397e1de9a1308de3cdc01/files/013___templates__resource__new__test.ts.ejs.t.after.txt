---
to: tests/e2e/api-<%= plural %>.spec.ts
---
import { test, expect } from '@nuxt/test-utils/playwright'

test.describe('/<%= plural %> API endpoints', () => {
  let _created<%= Name %>Id: string

  test('GET /<%= plural %> - should list <%= plural %>', async ({ page, goto }) => {
    await goto('/', { waitUntil: 'hydration' })

    const response = await page.request.get('/api/<%= plural %>')
    expect(response.status()).toBe(200)
    // TODO: Add tests for the response data
  })

  // TODO: Add tests for all the endpoints

}) 
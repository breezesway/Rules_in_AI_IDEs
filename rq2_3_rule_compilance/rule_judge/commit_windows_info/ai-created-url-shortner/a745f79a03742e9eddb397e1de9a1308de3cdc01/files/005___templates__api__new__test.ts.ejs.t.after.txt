---
to: tests/e2e/api-<%= testName %>.spec.ts
---
import { test, expect } from '@nuxt/test-utils/playwright'

test.describe('<%= method.toUpperCase() %> /api/<%= path %>', () => {
  test('should return success response', async ({ page, goto }) => {
    await goto('/', { waitUntil: 'hydration' })

    <% if (method === 'get') { %>    const response = await page.request.get('/api/<%= path %>'<% if (hasQueryParams) { %>, {
      params: {
        someParam: 'test-value',
        page: '1',
        limit: '10',
      }
    }<% } %>)<% } else if (method === 'post') { %>    const response = await page.request.post('/api/<%= path %>', {<% if (hasRequestBody) { %>
      data: {
        someField: 'test-value',
      }<% } %>
    })<% } else if (method === 'put') { %>    const response = await page.request.put('/api/<%= path %>', {<% if (hasRequestBody) { %>
      data: {
        someField: 'updated-value',
      }<% } %>
    })<% } else if (method === 'patch') { %>    const response = await page.request.patch('/api/<%= path %>', {<% if (hasRequestBody) { %>
      data: {
        someField: 'patched-value',
      }<% } %>
    })<% } else if (method === 'delete') { %>    const response = await page.request.delete('/api/<%= path %>')<% } %>

    expect(response.status()).toBe(200)
    
    // TODO: Add tests for the response data
  })

  // TODO: Add more specific test cases based on your business logic
}) 
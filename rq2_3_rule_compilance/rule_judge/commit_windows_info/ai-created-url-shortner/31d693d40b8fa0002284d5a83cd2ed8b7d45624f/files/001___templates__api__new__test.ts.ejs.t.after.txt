---
to: server/api/<%= path %>.<%= method %>.test.ts
---
// @vitest-environment nuxt
import { describe, it, expect } from "vitest";

describe("<%= method.toUpperCase() %> /api/<%= path %>", () => {
  it("should return the standard payload shape prescribed by defineApiResponse", async () => {
    const response = await $vitestFetch("/api/<%= path %>"<% if (method === 'get' && hasQueryParams) { %>, {
      query: {
        someParam: "test-value",
        page: "1",
        limit: "10",
      },
    }<% } else if (method === 'post' && hasRequestBody) { %>, {
      method: "POST",
      body: {
        someField: "test-value",
      },
    }<% } else if (method === 'put' && hasRequestBody) { %>, {
      method: "PUT", 
      body: {
        someField: "updated-value",
      },
    }<% } else if (method === 'patch' && hasRequestBody) { %>, {
      method: "PATCH",
      body: {
        someField: "patched-value", 
      },
    }<% } else if (method === 'delete') { %>, {
      method: "DELETE",
    }<% } %>);

    expect(response.statusCode).toBe(<% if (method === 'post') { %>201<% } else { %>200<% } %>);
    expect(response).toHaveProperty("message");
    expect(response).toHaveProperty("statusMessage");
    expect(response).toHaveProperty("data");
    expect(response).toHaveProperty("url");
    expect(response.error).toBeFalsy();
  });

  <% if (method === 'get') { %>it("should return expected data structure", async () => {
    const response = await $vitestFetch("/api/<%= path %>");
    
    // TODO: Add assertions for the expected data structure
    expect(response.data).toBeDefined();
  });

  <% if (hasQueryParams) { %>it("should handle query parameters correctly", async () => {
    const testParams = {
      someParam: "test-value",
      page: "1", 
      limit: "10",
    };
    
    const response = await $vitestFetch("/api/<%= path %>", {
      query: testParams,
    });

    expect(response.statusCode).toBe(200);
    // TODO: Add assertions for how query parameters affect the response
  });<% } %><% } %>

  <% if (method === 'post') { %>it("should create resource successfully", async () => {
    const testData = {
      someField: "test-value",
    };

    const response = await $vitestFetch("/api/<%= path %>", {
      method: "POST",
      body: testData,
    });

    expect(response.statusCode).toBe(201);
    expect(response.data).toBeDefined();
    // TODO: Add assertions for created resource structure
  });

  it("should validate required fields", async () => {
    const response = await $vitestFetch("/api/<%= path %>", {
      method: "POST",
      body: {},
    });

    // TODO: Update expected status code based on your validation logic
    expect([400, 422]).toContain(response.statusCode);
  });<% } %>

  <% if (method === 'put') { %>it("should update resource successfully", async () => {
    const testData = {
      someField: "updated-value",
    };

    const response = await $vitestFetch("/api/<%= path %>", {
      method: "PUT",
      body: testData,
    });

    expect(response.statusCode).toBe(200);
    expect(response.data).toBeDefined();
    // TODO: Add assertions for updated resource structure
  });<% } %>

  <% if (method === 'patch') { %>it("should partially update resource successfully", async () => {
    const testData = {
      someField: "patched-value",
    };

    const response = await $vitestFetch("/api/<%= path %>", {
      method: "PATCH", 
      body: testData,
    });

    expect(response.statusCode).toBe(200);
    expect(response.data).toBeDefined();
    // TODO: Add assertions for updated resource structure
  });<% } %>

  <% if (method === 'delete') { %>it("should delete resource successfully", async () => {
    const response = await $vitestFetch("/api/<%= path %>", {
      method: "DELETE",
    });

    expect(response.statusCode).toBe(200);
    // TODO: Add assertions for successful deletion response
  });<% } %>

  // TODO: Add more specific test cases based on your business logic
  // TODO: Add error handling tests (404, 500, etc.)
}); 
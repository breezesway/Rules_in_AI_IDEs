---
to: server/api/<%= plural %>/index.get.test.ts
---
// @vitest-environment nuxt
import { describe, it, expect } from "vitest";

describe("GET /api/<%= plural %>", () => {
  it("should return the standard payload shape prescribed by defineApiResponse", async () => {
    const response = await $vitestFetch("/api/<%= plural %>");

    expect(response.statusCode).toBe(200);
    expect(response).toHaveProperty("message");
    expect(response).toHaveProperty("statusMessage");
    expect(response).toHaveProperty("data");
    expect(response).toHaveProperty("url");
    expect(response.error).toBeFalsy();
  });

  it("should return an array of <%= plural %>", async () => {
    const response = await $vitestFetch("/api/<%= plural %>");

    expect(response.data).toBeDefined();
    expect(Array.isArray(response.data)).toBe(true);
    // TODO: Add assertions for <%= name %> object structure
  });

  it("should handle pagination parameters", async () => {
    const paginationParams = {
      page: "1",
      limit: "10",
    };

    const response = await $vitestFetch("/api/<%= plural %>", {
      query: paginationParams,
    });

    expect(response.statusCode).toBe(200);
    expect(response).toHaveProperty("pagination");
    expect(response.pagination).toHaveProperty("page");
    expect(response.pagination).toHaveProperty("limit");
    expect(response.pagination).toHaveProperty("total");
    // TODO: Add more pagination assertions
  });

  it("should handle search parameter", async () => {
    const searchParams = {
      search: "test-search-term",
    };

    const response = await $vitestFetch("/api/<%= plural %>", {
      query: searchParams,
    });

    expect(response.statusCode).toBe(200);
    // TODO: Add assertions for search functionality
  });

  it("should handle default pagination when no parameters provided", async () => {
    const response = await $vitestFetch("/api/<%= plural %>");

    expect(response.statusCode).toBe(200);
    expect(response).toHaveProperty("pagination");
    expect(response.pagination.page).toBe(1);
    expect(response.pagination.limit).toBe(20);
  });

  // TODO: Add tests for edge cases (empty results, invalid pagination, etc.)
}); 
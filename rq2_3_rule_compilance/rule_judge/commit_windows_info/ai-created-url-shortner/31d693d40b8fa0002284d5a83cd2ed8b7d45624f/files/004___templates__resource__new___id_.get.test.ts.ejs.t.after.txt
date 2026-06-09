---
to: server/api/<%= plural %>/[id].get.test.ts
---
// @vitest-environment nuxt
import { describe, it, expect } from "vitest";

describe("GET /api/<%= plural %>/[id]", () => {
  let testResourceId: string;

  // Setup: Create a test resource before running tests
  beforeEach(async () => {
    const createResponse = await $vitestFetch("/api/<%= plural %>", {
      method: "POST",
      body: {
        someField: "test-get-resource",
      },
    });
    
    if (createResponse.statusCode === 201 && createResponse.data?.id) {
      testResourceId = createResponse.data.id;
    } else {
      throw new Error("Failed to create test resource");
    }
  });

  it("should return the standard payload shape prescribed by defineApiResponse", async () => {
    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`);

    expect(response.statusCode).toBe(200);
    expect(response).toHaveProperty("message");
    expect(response).toHaveProperty("statusMessage");
    expect(response).toHaveProperty("data");
    expect(response).toHaveProperty("url");
    expect(response.error).toBeFalsy();
  });

  it("should return the correct <%= name %> by ID", async () => {
    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`);

    expect(response.statusCode).toBe(200);
    expect(response.data).toBeDefined();
    expect(response.data.id).toBe(testResourceId);
    expect(response.data).toHaveProperty("someField");
    // TODO: Add assertions for <%= name %> object structure
  });

  it("should return 404 for non-existent resource", async () => {
    const nonExistentId = "non-existent-id-12345";
    const response = await $vitestFetch(`/api/<%= plural %>/${nonExistentId}`);

    expect(response.statusCode).toBe(404);
    expect(response.error).toBeTruthy();
  });

  it("should handle invalid ID format", async () => {
    const invalidId = "invalid-id-format-!@#$%";
    const response = await $vitestFetch(`/api/<%= plural %>/${invalidId}`);

    // Depending on validation, this could be 400 (bad request) or 404 (not found)
    expect([400, 404]).toContain(response.statusCode);
    expect(response.error).toBeTruthy();
  });

  it("should handle empty ID parameter", async () => {
    const response = await $vitestFetch("/api/<%= plural %>/");

    // This should typically route to the index endpoint or return 404
    expect([200, 404]).toContain(response.statusCode);
  });
  
  // TODO: Add tests for specific business logic related to the resource
  // TODO: Add tests for resource relationships if applicable
}); 
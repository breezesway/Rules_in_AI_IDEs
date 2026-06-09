---
to: server/api/<%= plural %>/index.post.test.ts
---
// @vitest-environment nuxt
import { describe, it, expect } from "vitest";

describe("POST /api/<%= plural %>", () => {
  it("should return the standard payload shape prescribed by defineApiResponse", async () => {
    const testData = {
      // TODO: Customize payload as needed
      someField: "test-value",
    };

    const response = await $vitestFetch("/api/<%= plural %>", {
      method: "POST",
      body: testData,
    });

    expect(response.statusCode).toBe(201);
    expect(response).toHaveProperty("message");
    expect(response).toHaveProperty("statusMessage");
    expect(response).toHaveProperty("data");
    expect(response).toHaveProperty("url");
    expect(response.error).toBeFalsy();
  });

  it("should create a new <%= name %> successfully", async () => {
    const testData = {
      // TODO: Customize payload as needed
      someField: "test-value",
    };

    const response = await $vitestFetch("/api/<%= plural %>", {
      method: "POST",
      body: testData,
    });

    expect(response.statusCode).toBe(201);
    expect(response.data).toBeDefined();
    expect(response.data).toHaveProperty("id");
    // TODO: Add assertions for created <%= name %> structure
  });

  it("should validate required fields", async () => {
    const response = await $vitestFetch("/api/<%= plural %>", {
      method: "POST",
      body: {},
    });

    expect([400, 422]).toContain(response.statusCode);
    // TODO: Update expected status code based on your validation logic
  });

  // TODO: Add tests for specific business logic
    // Remember to handle edge cases and error scenarios
}); 
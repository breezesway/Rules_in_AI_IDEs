---
to: server/api/<%= plural %>/[id].put.test.ts
---
// @vitest-environment nuxt
import { describe, it, expect } from "vitest";

describe("PUT /api/<%= plural %>/[id]", () => {
  let testResourceId: string;

  // Setup: Create a test resource before running tests
  beforeEach(async () => {
    const createResponse = await $vitestFetch("/api/<%= plural %>", {
      method: "POST",
      body: {
        someField: "test-put-resource",
      },
    });
    
    if (createResponse.statusCode === 201 && createResponse.data?.id) {
      testResourceId = createResponse.data.id;
    } else {
      throw new Error("Failed to create test resource");
    }
  });

  it("should return the standard payload shape prescribed by defineApiResponse", async () => {
    const updateData = {
      someField: "updated-test-value",
    };

    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`, {
      method: "PUT",
      body: updateData,
    });

    expect(response.statusCode).toBe(200);
    expect(response).toHaveProperty("message");
    expect(response).toHaveProperty("statusMessage");
    expect(response).toHaveProperty("data");
    expect(response).toHaveProperty("url");
    expect(response.error).toBeFalsy();
  });

  it("should update the <%= name %> successfully", async () => {
    const updateData = {
      someField: "updated-test-value",
    };

    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`, {
      method: "PUT",
      body: updateData,
    });

    expect(response.statusCode).toBe(200);
    expect(response.data).toBeDefined();
    expect(response.data.id).toBe(testResourceId);
    expect(response.data.someField).toBe(updateData.someField);
    // TODO: Add assertions for updated <%= name %> structure
  });

  it("should validate required fields on update", async () => {
    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`, {
      method: "PUT",
      body: {},
    });

    expect([400, 422]).toContain(response.statusCode);
    expect(response.error).toBeTruthy();
    // TODO: Update expected status code based on your validation logic
  });

  it("should return 404 for non-existent resource", async () => {
    const nonExistentId = "non-existent-id-12345";
    const updateData = {
      someField: "updated-value",
    };

    const response = await $vitestFetch(`/api/<%= plural %>/${nonExistentId}`, {
      method: "PUT",
      body: updateData,
    });

    expect(response.statusCode).toBe(404);
    expect(response.error).toBeTruthy();
  });

  it("should handle invalid ID format", async () => {
    const invalidId = "invalid-id-format-!@#$%";
    const updateData = {
      someField: "updated-value",
    };

    const response = await $vitestFetch(`/api/<%= plural %>/${invalidId}`, {
      method: "PUT",
      body: updateData,
    });

    // Depending on validation, this could be 400 (bad request) or 404 (not found)
    expect([400, 404]).toContain(response.statusCode);
    expect(response.error).toBeTruthy();
  });

  it("should handle validation errors gracefully", async () => {
    const invalidData = {
      someField: "", // Invalid empty value
    };

    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`, {
      method: "PUT",
      body: invalidData,
    });

    expect([400, 422]).toContain(response.statusCode);
    expect(response.error).toBeTruthy();
    // TODO: Add assertions for validation error messages
  });

  it("should preserve ID during update", async () => {
    const updateData = {
      id: "different-id-should-be-ignored",
      someField: "updated-value",
    };

    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`, {
      method: "PUT",
      body: updateData,
    });

    expect(response.statusCode).toBe(200);
    expect(response.data.id).toBe(testResourceId); // Should not change
    expect(response.data.someField).toBe(updateData.someField);
  });

  // TODO: Add tests for specific business logic
  // TODO: Add tests for partial vs full updates
}); 
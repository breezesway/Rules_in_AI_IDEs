---
to: server/api/<%= plural %>/[id].delete.test.ts
---
// @vitest-environment nuxt
import { describe, it, expect } from "vitest";

describe("DELETE /api/<%= plural %>/[id]", () => {
  let testResourceId: string;

  // Setup: Create a test resource before running tests
  beforeEach(async () => {
    const createResponse = await $vitestFetch("/api/<%= plural %>", {
      method: "POST",
      body: {
        someField: "test-delete-resource",
      },
    });
    
    if (createResponse.statusCode === 201 && createResponse.data?.id) {
      testResourceId = createResponse.data.id;
    } else {
      throw new Error("Failed to create test resource");
    }
  });

  it("should return the standard payload shape prescribed by defineApiResponse", async () => {
    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`, {
      method: "DELETE",
    });

    expect(response.statusCode).toBe(200);
    expect(response).toHaveProperty("message");
    expect(response).toHaveProperty("statusMessage");
    expect(response).toHaveProperty("data");
    expect(response).toHaveProperty("url");
    expect(response.error).toBeFalsy();
  });

  it("should delete the <%= name %> successfully", async () => {
    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`, {
      method: "DELETE",
    });

    expect(response.statusCode).toBe(200);
    expect(response.data).toBeDefined();
    // TODO: Add assertions for successful deletion response structure
  });

  it("should confirm resource is deleted by verifying GET returns 404", async () => {
    // Delete the resource
    const deleteResponse = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`, {
      method: "DELETE",
    });
    expect(deleteResponse.statusCode).toBe(200);

    // Try to get the deleted resource
    const getResponse = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`);
    expect(getResponse.statusCode).toBe(404);
    expect(getResponse.error).toBeTruthy();
  });

  it("should return 404 for non-existent resource", async () => {
    const nonExistentId = "non-existent-id-12345";
    const response = await $vitestFetch(`/api/<%= plural %>/${nonExistentId}`, {
      method: "DELETE",
    });

    expect(response.statusCode).toBe(404);
    expect(response.error).toBeTruthy();
  });

  it("should handle invalid ID format", async () => {
    const invalidId = "invalid-id-format-!@#$%";
    const response = await $vitestFetch(`/api/<%= plural %>/${invalidId}`, {
      method: "DELETE",
    });

    // Depending on validation, this could be 400 (bad request) or 404 (not found)
    expect([400, 404]).toContain(response.statusCode);
    expect(response.error).toBeTruthy();
  });

  it("should handle deleting the same resource twice", async () => {
    // First deletion
    const firstDeleteResponse = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`, {
      method: "DELETE",
    });
    expect(firstDeleteResponse.statusCode).toBe(200);

    // Second deletion attempt
    const secondDeleteResponse = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`, {
      method: "DELETE",
    });
    expect(secondDeleteResponse.statusCode).toBe(404);
    expect(secondDeleteResponse.error).toBeTruthy();
  });

  it("should handle cascade deletes if applicable", async () => {
    // TODO: If this resource has related data that should be deleted,
    // add tests to verify proper cascade behavior
    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`, {
      method: "DELETE",
    });

    expect(response.statusCode).toBe(200);
    // TODO: Add assertions for cascade deletion verification
  });

  // TODO: Add tests for soft delete vs hard delete if applicable
  // TODO: Add tests for business logic constraints that prevent deletion
}); 
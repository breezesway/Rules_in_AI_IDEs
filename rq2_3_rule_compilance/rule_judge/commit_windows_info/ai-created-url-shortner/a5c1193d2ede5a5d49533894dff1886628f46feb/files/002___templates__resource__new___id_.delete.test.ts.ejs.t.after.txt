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
        // TODO: Customize payload as needed
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

  // TODO: Add other tests for specific business logic
    // Remember to handle edge cases and error scenarios
}); 
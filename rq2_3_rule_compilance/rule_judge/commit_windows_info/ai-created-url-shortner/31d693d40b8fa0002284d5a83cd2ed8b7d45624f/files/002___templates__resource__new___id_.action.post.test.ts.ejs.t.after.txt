---
to: server/api/<%= plural %>/[id]/action.post.test.ts
---
// @vitest-environment nuxt
import { describe, it, expect } from "vitest";

describe("POST /api/<%= plural %>/[id]/action", () => {
  let testResourceId: string;

  // Setup: Create a test resource before running tests
  beforeEach(async () => {
    const createResponse = await $vitestFetch("/api/<%= plural %>", {
      method: "POST",
      body: {
        someField: "test-action-resource",
      },
    });
    
    if (createResponse.statusCode === 201 && createResponse.data?.id) {
      testResourceId = createResponse.data.id;
    } else {
      throw new Error("Failed to create test resource");
    }
  });

  it("should return the standard payload shape prescribed by defineApiResponse", async () => {
    const actionData = {
      actionParam: "test-action-value",
    };

    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}/action`, {
      method: "POST",
      body: actionData,
    });

    expect(response.statusCode).toBe(200);
    expect(response).toHaveProperty("message");
    expect(response).toHaveProperty("statusMessage");
    expect(response).toHaveProperty("data");
    expect(response).toHaveProperty("url");
    expect(response.error).toBeFalsy();
  });

  it("should perform the custom action successfully", async () => {
    const actionData = {
      actionParam: "test-action-value",
    };

    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}/action`, {
      method: "POST",
      body: actionData,
    });

    expect(response.statusCode).toBe(200);
    expect(response.data).toBeDefined();
    // TODO: Add assertions for action result structure
    // TODO: Define what the custom action should return
  });

  it("should validate action parameters", async () => {
    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}/action`, {
      method: "POST",
      body: {},
    });

    // TODO: Update expected status code based on your validation logic
    expect([200, 400, 422]).toContain(response.statusCode);
    // If validation is required, expect error response
    // expect([400, 422]).toContain(response.statusCode);
    // expect(response.error).toBeTruthy();
  });

  it("should return 404 for non-existent resource", async () => {
    const nonExistentId = "non-existent-id-12345";
    const actionData = {
      actionParam: "test-action-value",
    };

    const response = await $vitestFetch(`/api/<%= plural %>/${nonExistentId}/action`, {
      method: "POST",
      body: actionData,
    });

    expect(response.statusCode).toBe(404);
    expect(response.error).toBeTruthy();
  });

  it("should handle invalid ID format", async () => {
    const invalidId = "invalid-id-format-!@#$%";
    const actionData = {
      actionParam: "test-action-value",
    };

    const response = await $vitestFetch(`/api/<%= plural %>/${invalidId}/action`, {
      method: "POST",
      body: actionData,
    });

    // Depending on validation, this could be 400 (bad request) or 404 (not found)
    expect([400, 404]).toContain(response.statusCode);
    expect(response.error).toBeTruthy();
  });

  it("should handle invalid action parameters", async () => {
    const invalidActionData = {
      actionParam: "", // Invalid empty value
      // Add other invalid parameters based on your action logic
    };

    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}/action`, {
      method: "POST",
      body: invalidActionData,
    });

    // TODO: Define expected behavior for invalid action parameters
    expect([400, 422]).toContain(response.statusCode);
    expect(response.error).toBeTruthy();
  });

  it("should verify action affects the resource appropriately", async () => {
    const actionData = {
      actionParam: "test-action-value",
    };

    // Perform the action
    const actionResponse = await $vitestFetch(`/api/<%= plural %>/${testResourceId}/action`, {
      method: "POST",
      body: actionData,
    });
    expect(actionResponse.statusCode).toBe(200);

    // Verify the resource state after action
    const getResponse = await $vitestFetch(`/api/<%= plural %>/${testResourceId}`);
    expect(getResponse.statusCode).toBe(200);
    
    // TODO: Add assertions to verify the action modified the resource as expected
    // For example, if the action changes a status or updates a field:
    // expect(getResponse.data.status).toBe("expected-status-after-action");
  });

  // TODO: Add tests for specific action business logic
  // TODO: Add tests for action side effects (notifications, logs, etc.)
  // TODO: Add tests for idempotency if the action should be idempotent
}); 
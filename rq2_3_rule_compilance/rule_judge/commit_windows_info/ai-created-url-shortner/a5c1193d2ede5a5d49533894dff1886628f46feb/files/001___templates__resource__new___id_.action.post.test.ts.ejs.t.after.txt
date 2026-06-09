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
        // TODO: Customize payload as needed
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
      // TODO: Customize payload as needed
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
      // TODO: Customize payload as needed
      actionParam: "test-action-value",
    };

    const response = await $vitestFetch(`/api/<%= plural %>/${testResourceId}/action`, {
      method: "POST",
      body: actionData,
    });

    expect(response.statusCode).toBe(200);
    expect(response.data).toBeDefined();
    // TODO: Add assertions for action specific results
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

  // TODO: Add other tests for specific action business logic
    // Remember to handle edge cases and error scenarios
}); 
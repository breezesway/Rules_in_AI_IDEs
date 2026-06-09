// @vitest-environment nuxt
import { describe, it, expect } from "vitest";
import packageJson from "../../package.json";

describe("GET /api/health", () => {
  it("should return the standard payload shape prescribed by defineApiResponse", async () => {
    const response = await $vitestFetch("/api/health");

    expect(response.statusCode).toBe(200);
    expect(response).toHaveProperty("message");
    expect(response).toHaveProperty("statusMessage");
    expect(response).toHaveProperty("data");
    expect(response).toHaveProperty("url");
    expect(response.error).toBeFalsy();
  });

  it("should return a healthy status response", async () => {
    const response = await $vitestFetch("/api/health");

    expect(response.data.status).toBe("healthy");
  });

  it("should accept and return optional data parameter", async () => {
    const testData = "test-health-data";
    const response = await $vitestFetch("/api/health", {
      query: {
        data: testData,
      },
    });

    expect(response.data.requestPayload).toBe(testData);
  });

  it("should return correct response structure", async () => {
    const response = await $vitestFetch("/api/health");

    const expectedKeys = ["status", "timestamp", "version"];
    expectedKeys.forEach((key) => {
      expect(response.data).toHaveProperty(key);
    });
  });

  it("should always return version from package.json", async () => {
    const response = await $vitestFetch("/api/health");
    expect(response.data.version).toBe(packageJson.version);
  });
});

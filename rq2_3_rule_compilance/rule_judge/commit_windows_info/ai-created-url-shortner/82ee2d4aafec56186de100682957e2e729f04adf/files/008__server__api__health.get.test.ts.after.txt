// @vitest-environment nuxt
import { describe, it, expect } from "vitest";
import packageJson from "../../package.json";


describe("GET /api/health", () => {
  it("should return a healthy status response", async () => {
    const response = await $vitestFetch("/api/health");
    
    expect(response.status).toBe("healthy");
  });

  it("should accept and return optional data parameter", async () => {
    const testData = "test-health-data";
    const response = await $vitestFetch("/api/health", {
    
      query: {
        data: testData,
      },
    });
    
    expect(response.data).toBe(testData);
  });

  it("should return correct response structure", async () => {
    const response = await $vitestFetch("/api/health");
    
    const expectedKeys = ["status", "timestamp", "version"];
    expectedKeys.forEach(key => {
      expect(response).toHaveProperty(key);
    });
  });

  it("should always return version from package.json", async () => {
    const response = await $vitestFetch("/api/health");
    expect(response.version).toBe(packageJson.version);
  });
});

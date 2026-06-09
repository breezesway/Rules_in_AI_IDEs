// @vitest-environment nuxt
import { describe, it, expect } from "vitest";
import { useDb } from "./db";

describe("Database Utilities", () => {
  it("should have db function available", () => {
    // Test that the db utility function is available
    expect(typeof useDb).toBe("function");
  });

  it("should return a database instance", () => {
    const db = useDb();
    expect(db).toBeDefined();
    expect(typeof db).toBe("object");
  });

  it("should be accessible and callable", () => {
    // This verifies the function exists and is callable
    expect(() => useDb()).not.toThrow();
  });
});

// @vitest-environment nuxt
import { describe, it, expect, vi, beforeEach } from "vitest";
import type { H3Event } from "h3";
import {
  defineApiResponse,
  definePaginatedApiResponse,
} from "./baseServerUtils";

// Mock H3 utilities
vi.mock("h3", async () => {
  const actual = await vi.importActual("h3");
  return {
    ...actual,
    getRequestURL: vi.fn(),
    getResponseStatus: vi.fn(),
    defineEventHandler: vi.fn((handler) => handler),
    getQuery: vi.fn(),
    readBody: vi.fn(),
    createError: vi.fn((config) => {
      const error = new Error(config.statusMessage);
      Object.assign(error, config);
      return error;
    }),
  };
});

describe("baseServerUtils", () => {
  let mockEvent: Partial<H3Event>;

  beforeEach(async () => {
    vi.clearAllMocks();

    mockEvent = {
      method: "GET",
      context: {
        params: {},
      },
    };

    // Setup default mocks
    const { getRequestURL, getResponseStatus } = await import("h3");
    vi.mocked(getRequestURL).mockReturnValue(
      new URL("https://example.com/api/test?page=1")
    );
    vi.mocked(getResponseStatus).mockReturnValue(200);
  });

  describe("defineApiResponse", () => {
    it("should return a properly formatted API response", () => {
      const testData = { id: 1, name: "Test User" };
      const response = defineApiResponse(mockEvent as H3Event, {
        data: testData,
        statusMessage: "User retrieved successfully",
      });

      expect(response).toEqual({
        error: false,
        url: new URL("https://example.com/api/test?page=1"),
        statusMessage: "User retrieved successfully",
        statusCode: 200,
        message: "User retrieved successfully",
        data: testData,
      });
    });

    it("should use default statusMessage when not provided", () => {
      const testData = { message: "Hello World" };
      const response = defineApiResponse(mockEvent as H3Event, {
        data: testData,
      });

      expect(response.statusMessage).toBe("Success!");
      expect(response.message).toBe("Success!");
    });

    it("should include the request URL and status code", async () => {
      const { getRequestURL, getResponseStatus } = await import("h3");
      const mockUrl = new URL("https://api.example.com/users/123");
      vi.mocked(getRequestURL).mockReturnValue(mockUrl);
      vi.mocked(getResponseStatus).mockReturnValue(201);

      const response = defineApiResponse(mockEvent as H3Event, {
        data: { created: true },
      });

      expect(response.url).toBe(mockUrl);
      expect(response.statusCode).toBe(201);
    });

    it("should handle null or undefined data", () => {
      const response = defineApiResponse(mockEvent as H3Event, {
        data: null,
        statusMessage: "No data found",
      });

      expect(response.data).toBeNull();
      expect(response.error).toBe(false);
    });
  });

  describe("definePaginatedApiResponse", () => {
    it("should return a properly formatted paginated API response", async () => {
      const { getRequestURL } = await import("h3");
      vi.mocked(getRequestURL).mockReturnValue(
        new URL("https://example.com/api/users?page=2")
      );

      const testData = [
        { id: 1, name: "User 1" },
        { id: 2, name: "User 2" },
      ];

      const response = definePaginatedApiResponse(mockEvent as H3Event, {
        data: testData,
        statusMessage: "Users retrieved successfully",
        pagination: {
          page: 2,
          limit: 10,
          total: 25,
        },
      });

      expect(response.data).toEqual(testData);
      expect(response.statusMessage).toBe("Users retrieved successfully");
      expect(response.pagination).toEqual({
        page: 2,
        limit: 10,
        total: 25,
        currentPageUrl: "https://example.com/api/users?page=2",
        firstPageUrl: "https://example.com/api/users",
        lastPageUrl: "https://example.com/api/users?page=3",
        nextPageUrl: "https://example.com/api/users?page=3",
        prevPageUrl: "https://example.com/api/users?page=1",
      });
    });

    it("should handle first page correctly", async () => {
      const { getRequestURL } = await import("h3");
      vi.mocked(getRequestURL).mockReturnValue(
        new URL("https://example.com/api/users")
      );

      const response = definePaginatedApiResponse(mockEvent as H3Event, {
        data: [],
        pagination: {
          page: 1,
          limit: 10,
          total: 25,
        },
      });

      expect(response.pagination.page).toBe(1);
      expect(response.pagination.currentPageUrl).toBe(
        "https://example.com/api/users"
      );
      expect(response.pagination.prevPageUrl).toBeNull();
      expect(response.pagination.nextPageUrl).toBe(
        "https://example.com/api/users?page=2"
      );
    });

    it("should handle last page correctly", async () => {
      const { getRequestURL } = await import("h3");
      vi.mocked(getRequestURL).mockReturnValue(
        new URL("https://example.com/api/users?page=3")
      );

      const response = definePaginatedApiResponse(mockEvent as H3Event, {
        data: [],
        pagination: {
          page: 3,
          limit: 10,
          total: 25,
        },
      });

      expect(response.pagination.page).toBe(3);
      expect(response.pagination.nextPageUrl).toBeNull();
      expect(response.pagination.prevPageUrl).toBe(
        "https://example.com/api/users?page=2"
      );
      expect(response.pagination.lastPageUrl).toBe(
        "https://example.com/api/users?page=3"
      );
    });

    it("should handle single page (no pagination needed)", () => {
      const response = definePaginatedApiResponse(mockEvent as H3Event, {
        data: [{ id: 1 }],
        pagination: {
          page: 1,
          limit: 10,
          total: 5,
        },
      });

      expect(response.pagination.nextPageUrl).toBeNull();
      expect(response.pagination.prevPageUrl).toBeNull();
      expect(response.pagination.lastPageUrl).toBe(
        "https://example.com/api/test?page=1"
      );
    });

    it("should use default statusMessage when not provided", () => {
      const response = definePaginatedApiResponse(mockEvent as H3Event, {
        data: [],
        pagination: {
          page: 1,
          limit: 10,
          total: 0,
        },
      });

      expect(response.statusMessage).toBe("Success!");
      expect(response.message).toBe("Success!");
    });

    it("should handle edge cases with zero total", () => {
      const response = definePaginatedApiResponse(mockEvent as H3Event, {
        data: [],
        pagination: {
          page: 1,
          limit: 10,
          total: 0,
        },
      });

      expect(response.pagination.total).toBe(0);
      expect(response.pagination.nextPageUrl).toBeNull();
      expect(response.pagination.prevPageUrl).toBeNull();
    });

    it("should preserve query parameters in URLs", async () => {
      const { getRequestURL } = await import("h3");
      vi.mocked(getRequestURL).mockReturnValue(
        new URL("https://example.com/api/users?search=john&sort=name&page=2")
      );

      const response = definePaginatedApiResponse(mockEvent as H3Event, {
        data: [],
        pagination: {
          page: 2,
          limit: 10,
          total: 25,
        },
      });

      // URLs should only contain the page parameter
      expect(response.pagination.currentPageUrl).toBe(
        "https://example.com/api/users?page=2"
      );
      expect(response.pagination.nextPageUrl).toBe(
        "https://example.com/api/users?page=3"
      );
      expect(response.pagination.firstPageUrl).toBe(
        "https://example.com/api/users"
      );
    });
  });
});

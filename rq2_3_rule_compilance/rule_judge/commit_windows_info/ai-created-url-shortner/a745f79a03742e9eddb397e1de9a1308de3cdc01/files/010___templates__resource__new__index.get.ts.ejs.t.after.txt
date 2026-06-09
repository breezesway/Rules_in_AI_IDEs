---
to: server/api/<%= plural %>/index.get.ts
---
import { z } from "zod";

defineRouteMeta({
  // TODO: fill out meta as needed
  openAPI: {
    tags: ["<%= plural %>"],
    description: "Get all <%= plural %>",
    parameters: [
      { in: "query", name: "page", required: false, schema: { type: "number", default: 1 } },
      { in: "query", name: "limit", required: false, schema: { type: "number", default: 20 } },
      { in: "query", name: "search", required: false, schema: { type: "string" } },
    ],
    responses: {
      200: {
        description: "List of <%= plural %>",
        content: {
          "application/json": {
            schema: {
              type: "object",
              properties: {
                error: { type: "boolean" },
                url: { type: "string" },
                statusMessage: { type: "string" },
                statusCode: { type: "number" },
                message: { type: "string" },
                data: {
                  type: "array",
                  items: {
                    type: "object",
                    // TODO: Customize your properties here
                    properties: {
                      id: { type: "string" },
                      someField: { type: "string" },
                    },
                  },
                },
                pagination: {
                  type: "object",
                  properties: {
                    page: { type: "number" },
                    limit: { type: "number" },
                    total: { type: "number" },
                    currentPageUrl: { type: "string" },
                    firstPageUrl: { type: "string" },
                    lastPageUrl: { type: "string" },
                    nextPageUrl: { type: "string", nullable: true },
                    prevPageUrl: { type: "string", nullable: true },
                  },
                },
              },
            },
          },
        },
      },
    },
  },
});

export default defineApiEventHandler({
  // TODO: fill out validation as needed
  validation: z.object({
    page: z.coerce.number().int().min(1).default(1),
    limit: z.coerce.number().int().min(1).max(100).default(20),
    search: z.string().optional(),
  }),
  handler: async (event, { page, limit, search }) => {
    const db = useDb();
    
    // TODO: implement API functionality
    
    // TODO: modify response as needed
    return definePaginatedApiResponse(event, {
      data: [], // TODO: Replace with actual data
      statusMessage: "Retrieved <%= plural %> successfully",
      pagination: {
        page,
        limit,
        total: 0, // TODO: Set actual total count
      },
    });
  },
}); 
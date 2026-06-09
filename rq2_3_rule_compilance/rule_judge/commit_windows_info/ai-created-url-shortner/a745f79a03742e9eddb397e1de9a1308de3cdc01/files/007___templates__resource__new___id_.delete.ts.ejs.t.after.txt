---
to: server/api/<%= plural %>/[id].delete.ts
---
import { z } from "zod";

defineRouteMeta({
  // TODO: fill out meta as needed
  openAPI: {
    tags: ["<%= plural %>"],
    description: "Delete a <%= name %> by ID",
    parameters: [
      { in: "path", name: "id", required: true, schema: { type: "string" } },
    ],
    responses: {
      200: {
        description: "<%= Name %> deleted successfully",
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
                  type: "object",
                  properties: {
                    id: { type: "string" },
                    deleted: { type: "boolean" },
                  },
                },
              },
            },
          },
        },
      },
      404: {
        description: "<%= Name %> not found",
      },
    },
  },
});

export default defineApiEventHandler({
  // TODO: fill out validation as needed
  validation: z.object({
    id: z.string().min(1, "ID is required"),
  }),
  // guards: [userIsLoggedInGuard], // TODO: Add authentication if needed
  handler: async (event, { id }) => {
    const db = useDb();
    
    // TODO: implement API functionality
    
    // TODO: modify response as needed
    return defineApiResponse(event, {
      data: { id, deleted: true },
      statusMessage: "<%= Name %> deleted successfully",
    });
  },
}); 
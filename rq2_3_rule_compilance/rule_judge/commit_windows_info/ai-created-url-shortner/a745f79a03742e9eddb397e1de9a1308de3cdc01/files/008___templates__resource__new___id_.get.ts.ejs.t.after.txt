---
to: server/api/<%= plural %>/[id].get.ts
---
import { z } from "zod";

defineRouteMeta({
  // TODO: fill out meta as needed
  openAPI: {
    tags: ["<%= plural %>"],
    description: "Get a <%= name %> by ID",
    parameters: [
      { in: "path", name: "id", required: true, schema: { type: "string" } },
    ],
    responses: {
      200: {
        description: "<%= Name %> found",
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
                  // TODO: Customize your properties here
                  properties: {
                    id: { type: "string" },
                    someField: { type: "string" },
                    
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
  handler: async (event, { id }) => {
    const db = useDb();
    
    // TODO: implement API functionality
    
    // TODO: modify response as needed
    return defineApiResponse(event, {
      data: { id }, // TODO: Replace with actual <%= name %> data
      statusMessage: "<%= Name %> retrieved successfully",
    });
  },
}); 
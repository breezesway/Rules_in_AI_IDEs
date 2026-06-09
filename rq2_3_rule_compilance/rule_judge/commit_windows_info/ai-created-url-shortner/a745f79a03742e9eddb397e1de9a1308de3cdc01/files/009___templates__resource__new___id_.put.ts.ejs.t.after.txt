---
to: server/api/<%= plural %>/[id].put.ts
---
import { z } from "zod";

defineRouteMeta({
  // TODO: fill out meta as needed
  openAPI: {
    tags: ["<%= plural %>"],
    description: "Update a <%= name %> by ID",
    parameters: [
      { in: "path", name: "id", required: true, schema: { type: "string" } },
    ],
    requestBody: {
      content: {
        "application/json": {
          schema: {
            type: "object",
            // TODO: Customize your properties here
            properties: {
              someField: { type: "string" },
            },
          },
        },
      },
    },
    responses: {
      200: {
        description: "<%= Name %> updated successfully",
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
      422: {
        description: "Validation error",
      },
    },
  },
});

export default defineApiEventHandler({
  // TODO: fill out validation as needed
  validation: z.object({
    id: z.string().min(1, "ID is required"),
    someField: z.string().min(1, "SomeField is required"),
    // TODO: Add validation for your <%= name %> properties
  }),
  // guards: [userIsLoggedInGuard], // TODO: Add authentication if needed
  handler: async (event, { id, ...updateData }) => {
    const db = useDb();
    
    // TODO: implement API functionality
    
    // TODO: modify response as needed
    return defineApiResponse(event, {
      data: { id, ...updateData }, // TODO: Replace with actual updated <%= name %> data
      statusMessage: "<%= Name %> updated successfully",
    });
  },
}); 
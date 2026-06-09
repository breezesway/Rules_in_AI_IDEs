---
to: server/api/<%= plural %>/index.post.ts
---
import { z } from "zod";

defineRouteMeta({
  // TODO: fill out meta as needed
  openAPI: {
    tags: ["<%= plural %>"],
    description: "Create a new <%= name %>",
    requestBody: {
      content: {
        "application/json": {
          schema: {
            type: "object",
            // TODO: Customize your properties here
            properties: {
              someField: { type: "string" },
            },
            required: ["someField"],
          },
        },
      },
    },
    responses: {
      201: {
        description: "<%= Name %> created successfully",
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
      400: {
        description: "Invalid input",
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
    someField: z.string().min(1, "SomeField is required"),
    // TODO: Add validation for your <%= name %> properties
  }),
  // guards: [userIsLoggedInGuard], // TODO: Add authentication if needed
  handler: async (event, payload) => {
    const db = useDb();
    
    // Set status code to 201 for creation
    setResponseStatus(event, 201);
    
    // TODO: implement API functionality
    
    // TODO: modify response as needed
    return defineApiResponse(event, {
      data: payload, // TODO: Replace with actual created <%= name %> data
      statusMessage: "<%= Name %> created successfully",
    });
  },
}); 
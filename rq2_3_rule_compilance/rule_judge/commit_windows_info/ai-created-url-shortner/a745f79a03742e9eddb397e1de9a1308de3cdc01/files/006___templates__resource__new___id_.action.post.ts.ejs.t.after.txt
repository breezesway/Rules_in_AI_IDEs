---
to: server/api/<%= plural %>/[id]/action.post.ts
---
import { z } from "zod";

defineRouteMeta({
  // TODO: fill out meta as needed
  openAPI: {
    tags: ["<%= plural %>"],
    description: "Perform custom action on a <%= name %> by ID",
    parameters: [
      { in: "path", name: "id", required: true, schema: { type: "string" } },
    ],
    requestBody: {
      content: {
        "application/json": {
          schema: {
            type: "object",
            properties: {
              someField: { type: "string" },
              // TODO: Add properties specific to the action action
            },
          },
        },
      },
    },
    responses: {
      200: {
        description: "Custom action performed successfully",
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
                    action: { type: "string" },
                    result: { type: "object" },
                    // TODO: Add properties returned by the action action
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
    someField: z.string().optional(),
    // TODO: Add validation specific to the action action
  }),
  // guards: [], // TODO: Add authentication if needed
  handler: async (event, { id, ...actionData }) => {
    const db = useDb();
    
    // TODO: implement action functionality
    
    // TODO: modify response as needed
    return defineApiResponse(event, {
      data: {
        id,
        action: "action",
        result: actionData, // TODO: Replace with actual action result
      },
      statusMessage: "Custom action performed successfully",
    });
  },
}); 
---
to: server/api/<%= path %>.<%= method %>.ts
---
import { z } from 'zod'

defineRouteMeta({
  // TODO: fill out meta as needed
  openAPI: {
    tags: ["<%= tag %>"],
    description: "TODO: Add description for this endpoint",
  },
})

export default defineApiEventHandler({
  // TODO: fill out validation as needed
  validation: z.object({<% if (hasQueryParams) { %>
    // Query parameters for GET endpoints
    someParam: z.string().optional(),
    page: z.coerce.number().int().min(1).default(1),
    limit: z.coerce.number().int().min(1).max(100).default(20),<% } %><% if (hasRequestBody) { %>
    // Request body for POST/PUT/PATCH endpoints
    someField: z.string().min(1, "Some field is required"),
    // TODO: Add validation for your specific properties<% } %><% if (!hasQueryParams && !hasRequestBody) { %>
    // Add validation as needed for your endpoint
    // someField: z.string().min(1),<% } %>
  }),
  handler: async (event, payload) => {<% if (hasQueryParams) { %>
    const { someParam, page, limit } = payload<% } %><% if (hasRequestBody) { %>
    const { someField } = payload<% } %>

    // TODO: implement API functionality

    // TODO: modify response as needed<% if (hasQueryParams) { %>
    return definePaginatedApiResponse(event, {
      data: {
        // TODO: Replace with actual data
        message: "TODO: Add your response data here",
        someParam,
      },
      statusMessage: "Success!",
      pagination: {
        page,
        limit,
        total: 0, // TODO: Set actual total count
      },
    })<% } else { %>
    return defineApiResponse(event, {
      data: {<% if (hasRequestBody) { %>
        message: "TODO: Add your response data here",
        received: { someField },<% } else { %>
        message: "TODO: Add your response data here",<% } %>
      },
      statusMessage: "Success!",
    })<% } %>
  },
}) 
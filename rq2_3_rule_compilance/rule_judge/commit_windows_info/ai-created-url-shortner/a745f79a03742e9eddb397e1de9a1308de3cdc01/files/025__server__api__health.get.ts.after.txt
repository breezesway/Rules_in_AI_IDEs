import { z } from "zod";

export default defineApiEventHandler({
  validation: z.object({
    data: z.string().optional(),
  }),
  handler: async (event, payload) => {
    return {
      data: payload.data,
      status: "healthy",
      timestamp: new Date().toISOString(),
      version: "1.0.0",
    };
  },
});

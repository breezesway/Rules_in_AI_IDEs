import { z } from "zod";
import packageJson from "../../package.json";

export default defineApiEventHandler({
  validation: z.object({
    data: z.string().optional(),
  }),
  handler: async (event, payload) => {
    return {
      data: payload.data,
      status: "healthy",
      timestamp: new Date().toISOString(),
      version: packageJson.version,
    };
  },
});

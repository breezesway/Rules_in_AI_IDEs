import { z } from "zod";
import packageJson from "../../package.json";

export default defineApiEventHandler({
  validation: z.object({
    data: z.string().optional(),
  }),
  handler: async (event, payload) => {
    return defineApiResponse(event, {
      data: {
        requestPayload: payload.data,
        timestamp: new Date().toISOString(),
        version: packageJson.version,
        status: "healthy",
      },
      statusMessage: "Health check successful",
    });
  },
});

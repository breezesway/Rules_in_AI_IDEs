import type { EventHandler, EventHandlerRequest, H3Event } from "h3";
import { defineEventHandler, getRequestURL, getResponseStatus } from "h3";
import type { z } from "zod";
import { ZodError } from "zod";

type Guard<T> = ReturnType<typeof defineGuard<T>>;

type ApiEventHandler<T extends EventHandlerRequest, D, S extends z.ZodType> = {
  validation: S;
  guards?: Guard<z.infer<S>>[];
  handler: (event: H3Event<T>, payload: z.infer<S>) => Promise<D> | D;
};

export function defineApiEventHandler<
  T extends EventHandlerRequest = EventHandlerRequest,
  D = unknown,
  S extends z.ZodType = z.ZodType
>(
  handlerOrConfig: ApiEventHandler<T, D, S> | EventHandler<T, D>
): EventHandler<T, D> {
  if (typeof handlerOrConfig === "function") {
    return defineEventHandler(handlerOrConfig);
  }

  const { validation, handler, guards } = handlerOrConfig;

  return defineEventHandler<T>(async (event) => {
    try {
      // get the rawData
      const rawData = await getPayload(event);

      // validate the rawData and transform it to the payload
      const payload = await runValidation<S>(rawData, validation);

      // run guards
      await runGuards<S>(event, payload, guards);

      // run the handler
      return handler(event, payload);
    } catch (err) {
      if (err instanceof ZodError) {
        throw createError({
          statusCode: 422,
          statusMessage: `Invalid request payload`,
          data: err,
        });
      }

      if (
        err instanceof Error &&
        "statusCode" in err &&
        "statusMessage" in err
      ) {
        throw err;
      }

      throw createError({
        statusCode: 500,
        statusMessage: "Internal server error",
        cause: err,
      });
    }
  });
}

// Local function to get the payload from the event
// should NOT be exported
async function getPayload(event: H3Event) {
  const method = event.method;

  let payload: Record<string, unknown> = getQuery(event) || {};

  if (["PUT", "POST"].includes(method)) {
    const body = await readBody(event);
    payload = {
      ...payload,
      ...body,
    };
  }

  return {
    ...payload,
    ...event.context.params,
  };
}

// local function to run guards
async function runGuards<T>(event: H3Event, payload: T, guards?: Guard<T>[]) {
  if (!guards) return;
  if (!Array.isArray(guards)) {
    throw createError({
      statusCode: 500,
      statusMessage: `Guards must be an array`,
    });
  }
  await Promise.all(guards.map((guard) => guard(event, payload)));
}

// local function to run validation
async function runValidation<T>(data: unknown, validation: z.ZodType<T>) {
  return await validation.parseAsync(data);
}

export const defineGuard = <T>(
  callback: (event: H3Event, payload: T) => Promise<void>
) => {
  return callback;
};

interface Pagination {
  page: number;
  limit: number;
  total: number;
  currentPageUrl: string;
  firstPageUrl: string;
  lastPageUrl: string;
  nextPageUrl?: string | null;
  prevPageUrl?: string | null;
}

export function definePaginatedApiResponse<T>(
  event: H3Event,
  {
    data,
    statusMessage = "Success!",
    pagination,
  }: {
    data: T;
    statusMessage?: string;
    pagination: Omit<
      Pagination,
      | "currentPageUrl"
      | "firstPageUrl"
      | "lastPageUrl"
      | "nextPageUrl"
      | "prevPageUrl"
    >;
  }
) {
  const url = getRequestURL(event);
  const urlObj = new URL(url);
  urlObj.searchParams.set("page", pagination?.page?.toString() || "1");
  const baseUrl = `${urlObj.protocol}//${urlObj.host}${urlObj.pathname}`;

  // First page URL
  const firstPageUrl = baseUrl;

  // Last page URL
  const lastPageUrl =
    pagination?.total && pagination?.limit
      ? `${baseUrl}?page=${Math.ceil(pagination.total / pagination.limit)}`
      : baseUrl;

  // Next page URL
  const nextPageUrl =
    pagination?.page && pagination?.limit && pagination?.total
      ? pagination.page * pagination.limit < pagination.total
        ? `${baseUrl}?page=${pagination.page + 1}`
        : null
      : null;

  // Previous page URL
  const prevPageUrl =
    pagination?.page && pagination?.page > 1
      ? `${baseUrl}?page=${pagination.page - 1}`
      : null;

  // Current page URL
  const currentPageUrl =
    pagination?.page && pagination?.page > 1
      ? `${baseUrl}?page=${pagination.page}`
      : baseUrl;
  return {
    ...defineApiResponse(event, {
      data,
      statusMessage,
    }),
    pagination: {
      page: pagination?.page || 1,
      limit: pagination?.limit || 10,
      total: pagination?.total || 0,
      currentPageUrl,
      firstPageUrl,
      lastPageUrl,
      nextPageUrl,
      prevPageUrl,
    },
  };
}

export function defineApiResponse<T>(
  event: H3Event,
  {
    data,
    statusMessage = "Success!",
  }: {
    data: T;
    statusMessage?: string;
  }
) {
  const statusCode = getResponseStatus(event);
  const url = getRequestURL(event);

  return {
    error: false,
    url,
    statusMessage,
    statusCode,
    message: statusMessage,
    data,
  };
}

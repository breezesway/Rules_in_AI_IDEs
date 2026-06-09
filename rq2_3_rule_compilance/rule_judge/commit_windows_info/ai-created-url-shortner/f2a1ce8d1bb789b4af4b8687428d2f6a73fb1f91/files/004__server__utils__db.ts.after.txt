import { drizzle } from "drizzle-orm/libsql";
import { createClient } from "@libsql/client";
import config from "../../drizzle.config";
import * as schema from "../db/drizzle-schema";

const client = createClient({ url: config.dbCredentials.url });
const db = drizzle(client, { schema });
export const useDb = () => db;
export const useDbSchema = () => schema;

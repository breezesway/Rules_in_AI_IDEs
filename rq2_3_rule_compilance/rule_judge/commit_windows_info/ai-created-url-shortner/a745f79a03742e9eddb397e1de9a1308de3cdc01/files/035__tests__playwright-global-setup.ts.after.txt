import { spawn } from "child_process";
import fetch from "node-fetch";
import detectPort from "detect-port";

const DEV_SERVER_PORT = 3000;

async function waitForServer(url: string, timeout = 20000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    try {
      // eslint-disable-next-line
      const res = await fetch(url);
      if (res.ok) return;
    } catch {
      console.log(`Waiting for server to start on ${url}`);
    }
    await new Promise((r) => setTimeout(r, 500));
  }
  throw new Error(`Timed out waiting for ${url}`);
}

let serverProcess: ReturnType<typeof spawn> | undefined;

export default async function globalSetup() {
  const port = await detectPort(DEV_SERVER_PORT);

  if (port === DEV_SERVER_PORT) {
    console.log("🚀 Starting Nuxt dev server...");
    serverProcess = spawn("npx", ["nuxi", "dev"], {
      stdio: "inherit",
      shell: true,
    });

    process.env.PLAYWRIGHT_DEV_SERVER_PID = String(serverProcess.pid);
    await waitForServer(`http://localhost:${DEV_SERVER_PORT}`);
  } else {
    console.log("⚡ Reusing existing Nuxt dev server on port 3000");
  }
}

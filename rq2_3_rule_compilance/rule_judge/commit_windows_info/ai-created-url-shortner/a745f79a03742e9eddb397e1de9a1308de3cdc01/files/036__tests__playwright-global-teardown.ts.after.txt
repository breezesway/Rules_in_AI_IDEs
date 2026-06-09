export default async function globalTeardown() {
  const pid = process.env.PLAYWRIGHT_DEV_SERVER_PID;
  if (pid) {
    console.log("🛑 Stopping Nuxt dev server...");
    process.kill(parseInt(pid), "SIGTERM");
  }
}

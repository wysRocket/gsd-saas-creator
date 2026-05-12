/**
 * index.ts — Entry point for the HITL Approver service.
 *
 * Starts the Hono HTTP server and logs the listening URL.
 * Environment variables are read from .env (dev) or the host environment (prod).
 */

import { serve } from "@hono/node-server";
import { app } from "./server.js";

const PORT = parseInt(process.env.PORT ?? "3456", 10);

serve(
  {
    fetch: app.fetch,
    port: PORT,
  },
  (info) => {
    console.log(`[hitl-approver] listening on http://localhost:${info.port}`);
    console.log(
      `[hitl-approver] auth: ${process.env.HITL_API_SECRET ? "enabled" : "DISABLED (dev mode)"}`
    );
    console.log(`[hitl-approver] model: ${process.env.HITL_MODEL ?? "openai/gpt-4o-mini"}`);
    console.log();
    console.log("API endpoints:");
    console.log(`  POST http://localhost:${info.port}/review`);
    console.log(`  GET  http://localhost:${info.port}/review/:id`);
    console.log(`  POST http://localhost:${info.port}/review/:id/respond`);
  }
);

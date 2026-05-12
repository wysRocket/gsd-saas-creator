/**
 * server.ts — Hono HTTP server exposing the HITL review API.
 *
 * Endpoints:
 *
 *   POST /review
 *     Start a review session.
 *     Body: { type: "brief" | "deployment" | "qa_failure", payload: {...} }
 *     → { session_id, status, result?, pending_calls? }
 *
 *   GET /review/:id
 *     Get session status + pending calls.
 *     → { session_id, status, result?, pending_calls? }
 *
 *   POST /review/:id/respond
 *     Submit a human decision for a paused call.
 *     Body: { call_id: string, decision: {...} }
 *     → { session_id, status, result?, pending_calls? }
 *
 *   GET /health
 *     Liveness check.
 *
 * Authentication: Bearer token via HITL_API_SECRET env var.
 * Set HITL_API_SECRET="" to disable auth (dev only).
 */

import { Hono } from "hono";
import { startReview, resumeReview, getSessionView } from "./agent.js";

const app = new Hono();

// ---------------------------------------------------------------------------
// Auth middleware
// ---------------------------------------------------------------------------

const API_SECRET = process.env.HITL_API_SECRET ?? "";

app.use("*", async (c, next) => {
  // Skip auth if secret is empty (dev convenience)
  if (API_SECRET === "") {
    await next();
    return;
  }
  const auth = c.req.header("Authorization") ?? "";
  if (auth !== `Bearer ${API_SECRET}`) {
    return c.json({ error: "Unauthorized" }, 401);
  }
  await next();
});

// ---------------------------------------------------------------------------
// Serialise a session view into the API response shape
// ---------------------------------------------------------------------------

function sessionResponse(
  session: ReturnType<typeof getSessionView>
): Record<string, unknown> {
  if (!session) return { error: "Session not found" };
  return {
    session_id: session.id,
    type: session.type,
    status: session.status,
    created_at: session.createdAt,
    updated_at: session.updatedAt,
    ...(session.result !== null ? { result: session.result } : {}),
    ...(session.pendingCalls.length > 0
      ? { pending_calls: session.pendingCalls }
      : {}),
    ...(session.error ? { error: session.error } : {}),
  };
}

// ---------------------------------------------------------------------------
// Routes
// ---------------------------------------------------------------------------

app.get("/health", (c) =>
  c.json({ status: "ok", service: "hitl-approver", ts: Date.now() })
);

/** POST /review — start a review session */
app.post("/review", async (c) => {
  let body: { type?: unknown; payload?: unknown };
  try {
    body = await c.req.json();
  } catch {
    return c.json({ error: "Invalid JSON body" }, 400);
  }

  const { type, payload } = body;
  if (type !== "brief" && type !== "deployment" && type !== "qa_failure") {
    return c.json(
      { error: "type must be one of: brief, deployment, qa_failure" },
      400
    );
  }
  if (!payload || typeof payload !== "object") {
    return c.json({ error: "payload must be an object" }, 400);
  }

  try {
    const session = await startReview(type, payload);
    const view = getSessionView(session.id);
    return c.json(sessionResponse(view), 202);
  } catch (err) {
    return c.json({ error: String(err) }, 500);
  }
});

/** GET /review/:id — session status */
app.get("/review/:id", (c) => {
  const id = c.req.param("id");
  const view = getSessionView(id);
  if (!view) return c.json({ error: "Session not found" }, 404);
  return c.json(sessionResponse(view));
});

/** POST /review/:id/respond — submit human decision */
app.post("/review/:id/respond", async (c) => {
  const id = c.req.param("id");
  let body: { call_id?: unknown; decision?: unknown };
  try {
    body = await c.req.json();
  } catch {
    return c.json({ error: "Invalid JSON body" }, 400);
  }

  const { call_id, decision } = body;
  if (typeof call_id !== "string" || !call_id) {
    return c.json({ error: "call_id must be a non-empty string" }, 400);
  }
  if (decision === undefined) {
    return c.json({ error: "decision is required" }, 400);
  }

  try {
    const session = await resumeReview(id, call_id, decision);
    const view = getSessionView(session.id);
    return c.json(sessionResponse(view));
  } catch (err) {
    const message = String(err);
    const status = message.includes("not found")
      ? 404
      : message.includes("not awaiting HITL")
      ? 409
      : 500;
    return c.json({ error: message }, status);
  }
});

export { app };

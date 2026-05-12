/**
 * agent.ts — OpenRouter callModel integration with HITL tools.
 *
 * Exports three functions:
 *  - startReview(type, payload)           Start a new HITL review session.
 *  - resumeReview(sessionId, callId, decision)  Resume a paused session.
 *  - getSessionView(sessionId)            Read-only status snapshot.
 */

import { OpenRouter } from "@openrouter/agent";
import {
  reviewBriefTool,
  approveDeploymentTool,
  reviewQaFailuresTool,
} from "./tools.js";
import {
  createSession,
  createStateAccessor,
  generateSessionId,
  getSession,
  updateSession,
  type ReviewType,
  type SessionRecord,
} from "./state.js";

// ---------------------------------------------------------------------------
// OpenRouter client (shared singleton)
// ---------------------------------------------------------------------------

const openrouter = new OpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY ?? "",
});

const HITL_MODEL = process.env.HITL_MODEL ?? "openai/gpt-4o-mini";

// All tools available in this service
const tools = [
  reviewBriefTool,
  approveDeploymentTool,
  reviewQaFailuresTool,
] as const;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Build the agent instruction for each review type. */
function buildInstruction(type: ReviewType, payload: unknown): string {
  const base = `You are the SaaS Pipeline HITL Orchestrator.
Your job is to call exactly ONE tool to review the pipeline artifact provided, then stop.
Do not add commentary before calling the tool. Call the tool immediately.`;

  const payloadJson = JSON.stringify(payload, null, 2);

  switch (type) {
    case "brief":
      return `${base}

Call the \`review_brief\` tool with the following arguments:
${payloadJson}`;

    case "deployment":
      return `${base}

Call the \`approve_deployment\` tool with the following arguments:
${payloadJson}`;

    case "qa_failure":
      return `${base}

Call the \`review_qa_failures\` tool with the following arguments:
${payloadJson}`;
  }
}

/**
 * Run a callModel round and persist the HITL outcome back to the session.
 */
async function runCallModel(
  sessionId: string,
  input: Parameters<typeof openrouter.callModel>[0]["input"],
  instruction: string
): Promise<SessionRecord> {
  const stateAccessor = createStateAccessor(sessionId);

  const result = openrouter.callModel({
    model: HITL_MODEL,
    input,
    instructions: instruction,
    tools,
    state: stateAccessor,
  });

  // Consume the result stream so the SDK completes tool execution
  await result.getText();

  // Read final conversation state
  const snapshot = await (result as any).getState?.();
  const isAwaitingHitl = snapshot?.status === "awaiting_hitl";

  if (isAwaitingHitl) {
    const pendingCalls = await (result as any).getPendingToolCalls?.() ?? [];
    return (
      updateSession(sessionId, {
        status: "awaiting_hitl",
        pendingCalls,
      }) ?? getSession(sessionId)!
    );
  }

  // Completed — extract the tool result from session state
  const session = getSession(sessionId)!;
  const convState = session.conversationState as any;
  const toolResults: unknown[] = convState?.toolResults ?? [];
  const lastResult =
    toolResults.length > 0 ? toolResults[toolResults.length - 1] : null;

  return (
    updateSession(sessionId, {
      status: "completed",
      pendingCalls: [],
      result: lastResult,
    }) ?? session
  );
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Start a new HITL review session.
 * Returns immediately with the session record; if the agent auto-resolves,
 * `status` will be 'completed'; if it pauses, `status` will be 'awaiting_hitl'.
 */
export async function startReview(
  type: ReviewType,
  payload: unknown
): Promise<SessionRecord> {
  const sessionId = generateSessionId();
  const session = createSession(sessionId, type);

  const instruction = buildInstruction(type, payload);

  try {
    return await runCallModel(
      sessionId,
      `Please review this ${type} and use the appropriate tool.`,
      instruction
    );
  } catch (err) {
    return (
      updateSession(sessionId, {
        status: "error",
        error: String(err),
      }) ?? session
    );
  }
}

/**
 * Resume a paused HITL session by supplying the human decision.
 *
 * @param sessionId  The session to resume.
 * @param callId     The `id` from the pending tool call.
 * @param decision   The human's decision (must match the tool's outputSchema).
 */
export async function resumeReview(
  sessionId: string,
  callId: string,
  decision: unknown
): Promise<SessionRecord> {
  const session = getSession(sessionId);
  if (!session) throw new Error(`Session not found: ${sessionId}`);
  if (session.status !== "awaiting_hitl") {
    throw new Error(
      `Session ${sessionId} is not awaiting HITL (status: ${session.status})`
    );
  }

  updateSession(sessionId, { status: "running" });

  const instruction = buildInstruction(session.type, null);

  try {
    return await runCallModel(
      sessionId,
      [
        {
          type: "function_call_output" as const,
          callId,
          output: JSON.stringify(decision),
        },
      ],
      instruction
    );
  } catch (err) {
    return (
      updateSession(sessionId, {
        status: "error",
        error: String(err),
      }) ?? session
    );
  }
}

/**
 * Return a safe, serialisable view of the session (no circular refs).
 */
export function getSessionView(
  sessionId: string
): Omit<SessionRecord, "conversationState"> | undefined {
  const session = getSession(sessionId);
  if (!session) return undefined;
  const { conversationState: _omit, ...view } = session;
  return view;
}

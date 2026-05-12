/**
 * state.ts — In-memory session store for HITL review sessions.
 *
 * Each session tracks:
 *  - The OpenRouter conversation state (persisted between callModel calls)
 *  - Session metadata (type, status, timestamps)
 *  - Pending HITL calls awaiting human decisions
 *
 * Replace the Map store with Redis or a database for production use.
 */

import type { ConversationState } from "@openrouter/agent";
import type { reviewBriefTool, approveDeploymentTool, reviewQaFailuresTool } from "./tools.js";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type ReviewType = "brief" | "deployment" | "qa_failure";

export type SessionStatus =
  | "running"
  | "awaiting_hitl"
  | "completed"
  | "error";

export interface PendingCall {
  id: string;
  name: string;
  arguments: unknown;
}

export interface SessionRecord {
  id: string;
  type: ReviewType;
  status: SessionStatus;
  createdAt: number;
  updatedAt: number;
  /** Calls waiting for a human decision */
  pendingCalls: PendingCall[];
  /** Final result from the agent, available when status === 'completed' */
  result: unknown;
  /** Error message when status === 'error' */
  error?: string;
  /** Opaque OpenRouter conversation state — do not mutate directly */
  conversationState: ConversationState<AllTools> | null;
}

// Union of all tools used in this service — required for correct typing of
// ConversationState and StateAccessor generics.
type AllTools = readonly [
  typeof reviewBriefTool,
  typeof approveDeploymentTool,
  typeof reviewQaFailuresTool
];

// ---------------------------------------------------------------------------
// In-memory store
// ---------------------------------------------------------------------------

const sessions = new Map<string, SessionRecord>();

export function createSession(id: string, type: ReviewType): SessionRecord {
  const record: SessionRecord = {
    id,
    type,
    status: "running",
    createdAt: Date.now(),
    updatedAt: Date.now(),
    pendingCalls: [],
    result: null,
    conversationState: null,
  };
  sessions.set(id, record);
  return record;
}

export function getSession(id: string): SessionRecord | undefined {
  return sessions.get(id);
}

export function updateSession(
  id: string,
  patch: Partial<Omit<SessionRecord, "id" | "createdAt">>
): SessionRecord | undefined {
  const record = sessions.get(id);
  if (!record) return undefined;
  const updated = { ...record, ...patch, updatedAt: Date.now() };
  sessions.set(id, updated);
  return updated;
}

/**
 * Returns a StateAccessor for the given session.
 * The accessor is the bridge between the in-memory store and the OpenRouter SDK.
 */
export function createStateAccessor(sessionId: string) {
  return {
    load: async (): Promise<ConversationState<AllTools> | null> => {
      return sessions.get(sessionId)?.conversationState ?? null;
    },
    save: async (state: ConversationState<AllTools>): Promise<void> => {
      const record = sessions.get(sessionId);
      if (record) {
        sessions.set(sessionId, {
          ...record,
          conversationState: state,
          updatedAt: Date.now(),
        });
      }
    },
  };
}

/** Generate a short unique session ID. */
export function generateSessionId(): string {
  return `hitl-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

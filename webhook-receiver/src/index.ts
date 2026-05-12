/**
 * saas-pipeline-webhook — Cloudflare Worker
 * ==========================================
 * Receives GitHub `projects_v2_item.edited` and `issue_comment.created`
 * webhook events, verifies the GitHub HMAC signature, enriches the event from
 * GitHub Projects v2, and fires a `repository_dispatch` to gsd-saas-creator.
 *
 * Deploy:
 *   cd webhook-receiver
 *   wrangler secret put GITHUB_WEBHOOK_SECRET
 *   wrangler secret put GH_TOKEN
 *   wrangler secret put REPO_OWNER         # e.g. wysRocket
 *   wrangler secret put REPO_NAME          # gsd-saas-creator
 *   wrangler deploy
 *
 * GitHub Webhook setup:
 *   org: SaaS-Pretty-Projects → Settings → Webhooks → Add webhook
 *   Payload URL:  https://saas-pipeline-webhook.<your-subdomain>.workers.dev/webhook
 *   Content type: application/json
 *   Secret:       <same as GITHUB_WEBHOOK_SECRET>
 *   Events:       Projects v2 item events + Issue comments
 */

export interface Env {
  GITHUB_WEBHOOK_SECRET: string;
  GH_TOKEN: string;
  REPO_OWNER: string;
  REPO_NAME: string;
}

const STAGE_FIELD_ID = "PVTSSF_lADOEHzfoM4BU-0MzhQD56k";
const NOTES_FIELD_ID = "PVTF_lADOEHzfoM4BU-0MzhP_kGg";
const REPO_URL_FIELD_ID = "PVTF_lADOEHzfoM4BU-0MzhQhuOI";
const AI_STUDIO_FIELD_ID = "PVTF_lADOEHzfoM4BU-0MzhQtV7M";
const VERTICAL_FIELD_ID = "PVTSSF_lADOEHzfoM4BU-0MzhQhuNE";
const COMPETITOR_URL_FIELD_NAME = "Competitor URL";

const STAGE_OPTION_TO_NAME: Record<string, string> = {
  cddac2f5: "brief",
  "0d90f5af": "clarification",
  "67a099a3": "design_md",
  e471f317: "stitch_prompt",
  "5339ae55": "designs_ready",
  cda08427: "ai_studio",
  "58cac058": "in_progress",
  e7d47d45: "revisions",
  "5198760c": "ready_for_prod",
  f01a3972: "launched",
  "79fb3f03": "operating",
  c15f4a82: "done",
};

const STAGE_LABEL_TO_NAME: Record<string, string> = {
  Brief: "brief",
  Clarification: "clarification",
  "Design.md": "design_md",
  "STITCH Prompt": "stitch_prompt",
  "Designs Ready": "designs_ready",
  "AI Studio": "ai_studio",
  "In Progress": "in_progress",
  Revisions: "revisions",
  "Ready for Prod": "ready_for_prod",
  Launched: "launched",
  Operating: "operating",
  Done: "done",
};

// ---------------------------------------------------------------------------
// HMAC-SHA256 signature verification
// ---------------------------------------------------------------------------

async function verifySignature(
  secret: string,
  signature: string,
  body: string
): Promise<boolean> {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, encoder.encode(body));
  const hex = Array.from(new Uint8Array(sig))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
  const expected = `sha256=${hex}`;
  // Constant-time comparison
  if (expected.length !== signature.length) return false;
  let diff = 0;
  for (let i = 0; i < expected.length; i++) {
    diff |= expected.charCodeAt(i) ^ signature.charCodeAt(i);
  }
  return diff === 0;
}

// ---------------------------------------------------------------------------
// Event parsing
// ---------------------------------------------------------------------------

type FieldChange = {
  field_name?: string;
  field_id?: string;
  field_node_id?: string;
  field_type?: string;
  to?: {
    id?: string;
    name?: string;
    optionId?: string;
    option_id?: string;
    single_select_option_id?: string;
    title?: string;
    date?: string;
    text?: string;
  };
};

function extractFieldChange(payload: any): FieldChange | null {
  return payload?.changes?.field_value ?? null;
}

function extractStageOptionId(change: FieldChange | null): string {
  return (
    change?.to?.id ??
    change?.to?.optionId ??
    change?.to?.option_id ??
    change?.to?.single_select_option_id ??
    ""
  );
}

function isStageFieldChange(change: FieldChange | null): boolean {
  if (!change) return false;
  if (change.field_node_id) return change.field_node_id === STAGE_FIELD_ID;
  if (change.field_id) return change.field_id === STAGE_FIELD_ID;
  return change.field_name === "Stage";
}

function deriveRepoName(repoUrl: string, fallbackRepoName: string): string {
  if (!repoUrl) return fallbackRepoName;

  const cleaned = repoUrl
    .trim()
    .replace(/[?#].*$/, "")
    .replace(/\/$/, "")
    .replace(/\.git$/, "");

  return cleaned.split("/").pop() || fallbackRepoName;
}

// ---------------------------------------------------------------------------
// Fetch project item metadata via GitHub GraphQL
// ---------------------------------------------------------------------------

type FieldValueNode = {
  text?: string;
  name?: string;
  field?: {
    id?: string;
    name?: string;
  };
};

type BoardItemFields = {
  itemId: string;
  issueNumber: number | null;
  repositoryName: string;
  title: string;
  stage: string;
  notes: string;
  repoUrl: string;
  aiStudio: string;
  vertical: string;
  competitorUrl: string;
};

async function githubGraphql(token: string, query: string, variables: Record<string, unknown>): Promise<any> {
  const resp = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      "User-Agent": "saas-pipeline-webhook/1.0",
    },
    body: JSON.stringify({ query, variables }),
  });

  if (!resp.ok) {
    throw new Error(`GitHub GraphQL request failed with ${resp.status}`);
  }

  const data: any = await resp.json();
  if (data.errors?.length) {
    throw new Error(`GitHub GraphQL errors: ${JSON.stringify(data.errors)}`);
  }

  return data;
}

async function fetchItemFields(token: string, itemId: string): Promise<BoardItemFields | null> {
  const query = `
    query($itemId: ID!) {
      node(id: $itemId) {
        ... on ProjectV2Item {
          id
          content {
            ... on Issue {
              title
              number
              repository { name }
            }
            ... on PullRequest {
              title
              number
              repository { name }
            }
            ... on DraftIssue {
              title
            }
          }
          fieldValues(first: 20) {
            nodes {
              ... on ProjectV2ItemFieldTextValue {
                text
                field { ... on ProjectV2FieldCommon { id name } }
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2FieldCommon { id name } }
              }
            }
          }
        }
      }
    }
  `;

  const data = await githubGraphql(token, query, { itemId });
  const item = data?.data?.node;
  if (!item?.id) return null;

  const fields: BoardItemFields = {
    itemId: item.id,
    issueNumber: item.content?.number ?? null,
    repositoryName: item.content?.repository?.name ?? "",
    title: item.content?.title ?? "",
    stage: "",
    notes: "",
    repoUrl: "",
    aiStudio: "",
    vertical: "",
    competitorUrl: "",
  };

  for (const fv of item.fieldValues?.nodes ?? []) {
    const node = fv as FieldValueNode;
    const fieldId = node.field?.id ?? "";
    const fieldName = node.field?.name ?? "";
    const value = node.text ?? node.name ?? "";

    if (fieldId === STAGE_FIELD_ID) fields.stage = value;
    if (fieldId === NOTES_FIELD_ID) fields.notes = value;
    if (fieldId === REPO_URL_FIELD_ID) fields.repoUrl = value;
    if (fieldId === AI_STUDIO_FIELD_ID) fields.aiStudio = value;
    if (fieldId === VERTICAL_FIELD_ID) fields.vertical = value;
    if (fieldName === COMPETITOR_URL_FIELD_NAME) fields.competitorUrl = value;
  }

  return fields;
}

async function findProjectItemIdForIssue(token: string, issueNodeId: string): Promise<string> {
  const query = `
    query($issueId: ID!) {
      node(id: $issueId) {
        ... on Issue {
          projectItems(first: 20) {
            nodes {
              id
              fieldValues(first: 10) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    field { ... on ProjectV2FieldCommon { id name } }
                  }
                  ... on ProjectV2ItemFieldTextValue {
                    field { ... on ProjectV2FieldCommon { id name } }
                  }
                }
              }
            }
          }
        }
      }
    }
  `;

  const data = await githubGraphql(token, query, { issueId: issueNodeId });
  const items: any[] = data?.data?.node?.projectItems?.nodes ?? [];
  const stageItem = items.find((item) =>
    (item.fieldValues?.nodes ?? []).some((fv: FieldValueNode) => fv.field?.id === STAGE_FIELD_ID)
  );

  return stageItem?.id ?? items[0]?.id ?? "";
}

// ---------------------------------------------------------------------------
// Fire repository_dispatch to gsd-saas-creator
// ---------------------------------------------------------------------------

type StageDispatchPayload = {
  stage: string;
  item_id: string;
  issue_number: number;
  repo_name: string;
  project_name: string;
  competitor_url: string;
  vertical: string;
  notes: string;
  comment_body: string;
};

async function dispatchStageChange(
  token: string,
  owner: string,
  repo: string,
  payload: StageDispatchPayload
): Promise<boolean> {
  const url = `https://api.github.com/repos/${owner}/${repo}/dispatches`;
  const resp = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      Accept: "application/vnd.github+json",
      "User-Agent": "saas-pipeline-webhook/1.0",
    },
    body: JSON.stringify({
      event_type: "stage_changed",
      client_payload: payload,
    }),
  });
  return resp.status === 204;
}

function buildDispatchPayload(
  stage: string,
  item: BoardItemFields,
  eventRepoName: string,
  fallbackIssueNumber: number | null,
  commentBody: string
): StageDispatchPayload {
  const repoName = deriveRepoName(item.repoUrl, item.repositoryName || eventRepoName);

  return {
    stage,
    item_id: item.itemId,
    issue_number: item.issueNumber ?? fallbackIssueNumber ?? 0,
    repo_name: repoName,
    project_name: item.title || repoName,
    competitor_url: item.competitorUrl,
    vertical: item.vertical,
    notes: item.notes,
    comment_body: commentBody,
  };
}

// ---------------------------------------------------------------------------
// Main handler
// ---------------------------------------------------------------------------

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Health check
    if (url.pathname === "/" || url.pathname === "/health") {
      return new Response(JSON.stringify({ status: "ok", stages: STAGE_OPTION_TO_NAME }), {
        headers: { "Content-Type": "application/json" },
      });
    }

    if (url.pathname !== "/webhook") {
      return new Response("Not Found", { status: 404 });
    }

    if (request.method !== "POST") {
      return new Response("Method Not Allowed", { status: 405 });
    }

    const body = await request.text();
    const signature = request.headers.get("x-hub-signature-256") ?? "";
    const event = request.headers.get("x-github-event") ?? "";

    // Verify HMAC signature
    if (env.GITHUB_WEBHOOK_SECRET) {
      const valid = await verifySignature(env.GITHUB_WEBHOOK_SECRET, signature, body);
      if (!valid) {
        return new Response("Forbidden: invalid signature", { status: 403 });
      }
    }

    let payload: any;
    try {
      payload = JSON.parse(body);
    } catch {
      return new Response("Bad Request", { status: 400 });
    }

    let stage = "";
    let itemId = "";
    let commentBody = "";
    let fallbackIssueNumber: number | null = null;
    const eventRepoName: string = payload?.repository?.name ?? "";

    if (event === "projects_v2_item") {
      if (payload.action !== "edited") {
        return new Response("Ignored (action)", { status: 200 });
      }

      const change = extractFieldChange(payload);
      if (!isStageFieldChange(change)) {
        return new Response("Ignored (field)", { status: 200 });
      }

      const optionId = extractStageOptionId(change);
      stage = STAGE_OPTION_TO_NAME[optionId] ?? STAGE_LABEL_TO_NAME[change?.to?.name ?? ""] ?? "";
      if (!stage) {
        return new Response(`Ignored (stage_option_id=${optionId})`, { status: 200 });
      }

      itemId = payload?.projects_v2_item?.node_id ?? "";
    } else if (event === "issue_comment") {
      if (payload.action !== "created") {
        return new Response("Ignored (action)", { status: 200 });
      }

      stage = "revisions";
      commentBody = payload?.comment?.body ?? "";
      fallbackIssueNumber = payload?.issue?.number ?? null;

      const issueNodeId: string = payload?.issue?.node_id ?? "";
      if (!issueNodeId) {
        return new Response("Ignored (missing issue node id)", { status: 200 });
      }

      itemId = await findProjectItemIdForIssue(env.GH_TOKEN, issueNodeId);
    } else {
      return new Response("Ignored", { status: 200 });
    }

    if (!itemId) {
      return new Response("Ignored (missing item id)", { status: 200 });
    }

    let item: BoardItemFields | null;
    try {
      item = await fetchItemFields(env.GH_TOKEN, itemId);
    } catch (error) {
      console.error("[pipeline] failed to fetch item fields", error);
      return new Response("Failed to fetch item fields", { status: 500 });
    }

    if (!item) {
      return new Response("Ignored (item not found)", { status: 200 });
    }

    const dispatchPayload = buildDispatchPayload(
      stage,
      item,
      eventRepoName,
      fallbackIssueNumber,
      commentBody
    );

    const dispatched = await dispatchStageChange(
      env.GH_TOKEN,
      env.REPO_OWNER,
      env.REPO_NAME,
      dispatchPayload
    );

    if (dispatched) {
      console.log(
        `[pipeline] dispatched stage_changed for ${dispatchPayload.project_name} (${dispatchPayload.repo_name}) stage=${stage}`
      );
      return new Response(
        JSON.stringify({ message: "Stage dispatched", repo: dispatchPayload.repo_name, stage }),
        { headers: { "Content-Type": "application/json" }, status: 200 }
      );
    }

    return new Response("Dispatch failed", { status: 500 });
  },
};

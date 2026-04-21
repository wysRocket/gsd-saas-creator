/**
 * saas-pipeline-webhook — Cloudflare Worker
 * ==========================================
 * Receives GitHub `projects_v2_item.edited` webhook events and
 * fires a `repository_dispatch` to gsd-saas-creator when the Stage
 * field changes to "Design.md".
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
 *   Events:       Projects v2 item events  (or "Let me select" → projects_v2_item)
 */

export interface Env {
  GITHUB_WEBHOOK_SECRET: string;
  GH_TOKEN: string;
  REPO_OWNER: string;
  REPO_NAME: string;
}

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
// Parse field values from the projects_v2_item event
// ---------------------------------------------------------------------------

type FieldChange = {
  field_name?: string;
  field_type?: string;
  to?: { name?: string; title?: string; date?: string; text?: string };
};

function extractFieldChange(payload: any): FieldChange | null {
  return payload?.changes?.field_value ?? null;
}

// ---------------------------------------------------------------------------
// Fetch project item metadata via GitHub GraphQL (to get Competitor URL etc.)
// ---------------------------------------------------------------------------

async function fetchItemFields(
  token: string,
  projectId: string,
  itemId: string
): Promise<Record<string, string>> {
  const query = `
    query($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          items(first: 100) {
            nodes {
              id
              fieldValues(first: 20) {
                nodes {
                  ... on ProjectV2ItemFieldTextValue {
                    text
                    field { ... on ProjectV2Field { name } }
                  }
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field { ... on ProjectV2SingleSelectField { name } }
                  }
                  ... on ProjectV2ItemFieldNumberValue {
                    number
                    field { ... on ProjectV2Field { name } }
                  }
                }
              }
            }
          }
        }
      }
    }
  `;

  const resp = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      "User-Agent": "saas-pipeline-webhook/1.0",
    },
    body: JSON.stringify({ query, variables: { projectId } }),
  });

  if (!resp.ok) return {};

  const data: any = await resp.json();
  const items: any[] = data?.data?.node?.items?.nodes ?? [];
  const item = items.find((n: any) => n.id === itemId);
  if (!item) return {};

  const fields: Record<string, string> = {};
  for (const fv of item.fieldValues?.nodes ?? []) {
    const name: string = fv.field?.name ?? "";
    const value: string = fv.text ?? fv.name ?? String(fv.number ?? "");
    if (name && value) fields[name] = value;
  }
  return fields;
}

// ---------------------------------------------------------------------------
// Fire repository_dispatch to gsd-saas-creator
// ---------------------------------------------------------------------------

async function dispatchStageChange(
  token: string,
  owner: string,
  repo: string,
  payload: Record<string, unknown>
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

// ---------------------------------------------------------------------------
// Main handler
// ---------------------------------------------------------------------------

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Health check
    if (url.pathname === "/" || url.pathname === "/health") {
      return new Response(JSON.stringify({ status: "ok" }), {
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

    // Only handle projects_v2_item.edited
    if (event !== "projects_v2_item") {
      return new Response("Ignored", { status: 200 });
    }

    let payload: any;
    try {
      payload = JSON.parse(body);
    } catch {
      return new Response("Bad Request", { status: 400 });
    }

    if (payload.action !== "edited") {
      return new Response("Ignored (action)", { status: 200 });
    }

    const change = extractFieldChange(payload);
    const newStage: string = change?.to?.name ?? "";

    // Only trigger on "Design.md" stage
    if (newStage !== "Design.md") {
      return new Response(`Ignored (stage=${newStage})`, { status: 200 });
    }

    const projectId: string = payload?.project_v2?.node_id ?? "";
    const itemId: string = payload?.projects_v2_item?.node_id ?? "";

    // Fetch all field values for this item
    const fields = await fetchItemFields(env.GH_TOKEN, projectId, itemId);

    const competitorUrl: string = fields["Competitor URL"] ?? "";
    const repoUrl: string = fields["Repo URL"] ?? "";
    const vertical: string = fields["Vertical"] ?? "";
    const priority: string = fields["Priority"] ?? "5";

    // Derive repo name from Repo URL or item title
    const repoName: string =
      repoUrl
        ? repoUrl.replace(/\/$/, "").split("/").pop() ?? ""
        : fields["Title"] ?? "untitled-saas";

    const projectName: string = fields["Title"] ?? repoName;

    if (!competitorUrl) {
      return new Response(
        JSON.stringify({ message: "Competitor URL not set — skipping pipeline trigger" }),
        { headers: { "Content-Type": "application/json" }, status: 200 }
      );
    }

    // Fire dispatch
    const dispatched = await dispatchStageChange(
      env.GH_TOKEN,
      env.REPO_OWNER,
      env.REPO_NAME,
      {
        item_id: itemId,
        project_id: projectId,
        new_stage: newStage,
        competitor_url: competitorUrl,
        repo_name: repoName,
        project_name: projectName,
        vertical,
        priority,
      }
    );

    if (dispatched) {
      console.log(`[pipeline] dispatched stage_changed for ${projectName} (${repoName})`);
      return new Response(
        JSON.stringify({ message: "Pipeline triggered", repo: repoName }),
        { headers: { "Content-Type": "application/json" }, status: 200 }
      );
    } else {
      return new Response("Dispatch failed", { status: 500 });
    }
  },
};

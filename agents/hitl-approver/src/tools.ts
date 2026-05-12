/**
 * tools.ts — HITL tool definitions for the SaaS pipeline.
 *
 * Three tools are defined:
 *  - reviewBriefTool     Auto-approve quality briefs; escalate weak ones.
 *  - approveDeploymentTool  Always escalate — Firebase deploys need human eyes.
 *  - reviewQaFailuresTool  Auto-approve non-critical QA; escalate critical failures.
 */

import { tool } from "@openrouter/agent";
import { z } from "zod";

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

const TEMPLATE_PLACEHOLDER_RE = /\[\.\.\.?\]|\{\{[^}]+\}\}/;
const REQUIRED_BRIEF_SECTIONS = [
  "Overview",
  "Target User",
  "Core Value",
  "Core Feature Set",
  "Pricing",
];

function briefQualityScore(content: string, wordCount: number): number {
  let score = 0;
  if (wordCount >= 300) score += 40;
  else if (wordCount >= 150) score += 20;
  if (!TEMPLATE_PLACEHOLDER_RE.test(content)) score += 30;
  const presentSections = REQUIRED_BRIEF_SECTIONS.filter((s) =>
    content.includes(s)
  );
  score += (presentSections.length / REQUIRED_BRIEF_SECTIONS.length) * 30;
  return Math.round(score);
}

// ---------------------------------------------------------------------------
// Tool: review_brief
// ---------------------------------------------------------------------------

export const reviewBriefTool = tool({
  name: "review_brief",
  description:
    "Review a generated brief.md for quality. Auto-approves if it meets all quality standards; escalates to a human reviewer if it is too short, missing sections, or contains template placeholders.",
  inputSchema: z.object({
    project_name: z.string().describe("Name of the SaaS project"),
    brief_content: z.string().describe("Full content of the generated brief.md"),
    competitor_url: z.string().describe("Competitor URL used to generate the brief"),
    word_count: z.number().int().describe("Word count of the brief"),
  }),
  outputSchema: z.object({
    approved: z.boolean().describe("Whether the brief is approved to proceed"),
    feedback: z
      .string()
      .describe("Detailed feedback on the brief quality or approval reason"),
    quality_score: z
      .number()
      .int()
      .min(0)
      .max(100)
      .describe("Quality score 0–100"),
    reviewed_at: z.number().optional().describe("Unix timestamp of human review"),
  }),

  onToolCalled: async (input) => {
    const score = briefQualityScore(input.brief_content, input.word_count);

    // Auto-approve: score >= 80, no placeholders, word count >= 300
    if (
      score >= 80 &&
      input.word_count >= 300 &&
      !TEMPLATE_PLACEHOLDER_RE.test(input.brief_content)
    ) {
      return {
        approved: true,
        feedback: `Auto-approved: quality score ${score}/100. All sections present, no template placeholders, word count ${input.word_count}.`,
        quality_score: score,
      };
    }

    // Escalate to human — return null to pause the loop
    return null;
  },

  onResponseReceived: async (raw) => {
    const result = z
      .object({
        approved: z.boolean(),
        feedback: z.string(),
        quality_score: z.number().int().min(0).max(100).optional().default(0),
      })
      .parse(raw);

    return {
      ...result,
      reviewed_at: Date.now(),
    };
  },
});

// ---------------------------------------------------------------------------
// Tool: approve_deployment
// ---------------------------------------------------------------------------

export const approveDeploymentTool = tool({
  name: "approve_deployment",
  description:
    "Request human approval before deploying to Firebase. This tool always escalates — no automated deployment is permitted without explicit human sign-off.",
  inputSchema: z.object({
    repo_name: z.string().describe("Target GitHub repo name"),
    project_name: z.string().describe("Human-readable project name"),
    firebase_project: z
      .string()
      .describe("Firebase project ID that will be deployed to"),
    qa_summary: z
      .string()
      .describe("One-paragraph summary of what QA validated"),
    scaffold_file_count: z
      .number()
      .int()
      .optional()
      .describe("Number of files in the scaffold"),
  }),
  outputSchema: z.object({
    approved: z.boolean().describe("Whether deployment is approved"),
    notes: z.string().describe("Reviewer notes or reason for rejection"),
    approved_by: z.string().optional().describe("Reviewer identifier"),
    approved_at: z.number().optional().describe("Unix timestamp of approval"),
  }),

  // Always escalate — deployment is never auto-approved
  onToolCalled: async (_input) => null,

  onResponseReceived: async (raw) => {
    const result = z
      .object({
        approved: z.boolean(),
        notes: z.string(),
        approved_by: z.string().optional(),
      })
      .parse(raw);

    return {
      ...result,
      approved_at: Date.now(),
    };
  },
});

// ---------------------------------------------------------------------------
// Tool: review_qa_failures
// ---------------------------------------------------------------------------

const QaActionSchema = z.enum(["approve", "fix_and_retry", "halt"]);

export const reviewQaFailuresTool = tool({
  name: "review_qa_failures",
  description:
    "Review QA failures and decide whether to approve anyway, request a fix-and-retry, or halt the pipeline. Auto-approves when the only failures are non-critical npm test stubs; escalates on missing files, invalid tokens, or template placeholders.",
  inputSchema: z.object({
    repo_name: z.string().describe("Repository name"),
    stage: z.string().describe("Pipeline stage where QA failed"),
    failures: z
      .array(z.string())
      .describe("List of specific failure messages from validate_all_stages"),
    qa_output: z.string().describe("Full QA output text"),
  }),
  outputSchema: z.object({
    action: QaActionSchema.describe(
      "'approve' = proceed anyway; 'fix_and_retry' = pipeline should fix + re-run QA; 'halt' = stop pipeline"
    ),
    instructions: z.string().describe("Instructions for the pipeline on what to do next"),
    reviewed_at: z.number().optional(),
  }),

  onToolCalled: async (input) => {
    // Critical failure patterns — must always escalate
    const criticalPatterns = [
      /missing required/i,
      /template placeholder/i,
      /invalid.*token/i,
      /no.*hex color/i,
      /file not found/i,
    ];

    const hasCritical = input.failures.some((f) =>
      criticalPatterns.some((re) => re.test(f))
    );

    if (hasCritical) {
      // Pause for human review
      return null;
    }

    // Non-critical only (npm test stubs, lint warnings) — auto-approve
    return {
      action: "approve" as const,
      instructions:
        "Non-critical QA failures only (likely npm test stubs). Proceeding to deployment.",
    };
  },

  onResponseReceived: async (raw) => {
    const result = z
      .object({
        action: QaActionSchema,
        instructions: z.string(),
      })
      .parse(raw);

    return {
      ...result,
      reviewed_at: Date.now(),
    };
  },
});

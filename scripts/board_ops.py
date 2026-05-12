import requests

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ID = "PVT_kwDOEHzfoM4BU-0M"
STAGE_FIELD_ID = "PVTSSF_lADOEHzfoM4BU-0MzhQD56k"
REPO_URL_FIELD_ID = "PVTF_lADOEHzfoM4BU-0MzhQhuOI"
AI_STUDIO_FIELD_ID = "PVTF_lADOEHzfoM4BU-0MzhQtV7M"
ORG = "SaaS-Pretty-Projects"

STAGE_IDS = {
    "brief": "cddac2f5",
    "clarification": "0d90f5af",
    "design_md": "67a099a3",
    "stitch_prompt": "e471f317",
    "designs_ready": "5339ae55",
    "ai_studio": "cda08427",
    "in_progress": "58cac058",
    "revisions": "e7d47d45",
    "ready_for_prod": "5198760c",
    "launched": "f01a3972",
    "operating": "79fb3f03",
    "done": "c15f4a82"
}

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def post_comment(repo_full_name, issue_number, body, token):
    """POST a comment to a GitHub issue/PR."""
    url = f"https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"body": body}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[warning] Failed to post comment: {e}")
        return None

def update_stage(item_id, stage_key, token):
    """Update the 'Stage' single-select field of a project item."""
    if stage_key not in STAGE_IDS:
        print(f"[warning] Unknown stage key: {stage_key}")
        return None

    option_id = STAGE_IDS[stage_key]
    mutation = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId,
        itemId: $itemId,
        fieldId: $fieldId,
        value: { singleSelectOptionId: $optionId }
      }) {
        projectV2Item { id }
      }
    }
    """
    variables = {
        "projectId": PROJECT_ID,
        "itemId": item_id,
        "fieldId": STAGE_FIELD_ID,
        "optionId": option_id
    }
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(GITHUB_GRAPHQL_URL, headers=headers, json={"query": mutation, "variables": variables})
        response.raise_for_status()
        result = response.json()
        if "errors" in result:
            print(f"[warning] GraphQL errors in update_stage: {result['errors']}")
            return None
        return result
    except Exception as e:
        print(f"[warning] Failed to update stage: {e}")
        return None

def update_text_field(item_id, field_id, value, token):
    """Update a text field of a project item."""
    mutation = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId,
        itemId: $itemId,
        fieldId: $fieldId,
        value: { text: $value }
      }) {
        projectV2Item { id }
      }
    }
    """
    variables = {
        "projectId": PROJECT_ID,
        "itemId": item_id,
        "fieldId": field_id,
        "value": value
    }
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(GITHUB_GRAPHQL_URL, headers=headers, json={"query": mutation, "variables": variables})
        response.raise_for_status()
        result = response.json()
        if "errors" in result:
            print(f"[warning] GraphQL errors in update_text_field: {result['errors']}")
            return None
        return result
    except Exception as e:
        print(f"[warning] Failed to update text field {field_id}: {e}")
        return None

def get_item_fields(item_id, token):
    """Query a ProjectV2Item's field values and return as a flat dict {field_name: value}."""
    query = """
    query($itemId: ID!) {
      node(id: $itemId) {
        ... on ProjectV2Item {
          fieldValues(first: 100) {
            nodes {
              ... on ProjectV2ItemFieldTextValue {
                text
                field { ... on ProjectV2FieldCommon { name id } }
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2FieldCommon { name id } }
              }
            }
          }
        }
      }
    }
    """
    variables = {"itemId": item_id}
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(GITHUB_GRAPHQL_URL, headers=headers, json={"query": query, "variables": variables})
        response.raise_for_status()
        data = response.json()
        if "errors" in data:
            print(f"[warning] GraphQL errors in get_item_fields: {data['errors']}")
            return {}
        nodes = data.get("data", {}).get("node", {}).get("fieldValues", {}).get("nodes", [])
        
        flat = {}
        for node in nodes:
            field = node.get("field", {})
            field_name = field.get("name")
            if not field_name:
                continue
            if "text" in node:
                flat[field_name] = node["text"]
            elif "name" in node:
                flat[field_name] = node["name"]
        return flat
    except Exception as e:
        print(f"[warning] Failed to get item fields: {e}")
        return {}

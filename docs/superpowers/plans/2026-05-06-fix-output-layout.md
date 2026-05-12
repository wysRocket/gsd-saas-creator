# Fix Pipeline Output Layout Mismatch

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ensure all pipeline artifacts are generated under `output/<repo-name>/` and fix argument parsing inconsistencies where `--repo-dir` was ignored or misinterpreted.

**Architecture:** Standardize all script entry points to use `argparse` with a consistent `--repo-dir` parameter. Update `orchestrate.py` to ensure it passes the correct arguments. Reorganize existing `output/` files into a dedicated subfolder.

**Tech Stack:** Python (argparse, pathlib)

---

### Task 1: Fix `scaffold.py` Argument Parsing

**Files:**
- Modify: `scripts/scaffold.py`

- [ ] **Step 1: Update `scaffold.py` to use `argparse`**

Replace positional `sys.argv[1]` logic with `argparse` supporting `--repo-dir` and `--name`.

```python
def main():
    parser = argparse.ArgumentParser(description="Scaffold project")
    parser.add_argument("output_dir", nargs="?", help="Positional output dir (legacy)")
    parser.add_argument("--repo-dir", help="Target repo directory")
    parser.add_argument("--name", help="Project name (overrides PROJECT_NAME env)")
    args = parser.parse_args()

    global OUTPUT_DIR, PROJECT_NAME
    if args.repo_dir:
        OUTPUT_DIR = Path(args.repo_dir)
    elif args.output_dir:
        OUTPUT_DIR = Path(args.output_dir)
    # else use default logic

    if args.name:
        PROJECT_NAME = args.name
    
    scaffold()
```

- [ ] **Step 2: Verify `scaffold.py` handles `--repo-dir` correctly**

Run: `python scripts/scaffold.py --repo-dir output/test-scaffold --name "Test Project"`
Expected: Files created in `output/test-scaffold/`

- [ ] **Step 3: Commit**

```bash
git add scripts/scaffold.py
git commit -m "fix: support --repo-dir and --name in scaffold.py"
```

### Task 2: Fix `deploy.py` Argument Parsing

**Files:**
- Modify: `scripts/deploy.py`

- [ ] **Step 1: Update `deploy.py` to support `--repo-dir`**

Even if not fully used yet for pathing within `deploy.py`, it must accept the argument if `orchestrate.py` passes it. Ideally, it should `cd` or use it as a base path.

```python
    parser.add_argument("--repo-dir", help="Target repo directory")
```

Update `deploy()` to use `repo_dir` if provided.

- [ ] **Step 2: Verify `deploy.py` accepts `--repo-dir`**

Run: `python scripts/deploy.py --dry-run --repo-dir output/test-repo`
Expected: Should not fail with "unrecognized arguments"

- [ ] **Step 3: Commit**

```bash
git add scripts/deploy.py
git commit -m "fix: support --repo-dir in deploy.py for orchestrator compatibility"
```

### Task 3: Standardize Generator Defaults

**Files:**
- Modify: `scripts/generate_brief.py`
- Modify: `scripts/generate_design_md.py`
- Modify: `scripts/generate_stitch_prompt.py`
- Modify: `scripts/generate_stitch_design_md.py`

- [ ] **Step 1: Update default `--repo-dir` in generators**

Change default from `./output` to `./output/default` (or similar) to avoid root clutter.

- [ ] **Step 2: Commit**

```bash
git add scripts/generate_brief.py scripts/generate_design_md.py scripts/generate_stitch_prompt.py scripts/generate_stitch_design_md.py
git commit -m "chore: standardize generator defaults to avoid root output clutter"
```

### Task 4: Reorganize Existing Artifacts

- [ ] **Step 1: Move misplaced artifacts**

Move `output/brief.md`, `output/design.md`, `output/stitch-prompt.md`, and `output/design/` to `output/arcane-ops/`.

```bash
mkdir -p output/arcane-ops
mv output/brief.md output/design.md output/stitch-prompt.md output/arcane-ops/
mv output/design output/arcane-ops/
```

- [ ] **Step 2: Verify structure**

Run: `ls -R output/arcane-ops`

- [ ] **Step 3: Commit**

```bash
git add output/
git commit -m "refactor: reorganize misplaced artifacts into arcane-ops subfolder"
```

### Task 5: Final Validation with `orchestrate.py`

- [ ] **Step 1: Run a dry run or manual test of orchestrate stages**

Run: `python scripts/orchestrate.py --stage brief --repo-name test-project --project-name "Test Project" --competitor-url "https://example.com" --vertical "SaaS"`
Expected: Artifacts in `output/test-project/`

- [ ] **Step 2: Verify no files were created in `output/` root**

- [ ] **Step 3: Commit**

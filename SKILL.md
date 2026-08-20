---
name: daily-mail-wiki-report
description: Orchestrate a scheduled Outlook-to-automotive-wiki reporting workflow. Use when Codex needs to run or maintain the daily automation that reads target Outlook emails, downloads attachments, converts documents to Markdown, imports them into the local automotive LLM wiki, searches wiki context, generates an analysis report, and sends the report through Outlook.
---

# Daily Mail Wiki Report

## Overview

Use this skill to run and maintain the fastest-landed daily automation for Outlook mail intake, automotive wiki retrieval, optional attachment ingestion, wiki-grounded model answering, report generation, and Outlook/SMTP report delivery.

The main executable is `D:\employee agent\scripts\run_daily_report.py`. It uses:

- `../outlook-access` for Outlook COM search and sending.
- IMAP/SMTP settings in `config.yaml` when Outlook COM is unavailable.
- `D:\\employee agent` for wiki search and document conversion through `work/mineru_api_convert.py`.
- An agent runtime folder under `D:\employee agent\runtime`.

## Quick Start

1. Create or edit the workflow config:

```powershell
New-Item -ItemType Directory -Force "D:\employee agent" | Out-Null
Copy-Item "D:\employee agent\config.example.yaml" "D:\employee agent\config.yaml"
```

2. Run a manual dry run:

```powershell
python "D:\employee agent\scripts\run_daily_report.py" --config "D:\employee agent\config.yaml"
```

If `workflow.mode: codex_assisted`, the run stops after creating `model_input.md/json` and waits for a manual Codex-authored answer/report. Use `--send-report <path>` later to mail an existing final report.

3. If Outlook COM is unavailable, set `mail.backend: imap` and `send.backend: smtp`, then fill the `mail.imap` and `send.smtp` blocks in `config.yaml`.

4. Put the model key directly in `config.yaml` under `llm.api_key`.

5. After confirming the report and recipients, set `send.dry_run: false` in `config.yaml`.

5. Install the Windows scheduled task:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\employee agent\scripts\install_scheduled_task.ps1"
```

## Workflow

Run the workflow in this order:

1. Load config and initialize workflow directories.
2. Search Outlook for target emails by subject keyword, optional sender, folder, and lookback days.
3. Skip emails already recorded as successful in `state.sqlite` unless `--force` is supplied.
4. Extract the full email body as the user question.
5. Download attachments into the workflow `downloads/` folder when present.
6. Convert supported document attachments to Markdown when `convert.enabled` is true.
7. Import Markdown into `D:\employee agent\llm_wiki\raw\documents\` as new source material.
8. Search wiki context using the email question, configured terms, and any attachment text.
9. Collect bounded wiki page excerpts/snippets from the top search hits.
10. Call the configured model with only that wiki context to generate a grounded answer.
11. Create a durable query page in `D:\employee agent\llm_wiki\queries\`.
12. Generate a Markdown report under the workflow `reports/` folder.
13. Send or dry-run an Outlook/SMTP email with the report attached.
14. Record completion status, logs, and processed email IDs.

In `codex_assisted` mode, the workflow stops after step 11 and writes `model_input.md/json` under the run folder instead of generating the final report automatically.

## Safety Rules

- Keep `send.dry_run: true` until the user has inspected the generated report.
- Never send to empty recipients.
- Preserve source provenance when importing converted Markdown into the wiki.
- Keep `llm.required: false` while debugging if fallback reports are acceptable; set it to `true` before production if a model answer is mandatory.
- Treat generated analysis as preliminary unless reviewed by a domain owner.
- Use `--force` only when reprocessing a known email is intentional.

## References

- See `references/workflow.md` for configuration fields, state behavior, and troubleshooting.
- See `config.example.yaml` for a starting configuration.

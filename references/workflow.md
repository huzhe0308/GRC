# Daily Mail Wiki Report Workflow

## Purpose

Automate the daily path from a target Outlook email to a wiki-grounded Markdown report and Outlook delivery.

## Runtime Folders

The default runtime root is `D:\employee agent\runtime`.

- `downloads/`: saved Outlook attachments grouped by run and email.
- `markdown/`: converted or copied Markdown files.
- `reports/`: generated report files.
- `logs/`: timestamped workflow logs.
- `state.sqlite`: processed email, attachment, and run status records.

## State Behavior

The workflow records Outlook `EntryID` values after successful processing. Re-running the script skips successful emails. Use `--force` to intentionally reprocess matched emails.

Attachment SHA-256 values are also stored for traceability.

## Conversion

When `convert.enabled` is true, supported documents are passed to:

```powershell
python C:\Users\30432\.codex\skills\automotive-llm-wiki\work\mineru_api_convert.py precise --input <file> --output <job-output> --markdown-dir <markdown-dir>
```

Markdown and text attachments are copied directly to the workflow Markdown folder.

## Non-COM Mail Backend

Use IMAP/SMTP when `Outlook.Application` COM is unavailable or when the installed Outlook client is the new web-backed Outlook.

Set:

```yaml
mail:
  backend: "imap"
  imap:
    host: "<imap-server>"
    port: 993
    username: "<mailbox-user>"
    password_env: "DAILY_MAIL_IMAP_PASSWORD"
    folder: "INBOX"
    use_ssl: true

send:
  backend: "smtp"
  smtp:
    host: "<smtp-server>"
    port: 465
    username: "<mailbox-user>"
    password_env: "DAILY_MAIL_SMTP_PASSWORD"
    from_address: "<mailbox-user>"
    use_ssl: true
```

Set the passwords in the current Windows user environment rather than storing them in `config.yaml`.

## Wiki Import

Converted Markdown files are imported into:

```text
automotive-llm-wiki/llm_wiki/raw/documents/
```

Each imported file gets raw-style frontmatter with mail metadata and a content hash. A query page is also created under `llm_wiki/queries/` so the daily run is easy to find from the wiki layer.

## Wiki-Grounded Answering

The upgraded first version treats the email body as the question. The workflow builds the wiki search query from:

- configured `wiki.query_terms`
- target email subject
- full captured email body
- attachment filenames
- short Markdown excerpts from converted attachments, when present

The top wiki hits are converted into a bounded context block. For each hit the script includes path, title, score, source references, matched lines, and a short excerpt from the wiki page when available.

When `llm.enabled: true`, the script calls the configured OpenAI-compatible Responses API endpoint with only the email question and wiki context. The model is instructed to answer only from the provided wiki context, cite wiki page paths or raw provenance paths, and explicitly say when evidence is insufficient.

Set:

```yaml
llm:
  enabled: true
  required: false
  model: "gpt-4o-mini"
  api_key_env: "OPENAI_API_KEY"
```

With `required: false`, missing API credentials or transient model failures produce an explicit fallback extractive answer. With `required: true`, the run fails instead of sending a non-model answer.

## Dual Mode

- `workflow.mode: codex_assisted`: the workflow stops after mail reading, wiki retrieval, context packaging, and `model_input.md/json` creation. Use this when you want Codex in the current session to author the final answer and report.
- `workflow.mode: api`: the workflow continues end-to-end and generates the answer and report automatically.
- `--send-report <path>` sends an already-written final report without re-running mail or wiki retrieval.

## Report Generation

The generated report includes:

- email metadata
- extracted email question
- wiki-grounded model answer, or an explicit fallback section
- attachment and conversion status
- imported wiki source paths
- wiki search matches
- preliminary risk level
- suggested follow-up actions

## Scheduling

Use `D:\employee agent\scripts\install_scheduled_task.ps1` to create the
15:30 Windows scheduled task. The scheduler wakes the agent daily; the agent
provides the workflow state, executable scripts, logs, and reports.

# G.R.C. Agent - Mail Wiki Report Agent

This dedicated Windows workflow agent:

1. Reads matching mail from the current Outlook profile via Windows COM.
2. Extracts the question from the email body.
3. Saves and converts supported attachments with the MinerU tool in the automotive wiki skill.
4. Imports converted Markdown into the local automotive wiki.
5. Searches wiki evidence and sends bounded context to the configured model.
6. Generates a Markdown report and sends it through Outlook.

## First run

The `config.yaml` file is the runtime configuration. Put the model key in
`llm.api_key`. Outlook access uses the signed-in desktop Outlook profile, so no
mail password env vars are needed:

```powershell
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "<百炼API key>", "User")
```

Install the Outlook COM dependency:

```powershell
pip install pyyaml requests pywin32
```

Run a manual dry run:

```powershell
.\run_agent.ps1
```

Open the local demo console:

```powershell
python -B .\demo_app\app.py
```

Then open `http://127.0.0.1:7860` in a browser.

The default configuration is `api` mode with `send.dry_run: true`. It creates
the report but does not send it.

After inspecting a report, change `send.dry_run` to `false`, then test once:

```powershell
.\run_agent.ps1 -Force
```

Install the 15:30 daily Windows task:

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\install_scheduled_task.ps1"
```

The agent stores runtime data under `D:\employee agent\runtime`, including
downloads, converted Markdown, reports, logs, and `state.sqlite`.

## Codex-assisted debug mode

For a model-free debugging pass:

```powershell
.\run_agent.ps1 -Mode codex_assisted
```

This creates `model_input.md` and `model_input.json` under the run directory.
Codex can inspect those files, author the final report, and send it with
`--send-report <report-path>` after review.

# GRC Agent - Local Client Distribution Package

## For End Users

1. **Install**: Double-click `install.bat`
   - It will ask for Turso database URL and Token (get from Railway dashboard)
   - Creates desktop + Start Menu shortcuts
   - Installs to `%LOCALAPPDATA%\GRC Agent`

2. **Launch**: Double-click the "GRC Agent" desktop shortcut

3. **Login**: Use your existing GRC Agent account (same as web version)

4. **Uninstall**: Double-click `uninstall_grc.ps1` (or delete the install folder)

## For Administrators

### Building the exe
```
python -m PyInstaller GRCAgent.spec --noconfirm
```
The exe will be in `dist/GRCAgent.exe`.

### Distribution
Copy the `installer/` folder (containing `GRCAgent.exe`, `install.bat`, `install_grc.ps1`) to share with users.

### What the installer does
- Creates `%LOCALAPPDATA%\GRC Agent\` directory
- Copies `GRCAgent.exe` there
- Creates `.env` file with Turso credentials
- Copies `config.yaml`, `.jira_config`, `contacts.json` if present
- Creates desktop and Start Menu shortcuts

### Requirements for end users
- Windows 10/11 (64-bit)
- No Python installation needed
- Outlook desktop app installed (for email scanning)
- Must be on VW internal network (for LLM Gateway and Jira access)

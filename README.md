# financial-data-scrapper


financial-data-scrapper --config config.json

uv pip install -e .

rclone config

## ☁️ Google Drive Setup with `rclone`

Follow these steps to configure `rclone` for automatically uploading generated report files to your Google Drive.

### 1. Install `rclone` (Linux / WSL)

If you haven't installed `rclone` yet, run the following command in your terminal:

```bash
sudo apt update && sudo apt install -y rclone
```

### 2. Configure the Remote Access
Run the interactive configuration wizard:
```bash
rclone config
```

Follow the step-by-step interactive prompt:

- `New Remote`: Type n and press Enter.

- `Name`: Type inverg (or the remote_name specified in your config.json) and press Enter.

- `Storage Type`: Select Google Drive by entering 18 (or typing drive) and press Enter.

- `Client ID`: Leave blank, press Enter.

- `Client Secret`: Leave blank, press Enter.

- `Scope`: Type 1 (Full access) and press Enter.

- `Service Account File`: Leave blank, press Enter.

- `Advanced Config`: Type n and press Enter.

- `Auto Config`: Type y and press Enter.


If using WSL or a remote terminal: Copy the generated `http://127.0.0.1:53682/auth...` URL into your web browser, sign in with your Google account, grant the required permissions, and copy the authorization code back if prompted.

- `Shared Drive`: Type n and press Enter.

- `Confirm`: Type y to accept the configuration.

- `Quit`: Type q to exit the setup wizard.

### 3. Verify the Connection
You can verify that your Google Drive remote is properly linked by listing the root directories:

```bash
rclone lsd inverg
```

### 4. Update config.json
Ensure your config.json includes the correct google_drive parameters matching your rclone remote name and target folder path:

```json
{
  "google_drive": {
    "enabled": true,
    "remote_name": "remote_name",
    "folder_name": "path_folder"
  }
}
```
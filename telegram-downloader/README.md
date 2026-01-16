# Telegram Downloader

An automated Docker service that monitors a Telegram channel or group and downloads all media files (videos, images, documents) posted to it.

> ⚠️ **IMPORTANT LEGAL NOTICE**: This service uses your personal Telegram account. Please read the [Important Notes & Disclaimer](#important-notes--disclaimer) section before proceeding to understand your responsibilities and potential risks regarding Telegram Terms of Service compliance.

## Features

- **Automatic monitoring** of Telegram channels/groups
- **Auto-download** all media files from new messages
- **Real-time progress tracking** with download speed and ETA
- **Cancellable downloads** via inline buttons
- **Organized storage** in configurable directory
- **Auto-restart** on container failure
- **Interactive status updates** in Telegram
## Prerequisites

1. **Telegram API credentials** from [my.telegram.org](https://my.telegram.org/)
   - Go to API development tools
   - Create a new application
   - Note down your `api_id` and `api_hash`

2. **Channel/Group ID** you want to monitor
   - Add `@userinfobot` to your channel/group to get the ID
   - Or use a channel username (e.g., `@channelname`)

## Setup

### 1. Configure Environment Variables

Copy the example environment file and edit it:

```bash
cp .env.sample .env
```

Edit `.env` with your configuration:

```env
# Telegram API credentials (from my.telegram.org)
TG_API_ID=123456
TG_API_HASH=abcdef0123456789abcdef0123456789

# Channel/group to monitor (ID or username)
WATCH_CHAT=-1001234567890

# Download directory (must exist on host)
DOWNLOAD_DIR=/media/downloads/telegram

# Optional: Session file location (inside container)
TG_SESSION_PATH=/session/telethon.session

# Optional: Progress update frequency (seconds)
PROGRESS_UPDATE_EVERY=2.0

# Optional: Delete partial files on cancel (1=yes, 0=no)
DELETE_PARTIAL_ON_CANCEL=1
```

### 2. Create Download Directory

Make sure the download directory exists on your host system:

```bash
mkdir -p /media/downloads/telegram
# Optional: Set permissions if needed
sudo chown -R $USER:$USER /media/downloads/telegram
```

### 3. Build and Deploy the Service

From the `telegram-downloader/` directory:

```bash
# Build the Docker image
docker compose build

# Deploy the service
docker compose up -d
```

## First Run Authentication

On the first run, you'll need to authenticate with Telegram:

1. Run the container interactively for initial setup:
   ```bash
   docker compose run --rm tg_downloader
   ```

2. When prompted, enter your phone number and verification code
3. Once authenticated successfully, stop the container (Ctrl+C)
4. The session will be saved and you can now run the service normally:
   ```bash
   docker compose up -d
   ```

## Configuration Details

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TG_API_ID` | Telegram API ID from my.telegram.org | `123456` |
| `TG_API_HASH` | Telegram API hash from my.telegram.org | `abcdef0123456789...` |
| `WATCH_CHAT` | Channel/group ID or username to monitor | `-1001234567890` or `@channelname` |
| `DOWNLOAD_DIR` | Host directory path for downloads | `/media/downloads/telegram` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TG_SESSION_PATH` | `/session/telethon.session` | Session file location in container |
| `PROGRESS_UPDATE_EVERY` | `2.0` | Update frequency for download progress (seconds) |
| `DELETE_PARTIAL_ON_CANCEL` | `1` | Delete incomplete files when cancelled |

## Usage

Once running, the bot will:

1. **Monitor** the configured channel/group for new messages
2. **Detect** any media files (photos, videos, documents)
3. **Start downloading** automatically with a status message
4. **Show progress** with real-time updates including:
   - Download percentage
   - Current/total file size
   - Download speed
   - Estimated time remaining
5. **Allow cancellation** via the "⛔ Cancel" button
6. **Save files** to the configured download directory
7. **Update status** when complete or failed

## File Organization

Downloaded files are saved directly to the `DOWNLOAD_DIR` with their original filenames. If files have duplicate names, Telegram's client will automatically append numbers (e.g., `video(1).mp4`).

## Important Notes & Disclaimer

⚠️ **Critical Warning**: This service uses your personal Telegram account credentials to monitor and download content from channels/groups. By using this service, you acknowledge:

- **Telegram Terms of Service**: You must comply with [Telegram's Terms of Service](https://telegram.org/tos) at all times
- **Account Responsibility**: Any violations of Telegram's ToS may result in **account suspension or permanent ban**
- **Legal Compliance**: You are responsible for ensuring your usage complies with local laws and regulations
- **Content Rights**: Only download content you have permission to access and store
- **Rate Limits**: Excessive API usage may trigger Telegram's anti-spam measures
- **Personal Risk**: Use this service at your own risk - account consequences are your responsibility

**Recommended Usage**:
- Only monitor channels/groups you own or have explicit permission to download from
- Respect content creators' rights and terms
- Monitor download frequency to avoid triggering rate limits
- Regularly review Telegram's updated terms and policies

📋 **Additional Resources**:
- [Telegram Terms of Service](https://telegram.org/tos)
- [Telegram Privacy Policy](https://telegram.org/privacy)
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)

## Support

The service uses the [Telethon](https://docs.telethon.dev/) library for Telegram integration. 

**Before seeking support**: Please ensure you have read and understood the [Important Notes & Disclaimer](#important-notes--disclaimer) section above, particularly regarding Telegram Terms of Service compliance.

For technical issues:
- Review the configuration in your `.env` file
- Check Docker logs: `docker compose logs -f`
- Verify your Telegram API credentials and permissions
- Ensure compliance with all terms and usage guidelines
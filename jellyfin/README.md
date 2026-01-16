# Jellyfin Media Server

A free, open-source media server that organizes, manages, and streams your media collection including movies, TV shows, music, and photos. Jellyfin provides a web interface, mobile apps, and various client applications for accessing your content.

## Features

- **Self-hosted media streaming** with no subscriptions or fees
- **Multi-device support** via web interface, mobile apps, and TV apps
- **Automatic metadata fetching** for movies, TV shows, music, and photos
- **Transcoding support** for compatibility across different devices
- **User management** with profiles and parental controls
- **DLNA support** for streaming to compatible devices
- **Hardware acceleration** support (Intel QSV, NVIDIA NVENC, AMD VCE)
- **Extensive format support** for virtually all media types

## Prerequisites

1. **Media collection** organized in folders
2. **Directory permissions** properly configured for the service user

## Setup

### 1. Configure Environment Variables

Copy the example environment file and edit it:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# General settings
PUID=1000
PGID=1000
TZ=Etc/UTC

# Directories
# Path to your media folder on the host
MEDIA_DIR=/path/to/media

# Path where service configurations will be stored
CONFIG_DIR=/path/to/config
```

### 2. Prepare Media and Configuration Directories

Create the necessary directories:

```bash
# Create configuration directory
mkdir -p /path/to/config/jellyfin

# Ensure media directory exists and is accessible
ls -la /path/to/media

# Optional: Set proper permissions
sudo chown -R $USER:$USER /path/to/config/jellyfin
```

### 3. Build and Deploy the Service

From the `jellyfin/` directory:

```bash
# Deploy the service
docker compose up -d
```

## Configuration Details

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PUID` | User ID for file permissions | `1000` |
| `PGID` | Group ID for file permissions | `1000` |
| `TZ` | Timezone for the container | `America/New_York` |
| `MEDIA_DIR` | Host path to your media collection | `/media/library` |
| `CONFIG_DIR` | Host path for storing configurations | `/docker/config` |

### Optional Configuration

You can uncomment and set the `JELLYFIN_PublishedServerUrl` environment variable in the docker-compose.yml if you want to specify your server's IP address for external access.

## First Run Setup

1. **Access the web interface**: Open your browser and go to `http://localhost:8096`

2. **Initial setup wizard**:
   - Set up an administrator account
   - Configure media libraries by pointing to `/data/media` (this maps to your `MEDIA_DIR`)
   - Configure metadata providers (TheMovieDB, TheTVDB, etc.)
   - Set up remote access if needed

3. **Media library organization**: For best results, organize your media like this:
   ```
   /path/to/media/
   ├── Movies/
   │   ├── Movie Title (Year)/
   │   │   └── Movie Title (Year).mkv
   │   └── Another Movie (Year)/
   │       └── Another Movie (Year).mp4
   ├── TV Shows/
   │   ├── Show Name/
   │   │   ├── Season 01/
   │   │   │   ├── S01E01 - Episode Title.mkv
   │   │   │   └── S01E02 - Episode Title.mkv
   │   │   └── Season 02/
   │   │       └── S02E01 - Episode Title.mkv
   └── Music/
       ├── Artist Name/
       │   └── Album Name/
       │       └── 01 - Track Title.mp3
   ```

## Network Configuration

The service uses `network_mode: host` for optimal performance and DLNA discovery. This provides:

- **Port 8096**: Web interface and API
- **Port 1900/udp**: DLNA discovery
- **Port 7359/udp**: Local network discovery

## Usage

### Accessing Jellyfin

- **Web Interface**: `http://localhost:8096` or `http://[your-server-ip]:8096`
- **Mobile Apps**: Available on iOS, Android, and various TV platforms
- **Desktop Clients**: Available for Windows, macOS, and Linux

### Adding Content

1. Place new media files in your configured `MEDIA_DIR`
2. In Jellyfin, go to Admin Dashboard → Libraries
3. Click "Scan All Libraries" or set up automatic scanning

### User Management

- Create additional user accounts from Admin Dashboard → Users
- Set up parental controls and viewing restrictions per user
- Configure user-specific settings and preferences

## Hardware Acceleration (Optional)

For better performance with transcoding, you can enable hardware acceleration:

1. **Intel Quick Sync Video (QSV)**: Requires `/dev/dri` device passthrough
2. **NVIDIA NVENC**: Requires NVIDIA container runtime
3. **AMD VCE**: Requires proper GPU drivers and device access

Modify the docker-compose.yml to add device access as needed.

## File Organization Tips

- Use consistent naming conventions
- Include year in movie folder names: `Movie Title (2023)`
- Use season/episode format for TV shows: `S01E01`
- Embed subtitles or place them alongside video files with matching names
- Use high-quality metadata-rich file names for better automatic detection

## Client Applications

Download official Jellyfin clients:
- **Android/iOS**: Search "Jellyfin" in app stores
- **Android TV/Fire TV**: Available on respective app stores
- **Smart TVs**: Samsung, LG, and others via app stores
- **Desktop**: Available at [jellyfin.org/downloads](https://jellyfin.org/downloads)
- **Kodi**: Install the Jellyfin for Kodi add-on

## Support

For technical support and documentation:
- **Official Documentation**: [jellyfin.org/docs](https://jellyfin.org/docs)
- **Community Forum**: [forum.jellyfin.org](https://forum.jellyfin.org)
- **GitHub Issues**: [github.com/jellyfin/jellyfin](https://github.com/jellyfin/jellyfin)
- **Docker Logs**: `docker compose logs -f` for troubleshooting
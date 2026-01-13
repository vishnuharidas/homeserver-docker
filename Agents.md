# AI Agents Guide - Homeserver Compose

This file provides context and instructions for AI agents assisting with this repository.

## Project Goal
Maintain a collection of Docker Compose configurations for a homeserver, following a specific structure to ensure ease of deployment and centralized configuration.

## Repository Structure
- `[service-name]/`: Each service has its own directory.
- `[service-name]/docker-compose.yml`: The compose file for that specific service.
- `.env`: (Root) Local environment variables (ignored by git).
- `.env.example`: (Root) Template for the environment variables.
- `README.md`: Overview and usage instructions.

## Conventions

### 1. Centralized Configuration
All service-specific configurations and data should reference variables defined in the root `.env` file.
- `PUID`/`PGID`: Use these for all LinuxServer.io based images.
- `TZ`: Global timezone.
- `CONFIG_DIR`: Base path for application data (e.g., `${CONFIG_DIR}/jellyfin`).
- `MEDIA_DIR`: Base path for media files.

### 2. Docker Images
Prefer images from [LinuxServer.io](https://www.linuxserver.io/) (`lscr.io/linuxserver/...`) where available, as they offer consistent environment variable support and permission handling.

### 3. Adding a New Service
When adding a new service:
1. Create a new directory named after the service.
2. Create a `docker-compose.yml` within that directory.
3. Use `${VARIABLE:-default}` syntax for environment variables to provide sane defaults while allowing overrides from the root `.env`.
4. Update the root `README.md` with the new service details and command.
5. If new environment variables are required, add them to `.env.example`.

## Execution Commands
Always run docker commands from the root of the repository to ensure `.env` is automatically picked up:
`docker compose -f <service>/docker-compose.yml up -d`

# Homeserver Docker Compose Repository

This repository contains Docker Compose configurations for setting up a homeserver, designed to be easily deployable and manageable.

## Structure

- Each service has its own dedicated directory (e.g., `jellyfin/`).
- A central `.env` file at the root contains shared environment variables:
    - `PUID`/`PGID`: User and Group ID for file permissions.
    - `TZ`: Timezone.
    - `MEDIA_DIR`: Path to your media library.
    - `CONFIG_DIR`: Path where all service configurations will be stored.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Copy `.env.example` to `.env` (or create a `.env` file based on the provided one).
2. Edit `.env` to match your system's configuration.
3. Run services from the root of the repository using the `-f` flag to ensure the `.env` file is loaded.

## Services

### Jellyfin
Media server for managing and streaming your media.
- Location: `./jellyfin/`
- Command: `docker compose -f jellyfin/docker-compose.yml up -d`

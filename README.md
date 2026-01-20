# Homeserver Docker Compose Repository

This repository contains Docker Compose configurations for setting up a homeserver, designed to be easily deployable and manageable.

## Structure

- Each service has its own dedicated directory (e.g., `jellyfin/`).

## Prerequisites

- Docker
- Docker Compose

## Services

### [Beszel](beszel/)
Lightweight server monitoring dashboard with Docker stats, system metrics, and alerts. ([beszel.dev](https://beszel.dev))

### [Jellyfin](jellyfin/)
Media server for managing and streaming your media library. ([jellyfin.org](https://jellyfin.org/))

### [Telegram File Downloader](telegram-downloader/)
Automated service that monitors Telegram channels/groups and downloads media files.

- **Legal Notice**: Uses your personal Telegram account - ensure compliance with Telegram Terms of Service to avoid account restrictions.

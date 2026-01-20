# Beszel

A lightweight server monitoring dashboard that provides real-time insights into your system performance, Docker container stats, and resource usage with a clean, modern interface.

## Features

- **Real-time system monitoring** (CPU, RAM, disk, network)
- **Docker container stats** and management
- **Multi-server support** with agent-hub architecture
- **Alerts and notifications** for system events
- **Clean, responsive web interface**
- **Lightweight and fast** with minimal resource usage

## Architecture

Beszel consists of two components:

- **Hub**: Web dashboard that collects and displays metrics (`hub/docker-compose.yml`)
- **Agent**: Lightweight collector that gathers system metrics (`agent/docker-compose.yml`)

## Quick Start

1. **Start the Hub** (monitoring dashboard):
   ```bash
   docker compose -f beszel/hub/docker-compose.yml up -d
   ```

2. **Configure and start the Agent**:
   - Access the hub at `http://localhost:8090`
   - Create an agent in the web interface to get the KEY and TOKEN
   - Update `beszel/agent/docker-compose.yml` with your KEY and TOKEN
   - Start the agent:
   ```bash
   docker compose -f beszel/agent/docker-compose.yml up -d
   ```

## Documentation

For detailed setup, configuration options, and advanced features, see the official documentation at [beszel.dev](https://beszel.dev).

## Ports

- **Hub**: 8090 (Web interface)
- **Agent**: 45876 (Internal communication)
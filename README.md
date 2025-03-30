# DummyJSON Plugin

This repository contains a simple Python plugin built for Anecdotes' home assignment.
It connects to the [DummyJSON](https://dummyjson.com) API to perform authentication and collect three types of evidence.

## Features
- Connectivity test via `/auth/login`
- E1: Fetch authenticated user details (`/auth/me`)
- E2: Fetch 60 posts (`/posts?limit=60`)
- E3: Fetch 60 posts with their comments (`/posts/{id}/comments`)

## Usage
```bash
python main.py
```

Make sure you have `requests` installed:
```bash
pip install requests
```

## Structure
- `PluginConfig`: Holds config (base URL, credentials)
- `BasePlugin`: Abstract base class defining required methods
- `DummyJSONPlugin`: Implements connectivity and evidence collection
- `main.py`: Entry point to run the plugin and print the evidence

## Design Highlights
- **Separation of Concerns**: `PluginConfig` cleanly separates configuration from logic
- **Generic Plugin Architecture**: `BasePlugin` defines a consistent interface for plugins
- **Reusability**: Code using `BasePlugin` can work with any plugin implementation without knowing internal details

This creates a clean, extensible, and testable plugin structure that is easy to maintain and scale.

## Example Credentials
Username: `emilys`  
Password: `emilyspass`




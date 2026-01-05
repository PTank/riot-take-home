# Enigma (Riot Take-Home Technical Challenge)

This project is a FastAPI application.

[specs](SPECIFICATION.md)

## Setup for Dev

This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/)

Once `uv` is installed, synchronize the project dependencies:

```bash
uv sync
```

## Running the Application

To run the application using Podman Compose or Docker Compose:

```bash
podman compose up --build
```

The application should then be accessible at `http://localhost:8000` (or the port specified in `docker-compose.yml`).


## Env Variables

```bash
ENCRYPTION_TYPE="base64"
SIGNER_TYPE="hmac"
SIGNING_SECRET_KEY="secret key"
```

Env variables can be set in the `.env` file.

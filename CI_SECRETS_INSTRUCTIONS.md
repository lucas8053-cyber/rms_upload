CI/CD Secrets & Quick Start
===========================

This file lists the repository secrets and quick steps to run the GitHub Actions workflow that builds and pushes the Docker image, and optionally triggers a Render deploy.

Required GitHub Actions secrets (set at GitHub → Settings → Secrets and variables → Actions):

- `DOCKERHUB_USERNAME` – your Docker Hub username
- `DOCKERHUB_TOKEN` – Docker Hub access token or password (token recommended)

Optional (but recommended) secrets:

- `DOCKERHUB_REPOSITORY` – e.g. `mydockeruser/rms_upload` (if omitted the workflow uses `${{ github.repository_owner }}/rms_upload`)
- `RENDER_API_KEY` – Render API key (for API deploy trigger)
- `RENDER_SERVICE_ID` – Render service ID (the target service to trigger)
- `RENDER_DEPLOY_HOOK` – If you prefer a deploy webhook URL, set it here instead of API key

How to create Docker Hub token

1. Sign in to Docker Hub → Account Settings → Security → New Access Token.
2. Copy the token and add it as `DOCKERHUB_TOKEN` in GitHub Secrets.

How to get Render values

- `RENDER_SERVICE_ID`: in Render dashboard open your service and copy the service id from the URL or service settings.
- `RENDER_API_KEY`: in Render account settings → API Keys → create a key.

Testing & manual run

1. Push any commit to `main` or open Actions → Workflows → "Build and Publish Docker Image" → "Run workflow".
2. Check the workflow logs in GitHub Actions: it will build multi-arch image and push tags `:latest` and `:${{GITHUB_SHA}}`.
3. If Render secrets are present the workflow will trigger a deploy.

Local build & run (quick smoke test)

```bash
docker build -t yourname/rms_upload:local .
docker run -p 8501:8501 yourname/rms_upload:local
# open http://localhost:8501
```

Manual push to Docker Hub (if you prefer local build then push):

```bash
docker login -u <DOCKERHUB_USERNAME>
docker tag yourname/rms_upload:local yourname/rms_upload:latest
docker push yourname/rms_upload:latest
```

Notes
- The workflow expects a `Dockerfile` at repository root. It uses `DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN` to authenticate.
- If your app requires persistent DB, configure Render volumes or migrate DB to managed Postgres. See `README_DEPLOY.md`.

If you want, I can add a short README section instructing where to paste these secrets, or attempt a first Action run after you add the secrets.

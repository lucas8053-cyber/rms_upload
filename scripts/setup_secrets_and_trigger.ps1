<#
Interactive helper to set required GitHub Actions secrets and trigger the CI workflow.
Run this locally where `gh` is installed and you're authenticated (gh auth login).

Usage: open PowerShell in project root and run:
  .\scripts\setup_secrets_and_trigger.ps1

This script will prompt for values and call `gh secret set` for:
  DOCKERHUB_USERNAME, DOCKERHUB_TOKEN
Optional: DOCKERHUB_REPOSITORY, RENDER_API_KEY, RENDER_SERVICE_ID, RENDER_DEPLOY_HOOK

It then triggers the workflow `docker-publish.yml` on branch `main` and prints the run id.
#>

# ensure gh is available
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI (gh) not found. Install from https://cli.github.com/ and run 'gh auth login' first."
    exit 1
}

Write-Host "Ensure you're authenticated with gh:"
$null = gh auth status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Please run 'gh auth login' then re-run this script.";
    exit 1
}

# prompt required
$dockerUser = Read-Host "DOCKERHUB_USERNAME"
$dockerToken = Read-Host "DOCKERHUB_TOKEN (will be hidden)" -AsSecureString
# convert securestring to plain for gh CLI usage (local only)
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($dockerToken)
$dockerTokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto($ptr)
[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)

gh secret set DOCKERHUB_USERNAME --body "$dockerUser"
gh secret set DOCKERHUB_TOKEN --body "$dockerTokenPlain"
Write-Host "Set DOCKERHUB_USERNAME and DOCKERHUB_TOKEN"

# optional secrets
$askOpt = Read-Host "Set optional secrets for Render/Docker repository? (y/N)"
if ($askOpt -match '^[Yy]') {
    $repo = Read-Host "DOCKERHUB_REPOSITORY (leave empty to skip)"
    if ($repo) { gh secret set DOCKERHUB_REPOSITORY --body "$repo"; Write-Host "Set DOCKERHUB_REPOSITORY" }
    $renderKey = Read-Host "RENDER_API_KEY (leave empty to skip)" -AsSecureString
    if ($renderKey) {
        $ptr2 = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($renderKey)
        $renderKeyPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto($ptr2)
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr2)
        gh secret set RENDER_API_KEY --body "$renderKeyPlain"
        Write-Host "Set RENDER_API_KEY"
    }
    $renderService = Read-Host "RENDER_SERVICE_ID (leave empty to skip)"
    if ($renderService) { gh secret set RENDER_SERVICE_ID --body "$renderService"; Write-Host "Set RENDER_SERVICE_ID" }
    $renderHook = Read-Host "RENDER_DEPLOY_HOOK (leave empty to skip)"
    if ($renderHook) { gh secret set RENDER_DEPLOY_HOOK --body "$renderHook"; Write-Host "Set RENDER_DEPLOY_HOOK" }
}

# trigger workflow
Write-Host "Triggering workflow docker-publish.yml on branch main..."
$runResp = gh workflow run docker-publish.yml --ref main 2>&1
Write-Host $runResp

Start-Sleep -Seconds 2

# list recent runs
$runList = gh run list --workflow docker-publish.yml --limit 5
Write-Host "Recent runs:"
Write-Host $runList

# attempt to extract the most recent run id
$firstLine = ($runList -split "`n" | Select-Object -First 1)
if ($firstLine -match '^\s*(\d+)') {
    $runId = $Matches[1]
    Write-Host "Watching run id $runId (this will stream logs until completion)..."
    gh run watch $runId
} else {
    Write-Host "Could not parse run id from gh run list output. Use 'gh run list --workflow docker-publish.yml' to find the run id and then 'gh run watch <id>'."
}

Write-Host "Done. If the workflow failed, run: gh run view <run-id> --log and paste the failing step logs here for analysis."

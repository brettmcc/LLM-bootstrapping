# Robust venv setup: accept a parameter, env var, or default to user's profile
param(
    [string]$VenvPathParam
)

# Determine venv path: priority -> param, NHK_VENV env var, default to $USERPROFILE\.venvs\NHK-replications
if ($VenvPathParam) {
    $VenvPath = $VenvPathParam
} elseif ($env:NHK_VENV) {
    $VenvPath = $env:NHK_VENV
} else {
    if ($env:USERPROFILE) { $userProfile = $env:USERPROFILE } elseif ($env:HOME) { $userProfile = $env:HOME } else { Write-Error "Cannot determine user profile path. Set `NHK_VENV` or pass `-VenvPath`."; exit 1 }
    $VenvPath = Join-Path $userProfile ".venvs\NHK-replications"
}

$VenvPath = [System.IO.Path]::GetFullPath($VenvPath)
Write-Host "Using virtual environment path:`n  $VenvPath"

# Ensure parent directory exists
$parent = Split-Path $VenvPath -Parent
if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }

# Create virtual environment: prefer 'uv' if available, otherwise use 'python -m venv'
$uvCmd = Get-Command "uv" -ErrorAction SilentlyContinue
if ($uvCmd) {
    Write-Host "Creating virtual environment using 'uv'..."
    & uv venv "$VenvPath"
} else {
    $pyCmd = Get-Command "python" -ErrorAction SilentlyContinue
    if (-not $pyCmd) {
        Write-Error "Neither 'uv' nor 'python' were found in PATH. Please install Python or 'uv'."
        exit 1
    }
    Write-Host "'uv' not found. Creating virtual environment using 'python -m venv'..."
    & python -m venv "$VenvPath"
}

# Locate Python executable inside the venv
$venvPython = Join-Path $VenvPath "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    # On non-standard installs, fall back to system python
    $systemPy = (Get-Command python -ErrorAction SilentlyContinue).Source
    if ($systemPy) {
        $venvPython = $systemPy
        Write-Host "Warning: python in venv not found; falling back to system python: $venvPython"
    } else {
        Write-Error "Cannot find python executable in the venv or on PATH."
        exit 1
    }
}

Write-Host "Installing requirements from requirements.txt using: $venvPython"
try {
    & "$venvPython" -m pip install --upgrade pip
    & "$venvPython" -m pip install -r (Join-Path (Get-Location) "requirements.txt")
} catch {
    Write-Error "pip install failed: $_"
    exit 1
}

Write-Host "Environment setup complete. Activate with:`n  $VenvPath\Scripts\Activate.ps1"

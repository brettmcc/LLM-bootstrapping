# Robust activation for different machines/users.
# Looks for the Activate.ps1 under the user's home .venvs folder,
# supports an override via the NHK_REPLICATIONS_VENV env var,
# and falls back to common script-relative locations.

$userHome = $env:USERPROFILE
if (-not $userHome -or $userHome -eq '') { $userHome = $env:HOME }

$venvCandidates = @(
	($userHome + '\.venvs\NHK-replications\Scripts\Activate.ps1'),
	($userHome + '\.venvs\NHK-replications\Scripts\activate.ps1'),
	($PSScriptRoot + '\.venvs\NHK-replications\Scripts\Activate.ps1'),
	($PSScriptRoot + '\env\Scripts\Activate.ps1'),
	($PSScriptRoot + '\venv\Scripts\Activate.ps1')
)

if ($env:NHK_REPLICATIONS_VENV -and $env:NHK_REPLICATIONS_VENV -ne '') {
	$venvCandidates = @($env:NHK_REPLICATIONS_VENV) + $venvCandidates
}

$found = $null
foreach ($c in $venvCandidates) {
	if (Test-Path $c) { $found = $c; break }
}

if ($found) {
	Write-Host "Sourcing virtualenv activate script: $found"
	& $found
} else {
	Write-Host "Could not find Activate.ps1 for .venvs/NHK-replications."
	Write-Host "Set the environment variable NHK_REPLICATIONS_VENV to the full path of Activate.ps1 to override."
	Write-Host "Searched locations:"
	foreach ($c in $venvCandidates) { Write-Host " - $c" }
	exit 1
}

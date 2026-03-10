<#
.SYNOPSIS
    Copies the shelves and scripts folders to a given directory.

.DESCRIPTION
    Recursively copies all files from the local "shelves" and "scripts"
    folders into the specified destination path, preserving the directory
    structure. Warns before overwriting any file that already exists.

.PARAMETER Destination
    The target directory to copy the folders into.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, HelpMessage = "Target directory to copy shelves and scripts into.")]
    [ValidateNotNullOrEmpty()]
    [string]$Destination
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# --- Resolve paths --------------------------------------------------------

$RepoRoot = Split-Path -Parent $PSScriptRoot          # repo root
$Folders  = @("shelves", "scripts")

if (-not (Test-Path $Destination)) {
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    Write-Host "Created destination directory: $Destination" -ForegroundColor Yellow
}

# --- Copy with overwrite warnings ----------------------------------------

$CopiedCount    = 0
$OverwriteCount = 0
$ErrorCount     = 0

foreach ($Folder in $Folders) {
    $SourceDir = Join-Path $RepoRoot $Folder

    if (-not (Test-Path $SourceDir)) {
        Write-Warning "Source folder not found, skipping: $SourceDir"
        continue
    }

    $DestDir = Join-Path $Destination $Folder
    $Files   = Get-ChildItem -Path $SourceDir -Recurse -File

    foreach ($File in $Files) {
        $RelativePath = $File.FullName.Substring($SourceDir.Length)
        $DestFile     = Join-Path $DestDir $RelativePath
        $DestFolder   = Split-Path -Parent $DestFile

        # Ensure the target directory exists
        if (-not (Test-Path $DestFolder)) {
            New-Item -ItemType Directory -Path $DestFolder -Force | Out-Null
        }

        # Warn if the file already exists
        if (Test-Path $DestFile) {
            $OverwriteCount++
            Write-Warning "File already exists and will be overwritten: $DestFile"
        }

        try {
            Copy-Item -Path $File.FullName -Destination $DestFile -Force
            Write-Host "  Copied: $Folder$RelativePath" -ForegroundColor Green
            $CopiedCount++
        }
        catch {
            Write-Error "Failed to copy '$($File.FullName)': $_"
            $ErrorCount++
        }
    }
}

# --- Summary --------------------------------------------------------------

Write-Host ""
Write-Host "--- Summary ---" -ForegroundColor Cyan
Write-Host "  Files copied     : $CopiedCount"
Write-Host "  Files overwritten : $OverwriteCount"
Write-Host "  Errors            : $ErrorCount"

if ($ErrorCount -gt 0) {
    Write-Warning "Some files could not be copied. Review the errors above."
    exit 1
}

Write-Host "Done." -ForegroundColor Green
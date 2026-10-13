# Restore only a pinned release's destination-parent ACLs. Never change bytes.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Manifest,
    [Parameter(Mandatory = $true)][string]$Output,
    [switch]$Apply
)
$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$prefix = $projectRoot.TrimEnd('\') + '\'
function Resolve-ProjectFile([string]$Relative) {
    if ([IO.Path]::IsPathRooted($Relative)) { throw 'Absolute manifest path refused' }
    $resolved = [IO.Path]::GetFullPath((Join-Path $projectRoot $Relative))
    if (-not $resolved.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Target outside project: $resolved"
    }
    if (-not (Test-Path -LiteralPath $resolved -PathType Leaf)) { throw "Missing file: $resolved" }
    return $resolved
}
$manifestPath = [IO.Path]::GetFullPath($Manifest)
$manifestPrefix = (Join-Path $projectRoot 'manifests').TrimEnd('\') + '\'
if (-not $manifestPath.StartsWith($manifestPrefix, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Manifest outside project manifests'
}
$release = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($release.schema_version -ne 1 -or $release.artifacts.Count -eq 0) { throw 'Invalid release manifest' }
$rows = @()
foreach ($artifact in $release.artifacts) {
    $target = Resolve-ProjectFile $artifact.destination
    $outputPrefix = (Join-Path $projectRoot 'outputs').TrimEnd('\') + '\'
    $dashboardPrefix = (Join-Path $projectRoot 'wiki/dashboards').TrimEnd('\') + '\'
    if (-not ($target.StartsWith($outputPrefix, [StringComparison]::OrdinalIgnoreCase) -or
        $target.StartsWith($dashboardPrefix, [StringComparison]::OrdinalIgnoreCase))) {
        throw "Refuse permission changes outside published outputs: $target"
    }
    $hash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne $artifact.sha256) { throw "Hash mismatch: $target" }
    $rows += [pscustomobject]@{ path = $target; sha256 = $hash }
}
$rows += [pscustomobject]@{
    path = $manifestPath
    sha256 = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
}
if (@($rows.path | Select-Object -Unique).Count -ne $rows.Count) { throw 'Duplicate target' }
$before = foreach ($row in $rows) {
    $acl = Get-Acl -LiteralPath $row.path
    [pscustomobject]@{ path = $row.path; sha256 = $row.sha256; sddl = $acl.Sddl
        inheritance_protected = $acl.AreAccessRulesProtected }
}
if (-not $Apply) {
    $before | ConvertTo-Json -Depth 5
    Write-Output "PREVIEW: $($rows.Count) exact files; no permissions changed"
    exit 0
}
$outputPath = [IO.Path]::GetFullPath($Output)
if (-not $outputPath.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase) -or
    (Test-Path -LiteralPath $outputPath)) { throw 'Evidence folder must be new and inside project' }
New-Item -ItemType Directory -Path $outputPath | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText((Join-Path $outputPath 'before.json'), ($before | ConvertTo-Json -Depth 5), $utf8)
$after = foreach ($row in $rows) {
    & icacls $row.path /reset | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "ACL reset failed; retain before.json for recovery: $($row.path)" }
    $hash = (Get-FileHash -LiteralPath $row.path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne $row.sha256) { throw "Content changed: $($row.path)" }
    $acl = Get-Acl -LiteralPath $row.path
    if ($acl.AreAccessRulesProtected) { throw "Inheritance still protected: $($row.path)" }
    [pscustomobject]@{ path = $row.path; sha256 = $hash; sddl = $acl.Sddl
        inheritance_protected = $acl.AreAccessRulesProtected }
}
[IO.File]::WriteAllText((Join-Path $outputPath 'after.json'), ($after | ConvertTo-Json -Depth 5), $utf8)
Write-Output "PASS: $($rows.Count) exact files inherit normal folder permissions; all bytes unchanged"

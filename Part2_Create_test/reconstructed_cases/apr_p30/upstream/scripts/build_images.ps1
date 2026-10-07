# Build the agent sandboxes. Pass -Modern/-Legacy to override the version lists.
#   .\scripts\build_images.ps1
#   .\scripts\build_images.ps1 -Modern "0.46.3 1.2.4 2.5.0 2.4.0"
param(
    [string]$Modern = "0.46.3 1.2.4 2.5.0",
    [string]$Legacy = "0.25.3",
    [switch]$SkipLegacy
)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $PSScriptRoot
$ctx = Join-Path $here "docker"

docker build -f "$ctx\Dockerfile.modern" --build-arg "QISKIT_VERSIONS=$Modern" -t qiskit-apr:modern $ctx
if (-not $SkipLegacy) {
    docker build -f "$ctx\Dockerfile.legacy" --build-arg "QISKIT_VERSIONS=$Legacy" -t qiskit-apr:legacy $ctx
}
docker run --rm qiskit-apr:modern ls /opt/venvs
if (-not $SkipLegacy) { docker run --rm qiskit-apr:legacy ls /opt/venvs }

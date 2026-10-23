# Input stays out of PowerShell command history and is stored only in this process.
$secureKey = Read-Host 'Paste the API key for the model you are about to run' -AsSecureString
$pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
try {
    $env:OPENAI_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
}
finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
    $secureKey.Dispose()
}
if ([string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) {
    throw 'No key entered. OPENAI_API_KEY is not set.'
}
Write-Host 'OPENAI_API_KEY is set for this PowerShell session. Its value is not displayed.'

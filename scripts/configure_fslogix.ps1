<#
.SYNOPSIS
Brief description of the function or script.
#>

.DESCRIPTION
Detailed description of the function or script, including its purpose and functionality.
This script downloads and executes a PowerShell script from a specified URL. The downloaded script is saved to a temporary location and then executed with specific parameters to configure remoting for FSLogix.

The script uses `System.Net.WebClient` to download the file and `powershell.exe` to execute it with the `-ExecutionPolicy ByPass` parameter to allow the script to run without being blocked by the execution policy. Additional parameters such as `-ForceNewSSLCert` and `-EnableCredSSP` are passed to the script to configure SSL certificates and Credential Security Support Provider (CredSSP) for remoting.

.PARAMETER <ParameterName>
Description of the parameter and its purpose.

.EXAMPLE
Example of how to use the function or script.

.NOTES
Additional information about the function or script, such as author, date, and version.

.LINK
Related links or references.
#>

param (
  [string]$profilefileShare,
  [string]$useraccount,
  [string]$accesskey,
  [strung]$fileShare
)

$url = "https://raw.githubusercontent.com/CGDORNELES/utilities/main/scripts/ConfigureRemotingForFSLogix.ps1"
$file = "$env:temp\ConfigureRemotingForFSLogix.ps1"

(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)

powershell.exe -ExecutionPolicy ByPass -File $file -ForceNewSSLCert -EnableCredSSP -Verbose -profilefileShare $profilefileShare -useraccount $useraccount -accesskey $accesskey -fileShare $fileShare

Enable-WSManCredSSP -Role Server -Force

Set-Item -Path "WSMan:\localhost\Service\Auth\CredSSP" -Value $true
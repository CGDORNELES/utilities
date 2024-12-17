
<#
.SYNOPSIS
Configures FSLogix settings for remoting.

.DESCRIPTION
This script configures various FSLogix settings by creating and setting registry keys and values. It ensures that FSLogix Profiles are enabled and configured with the specified settings.

.PARAMETER profilefileShare
The network location where VHD files will be stored.

.EXAMPLE
.\ConfigureRemotingForFSLogix.ps1 -profilefileShare "\\server\share"

.NOTES
Author: Your Name
Date: Today's Date
Version: 1.0
#>
param (
  [string]$profilefileShare,
  [string]$useraccount,
  [string]$accesskey,
  [string]$fileShare
)

# Create a new registry key for FSLogix under SOFTWARE, ignore if it already exists
New-Item -Path "HKLM:\SOFTWARE" -Name "FSLogix" -ErrorAction Ignore
# Create a new registry key for Profiles under FSLogix, ignore if it already exists
New-Item -Path "HKLM:\SOFTWARE\FSLogix" -Name "Profiles" -ErrorAction Ignore
# Enable FSLogix Profiles
New-ItemProperty -Path "HKLM:\SOFTWARE\FSLogix\Profiles" -Name "Enabled" -Value 1 -force
# Set the location for VHD files
New-ItemProperty -Path "HKLM:\SOFTWARE\FSLogix\Profiles" -Name "VHDLocations" -Value $profilefileShare -force
# Allow concurrent user sessions
New-ItemProperty -Path "HKLM:\SOFTWARE\FSLogix\Profiles" -Name "ConcurrentUserSessions" -Value 1 -force
# Delete the local profile when a VHD should be applied
New-ItemProperty -Path "HKLM:\SOFTWARE\FSLogix\Profiles" -Name "DeleteLocalProfileWhenVHDShouldApply" -Value 1 -force
# Change the profile directory name on each login/logout
New-ItemProperty -Path "HKLM:\SOFTWARE\FSLogix\Profiles" -Name "FlipFlopProfileDirectoryName" -Value 1 -force
# Enable dynamic VHD(X) disk type
New-ItemProperty -Path "HKLM:\SOFTWARE\FSLogix\Profiles" -Name "IsDynamic" -Value 1 -force
# Do not keep a local copy of the profile directory
New-ItemProperty -Path "HKLM:\SOFTWARE\FSLogix\Profiles" -Name "KeepLocalDir" -Value 0 -force
# Set the profile type to local
New-ItemProperty -Path "HKLM:\SOFTWARE\FSLogix\Profiles" -Name "ProfileType" -Value 0 -force
# Set the maximum size of the VHD(X) in MBs
New-ItemProperty -Path "HKLM:\SOFTWARE\FSLogix\Profiles" -Name "SizeInMBs" -Value 15000 -force
# Set the disk type to VHDX
New-ItemProperty -Path "HKLM:\SOFTWARE\FSLogix\Profiles" -Name "VolumeType" -Value "VHDX" -force
# Access the network as a computer object
New-ItemProperty -Path "HKLM:\SOFTWARE\FSLogix\Profiles" -Name "AccessNetworkAsComputerObject" -Value 1 -force

# Store credentials to access the storage account
cmdkey.exe /add:$fileShare /user:$($useraccount) /pass:$($accesskey)
# Disable Windows Defender Credential Guard (only needed for Windows 11 22H2)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "LsaCfgFlags" -Value 0 -force
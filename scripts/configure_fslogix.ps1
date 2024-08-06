configuration configureFSlogix {

    param
    (
        [Parameter(Mandatory = $true)]
        [string]$storageAccountName
    )

    Node localhost {

        $regPath = "HKLM:\SOFTWARE\FSLogix\profiles"
        New-ItemProperty -Path $regPath -Name Enabled -PropertyType DWORD -Value 1 -Force
        New-ItemProperty -Path $regPath -Name VHDLocations -PropertyType MultiString -Value \\$storageAccountName.file.core.windows.net\fslogix -Force
    
    }

}

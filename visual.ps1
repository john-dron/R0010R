while ($true) {
Get-ChildItem
Write-Output(" ")
Get-ChildItem backup
Write-Output(" ")
Get-ChildItem gs
Start-Sleep -Seconds 5
}

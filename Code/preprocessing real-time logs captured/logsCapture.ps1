# Specify the path to the Sysmon EVTX file
$evtxFilePath = "C:\Windows\System32\winevt\Logs\Microsoft-Windows-Sysmon%4Operational.evtx"

# Specify the output XML file path
$xmlOutputPath = "D:\New folder-Copy\xml\SysmonLogs.xml"

# Query Sysmon events from the EVTX file
$sysmonEvents = Get-WinEvent -Path $evtxFilePath -FilterXPath "*[System[(Provider[@Name='Microsoft-Windows-Sysmon'])]]"

# Convert events to XML and save to file
$sysmonEvents | ForEach-Object {
    $_.ToXml() | Out-File -Append -FilePath $xmlOutputPath
}

Write-Host "Sysmon logs exported to XML: $xmlOutputPath"


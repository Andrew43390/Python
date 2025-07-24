$taskName = "RoutineCIPush"
$pythonPath = "python"  # Use full path if needed, e.g., C:\Python311\python.exe
$scriptPath = "C:\Users\james\Desktop\Network\routine_ci_trigger.py"

$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM  # Change as needed
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal

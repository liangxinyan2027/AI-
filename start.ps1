$ErrorActionPreference = 'Stop'
$project = $PSScriptRoot
$python = 'D:\PYTHON-project\APO-cdr\.venv\Scripts\python.exe'
$node = 'C:\Users\15729\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
if (!(Test-Path $python)) { throw "Python not found: $python" }
if (!(Test-Path $node)) { $node = (Get-Command node).Source }
if (!(Test-NetConnection 127.0.0.1 -Port 8000 -InformationLevel Quiet -WarningAction SilentlyContinue)) {
  Start-Process $python -ArgumentList '-m uvicorn main:app --host 127.0.0.1 --port 8000' -WorkingDirectory "$project\backend" -WindowStyle Hidden -RedirectStandardOutput "$project\backend.stdout.log" -RedirectStandardError "$project\backend.stderr.log"
}
if (!(Test-NetConnection 127.0.0.1 -Port 5173 -InformationLevel Quiet -WarningAction SilentlyContinue)) {
  Start-Process $node -ArgumentList 'node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5173' -WorkingDirectory "$project\frontend" -WindowStyle Hidden -RedirectStandardOutput "$project\frontend.stdout.log" -RedirectStandardError "$project\frontend.stderr.log"
}
for ($attempt=0; $attempt -lt 30; $attempt++) {
  try {
    $health = Invoke-RestMethod 'http://127.0.0.1:5173/api/health'
    if ($health.status) { Start-Process 'http://127.0.0.1:5173/'; exit 0 }
  } catch { }
  Start-Sleep -Seconds 1
}
throw 'Startup failed. Please inspect backend.stderr.log and frontend.stderr.log.'

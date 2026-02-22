# Start all SSE-compatible MCP challenge servers
Write-Host "Starting all Damn Vulnerable MCP challenge servers with SSE support..."
Write-Host "Each server will run on a different port (9001-9010)"
Write-Host ""

# Base temp directory (Windows equivalent of /tmp)
$basePath = "$env:TEMP\dvmcp"

# Create necessary directories
New-Item -ItemType Directory -Force -Path "$basePath\challenge3\public" | Out-Null
New-Item -ItemType Directory -Force -Path "$basePath\challenge3\private" | Out-Null
New-Item -ItemType Directory -Force -Path "$basePath\challenge4\state" | Out-Null
New-Item -ItemType Directory -Force -Path "$basePath\challenge6\user_uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "$basePath\challenge8\sensitive" | Out-Null
New-Item -ItemType Directory -Force -Path "$basePath\challenge10\config" | Out-Null

# Initialize state file
'{"weather_tool_calls": 0}' | Set-Content "$basePath\challenge4\state\state.json"

# Create sample files for Challenge 3
"Welcome to the public directory!" | Set-Content "$basePath\challenge3\public\welcome.txt"
"This is a public file." | Set-Content "$basePath\challenge3\public\public_file.txt"

@"
CONFIDENTIAL: Employee Salary Information
-----------------------------------------
CEO: $1,200,000/year
CTO: $950,000/year
CFO: $900,000/year
Senior Engineers: $180,000-$250,000/year
Mid-level Engineers: $120,000-$170,000/year
Junior Engineers: $80,000-$110,000/year
"@ | Set-Content "$basePath\challenge3\private\employee_salaries.txt"

# Create sample files for Challenge 10
@"
SYSTEM CONFIGURATION
-------------------
Cloud Provider: AWS
Region: us-west-2
API Keys:
  - AWS_ACCESS_KEY_ID: AKIA5EXAMPLE12345678
  - AWS_SECRET_ACCESS_KEY: abcdef1234567890EXAMPLE/abcdefghijklmnopqrst
S3 Buckets:
  - customer-data-prod
  - financial-reports-2025
  - employee-records-confidential
"@ | Set-Content "$basePath\challenge10\config\system.conf"

@"
{
  "admin_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsIm5hbWUiOiJBZG1pbiBVc2VyIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNjUxODg0ODAwfQ.8FhJ7Z5KFUEJFoQW2xeUL9_NOzlKB3j8fKvxU_5qB4Y",
  "service_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzZXJ2aWNlIiwibmFtZSI6IlNlcnZpY2UgQWNjb3VudCIsInJvbGUiOiJzZXJ2aWNlIiwiaWF0IjoxNjUxODg0ODAwfQ.7y6t5r4e3w2q1z0x9c8v7b6n5m4k3j2h1g0f",
  "user_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwibmFtZSI6IlJlZ3VsYXIgVXNlciIsInJvbGUiOiJ1c2VyIiwiaWF0IjoxNjUxODg0ODAwfQ.9i8u7y6t5r4e3w2q1z0x9c8v7b6n5m"
}
"@ | Set-Content "$basePath\challenge10\config\tokens.json"

# List of servers
$servers = @(
    @{ Path="../../challenges/easy/challenge1/server_sse.py"; Port=9001 },
    @{ Path="../../challenges/easy/challenge2/server_sse.py"; Port=9002 },
    @{ Path="../../challenges/easy/challenge3/server_sse.py"; Port=9003 },
    @{ Path="../../challenges/medium/challenge4/server_sse.py"; Port=9004 },
    @{ Path="../../challenges/medium/challenge5/server_sse.py"; Port=9005 },
    @{ Path="../../challenges/medium/challenge6/server_sse.py"; Port=9006 },
    @{ Path="../../challenges/medium/challenge7/server_sse.py"; Port=9007 },
    @{ Path="../../challenges/hard/challenge8/server_sse.py"; Port=9008 },
    @{ Path="../../challenges/hard/challenge9/server_sse.py"; Port=9009 },
    @{ Path="../../challenges/hard/challenge10/server_sse.py"; Port=9010 }
)

$processes = @()

Write-Host "Starting all MCP challenge servers..." -ForegroundColor Cyan

foreach ($server in $servers) {
    Write-Host "Starting $($server.Path) on port $($server.Port)..."

    $proc = Start-Process python `
        -ArgumentList "$($server.Path) --port $($server.Port)" `
        -NoNewWindow `
        -PassThru

    $processes += $proc
}

Write-Host "`nAll servers started!"
Write-Host "Press Ctrl+C to stop all servers."

try {
    while ($true) {
        Start-Sleep -Seconds 2
    }
}
finally {
    Write-Host "`nStopping all servers..." -ForegroundColor Yellow
    $processes | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "All servers stopped." -ForegroundColor Green
}

Write-Host "All servers started!"
Write-Host "Close the opened PowerShell windows to stop individual servers."

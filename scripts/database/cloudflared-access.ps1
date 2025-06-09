# Start Cloudflared tunnels
$pgOutput = "pg_output.txt"
$pgError = "pg_error.txt"

$pgPort = "5433"

Remove-Item $pgOutput, $pgError -ErrorAction SilentlyContinue

$pg = Start-Process -FilePath "cloudflared" -ArgumentList "access tcp --hostname postgres.cottonbuds.dev --url localhost:$pgPort" `
    -RedirectStandardOutput $pgOutput -RedirectStandardError $pgError -NoNewWindow -PassThru

Write-Host "`nPostgres running on port ($pgPort)" -ForegroundColor Blue 
Write-Host "Connect to the services to initialize authentication and get access" -ForegroundColor Blue 
Write-Host "`nTunnels are running. Press 'q' to stop..." -ForegroundColor Green

function Output-RealTime {
    param (
        [string]$filePath
    )
    Get-Content $filePath -Wait | ForEach-Object { Write-Host $_ }
}

$pgOutputTask = Start-Job { Output-RealTime -filePath "pg_output.txt" }
$pgErrorTask = Start-Job { Output-RealTime -filePath "pg_error.txt" }

while ($true) {
    if ([console]::KeyAvailable) {
        $key = [console]::ReadKey($true)
        if ($key.KeyChar -eq 'q') {
            Write-Host "`nStopping tunnels..." -ForegroundColor Yellow

            if ($pg -and (Get-Process -Id $pg.Id -ErrorAction SilentlyContinue)) {
                Stop-Process -Id $pg.Id -Force
            }

            Stop-Job $pgOutputTask, $pgErrorTask
            Remove-Job $pgOutputTask, $pgErrorTask
            break
        }
    }
    Start-Sleep -Milliseconds 100
}

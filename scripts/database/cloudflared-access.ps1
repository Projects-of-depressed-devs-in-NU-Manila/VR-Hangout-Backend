# Start Cloudflared tunnels
$pgOutput = "pg_output.txt"
$pgError = "pg_error.txt"
$redisOutput = "redis_output.txt"
$redisError = "redis_error.txt"

# Clean up old output files
Remove-Item $pgOutput, $pgError, $redisOutput, $redisError -ErrorAction SilentlyContinue

# Start processes
$pg = Start-Process -FilePath "cloudflared" -ArgumentList "access tcp --hostname postgres.cottonbuds.org --url localhost:5433" `
    -RedirectStandardOutput $pgOutput -RedirectStandardError $pgError -NoNewWindow -PassThru

$redis = Start-Process -FilePath "cloudflared" -ArgumentList "access tcp --hostname redis.cottonbuds.org --url localhost:6379" `
    -RedirectStandardOutput $redisOutput -RedirectStandardError $redisError -NoNewWindow -PassThru

Write-Host "`nPostgres running on port (5432)" -ForegroundColor Blue 
Write-Host "`nRedis running on port (6379)" -ForegroundColor Blue 
Write-Host "Connect to the services to initialize authentication and get access" -ForegroundColor Blue 
Write-Host "`nTunnels are running. Press 'q' to stop..." -ForegroundColor Green

# Setup function to output content to console in real-time
function Output-RealTime {
    param (
        [string]$filePath
    )
    Get-Content $filePath -Wait | ForEach-Object { Write-Host $_ }
}

# Start output streaming in background for both cloudflared processes
$pgOutputTask = Start-Job { Output-RealTime -filePath "pg_output.txt" }
$pgErrorTask = Start-Job { Output-RealTime -filePath "pg_error.txt" }
$redisOutputTask = Start-Job { Output-RealTime -filePath "redis_output.txt" }
$redisErrorTask = Start-Job { Output-RealTime -filePath "redis_error.txt" }

# Monitor for 'q' keypress
while ($true) {
    if ([console]::KeyAvailable) {
        $key = [console]::ReadKey($true)
        if ($key.KeyChar -eq 'q') {
            Write-Host "`nStopping tunnels..." -ForegroundColor Yellow
            Stop-Process -Id $pg.Id -Force
            Stop-Process -Id $redis.Id -Force
            Stop-Job $pgOutputTask, $redisOutputTask, $pgErrorTask, $redisErrorTask
            Remove-Job $pgOutputTask, $redisOutputTask, $pgErrorTask, $redisErrorTask
            break
        }
    }
    Start-Sleep -Milliseconds 100
}

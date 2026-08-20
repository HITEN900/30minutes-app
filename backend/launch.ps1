# ============================================
# LAUNCH 30 MINUTES APP - COMPLETE
# ============================================

Write-Host "🚀 Starting 30 Minutes App..." -ForegroundColor Cyan

# Navigate to backend
cd C:\Users\Lenovo\30minutes-app\backend

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Run migrations
Write-Host "🔄 Running migrations..." -ForegroundColor Yellow
python manage.py migrate

# Collect static files
Write-Host "📁 Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Start the server
Write-Host ""
Write-Host "🌐 Server running at: http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host "📱 Open this URL in your browser to see the interface!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver

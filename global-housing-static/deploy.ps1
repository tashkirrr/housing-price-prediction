# PowerShell script to deploy to GitHub
# Usage: ./deploy.ps1 -RepoUrl "https://github.com/YOUR_USERNAME/REPO_NAME.git"

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl
)

Write-Host "🚀 Deploying to GitHub..." -ForegroundColor Green

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✓ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git not found. Please install Git first." -ForegroundColor Red
    exit 1
}

# Initialize git if not already
if (-not (Test-Path .git)) {
    Write-Host "📁 Initializing git repository..." -ForegroundColor Yellow
    git init
}

# Add all files
Write-Host "📦 Adding files..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "💾 Committing..." -ForegroundColor Yellow
git commit -m "Update website with modern real estate design"

# Add remote
Write-Host "🔗 Adding remote..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin $RepoUrl

# Push
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main -f

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Your site will be available at: https://YOUR_USERNAME.github.io/REPO_NAME/" -ForegroundColor Cyan

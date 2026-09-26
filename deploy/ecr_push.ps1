<#
.SYNOPSIS
  Builds the Docker image and pushes it to Amazon ECR.

.NOTES
  Prerequisites: AWS CLI v2 configured (aws configure), Docker Desktop running.
  Run from the repository root: .\deploy\ecr_push.ps1
#>

param(
    [string]$AwsRegion = "us-east-1",
    [string]$RepoName = "eugene-agentcore-poc",
    [string]$ImageTag = "latest"
)

$ErrorActionPreference = "Stop"

$AccountId = (aws sts get-caller-identity --query Account --output text)
if (-not $AccountId) {
    throw "Unable to resolve AWS account id. Check 'aws configure' / credentials."
}

$RepoUri = "$AccountId.dkr.ecr.$AwsRegion.amazonaws.com/$RepoName"

Write-Host "Account: $AccountId | Region: $AwsRegion | Repo: $RepoUri"

# 1. Create the ECR repository if it doesn't already exist
$ErrorActionPreference = "Continue"
$existing = aws ecr describe-repositories --repository-names $RepoName --region $AwsRegion 2>$null
$ErrorActionPreference = "Stop"
if (-not $existing) {
    Write-Host "Creating ECR repository '$RepoName'..."
    aws ecr create-repository `
        --repository-name $RepoName `
        --region $AwsRegion `
        --image-scanning-configuration scanOnPush=true `
        --encryption-configuration encryptionType=AES256 | Out-Null
}

# 2. Authenticate Docker to ECR
aws ecr get-login-password --region $AwsRegion | docker login --username AWS --password-stdin "$AccountId.dkr.ecr.$AwsRegion.amazonaws.com"

# 3. Build, tag, push
docker build -t "$RepoName`:$ImageTag" .
docker tag "$RepoName`:$ImageTag" "$RepoUri`:$ImageTag"
docker push "$RepoUri`:$ImageTag"

Write-Host "Pushed image: $RepoUri`:$ImageTag"

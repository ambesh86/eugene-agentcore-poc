<#
.SYNOPSIS
  Uploads local data/ (JSON + PDFs) to an S3 bucket for the app to consume with DATA_SOURCE=s3.

.NOTES
  Run from the repository root: .\deploy\upload_data_to_s3.ps1 -BucketName my-bucket
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$BucketName,
    [string]$Prefix = "data",
    [string]$AwsRegion = "us-east-1"
)

$ErrorActionPreference = "Stop"

$ErrorActionPreference = "Continue"
aws s3api head-bucket --bucket $BucketName 2>$null
$bucketExists = $?
$ErrorActionPreference = "Stop"
if (-not $bucketExists) {
    Write-Host "Creating bucket '$BucketName' in $AwsRegion..."
    if ($AwsRegion -eq "us-east-1") {
        aws s3api create-bucket --bucket $BucketName --region $AwsRegion | Out-Null
    } else {
        aws s3api create-bucket --bucket $BucketName --region $AwsRegion `
            --create-bucket-configuration LocationConstraint=$AwsRegion | Out-Null
    }
    aws s3api put-public-access-block --bucket $BucketName --public-access-block-configuration `
        BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true | Out-Null
}

aws s3 sync .\data "s3://$BucketName/$Prefix" --region $AwsRegion

Write-Host "Data synced to s3://$BucketName/$Prefix"
Write-Host "Set DATA_SOURCE=s3, S3_BUCKET=$BucketName, S3_DATA_PREFIX=$Prefix in your environment/task definition."

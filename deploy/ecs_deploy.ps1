<#
.SYNOPSIS
  Registers the ECS task definition and creates/updates a Fargate service behind an ALB.

.NOTES
  Fill in the placeholders below (VPC subnets, security group, ALB target group) before running.
  This assumes the task definition JSON has already had <ACCOUNT_ID>/<AWS_REGION>/<S3_BUCKET_NAME>
  placeholders substituted (see deploy/ecs-task-definition.json).
#>

param(
    [string]$AwsRegion = "us-east-1",
    [string]$ClusterName = "eugene-agentcore-cluster",
    [string]$ServiceName = "eugene-agentcore-service",
    [string]$TaskDefFile = "deploy/ecs-task-definition.json",
    [Parameter(Mandatory = $true)][string[]]$SubnetIds,
    [Parameter(Mandatory = $true)][string]$SecurityGroupId,
    [string]$TargetGroupArn
)

$ErrorActionPreference = "Stop"

# 1. Create the cluster if it doesn't exist
$clusters = aws ecs describe-clusters --clusters $ClusterName --region $AwsRegion | ConvertFrom-Json
if (-not ($clusters.clusters | Where-Object { $_.status -eq "ACTIVE" })) {
    aws ecs create-cluster --cluster-name $ClusterName --region $AwsRegion | Out-Null
}

# 2. Register the task definition
$registered = aws ecs register-task-definition `
    --cli-input-json file://$TaskDefFile `
    --region $AwsRegion | ConvertFrom-Json

$taskDefArn = $registered.taskDefinition.taskDefinitionArn
Write-Host "Registered task definition: $taskDefArn"

$subnetArg = ($SubnetIds -join ",")
$networkConfig = "awsvpcConfiguration={subnets=[$subnetArg],securityGroups=[$SecurityGroupId],assignPublicIp=ENABLED}"

# 3. Create or update the service
$service = aws ecs describe-services --cluster $ClusterName --services $ServiceName --region $AwsRegion | ConvertFrom-Json
if ($service.services -and $service.services[0].status -eq "ACTIVE") {
    Write-Host "Updating existing service '$ServiceName'..."
    aws ecs update-service `
        --cluster $ClusterName `
        --service $ServiceName `
        --task-definition $taskDefArn `
        --region $AwsRegion | Out-Null
} else {
    Write-Host "Creating new service '$ServiceName'..."
    $loadBalancerArgs = @()
    if ($TargetGroupArn) {
        $loadBalancerArgs = @(
            "--load-balancers",
            "targetGroupArn=$TargetGroupArn,containerName=eugene-agentcore-poc,containerPort=8501"
        )
    }

    aws ecs create-service `
        --cluster $ClusterName `
        --service-name $ServiceName `
        --task-definition $taskDefArn `
        --desired-count 1 `
        --launch-type FARGATE `
        --network-configuration $networkConfig `
        --region $AwsRegion `
        @loadBalancerArgs | Out-Null
}

Write-Host "Deployment triggered. Check status with: aws ecs describe-services --cluster $ClusterName --services $ServiceName --region $AwsRegion"

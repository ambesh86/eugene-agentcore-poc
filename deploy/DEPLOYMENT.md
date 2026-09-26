# AWS Runtime Deployment Guide

End-to-end steps to take this POC from local Streamlit app to a containerized,
Bedrock-powered service running on ECS Fargate, backed by S3 for data.

## Prerequisites

- AWS CLI v2, configured (`aws configure`) with an account that can manage ECR/ECS/S3/IAM
- Docker Desktop running
- Bedrock model access enabled in your AWS account/region for the Claude model you choose
  (Bedrock console → Model access)

## 1. Dockerize the POC

```powershell
docker build -t eugene-agentcore-poc:latest .
docker run -p 8501:8501 --env-file .env eugene-agentcore-poc:latest
```

Open http://localhost:8501 to verify locally before pushing.

Files: [Dockerfile](../Dockerfile), [.dockerignore](../.dockerignore), [docker-compose.yml](../docker-compose.yml)

## 2. Push image to Amazon ECR

```powershell
.\deploy\ecr_push.ps1 -AwsRegion us-east-1 -RepoName eugene-agentcore-poc -ImageTag latest
```

This creates the ECR repo (if missing), authenticates Docker, and pushes the image.
Note the printed repo URI — you'll need it for the task definition.

## 3. Store data in S3

```powershell
.\deploy\upload_data_to_s3.ps1 -BucketName <your-bucket-name> -AwsRegion us-east-1
```

Syncs `data/` (drugs.json, publication.json, graph.json, pdfs/) to S3. The app reads via
[utils/s3_client.py](../utils/s3_client.py), toggled by the `DATA_SOURCE` env var:

- `DATA_SOURCE=local` (default) — reads from the local `data/` folder, unchanged behavior
- `DATA_SOURCE=s3` — reads from `s3://$S3_BUCKET/$S3_DATA_PREFIX/...`

## 4. Integrate Amazon Bedrock (replace rule-based Supervisor)

Set `USE_BEDROCK_SUPERVISOR=true` to route intent classification through
[agents/bedrock_supervisor_agent.py](../agents/bedrock_supervisor_agent.py) (Claude Sonnet/Haiku via
`langchain-aws`). The prompt lives in [prompt/supervisor.txt](../prompt/supervisor.txt).
If Bedrock fails or returns an unparseable response, it automatically falls back to the
deterministic [agents/supervisor_agent.py](../agents/supervisor_agent.py) — no hard failure.

Required env vars: `AWS_REGION`, `BEDROCK_MODEL_ID` (defaults to
`us.anthropic.claude-haiku-4-5-20251001-v1:0`, a cross-region inference profile — newer Claude
models on Bedrock reject direct on-demand invocation and require an inference profile ID), and
AWS credentials with `bedrock:InvokeModel` permission (grant via the ECS task role — see step 5).

**One-time console step (cannot be done via CLI with PowerUserAccess):** open
**Bedrock console → Model access** in `us-east-1` and request/enable access for the Anthropic
Claude model(s) you intend to use. Until access is granted, invocation fails with
`AccessDeniedException: ... aws-marketplace:Subscribe ...` — this was confirmed via
`aws bedrock-runtime invoke-model` in this account. Run
`aws bedrock list-inference-profiles --region us-east-1` to confirm the exact profile ID once
access is granted.

## 5. Deploy on ECS Fargate

1. Edit [deploy/ecs-task-definition.json](../deploy/ecs-task-definition.json) and replace
   `<ACCOUNT_ID>`, `<AWS_REGION>`, `<S3_BUCKET_NAME>` with real values.
2. Create IAM roles (one-time):
   - `ecsTaskExecutionRole` — standard ECS execution role (pull image, write logs). Attach the
     managed policy `AmazonECSTaskExecutionRolePolicy`.
   - `eugeneAgentCoreTaskRole` — the app's runtime role. Attach policies granting:
     - `s3:GetObject`, `s3:ListBucket` on your data bucket
     - `bedrock:InvokeModel` on the Claude model(s)/inference profile(s) you use
3. Run:

```powershell
.\deploy\ecs_deploy.ps1 `
  -AwsRegion us-east-1 `
  -SubnetIds subnet-aaaa,subnet-bbbb `
  -SecurityGroupId sg-xxxxxxxx `
  -TargetGroupArn arn:aws:elasticloadbalancing:...:targetgroup/eugene-tg/xxxx
```

This creates the cluster (if missing), registers the task definition, and creates/updates the
Fargate service. Omit `-TargetGroupArn` if you don't have an ALB yet (service will still run;
add a load balancer later via `aws ecs update-service`).

Security group must allow inbound TCP 8501 from your ALB/security group, and outbound HTTPS
(443) for Bedrock, S3, and ECR pulls.

## 6. Future upgrade path → Amazon Bedrock AgentCore

| Current POC component                          | AgentCore equivalent        |
|-------------------------------------------------|------------------------------|
| `agents/supervisor_agent.py` / `bedrock_supervisor_agent.py` | AgentCore Supervisor (orchestration + routing) |
| `mcp/gateway.py`, `mcp/registry.py`             | AgentCore Gateway (tool registration/invocation) |
| `memory/memory_store.py`, `memory/checkpoint.py`| AgentCore Memory (session + long-term memory)   |
| `agents/foundation_agent.py`, `graph_agent.py`, `publication_agent.py` | AgentCore Agents (same responsibilities, hosted runtime) |
| LangGraph `graph/workflow.py`                   | AgentCore Runtime workflow orchestration        |

Migration is incremental: the MCP tool interface (`invoke_tool(name, *args)`) maps cleanly onto
AgentCore Gateway's tool-invocation contract, and the Supervisor's `run(state)` contract maps onto
an AgentCore Supervisor action. No changes to `tools/*` business logic are expected.

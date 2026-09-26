# Eugene AgentCore + LangGraph Multi-Agent Research Assistant POC

## Overview

Eugene POC is a Multi-Agent Research Assistant built using LangGraph, MCP Gateway, Memory, Graph Analytics, and Domain-Specific Agents. The system demonstrates how multiple AI agents collaborate to analyze biomedical research queries, retrieve information from structured and unstructured sources, perform graph analysis, and generate a consolidated research report.

## Key Features

- Supervisor Agent for intent classification and routing
- Foundation Agent for drug, disease, target and pathway information
- Graph Agent for relationship discovery and graph analytics
- Publication Agent for PDF and publication evidence retrieval
- MCP Gateway for tool orchestration
- Short-Term Memory (Session Context)
- Long-Term Memory (Persistent Knowledge)
- LangGraph Workflow Orchestration
- Graph Analytics (PageRank, Degree Centrality, Betweenness, Closeness)
- Streamlit User Interface

---

# High-Level Architecture

```text
User
 │
 ▼
Streamlit UI
 │
 ▼
Short-Term Memory
 │
 ▼
Supervisor Agent
 │
 ▼
Long-Term Memory
 │
 ▼
LangGraph StateGraph
 │
 ├──────────────┬──────────────┬──────────────┐
 ▼              ▼              ▼
Foundation    Graph Agent   Publication Agent
 Agent
 │              │              │
 └───────┬──────┴──────┬───────┘
         ▼
     MCP Gateway
         │
 ┌───────┼──────────────┐
 ▼       ▼              ▼
Drug   Graph Tool    PDF Tool
Tool
 │       │              │
 ▼       ▼              ▼
JSON  Graph Analytics  PDFs
```

---

# Agent Responsibilities

## Supervisor Agent

Responsibilities:
- Intent Classification
- Entity Extraction
- Query Resolution
- Agent Selection
- Memory Lookup

Example:

```text
Query:
Analyze KRAS importance

Selected Agents:
Graph Agent
```

## Foundation Agent

Responsibilities:
- Drug Search
- Disease Search
- Target Search
- Pathway Information

Sources:

```text
drugs.json
```

## Graph Agent

Responsibilities:
- Relationship Discovery
- Multi-hop Traversal
- Graph Analytics
- Graph-Based Reasoning

## Publication Agent

Responsibilities:
- Publication Search
- PDF Search
- Evidence Retrieval
- Research Summarization

---

# MCP Gateway

Purpose:

```text
Central Tool Router
```

Responsibilities:

- Tool Discovery
- Tool Registry
- Tool Invocation
- Request Logging
- Response Handling

Flow:

```text
Agent
   ↓
MCP Gateway
   ↓
Tool Registry
   ↓
Tool Execution
   ↓
Response
```

---

# Memory Architecture

## Short-Term Memory

Purpose:

- Session Context
- Last Query Tracking
- Last Entity Tracking

Example:

```json
{
  "last_entity":"KRAS",
  "last_query":"Tell me about KRAS inhibitors"
}
```

## Long-Term Memory

Purpose:

- Historical Research Storage
- Context Reuse Across Sessions
- Knowledge Persistence

Storage:

```text
data/long_term_memory.json
```

Example:

```json
{
  "entity":"KRAS",
  "pathway":"MAPK",
  "disease":"Pancreatic Cancer"
}
```

---

# Graph Analytics

## PageRank

Purpose:
Determine the most influential node in the graph.

Eugene Example:

```text
Sotorasib
   ↓
KRAS
   ↓
MAPK
   ↓
Pancreatic Cancer
```

Result:

```text
KRAS receives highest PageRank score.
```

## Degree Centrality

Purpose:
Measure how many direct connections a node has.

Example:

```text
KRAS connected to:
Drug
Disease
Pathway
Target
```

Higher connections = Higher Degree Centrality.

## Betweenness Centrality

Purpose:
Identify bridge nodes.

Example:

```text
Drug
 ↓
KRAS
 ↓
Disease
```

KRAS acts as a bridge between entities.

## Closeness Centrality

Purpose:
Determine how quickly a node can reach other nodes.

Example:

```text
KRAS reaches most nodes in few hops.
```

---

# Project Structure

```text
eugene-agentcore-poc/
│
├── agents/
├── graph/
├── tools/
├── retrievers/
├── mcp/
├── memory/
├── data/
├── ui/
├── app.py
├── requirements.txt
└── README.md
```

---

# Running the POC Locally

## Create Environment

```bash
python -m venv .venv
```

## Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Launch Streamlit

```bash
streamlit run ui/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

# Example Queries

```text
Tell me about KRAS inhibitors
```

```text
Analyze KRAS importance
```

```text
Show publication evidence for KRAS
```

```text
Show related pathways
```

---

# AWS Deployment Guide

## Step 1 - Dockerize Application

```bash
docker build -t eugene-poc .
```

## Step 2 - Push to Amazon ECR

```bash
docker tag eugene-poc <account>.dkr.ecr.<region>.amazonaws.com/eugene-poc
```

```bash
docker push <ecr-uri>
```

## Step 3 - Deploy to ECS Fargate

Services:

- ECS Fargate
- ECR
- IAM
- CloudWatch

## Step 4 - Store Documents in S3

```text
PDF Files
JSON Knowledge Base
Research Documents
```

## Step 5 - Future Bedrock Integration

Replace Rule-Based Supervisor with:

```text
Claude Sonnet
Claude Haiku
```

## Step 6 - Future AgentCore Migration

```text
Supervisor Agent   → AgentCore Supervisor
MCP Gateway        → AgentCore Gateway
Memory Store       → AgentCore Memory
LangGraph          → AgentCore Workflows
```

---

# Use Cases

- Drug Discovery
- Biomedical Research
- Literature Review
- Knowledge Graph Exploration
- Research Evidence Generation
- Multi-Agent Reasoning

---

# Future Roadmap

Phase 1
- LangGraph
- MCP Gateway
- Memory

Phase 2
- Neo4j Integration
- GraphRAG

Phase 3
- Bedrock Claude Models

Phase 4
- AgentCore Runtime
- AgentCore Memory
- AgentCore Gateway

---

# Conclusion

This POC demonstrates a complete Multi-Agent Research Assistant architecture built on LangGraph, MCP Gateway, Memory, Graph Analytics, and Domain Agents. It provides a foundation for evolving toward AWS Bedrock AgentCore, Neo4j GraphRAG, and enterprise-scale biomedical research workflows.

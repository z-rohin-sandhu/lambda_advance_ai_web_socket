# Advance AI WebSocket Service

This repository contains the AWS Lambda–based WebSocket backend
for Advance AI real-time LLM + audio streaming.

## Architecture

- AWS API Gateway (WebSocket)
- AWS Lambda (Python 3.11)
- Redis (ElastiCache) for session & connection state
- Action-based WebSocket protocol

## Supported Actions
 -------------------------------------------------
| Action       | Description                      |
|--------------|----------------------------------|
| ping         | Health check                     |
| get_response | Start AI response streaming      |
 -------------------------------------------------



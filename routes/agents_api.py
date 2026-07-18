from fastapi import APIRouter, Request
from typing import List
from entities.api_agent_info import ApiAgentInfo
import services.agents_service as agents_service

agents_router = APIRouter(prefix="/agents", tags=["Agents"])

@agents_router.post("/")
def create_agent(agent_data: ApiAgentInfo, request: Request):
    token = getattr(request.state, "token", None)
    return agents_service.create_agent(agent_data, token)

@agents_router.put("/{agent_id}")
def update_agent(agent_id: str, agent_data: ApiAgentInfo, request: Request):
    token = getattr(request.state, "token", None)
    return agents_service.update_agent(agent_id, agent_data, token)

@agents_router.delete("/{agent_id}")
def delete_agent(agent_id: str, request: Request):
    token = getattr(request.state, "token", None)
    return agents_service.delete_agent(agent_id, token)

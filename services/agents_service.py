from fastapi import HTTPException
from typing import Optional
from entities.api_agent_info import ApiAgentInfo
from services.supabase_db_connection.supabase_client import get_supabase
from datetime import datetime


def create_agent(agent_data: ApiAgentInfo, token: Optional[str]) -> dict:
    supabase = get_supabase(access_token=token)
    try:
        response = supabase.table("user_api_agents").insert(agent_data.model_dump(exclude={"id"})).execute()
        return {"message": "Agent created successfully", "data": response.data}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

def update_agent(agent_id: str, agent_data: ApiAgentInfo, token: Optional[str]) -> dict:
    supabase = get_supabase(access_token=token)
    try:
        data = agent_data.model_dump(exclude={"id", "user_id"})
        data["updated_at"] = datetime.utcnow().isoformat()
        print(data)
        supabase.table("user_api_agents").update(data).eq("id", agent_id).execute()
        return {"message": "Agent updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def delete_agent(agent_id: str, token: Optional[str]) -> dict:
    supabase = get_supabase(access_token=token)
    try:
        supabase.table("user_api_agents").delete().eq("id", agent_id).execute()
        return {"message": "Agent deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

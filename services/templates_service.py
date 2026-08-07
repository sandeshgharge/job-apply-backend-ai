from bson import ObjectId
from fastapi import HTTPException
from entities.template_model import TemplateModel, TemplateCreate, TemplateUpdate, TemplatePreviewRequest
from services.mongo_db_connection.db import cv_templates_collection, cl_templates_collection
from services.doc_service.template_management import template_env
import json
from jinja2 import Environment, BaseLoader

# We need to create an environment similar to template_env but able to load from string
preview_env = Environment(autoescape=True)
preview_env.filters["format_date"] = template_env.filters["format_date"]
preview_env.filters["tojson"] = template_env.filters["tojson"]

def get_collection(docType: str):
    if docType == "cv":
        return cv_templates_collection
    elif docType == "cl":
        return cl_templates_collection
    else:
        raise HTTPException(status_code=400, detail="Invalid docType")

async def get_templates(docType: str, user_id: str, include_public: bool = False):
    collection = get_collection(docType)
    
    query = {"$or": [{"userId": user_id}]}
    if include_public:
        query["$or"].append({"isPublic": True})
        
    cursor = collection.find(query)
    templates = []
    async for t in cursor:
        t["_id"] = str(t["_id"])
        templates.append(t)
    return templates

async def create_template(docType: str, template: TemplateCreate):
    collection = get_collection(docType)
    payload = template.model_dump()
    result = await collection.insert_one(payload)
    created = await collection.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created

async def update_template(docType: str, id: str, template: TemplateUpdate, user_id: str):
    collection = get_collection(docType)
    existing = await collection.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Template not found")
    if existing.get("userId") != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    update_data = template.model_dump(exclude_unset=True)
    update_data.pop("userId", None) # prevent changing owner
    
    updated = await collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=True
    )
    updated["_id"] = str(updated["_id"])
    return updated

async def delete_template(docType: str, id: str, user_id: str):
    collection = get_collection(docType)
    existing = await collection.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Template not found")
    if existing.get("userId") != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    await collection.delete_one({"_id": ObjectId(id)})
    return {"message": "Deleted"}

async def preview_template(req: TemplatePreviewRequest):
    # Here we would fetch actual user profile data to pass to Jinja
    # For now, we mock some data so the preview works seamlessly
    try:
        jinja_template = preview_env.from_string(req.html_template)
        
        # Mock data (you'd normally fetch real profile data)
        mock_data = {
            "p": {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "phone": "+1 234 567 8900",
                "link": "https://linkedin.com/in/janedoe"
            },
            "experience": [
                {"title": "Software Engineer", "company": "Tech Corp", "start_date": "2020-01", "end_date": "2023-01", "description": "Developed web applications.", "include": True}
            ],
            "skills": {
                "frontend": ["Angular", "React", "HTML"],
                "backend": ["Python", "Node.js"]
            }
        }
        
        rendered_html = jinja_template.render(**mock_data)
        return {"rendered_html": rendered_html}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

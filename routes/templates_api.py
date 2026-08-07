from fastapi import APIRouter, Query, Request
import services.templates_service as templates_service
from entities.template_model import TemplateCreate, TemplateUpdate, TemplatePreviewRequest

templates_router = APIRouter(prefix="/templates", tags=["Templates"])

@templates_router.get("/{docType}/user/{userId}")
async def get_templates(docType: str, userId: str, includePublic: bool = Query(False)):
    return await templates_service.get_templates(docType, userId, includePublic)

@templates_router.post("/preview")
async def preview_template(req: TemplatePreviewRequest):
    return await templates_service.preview_template(req)

@templates_router.post("/{docType}")
async def create_template(docType: str, template: TemplateCreate):
    return await templates_service.create_template(docType, template)

@templates_router.put("/{docType}/{id}")
async def update_template(docType: str, id: str, template: TemplateUpdate):
    return await templates_service.update_template(docType, id, template, template.userId)

@templates_router.delete("/{docType}/{id}")
async def delete_template(docType: str, id: str, userId: str = Query(...)):
    return await templates_service.delete_template(docType, id, userId)

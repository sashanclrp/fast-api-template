from fastapi import APIRouter, HTTPException, Query, Path, Body
from typing import Dict, Any, List, Optional

from schemas.template_schemas import TemplateCreate, TemplateResponse, TemplateUpdate
from services.template_service import get_templates, get_template_by_id, create_template, update_template, delete_template
from utils.logger import logger

router = APIRouter()

@router.get("/", response_model=List[TemplateResponse])
async def list_templates(
    skip: int = Query(0, description="Number of templates to skip"),
    limit: int = Query(10, description="Maximum number of templates to return")
):
    """
    Get a list of templates with pagination.
    """
    templates = await get_templates(skip, limit)
    return templates

@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: str = Path(..., description="The ID of the template to get")
):
    """
    Get a template by ID.
    """
    template = await get_template_by_id(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.post("/", response_model=TemplateResponse, status_code=201)
async def create_new_template(
    template: TemplateCreate = Body(..., description="Template data to create")
):
    """
    Create a new template.
    """
    created_template = await create_template(template)
    return created_template

@router.put("/{template_id}", response_model=TemplateResponse)
async def update_existing_template(
    template_id: str = Path(..., description="The ID of the template to update"),
    template: TemplateUpdate = Body(..., description="Template data to update")
):
    """
    Update an existing template.
    """
    updated_template = await update_template(template_id, template)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Template not found")
    return updated_template

@router.delete("/{template_id}")
async def delete_existing_template(
    template_id: str = Path(..., description="The ID of the template to delete")
):
    """
    Delete a template.
    """
    success = await delete_template(template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"message": "Template deleted successfully"} 
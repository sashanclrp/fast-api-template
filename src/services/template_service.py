from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime
import asyncio

from utils.logger import logger

# In-memory storage for templates (replace with a database in a real application)
templates_db = {}

async def get_templates(skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get a list of templates with pagination.
    
    Args:
        skip: Number of templates to skip
        limit: Maximum number of templates to return
        
    Returns:
        A list of templates
    """
    try:
        # Convert the templates dictionary to a list and apply pagination
        templates_list = list(templates_db.values())
        return templates_list[skip:skip + limit]
    
    except Exception as e:
        logger.error(f"Error getting templates: {str(e)}", exc_info=True)
        return []

async def get_template_by_id(template_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a template by ID.
    
    Args:
        template_id: The ID of the template to get
        
    Returns:
        The template or None if not found
    """
    try:
        return templates_db.get(template_id)
    
    except Exception as e:
        logger.error(f"Error getting template {template_id}: {str(e)}", exc_info=True)
        return None

async def create_template(template_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new template.
    
    Args:
        template_data: The template data to create
        
    Returns:
        The created template
    """
    try:
        # Generate a unique ID for the template
        template_id = str(uuid.uuid4())
        
        # Get the current timestamp
        now = datetime.now()
        
        # Create the template
        template = {
            "id": template_id,
            "name": template_data.name,
            "description": template_data.description,
            "content": template_data.content,
            "tags": template_data.tags,
            "created_at": now,
            "updated_at": now
        }
        
        # Store the template
        templates_db[template_id] = template
        
        logger.info(f"Created template: {template_id}")
        
        return template
    
    except Exception as e:
        logger.error(f"Error creating template: {str(e)}", exc_info=True)
        raise

async def update_template(template_id: str, template_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update an existing template.
    
    Args:
        template_id: The ID of the template to update
        template_data: The template data to update
        
    Returns:
        The updated template or None if not found
    """
    try:
        # Check if the template exists
        template = templates_db.get(template_id)
        if not template:
            logger.warning(f"Template not found: {template_id}")
            return None
        
        # Update the template fields if provided
        if template_data.name is not None:
            template["name"] = template_data.name
        
        if template_data.description is not None:
            template["description"] = template_data.description
        
        if template_data.content is not None:
            template["content"] = template_data.content
        
        if template_data.tags is not None:
            template["tags"] = template_data.tags
        
        # Update the updated_at timestamp
        template["updated_at"] = datetime.now()
        
        # Store the updated template
        templates_db[template_id] = template
        
        logger.info(f"Updated template: {template_id}")
        
        return template
    
    except Exception as e:
        logger.error(f"Error updating template {template_id}: {str(e)}", exc_info=True)
        return None

async def delete_template(template_id: str) -> bool:
    """
    Delete a template.
    
    Args:
        template_id: The ID of the template to delete
        
    Returns:
        True if the template was deleted, False otherwise
    """
    try:
        # Check if the template exists
        if template_id not in templates_db:
            logger.warning(f"Template not found: {template_id}")
            return False
        
        # Delete the template
        del templates_db[template_id]
        
        logger.info(f"Deleted template: {template_id}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error deleting template {template_id}: {str(e)}", exc_info=True)
        return False 
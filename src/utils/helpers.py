import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

from logger import logger

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object to a string.
    
    Args:
        dt: The datetime object to format
        format_str: The format string
        
    Returns:
        The formatted datetime string
    """
    return dt.strftime(format_str)

def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """
    Parse a datetime string to a datetime object.
    
    Args:
        dt_str: The datetime string to parse
        format_str: The format string
        
    Returns:
        The parsed datetime object or None if parsing fails
    """
    try:
        return datetime.strptime(dt_str, format_str)
    except ValueError as e:
        logger.error(f"Error parsing datetime {dt_str}: {str(e)}")
        return None

def validate_json(json_str: str) -> Union[Dict[str, Any], List[Any], None]:
    """
    Validate a JSON string.
    
    Args:
        json_str: The JSON string to validate
        
    Returns:
        The parsed JSON data or None if parsing fails
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {str(e)}")
        return None

def truncate_string(s: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length.
    
    Args:
        s: The string to truncate
        max_length: The maximum length
        suffix: The suffix to add if the string is truncated
        
    Returns:
        The truncated string
    """
    if len(s) <= max_length:
        return s
    
    return s[:max_length - len(suffix)] + suffix 
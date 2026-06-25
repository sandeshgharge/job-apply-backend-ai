# core/template_manager.py

from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


TEMPLATES_DIR = Path(__file__).parent / "html_templates"

def format_date(value: str) -> str:
    if not value or not isinstance(value, str):
        return value or ""
    
    # Try parsing different common ISO date formats
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            dt = datetime.strptime(value.strip(), fmt)
            return dt.strftime("%b %y")
        except ValueError:
            continue
            
    # Try parsing just the year
    try:
        dt = datetime.strptime(value.strip(), "%Y")
        return dt.strftime("%Y")
    except ValueError:
        pass
        
    return value

template_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"])
)

# Register the date formatter filter
template_env.filters["format_date"] = format_date
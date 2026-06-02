# core/template_manager.py

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


TEMPLATES_DIR = Path(__file__).parent / "html_templates"

template_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"])
)
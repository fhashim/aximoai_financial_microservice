from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# Set up Jinja2 environment
TEMPLATES_DIR = Path(__file__).parent.parent / "sql"
jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

def render_sql_template(template_name, **params):
    template = jinja_env.get_template(template_name)
    return template.render(**params)

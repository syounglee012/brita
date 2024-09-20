import jinja2
import os

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


def process_template(template_file, context):
    try:
        template = jinja_env.get_template(template_file)
        return template.render(context)
    except jinja2.exceptions.TemplateNotFound:
        print(f"Template '{template_file}' not found in '{template_dir}'")
        raise

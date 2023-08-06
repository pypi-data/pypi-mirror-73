import os
import shutil

from django.conf import settings
from django_assets import Bundle, register

static = os.path.join(settings.PROJECT_DIR, "static")
node_modules = os.path.join(static, "node_modules")
svg_folder = os.path.join(node_modules, "@fortawesome", "fontawesome-free", "svgs")
destination = os.path.join(static, "svg", "fontawesome")
if not os.path.exists(destination) and os.path.isdir(svg_folder):
    shutil.copytree(svg_folder, destination)

scss = Bundle("scss/app.scss", filters="scss", output="css/app.scss")

css_all = Bundle(scss, filters="cssrewrite", output="css/app.css")

ORIGINAL_CSS_PATH = os.path.join(settings.STATIC_ROOT, css_all.output + ".original.css")
if os.path.exists(ORIGINAL_CSS_PATH):
    os.remove(ORIGINAL_CSS_PATH)

register("css_all", css_all)

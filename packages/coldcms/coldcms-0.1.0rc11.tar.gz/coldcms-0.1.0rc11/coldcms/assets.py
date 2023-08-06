import os

from django.conf import settings
from django_assets import Bundle, register

scss = Bundle("scss/app.scss", filters="scss", output="css/app.scss")

css_all = Bundle(scss, filters="cssrewrite", output="css/app.css")

ORIGINAL_CSS_PATH = os.path.join(settings.STATIC_ROOT, css_all.output + ".original.css")
if os.path.exists(ORIGINAL_CSS_PATH):
    os.remove(ORIGINAL_CSS_PATH)

register("css_all", css_all)

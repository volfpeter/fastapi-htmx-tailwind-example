from fastapi.templating import Jinja2Templates
from fasthx import Jinja

from .constants import templates_dir

jinja = Jinja(Jinja2Templates(templates_dir))

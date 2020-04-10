from .app import get_application
from .core import config, session
from .models import DOCUMENTS
from .scripts import cli

__version__ = "0.1.0"

app = get_application(config)

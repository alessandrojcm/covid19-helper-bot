import sys
import inspect
from pathlib import Path

from app.models import Config


def generate_dev_env():
    """
    Gets the absolute path of the file which was called as a script,
    in this particular project that is the cli() function which is at the root folder.
    Then, writes a .env file with the default settings.
    """
    module = sys.modules["__main__"]
    if not inspect.getfile(module):
        raise RuntimeError("Not executing as a script")
    path = Path(module.__file__).absolute().resolve().parent

    with open(path.joinpath(".env"), "w") as f:
        for key, value in dict(Config(DEBUG=True)).items():
            f.write("{k}={v}\n".format(k=key, v=value))

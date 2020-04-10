import inspect
import sys
from pathlib import Path


def get_entry_point():
    """
       Gets the absolute path of the file which was called as a script,
       in this particular project that is the cli() function which is at the root folder.
       Then, writes a .env file with the default settings.
       """
    module = sys.modules["__main__"]
    if not inspect.getfile(module):
        raise RuntimeError("Not executing as a script")
    return Path(module.__file__).absolute().resolve().parent

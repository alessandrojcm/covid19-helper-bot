import json
import re

from loguru import logger

from app.core import config
from app.utils import get_entry_point


@logger.catch
def replace_variables():
    """
        This utility function loads the schema json and replaces its variable keys with
        the values loaded from either the .env file or from environment variables
    """
    logger.info("Reading schema file...")
    path = get_entry_point()
    schema = None
    with open(path.joinpath("assistant/schema.json")) as schema_file:
        schema = schema_file.read().replace("\n", "")

    logger.info("Replacing keys...")
    for key, val in config:
        if schema.find(key) != -1:
            logger.info("Replacing {k} for {v}".format(k=key, v=val))
            schema = re.sub(r"\b%{key}%|\B%{key}%".format(key=key), val, schema)
    logger.info("Writing schema file as schema_ready.json...")
    with open(path.joinpath("assistant/schema_ready.json"), "w") as ready_schema:
        # Prettify the file
        ready_schema.write(json.dumps(json.loads(schema)))
    logger.info("Schema written successfully.")

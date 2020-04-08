from app.models import Config
from app.utils import get_entry_point


def generate_dev_env():
    path = get_entry_point()

    with open(path.joinpath(".env"), "w") as f:
        for key, value in dict(Config(DEBUG=True)).items():
            f.write("{k}={v}\n".format(k=key, v=value))

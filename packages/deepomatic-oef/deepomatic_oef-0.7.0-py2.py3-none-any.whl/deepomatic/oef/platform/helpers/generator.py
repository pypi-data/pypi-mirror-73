import json
from pathlib import Path

from ..config import form


def make_json_payload(get_backend_fn):
    """
    Return the JSON payload as a Python dict.
    """
    return form.json(get_backend_fn)

def dump_json_payload(get_backend_fn):
    """
    Dump the JSON payload in OEF, as a JSON file that will be exposed via an API.
    """
    this_dir = Path(__file__).parent
    path = this_dir / '..' / 'default_models.json'
    with open(str(path), 'w') as f:
        json.dump(make_json_payload(get_backend_fn), f, indent=4)


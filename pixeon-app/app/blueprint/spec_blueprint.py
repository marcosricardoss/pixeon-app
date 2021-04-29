"""Blueprint to organize and group, views related
to the '/spec' endpoint of HTTP REST API.
"""

import os
from flask import Blueprint, Response, send_from_directory

bp = Blueprint('spec', __name__)

@bp.route('/<string:filename>', methods=('GET',))
def get_spec(filename: str) -> Response:
    """Return a spec file identified by path parameters.
    
    Parameters:
    filename (str): the spec filename.

    Returns:
    a static file
    """

    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'pixeon/spec'), filename)

    
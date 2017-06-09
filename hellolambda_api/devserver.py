from flask_cors import CORS
from hellolambda_api import config as config
from api import app

"""
For running locally (to debug)
"""

if __name__ == "__main__":
    config.is_debug_server = True
    CORS(app)

    app.run(port=config.FLASK_PORT, debug=True)

__version__ = "0.1.0"

import logging
import sys

import cool_app.settings as settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
        logging.FileHandler(settings.LOG_FILE),
    ],
)

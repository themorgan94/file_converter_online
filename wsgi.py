import sys
import logging
logging.basicConfig(stream=sys.stderr)
from app import app as application

if __name__ == "__main__":
    application.run(host='0.0.0.0')
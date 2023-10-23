import os
import time
import glob
import shutil
from datetime import datetime, timedelta
import logging

dir_path = os.path.dirname(os.path.realpath(__file__))

def expire_files():
    for folder in glob.glob(dir_path + "/static/uploads/*/"):
        st = os.stat(folder)
        created = datetime.utcfromtimestamp(st.st_ctime)
        lastday = datetime.now() - timedelta(hours=1)
        if created < lastday:
            logging.info("deleting folder " + folder )
            shutil.rmtree(folder, True)
import os

from streamlit import config as _config
from streamlit.web.bootstrap import run

if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "main.py")

    _config.set_option("server.headless", True)
    run(filename, args=[], flag_options=[], is_hello=False)

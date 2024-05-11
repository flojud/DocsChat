import os

from streamlit.web import cli

if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "main.py")
    cli.main_run([filename])

from streamlit.web import cli
import os

if __name__ == "__main__":
    print("Running streamlit")

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "main.py")
    cli.main_run([filename, "--server.port", "1000"])

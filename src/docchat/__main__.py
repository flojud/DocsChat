import pathlib

import streamlit.web.bootstrap as bootstrap

PATH = pathlib.Path(__file__).parent

if __name__ == "__main__":
    print("This script is not meant to be run directly.")


def run():
    flag_options = {
        "server.port": 8501,
        "global.developmentMode": False,
    }

    bootstrap.load_config_options(flag_options=flag_options)

    bootstrap.run(
        str(PATH.joinpath("app.py")),
        True,
        [],
        {"_is_running_with_streamlit": True},
    )

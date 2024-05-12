import os
import pathlib

import streamlit.web.bootstrap as bootstrap

PATH = pathlib.Path(__file__).parent


def app():

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


if __name__ == "__main__":
    app()

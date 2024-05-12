import pathlib

import streamlit.web.bootstrap as bootstrap

PATH = pathlib.Path(__file__).parent


def app():
    bootstrap.run(
        str(PATH.joinpath("app.py")),
        is_hello=False,
        args=list(),
        flag_options=dict(),
    )


if __name__ == "__main__":
    app()

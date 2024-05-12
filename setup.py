from setuptools import setup

setup(
    name="DocChat",
    version="2.0.0",
    package_dir={"": "src"},
    packages=["docchat"],
    author="flojud",
    author_email="dev.flojud@gmail.com",
    description="Chat with your docs using langchain in a streamlit app with mistral or llama in ollama.",
    keywords="llama, mistral, chat, streamlit, langchain, talk2docs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/flojud/chat-with-my-docs",
    install_requires=[
        "streamlit",
        "langchain==0.1.19",
        "langchain_chroma==0.1.0",
        "langchain-community==0.0.38",
        "langchain-experimental==0.0.58",
        "stqdm",
        "watchdog",
        "pypdf",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/flojud/chat-with-my-docs/issues",
    },
    entry_points={
        "console_scripts": [
            "docchat = docchat.__main__:run",
        ],
    },
    python_requires=">=3.10",
    license="MIT",
)

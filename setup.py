from setuptools import setup

setup(
    name="DocChat",
    version="0.12.0",
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
        "langchain",
        "langchain_chroma",
        "langchain_community",
        "langchain_experimental",
        "stqdm",
        "watchdog",
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

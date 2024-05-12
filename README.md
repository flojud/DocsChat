# DocsChat 📚🗣️

This repository contains code for a chatbot application that allows users to interact with documents using conversational queries.

`docchat` is a command-line interface that let's you start a local streamlit server and interact with your documents.

## Installation

To run the application locally, follow these steps for installation.

```bash
pip install DocChat
```

Start the Ollama server:

```bash
ollama pull llama3
ollama pull llama2
ollama pull gemma
ollama pull mistral
ollama pull codellama
ollama run llama3
```

Run the application:

```bash
docchat
```

## Overview

The chatbot utilizes a conversational retrieval chain to answer user queries based on the content of embedded documents. It leverages various NLP techniques, including language models and embeddings, to provide relevant responses.

## Features

- **Document Embedding:** Embeds PDF documents for efficient retrieval of information.
- **Conversational Interface:** Allows users to interact with documents through a chat interface.
- **Settings:** Provides customizable settings for configuring document retrieval and model parameters.

# Chat with my docs 🤖

This repository contains code for a chatbot application that allows users to interact with documents using conversational queries.

## Overview

The chatbot utilizes a conversational retrieval chain to answer user queries based on the content of embedded documents. It leverages various NLP techniques, including language models and embeddings, to provide relevant responses.

## Features

- **Document Embedding:** Embeds PDF documents for efficient retrieval of information.
- **Conversational Interface:** Allows users to interact with documents through a chat interface.
- **Settings:** Provides customizable settings for configuring document retrieval and model parameters.

## Installation

To run the application locally, follow these steps:

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the Ollama server:

```bash
ollama pull llama3
ollama pull llama2
ollama pull gemma
ollama pull mistral
ollama pull codellama
ollama run llama3
```

3. Run the application:

```bash
streamlit run main.py
```

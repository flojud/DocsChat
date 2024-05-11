import fnmatch
import os

import langchain
import streamlit as st
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from stqdm import stqdm

chain, embeddings, llm, db = None, None, None, None

config = {
    "ollama": {
        "url": "http://localhost:11434",
        "model": "llama3",
        "temperature": 0.8,
        "tfs_z": 1.0,
        "top_k": 40,
        "top_p": 0.9,
    },
    "db": {
        "source": "/Users/florjud/Downloads",
        "persist_directory": "./vector_db",
        "search_type": "mmr",
        "top_k": 10,
        "fetch_k": 10,
        "lambda_mult": 0.5,
        "score_threshold": 0.8,
    },
    "splitter": "None",
}


def setup() -> None:
    """
    This function initializes the global variables `llm`, `embeddings` and `db`.
    The configuration values for these instances are read from the global `config` variable.

    :return: None
    """

    global embeddings, db, llm

    llm = Ollama(
        base_url=config["ollama"]["url"],
        model=config["ollama"]["model"],
        temperature=config["ollama"]["temperature"],
        tfs_z=config["ollama"]["tfs_z"],
        top_k=config["ollama"]["top_k"],
        top_p=config["ollama"]["top_p"],
    )

    embeddings = OllamaEmbeddings(
        base_url=config["ollama"]["url"],
        model=config["ollama"]["model"],
        temperature=config["ollama"]["temperature"],
        tfs_z=config["ollama"]["tfs_z"],
        top_k=config["ollama"]["top_k"],
        top_p=config["ollama"]["top_p"],
    )
    db = Chroma(
        embedding_function=embeddings,
        persist_directory=config["db"]["persist_directory"],
        collection_name="talk2docs",
    )


def delete_db() -> None:
    """
    This function deletes the collection in the global `db` variable.

    :return: None
    """
    global db
    db.delete_collection()


def get_splitter() -> any:
    """
    This function returns a text splitter based on the configuration value in the global `config` variable.

    :return: any - The text splitter object
    """
    global config

    if config["splitter"] == "SemanticChunker":
        return SemanticChunker(embeddings)
    elif config["splitter"] == "CharacterTextSplitter":
        return CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
    elif config["splitter"] == "RecursiveCharacterTextSplitter":
        return RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
    elif config["splitter"] == "None":
        return None
    else:
        raise ValueError("Unknown splitter")


def sync() -> None:
    """
    This function loads all PDFs from the source folder in the global `config` variable and embeds them using the global `embeddings` object.
    If a text splitter is configured in the global `config` variable, the documents are split before embedding.

    :return: None
    """
    pdfs = []
    splitter = get_splitter()

    # Find all PDFs in the source folder
    for root, dirs, files in os.walk(config["db"]["source"]):
        for file in files:
            if fnmatch.fnmatch(file, "*.pdf"):
                pdfs.append(os.path.join(root, file))

    # Load and split documents
    for pdf_file in stqdm(pdfs, desc="Embedd PDF documents", st_container=st.sidebar):

        # Load PDFs
        loader = PyPDFLoader(pdf_file)
        docs = loader.load()

        # Split documents using model embeddings
        if splitter:
            docs = splitter.split_documents(docs)

        # Add to database
        db.add_documents(docs)


def get_seach_kwargs() -> dict:
    """
    This function returns the search kwargs based on the configuration value in the global `config` variable.
    :return: dict - The search kwargs
    """

    if config["db"]["search_type"] == "similarity_score_threshold":
        return {
            "k": config["db"]["top_k"],
            "score_threshold": config["db"]["score_threshold"],
        }
    elif config["db"]["search_type"] == "mmr":
        return {
            "k": config["db"]["top_k"],
            "fetch_k": config["db"]["fetch_k"],
            "lambda_mult": config["db"]["lambda_mult"],
        }
    elif config["db"]["search_type"] == "similarity":
        return {"k": config["db"]["top_k"]}
    else:
        raise ValueError("Unknown search type")


def run_chain(question: str, chat_history: list[str]) -> list[any]:
    """
    This function runs a conversational retrieval chain with the given question and chat history.
    The chain is initialized with the global `llm` object and the global `db` object.
    The chain uses a text splitter based on the configuration value in the global `config` variable.

    :return: list[any] - The response object from the chain
    """

    template = """
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context:
    {context}

    Question: {question}
    Helpful Answer:
    """

    condense_prompt = """
    Given the following conversation and a follow up question,
    rephrase the follow up question to be a standalone question.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:
    """

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    condense_prompt = PromptTemplate(
        template=condense_prompt, input_variables=["question", "chat_history"]
    )

    langchain.globals.set_verbose("true")

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=db.as_retriever(
            search_type=config["db"]["search_type"],
            search_kwargs=get_seach_kwargs(),
        ),
        condense_question_prompt=condense_prompt,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt},
    )

    return chain({"question": question, "chat_history": chat_history})


def start_chatbot():
    global config

    st.title("Chat with my docs 🤖")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.markdown(
            """
            This app requires the Ollama server to be running. 
            You can install and run it with the following commands:
            ```bash
            brew install ollama
            ollama pull llama3
            ollama run llama3
            ```
            Let's chat! 🚀
            """
        )

    # Display chat messages from history on app rerun
    for history_question, history_answer in st.session_state.messages:
        st.chat_message("user").markdown(history_question)
        st.chat_message("assistant").markdown(history_answer)

    # React to user input
    if prompt := st.chat_input("What is up?"):
        st.chat_message("user").markdown(prompt)

        response = run_chain(prompt, st.session_state.messages)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response["answer"])
            with st.expander("Response Object"):
                st.write(response)
            with st.expander("History"):
                st.write(st.session_state.messages)

        # Add to chat history
        st.session_state.messages.append((prompt, response["answer"]))

    # Sidebar
    with st.sidebar:

        st.title("Settings")

        # Display settings form
        with st.form(key="settings"):

            st.header("Documents")

            sync_folder_path = st.text_input(
                "PDF source folder",
                value="/Users/florjud/Downloads",
                help="This is the folder where the app will look recursively for PDFs to embed.",
            )

            splitter_to_use = st.selectbox(
                "Retrieval Text Splitter",
                [
                    "None",
                    "SemanticChunker",
                    "CharacterTextSplitter",
                    "RecursiveCharacterTextSplitter,",
                ],
                help="If you want to split the text into smaller chunks before embedding, select a splitter. A deletion of the database is required to apply the new splitter.",
            )

            st.divider()
            st.header("Vector Store")

            persist_directory = st.text_input(
                "Persist directory",
                value="/Users/florjud/Downloads",
                help="This is the folder where the app will store the vector store.",
            )

            search_type_retriever = st.selectbox(
                "Retriever search type",
                [
                    "mmr",
                    "similarity",
                    "similarity_score_threshold",
                ],
                help="",
            )

            top_k_retriever = st.slider(
                "Top k",
                1,
                100,
                4,
                help="Amount of documents to return (Default: 4)",
            )

            st.caption("Similarity score threshold settings")
            score_threshold_retriever = st.slider(
                "Similarity score threshold",
                0.0,
                1.0,
                0.8,
                help="Minimum relevance threshold for similarity_score_threshold",
            )

            st.caption("MMR settings")
            fetch_k_retriever = st.slider(
                "Fetch k",
                1,
                100,
                20,
                help="Amount of documents to pass to MMR algorithm (Default: 20)",
            )
            lambda_mult_retriever = st.slider(
                "Lambda mult",
                0.0,
                1.0,
                0.5,
                help="Diversity of results returned by MMR; 1 for minimum diversity and 0 for maximum. (Default: 0.5)",
            )

            st.divider()
            st.header("Ollama")

            url = st.text_input(
                "Ollama url",
                value=config["ollama"]["url"],
                help="The base url the model is hosted under. Usually it's http://localhost:11434",
            )

            model = st.selectbox(
                "🦙 Model",
                ["llama3", "llama2", "gemma", "mistral", "codellama"],
                help="Pick the model you want to use. Futher models can be added by running `ollama pull <model_name>` in the terminal. Full list see here: https://ollama.com/library?sort=popular",
            )

            temperature = st.slider(
                "The temperature of the model",
                0.0,
                1.0,
                0.8,
                help="The temperature of the model. Increasing the temperature will make the model answer more creatively. (Default: 0.8)",
            )

            tfs_z = st.slider(
                "Tail free sampling",
                0.0,
                4.0,
                1.0,
                help="Tail free sampling is used to reduce the impact of less probable tokens from the output. A higher value (e.g., 2.0) will reduce the impact more, while a value of 1.0 disables this setting. (default: 1)",
            )

            top_k = st.slider(
                "Top_k sampling",
                0,
                100,
                40,
                help="Reduces the probability of generating nonsense. A higher value (e.g. 100) will give more diverse answers, while a lower value (e.g. 10) will be more conservative. (Default: 40)",
            )

            top_p = st.slider(
                "Top_p sampling",
                0.0,
                1.0,
                0.9,
                help="Works together with top-k. A higher value (e.g., 0.95) will lead to more diverse text, while a lower value (e.g., 0.5) will generate more focused and conservative text. (Default: 0.9)",
            )

            if st.form_submit_button("Save"):
                config["ollama"]["url"] = url
                config["ollama"]["model"] = model
                config["ollama"]["temperature"] = temperature
                config["ollama"]["tfs_z"] = tfs_z
                config["ollama"]["top_k"] = top_k
                config["ollama"]["top_p"] = top_p

                config["db"]["source"] = sync_folder_path
                config["db"]["persist_directory"] = persist_directory
                config["db"]["search_type"] = search_type_retriever
                config["db"]["top_k"] = top_k_retriever
                config["db"]["fetch_k"] = fetch_k_retriever
                config["db"]["lambda_mult"] = lambda_mult_retriever
                config["db"]["score_threshold"] = score_threshold_retriever
                config["splitter"] = splitter_to_use
                setup()

        st.title("Actions")

        with st.form(key="actions"):
            st.caption("Read, chunk and embedd all PDFs")
            if st.form_submit_button("Sync now"):
                with st.spinner(text="In progress"):
                    sync()
                    st.success("Done")

            st.caption("Delete vectore store collection")
            if st.form_submit_button(label="Delete DB", type="primary"):
                with st.spinner(text="In progress"):
                    delete_db()
                    st.success("Done")


if __name__ == "__main__":
    setup()
    start_chatbot()

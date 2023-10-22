import requests
import ast
import os
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo,
)
from langchain.document_loaders.pdf import PyPDFParser
from langchain.document_loaders.blob_loaders import Blob
from langchain.document_loaders import WebBaseLoader
from langchain.utilities import BingSearchAPIWrapper
from langchain.chains import VectorDBQA
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# from langchain.text_splitter import CharacterTextSplitter


os.environ["BING_SUBSCRIPTION_KEY"] = "f911e38cb5f94c319a38b256bd984cd8"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"
os.environ["OPENAI_API_KEY"] = "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"


def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)


def sanitize_url(url):
    # Remove any invalid characters and return the sanitized string
    invalid_chars = ['/', '\\', '?', '%', '*',
                     ':', '|', '"', '<', '>', '.', ' ']
    for char in invalid_chars:
        url = url.replace(char, '_')
    return url + ".pdf"


def process_data(data):
    prompt = data['text']
    files = [[pdf['url'], pdf['description']] for pdf in data['pdfs']]

    for i, file in enumerate(files):
        url = file[0]
        sanitized_filename = sanitize_url(url)
        download_file(url, sanitized_filename)
        # Update the filename in the files list
        files[i][0] = sanitized_filename

    # prompt = "I want to study the timeline of the Russian-Ukrainian war"
    # time_limits = 0 # insert: INPUT TIME_LIMITS
    # files = []
    # for filename in os.listdir(os.getcwd() + "/PDFs"):
    #    files.append([filename, "INPUT DESCRIPTION"])

    loader = PyPDFParser()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0, add_start_index=True)
    embeddings = OpenAIEmbeddings()

    basic_use_model = ChatOpenAI(model_name="gpt-4", temperature=0)

    extracted_topic = basic_use_model.predict(
        "Here is the user's prompt: \"" + prompt +
        "\" What is the topic? IMPORTANT: respond in at most 4 words"
    )

    L = []

    for file in files:
        name = file[0]
        description = file[1]

        docs = loader.lazy_parse(Blob(path="PDFs/" + name))

        txts = text_splitter.split_documents(docs)

        vectorized_txts = Chroma.from_documents(
            txts, embeddings, collection_name=name + "-article"
        )

        query_for_vzd = "I want to better understand this topic: " + \
            extracted_topic + " What are the most significant events?"
        query_response_docs = vectorized_txts.max_marginal_relevance_search(
            query_for_vzd, k=6, fetch_k=40, lambda_mult=0.25)
        query_response = "\n\n".join(["Chunk {}: \n{}".format(
            i, doc.page_content) for i, doc in enumerate(query_response_docs)])

        top_3_events_prompt = (
            "I have extracted 6 chunks of information from an online article:\n"
            + query_response
            + "Here is also a short description on the article: " + description
            + "Based on this, what are the three most significant events you can extract relvant for understanding this topic\:"
            + extracted_topic
        )

        top_3_events_response = basic_use_model.predict(top_3_events_prompt)

        vectorstore_info = VectorStoreInfo(
            name=name,
            description=description,
            vectorstore=vectorized_txts
        )

        toolkit = VectorStoreToolkit(
            vectorstore_info=vectorstore_info,
            # the magic sauce
            llm=ChatOpenAI(model_name="gpt-4", temperature=0)
        )

        agent_executor = create_vectorstore_agent(
            # potential issue: 16k tokens to 8k
            llm=ChatOpenAI(model_name="gpt-4", temperature=0),
            toolkit=toolkit,
            verbose=True,
            handle_parsing_errors=True
        )

        event_prompt_template = (
            "Here are the 3 most imporant events from the given document on the topic of " +
            extracted_topic + ":"
            + top_3_events_response
            + "Write a title and a description for the {order} event, and find the date. If you can't find the date, make a guess."
            +
            """
            Format the output as follows: [Title, Description, Date Month/Day/Year]
            IMPORTANT: even if you estimate the date, strictly format it as Month/Day/Year
            """
        )
        event_strings = ["", "", ""]
        event_strings[0] = agent_executor.run(
            event_prompt_template.format(order="first"))
        event_strings[1] = agent_executor.run(
            event_prompt_template.format(order="second"))
        event_strings[2] = agent_executor.run(
            event_prompt_template.format(order="third"))

        for i in range(3):
            L.append(ast.literal_eval(event_strings[i]))

    search = BingSearchAPIWrapper()
    bing_query_prompt = "In depth scholarly articles on this topic: " + extracted_topic
    bing_raw_results = search.results(bing_query_prompt, 2)
    bing_result_links = [bing_raw_results[i].get("link") for i in range(2)]
    data = [WebBaseLoader(bing_result_links[i]).load() for i in range(2)]

    for d in data:

        txts = text_splitter.split_documents(d)

        vectorized_txts = Chroma.from_documents(
            txts, embeddings, collection_name=name + "-article"
        )

        query_for_vzd = "I want to better understand this topic: " + \
            extracted_topic + " What are the most significant events?"
        query_response_docs = vectorized_txts.max_marginal_relevance_search(
            query_for_vzd, k=6, fetch_k=40, lambda_mult=0.25)
        query_response = "\n\n".join(["Chunk {}: \n{}".format(
            i, doc.page_content) for i, doc in enumerate(query_response_docs)])

        top_3_events_prompt = (
            "I have extracted 6 chunks of information from an online article:\n"
            + query_response
            + "Based on this, what are the three most significant events you can extract relvant for understanding this topic\:"
            + extracted_topic
        )

        top_3_events_response = basic_use_model.predict(top_3_events_prompt)

        vectorstore_info = VectorStoreInfo(
            name=name,
            description="online article with some info on topic: " + extracted_topic,
            vectorstore=vectorized_txts
        )

        toolkit = VectorStoreToolkit(
            vectorstore_info=vectorstore_info,
            # the magic sauce
            llm=ChatOpenAI(model_name="gpt-4", temperature=0)
        )

        agent_executor = create_vectorstore_agent(
            # potential issue: 16k tokens to 8k
            llm=ChatOpenAI(model_name="gpt-4", temperature=0),
            toolkit=toolkit,
            verbose=True,
            handle_parsing_errors=True
        )

        event_prompt_template = (
            "Here are the 3 most imporant events from the given document on the topic of " +
            extracted_topic + ":"
            + top_3_events_response
            + "Write a title and a description for the {order} event, and find the month, day, and year. If you can't, make an educated guess, or wost case make a complete guess."
            +
            """
            STRICTLY FORMAT THE OUTPUT AS FOLLOWS: [Title (str), Description (str), Month (int), Day (int), Year (int)]
            """
        )
        event_strings = ["", "", ""]
        event_strings[0] = agent_executor.run(
            event_prompt_template.format(order="first"))
        event_strings[1] = agent_executor.run(
            event_prompt_template.format(order="second"))
        event_strings[2] = agent_executor.run(
            event_prompt_template.format(order="third"))

        for i in range(3):
            L.append(ast.literal_eval(event_strings[i]))
        return L


@app.route('/api', methods=['POST'])
def receive_data():
    data = request.json
    print(data)
    results = process_data(data)
    return jsonify(results)


# Running app
if __name__ == '__main__':
    app.run(debug=True, port=8000)

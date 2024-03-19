from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from pprint import pprint


def llm(data):
    # helps to convert output into string
    output_parser = StrOutputParser()

    loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")

    docs = loader.load()
    # print(docs)
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")

    llm = Ollama(model="qwen:1.8b")
    document_chain = create_stuff_documents_chain(llm, prompt)

    embeddings = OllamaEmbeddings(model="qwen:1.8b")
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.create_documents(data)
    gmail_split = text_splitter.split_documents(documents)
    pprint(gmail_split)

    docs_split = text_splitter.split_documents(docs)
    vector = FAISS.from_documents(gmail_split, embeddings)

    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({"input": "Summarize the emails"})
    print(response["answer"])

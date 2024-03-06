from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from .gmail_api import email


def llm():
    # helps to convert output into string
    output_parser = StrOutputParser()

    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")

    llm = Ollama(model="phi")
    document_chain = create_stuff_documents_chain(llm, prompt)

    gmail_data = email()
    embeddings = OllamaEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.create_documents(gmail_data[0])
    gmail_split = text_splitter.split_documents(documents)
    vector = FAISS.from_documents(gmail_split, embeddings)

    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({"input": "Summarize the emails"})
    print(response["answer"])

from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..state.gmail_api import gmail_message

# make i do a chain selection
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert summarizer.  When you recieve the information you will do your best to combine the information given into short and sweet summary ",
        ),
        ("user", "{input}"),
    ]
)

llm = Ollama(model="phi")
chain = prompt | llm | output_parser

chain.invoke(
    {"input": "Summarize the emails. The summarizations need to be in done categories"}
)

embeddings = OllamaEmbeddings()
text_splitter = RecursiveCharacterTextSplitter()
gmail_data = gmail_message.message_list 
gmail_split = text_splitter.split_documents(gmail_data)
vector = FAISS.from_documents(gmail_split, embeddings)

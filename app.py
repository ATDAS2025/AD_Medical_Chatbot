from flask import Flask, request, jsonify,render_template
from src.helper import load_pdf_files,download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embeddings = download_embeddings()
index_name = "ad-medical-chatbot"
docsearch = PineconeVectorStore(index_name=index_name
                                ,embedding=embeddings)

retriever = docsearch.as_retriever(search_tyepe="similarity", search_kwargs={"k": 3})

chatModel = ChatOpenAI(model="gpt-4.1-mini")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt), 
        ("human", "{input}")
    ]
)

question_answer_chain = create_stuff_documents_chain(llm=chatModel, prompt=prompt)
rag_chain = create_retrieval_chain(retriever
                                   , question_answer_chain)


@app.route('/chat', methods=['POST','GET'])
def chat():
    #msg = request.form["msg"]
    #input = msg
    user_message = request.get_json().get("message")
    response = rag_chain.invoke({"input": user_message})
    return jsonify({"answer": response["answer"]})

@app.route('/')
def index():
    return render_template('chat.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, log_level="debug")
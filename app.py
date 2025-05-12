from flask import Flask, render_template, jsonify, request ,url_for
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *
import os
from langchain_groq import ChatGroq


app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

embeddings = download_hugging_face_embeddings()

#Initializing the Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("medicalchatbot")

index_name = "medicalchatbot"

#Loading the index
docsearch=PineconeVectorStore.from_existing_index(index_name, embeddings)


PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])

chain_type_kwargs={"prompt": PROMPT}

# llm=CTransformers(model=r"E:\project_ai\medical_chatbot\model\llama-2-7b-chat.ggmlv3.q4_0.bin",
#                   model_type="llama",
#                   config={'max_new_tokens':512,
#                           'temperature':0.8})

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY, 
    model_name="Llama3-8b-8192", 
    streaming=True ,
    temperature=0)

qa=RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs)



@app.route("/")
def index():
    return render_template('chat.html')



@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa.invoke({"query": input})
    print("Response : ", result["result"])
    # return str(result["result"])
    return result["result"].replace("\n", "<br>")



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)


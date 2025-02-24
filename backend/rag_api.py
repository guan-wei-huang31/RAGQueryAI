from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd

# **1. Flask setup**
app = Flask(__name__)
CORS(app)

# **2️. SQLite connection**
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "functional_products.db")
db_uri = f"sqlite:///{DB_PATH}"
engine = create_engine(db_uri)

# **3. Retrieve information from database**
query = """
    SELECT product_name, weight, manufacturer, expiration_date, storage_method, 
           delivery_time, reference_price, allergy_info, in_stock, 
           certifications, health_description, product_details 
    FROM Functional_Products
"""
df = pd.read_sql(query, engine)

# **4. Transfer to dataframe**
df["text"] = df.apply(lambda row: f"Product Name: {row['product_name']}\n"
                                  f"Weight: {row['weight']}g\n"
                                  f"Manufacturer: {row['manufacturer']}\n"
                                  f"Storage Method: {row['storage_method']}\n"
                                  f"Stock Status: {'In Stock' if int(row['in_stock']) == 1 else 'Out of Stock'}\n"
                                  f"Health Description: {row['health_description']}\n"
                                  f"Product Details: {row['product_details']}\n", axis=1)

# **5. Initialize Ollama & ChromaDB**
llm = OllamaLLM(model="mistral")

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_db = Chroma.from_texts(
    df["text"].tolist(),
    embedding=embeddings,
    persist_directory="db",
    collection_name="functional_products",
    metadatas=[
        {
            "product_name": row["product_name"],
            "manufacturer": row["manufacturer"],
            "category": row.get("category", "general"),
            "in_stock": row["in_stock"],
        }
        for _, row in df.iterrows()
    ],
)

retriever = vector_db.as_retriever(search_kwargs={"k": 3})

# **6. Prompt engineering setup**
system_prompt =  """
You are answering questions based on product information stored in a structured database.
The database contains the following fields:
- Product Name
- Weight (grams)
- Manufacturer
- Expiration Date
- Storage Method
- Stock Status
- Health Description
- Certifications
- Price

If the question asks for structured information (such as price, manufacturer, stock status), retrieve it using the database.
If the question asks for general product descriptions, retrieve information from the vector database.

Always answer concisely and only provide relevant information.
\n\n{context}
"""
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", "Question: {input}"),
    ]
)

# **7. Setup RAG flow**
document_chain = create_stuff_documents_chain(llm, prompt_template)   ## Combine prompt engineering + user query + vectorDB, assign llm
retrieval_chain = create_retrieval_chain(retriever, document_chain)   ## invoke llm, based on document_chain and retriever

# **8. SQL structure data**
def query_product_info(product_name, column):
    query = text(f"SELECT {column} FROM Functional_Products WHERE product_name = :product_name")

    with engine.connect() as connection:
        result = connection.execute(query, {"product_name": product_name}).fetchone()
    
    return result[0] if result else "I don't know."

# **9. Query Rewriting (vague query)**
def rewrite_query(input_text, last_product):
    vague_phrases = ["this product", "it", "the price", "the weight", "certifications"]
    if last_product:
        for phrase in vague_phrases:
            if phrase in input_text.lower():
                input_text = input_text.lower().replace(phrase, f"the {last_product}")
                print(f"\n🔄 Rewritten question: {input_text}")
                break
    return input_text

# **10. Memorize previous question**
context = []
last_product = None

# **11. Flask API**
@app.route("/ask", methods=["POST"])
def ask_question():
    global last_product, context  # 記住用戶的 `last_product` 和 `context`

    data = request.json
    input_text = data.get("question", "").strip()
    
    if not input_text:
        return jsonify({"error": "No question provided"}), 400

    # 🚀 **Step 1: Query Rewriting**
    input_text = rewrite_query(input_text, last_product)

    # 🚀 **Step 2: SQL 查詢**
    structured_questions = {
        "price": "reference_price",
        "manufacturer": "manufacturer",
        "expiration": "expiration_date",
        "stock": "in_stock",
    }
    
    for key, column in structured_questions.items():
        if key in input_text.lower():
            if last_product:
                answer = query_product_info(last_product, column)
                return jsonify({"answer": answer, "product_name": last_product})

    # 🚀 **Step 3: 向量檢索（ChromaDB）**
    response = retrieval_chain.invoke({"input": input_text, "context": context})
    answer = response["answer"]

    # 🚀 **Step 4: 記住 `last_product`，支援多輪對話**
    for product in df["product_name"].tolist():
        if product.lower() in answer.lower():
            last_product = product
            break 

    # 🚀 **Step 5: 記住 `context`**
    context = response.get("context", [])

    return jsonify({"answer": answer, "last_product": last_product})

# **🔹 啟動 Flask API**
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)


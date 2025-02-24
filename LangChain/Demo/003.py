"""
    RAG demo
"""
# 步骤1：法律文本向量化
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 加载《劳动合同法》文本
loader = TextLoader("../datasets/000.txt")
documents = loader.load()

# 文本分块（法律条款级切割）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,  # 确保每个法条完整
    chunk_overlap=50
)
docs = text_splitter.split_documents(documents)

# 使用轻量级嵌入模型
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
print("loading vector database...")
vectorstore = FAISS.from_documents(docs, embeddings)

# 步骤2：检索增强生成
from langchain.chains import RetrievalQA
# from langchain_community.llms import OpenAI
from langchain_ollama import OllamaLLM

print("using deepseek...")
ollama_model = OllamaLLM(model="deepseek-r1:1.5b", temperature=0.5)  # 本地模型 deepseek-r1:1.5b

qa_chain = RetrievalQA.from_chain_type(
    # llm=OpenAI(temperature=0.5),
    llm=ollama_model,  # 替换为本地模型
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

# 测试问答
query = "我在公司工作3年月薪8000，被无故解雇怎么索赔？"
print(qa_chain.run(query))

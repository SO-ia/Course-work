# ChatOllama: Chat model
# OllamaLLM: LLM model
from langchain_ollama import OllamaLLM, ChatOllama
from langchain_core.prompts import ChatPromptTemplate

template = """你是一位资深{role}，请用不超过3句话解释以下概念：{concept}"""
# set proper prompt
prompt = ChatPromptTemplate.from_template(
    template=template
)

"""
chat model: return a structured information (langchain_core.messages.ai.AIMessage)
llm model: return a string of model's output
"""

"""
chat模型: 返回结构化的信息 (content为模型返回的输出)
llm模型: 始终返回模型输出的字符串
"""

# chat model
# use local deepseek-r1:1.5b
chat_model = ChatOllama(model="deepseek-r1:1.5b", temperature=0.5)
# 创建一个简单链
# output of prompt will be passed to model (like ds-r1)
# model will process it based on the output
chat_chain = prompt | chat_model
# use chain
chat_result = chat_chain.invoke({"role": "机器学习工程师", "concept": "过拟合"})
print(chat_result)
print(type(chat_result))

# llm model
llm_model = OllamaLLM(model="deepseek-r1:1.5b", temperature=0.5)
llm_chain = prompt | llm_model
llm_result = llm_chain.invoke({"role": "机器学习工程师", "concept": "过拟合"})
print(llm_result)

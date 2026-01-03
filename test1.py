from langchain_ollama import ChatOllama

llm = ChatOllama(
    model = "phi:latest",
    temperature = 0.3
)

response = llm.invoke("do you remember our previous conversation?")

print(response)
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate 

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llava")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation():
    context = ""
    print("Welcome to the HeloAI ChatBot. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        result = chain.invoke({"context": context, "question": user_input})    
        print("HeloAI: ", result)
        context += f"User: {user_input}\nAI: {result}\n"

if __name__ == "__main__":
    handle_conversation()
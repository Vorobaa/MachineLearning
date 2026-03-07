import os
from platform import system

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="Ти дружній асистент, що відповідає просто та корисно",
    debug=False,
)

def get_output(result: dict) -> str:
    messages = result.get("messages", [])
    for msg in reversed(messages):
        content = getattr(msg, "content", None)
        tool_calls = getattr(msg, "tool_calls", None) or []
        if content and not tool_calls:
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                return "".join(
                    c.get("text", str(c)) if isinstance(c, dict) else str(c) for c in content
                )
    return ""

chat_messages = []
def chat(user_input: str, agent=agent) -> str:
    chat_messages.append({"role": "user", "content": user_input})

    result = agent.invoke({"messages": chat_messages})

    chat_messages.clear()
    chat_messages.extend(result["messages"])

    return get_output(result)

def run_demo():
    print("Відповідь 1:", chat("Привіт! Мене звати Егор"))
    print("Відповідь 2:", chat("Запам'ятай, я люблю програмування"))
    print("Відповідь 3:", chat("Нагадай, як мене звати і що мені подобається?"))

def run_interactive(agent=agent):
    print("Інтерактивний режим. Напишіть 'exit' для виходу.")

    while True:
        user_input = input("Ви: ")

        if user_input.lower() in ["exit"]:
            print("Завершення програми.")
            break

        response = chat(user_input, agent=agent)
        print("Агент:", response)

if __name__ == "__main__":
    mode = input("Оберіть режим (demo чи interactive): ").strip().lower()
    if mode == "demo":
        run_demo()
    elif mode == "interactive":
        run_interactive()
    else:
        print("Невідомий режим.")
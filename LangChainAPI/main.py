# from simple_llm import llm

from tool_chain import tools
from memory import run_interactive, llm
from langchain.agents import create_agent

prompt = (
    "You have access to a tool that retrieves context from a blog post. "
    "Use the tool to help answer user queries."
    "Use weather_api tool to retrieve weather information."
    "Use search_faq tool to retrieve the most relevant FAQ/blog content using semantic search."
    "The search_faq tool returns relevant context text."
    "Use that context to generate the final answer."
    "If the tool returns Нічого не знайдемо у FAQ, tell the user that the information was not found."
    "Do NOT invent information that is not in the retrieved content."
    "If the question does not require FAQ data, answer normally."
)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="Ти дружній асистент, що відповідає просто та корисно",
    debug=False,
)


run_interactive(agent=agent)
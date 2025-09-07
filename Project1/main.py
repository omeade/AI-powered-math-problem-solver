from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
import os


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("TOGETHER_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://api.together.xyz/v1"


@tool
def calculator_tool(expression: str) -> str:
    """Evaluates a math expression like '3 * 4 + 2'."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"
def code_advice_prompt(code: str) -> str:
    return f"""
    Here is some code:

    {code}

    Please:
    1. Review it for errors or inefficiencies.
    2. Suggest improvements or best practices.
    3. Explain what the code does briefly.
    """



def code_advice_tool(code: str) -> str:
    prompt = code_advice_prompt(code)
    response = llm.invoke(prompt)
    return response
tools = [
    Tool.from_function(
        func=calculator_tool,
        name="Calculator",
        description="Use this for basic maths like '2 + 2 * 5'"
    ),
    Tool.from_function(
        func=code_advice_tool,
        name="CodeAdvisor",
        description="Analyzes Python code, suggests improvements, and explains it."
    )
]


llm = ChatOpenAI(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0
)


agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)



def ask_ai(prompt: str) -> str:
    try:
        result = agent.invoke({"input": prompt})
        return result.get("output", result)
    except Exception as e:
        return f"[Error] {e}"


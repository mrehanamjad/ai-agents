import os
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from custom_tools import TemporalToolkit

# weather tool
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain_community.tools.openweathermap.tool import OpenWeatherMapQueryRun


# load .env
load_dotenv()

# your OpenWeatherMap API key
api_key = os.getenv("OPENWEATHERMAP_API_KEY")
print("OpenWeatherMap API Key:", api_key)

# 1. Setup the Model
model = ChatOllama(model="llama3.2:1b")

toolkit = TemporalToolkit()

weather_tool = OpenWeatherMapQueryRun(
    api_wrapper=OpenWeatherMapAPIWrapper(openweathermap_api_key=api_key)
)

# other tools from your custom toolkit
tools = toolkit.get_tools()

# add weather.run (the tool function) to tools list
tools += [weather_tool]

# bind tools to the model
model_with_tools = model.bind_tools(tools)

# system prompt
system_msg = SystemMessage("""
You are a smart daily helpful assistant. Use multiple tools when needed.
""")

# example user message
human_msg = HumanMessage("Can you tell me the current weather in Karachi and then current day/time?")

# build up initial messages
messages = [
    system_msg,
    human_msg
]

# call model_with_tools once to allow tool invocation
response = model_with_tools.invoke(messages)

print("- - - Tool Calls - - -")
for tool_call in response.tool_calls:
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")
    print(f"ID: {tool_call['id']}")

# Now run the requested tools
tool_messages = []
tool_map = {tool.name: tool for tool in tools}

for tool_call in response.tool_calls:
    tool = tool_map.get(tool_call["name"])
    if tool:
        # invoke the tool with args
        result = tool.invoke(tool_call["args"])
        tool_messages.append(
            ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            )
        )

# add tool messages to final context with original human message
final_response = model_with_tools.invoke(
    [system_msg, human_msg] + tool_messages
)

print("\nAI Response:")
print(final_response.content)

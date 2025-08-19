from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import json
import os

load_dotenv()

model1 = ChatGroq(
    model="llama3-8b-8192",   # or "llama3-70b-8192"
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

st.title("Steps to perform a task")

agents = ['Agent1', 'Agent2', 'Agent3', 'Agent4', 'Agent5']

prompt1 = PromptTemplate(
    template="""Give a list of strictly 5 subtasks for the task '{task}'.
                Return ONLY a JSON array of strings like:
                ["subtask1", "subtask2", "subtask3", "subtask4", "subtask5"]
                No extra text.""",
    input_variables=['task']
)

task = st.text_input('Enter task : ')

parser1 = StrOutputParser()

chain1 = prompt1 | model1 | parser1
if st.button('Get Steps'):

    result1 = chain1.invoke({
        'task' : task
    })

    try:
        result = json.loads(result1)
    except json.JSONDecodeError:
        st.error("Error: LLM did not return valid JSON. Output was:")
        st.write(result1)
        result = []

    st.header("List of Subtasks : \n")
    
    for task in result:
        st.write("->",task)

    agent_subtask={}
    i = 0
    for agent in agents:
        agent_subtask[agent] = result[i]
        i += 1

    def return_status(agent_name, subtask):
        st.divider()
        st.write(f"**Subtask:** {subtask}  ::  **Agent:** {agent_name}")
        st.write("Status: Initializing task")
        st.write("Status: In progress")
        st.write("Status: Completed successfully")

    st.header("Status of each subtask : \n")

    for agent in agent_subtask.keys():
        return_status(agent, agent_subtask[agent])
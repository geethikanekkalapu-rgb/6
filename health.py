import os
import streamlit as st
from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from operator import add

#1 Set your GROQ API Key
api_key=os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Groq_API_Key not set. Please configure it.")
    st.stop()

#2 Setup LLM
llm=ChatGroq(
    temperature=0,
    model_name="llama-3.1-8b-instant",
    api_key=api_key
)

#
class HealthState(TypedDict):
    query:str
    context:str
    messages:Annotated[list,add]
    response:str

#4
def healthcare_guideline_helper(query:str)->str:
    """
    Helper function that retrieves healthcare guidelines
    (not a tool - can be called directly)
    """
    guidelines={
        "diabetes":"follow a balanced diet, monitor blood sugar regularly, and maintain physcial activity.",
        "hypertension":"monitor blood pressure daily, reduce salt intake, and follow pysician-prescribed medication.",
        "mental health":"practice mindfulness, regular exercise, therapy sessions and adequate sleep."
    }
    results=[v for k, v in guidelines.items() if k.lower() in query.lower()]
    return "\n".join(results) if results else "no specific guidelines found, please consult a healthcare professional"

#define tools for the agent
@tool
def get_healthcare_recommendations(query:str)->str:
    """get healthcare recommendations and guidelines based on the query"""
    return healthcare_guideline_helper(query)

tools=[get_healthcare_recommendations]

#5 LangGraph Nodes
def retrieve_context_node(state:HealthState)->HealthState:
    """Node 1: Retrieve healthcare context using helper function"""
    query=state["query"]
    context=healthcare_guideline_helper(query)
    return {**state, "context": context, "messages": [HumanMessage(content=f"Retrieved context: {context}")]}

def create_prompt_node(state:HealthState)->HealthState:
    """Node 2: Create structured prompt with context"""
    query=state["query"]
    context=state["context"]
    prompt=f"""you are a helpful healthcare assistant.

Context:
{context}

User Question:{query}

Provide a clear, accurate, and actionable response.
Mention relevant guidelines if available."""
    return {**state, "messages":state["messages"]+[HumanMessage(content=prompt)]}

def generate_response_node(state:HealthState)->HealthState:
    """Node 3: Generate response using the react agent"""
    agent=create_react_agent(model=llm,tools=tools)
    response=agent.invoke({"messages":state["messages"]})

    if response and "messages" in response:
        bot_message=response["messages"][-1]
        response_text=bot_message.content
    else:
        response_text=str(response)
    return {**state, "response": response_text, 
            "messages": state["messages"]+
            [AIMessage(content=response_text)]}

def build_health_graph():

    graph = StateGraph(HealthState)
    graph.add_node("retrieve_context", retrieve_context_node)
    graph.add_node("create_prompt", create_prompt_node)
    graph.add_node("generate_response", generate_response_node)

    graph.add_edge(START, "retrieve_context")
    graph.add_edge("retrieve_context", "create_prompt")
    graph.add_edge("create_prompt", "generate_response")
    graph.add_edge("generate_response", END)

    return graph.compile()

health_workflow = build_health_graph()
st.title("HealthCare Advice Chatbot (LangGraph + Tool Agent)")

#initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation=[]

#user box for code
user_query=st.text_input("ask your healthcare question:")

if user_query:
    try:
        with st.spinner("processing your query ..."):
            initial_state={"query":user_query,"context":"","messages":[],"response":""}
            result=health_workflow.invoke(initial_state)
            bot_response_text=result.get("response","No response generated")
            st.session_state.conversation.append({"user":user_query,"bot":bot_response_text})

        st.success("response ready")
        st.markdown(f"**You:**{user_query}")
        st.markdown(f"**Assistant:**{bot_response_text}")

        with st.expander("Context Used"):
            st.text(result.get("context","No context available"))
    except Exception as e:
        st.error(f" Error:{str(e)}")
        import traceback
        st.error(traceback.format_exc())

if st.session_state.conversation:
    st.divider()
    st.subheader("Conversation History")
    for turn in st.session_state.conversation:
        st.markdown(f"**You:**{turn['user']}")
        st.markdown(f"**Assistant:**{turn['bot']}")
        st.divider()
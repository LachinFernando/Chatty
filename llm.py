from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os
import streamlit as st


os.environ["OPENAI_API_KEY"] = st.secrets["keys"]["OPENAI_API_KEY"]
os.environ["GROQ_API_KEY"] = st.secrets["keys"]["GROQ_API_KEY"]

QA_MODEL = "gpt-4o-mini"
LLM_MODELS = ("OpenAI", "llama3-70b-8192", "mixtral-8x7b-32768")


COMMON_TEMPLATE = """
"You are Chatty, an highly intelligent and friendly chatbot dedicated to answer user questions."
"Provide clear and consicse answers."
"\n\n"
Question: {question}
"n"
"Helpful answer:   "
"""

def get_openai_model():
    model = ChatOpenAI(model=QA_MODEL, api_key=os.environ["OPENAI_API_KEY"])
    return model


def get_groq_model(model_type: str):
    model = ChatGroq(temperature=0, groq_api_key=os.environ["GROQ_API_KEY"], model_name=model_type)
    return model


def streaming_question_answering(query_question: str, llm_model: str, template: str = COMMON_TEMPLATE):
    prompt = ChatPromptTemplate.from_template(template)

    # select the model
    if llm_model == LLM_MODELS[0]:
        model = get_openai_model()
    else:
        model = get_groq_model(llm_model)

    # output parser
    output_parser = StrOutputParser()

    # create the chain
    chain = prompt | model | output_parser

    # get the answer
    return chain.stream({"question": query_question})
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models import BaseChatModel
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
def get_gemini_llm():

    return  client

def get_groq_llm(model_name:str, temperature:int=0) -> BaseChatModel:

    return ChatGroq(
        model=model_name,
        temperature=temperature,
        api_key=os.getenv('GROQ_API_KEY')
    )
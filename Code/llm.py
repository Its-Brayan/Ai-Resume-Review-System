from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(model_name:str,temperature:float = 0.2) -> BaseChatModel:

    return ChatGroq(
        model=model_name,
        temperature=temperature,
        api_key=os.getenv('GROQ_API_KEY')
    )
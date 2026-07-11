from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models import BaseChatModel
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
def get_llm():

    return  client
    
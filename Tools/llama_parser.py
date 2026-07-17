from llama_cloud import LlamaCloud
import os
from dotenv import load_dotenv
from typing import Any
load_dotenv()
client = LlamaCloud(api_key=os.getenv('LLAMA_API_KEY'))

# 1. Add this helper function above run_pipeline
def extract_text_from_parse_obj(doc_obj):
    """Extracts plain text/markdown from a LlamaParse object"""
    # If it's already a string, just return it
    if isinstance(doc_obj, str):
        return doc_obj
        
    try:
        # Try to get Markdown pages first (best for LLMs)
        if hasattr(doc_obj, 'markdown') and doc_obj.markdown.pages:
            return "\n".join([page.markdown for page in doc_obj.markdown.pages])
        # Fallback to plain text pages
        elif hasattr(doc_obj, 'text') and doc_obj.text.pages:
            return "\n".join([page.text for page in doc_obj.text.pages])
    except Exception as e:
        print(f"Could not extract clean text: {e}")
def parse_document(document: Any):
    file = client.files.create(file=document,purpose="parse")
    result = client.parsing.parse(
        file_id=file.id,
        tier="agentic",
        version="latest",
        processing_options={
        "ocr_parameters": {"languages": ["en"]},
        },
        expand=["text", "markdown"]
    )
    extracted_text = extract_text_from_parse_obj(result)
    return extracted_text
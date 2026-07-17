from llama_cloud import LlamaCloud
import os
from dotenv import load_dotenv
from typing import Any
load_dotenv()
client = LlamaCloud(api_key=os.getenv('LLAMA_API_KEY'))


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
    return result
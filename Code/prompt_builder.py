from typing import Union,Any

def lower_text_character(text:str) -> str:
    return text[0].lower() + text[1:] if text else text


def format_prompt_section(lead_in:str, value:Union[str,list[str]]) -> str:

    if isinstance(value,list):
        formatted_items = []
        for item in value:
            if isinstance(item,dict):
                formatted_items.append(str(item))
            else:
                formatted_items.append(str(item))
            formatted_prompt = "/n".join(formatted_items)
    else:
        formatted_prompt = str(value)
    return f"{lead_in}\n{formatted_prompt}"

def build_prompt_body(
        prompt_config:dict[str,Any],
        input_prompt:Union[str,list[str],dict[str,Any]] | None = None
        ) -> str:
    prompt_parts = []
    if role := prompt_config.get('role'):
        prompt_parts.append(lower_text_character(role.strip()))

    if instructions := prompt_config.get('instructions'):
        if not instructions:
            raise ValueError("Instructions must be provided")
        prompt_parts.append(format_prompt_section("You are required to follow these instructions",instructions))
    
    if context := prompt_config.get('context'):
        prompt_parts.append(format_prompt_section("Use the following context",context))
    
    if examples := prompt_config.get('examples'):
        if isinstance(examples,list):
            for i,example in enumerate(examples):
             prompt_parts.append(format_prompt_section(f"Examples: {i}:\n {example}"))
        else:
            prompt_parts.append(format_prompt_section("Use the following examples",examples))
        
    if output_constraints := prompt_config.get('output_constraints'):
        prompt_parts.append(format_prompt_section("Follow these guidelines when it comes to the output",output_constraints))
    
    if goals := prompt_config.get('goals'):
        prompt_parts.append(format_prompt_section("You are required to achieve the following",goals))
    
    if style_or_tone := prompt_config.get('style_or_tone'):
        prompt_parts.append(format_prompt_section("format these style and tone guidance in your response",style_or_tone))
    
    if output := prompt_config.get('output'):
        prompt_parts.append(format_prompt_section("Structure the output as follows",output))
    
    if input_prompt is not None:
        prompt_parts.append(input_prompt)

    return "\n\n".join(str(part) for part in prompt_parts)
    

        
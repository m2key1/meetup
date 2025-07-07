import json
import requests
from typing import Optional
from pydantic import BaseModel

GRAMMAR = r'''
root ::= knowledge-graph-object
knowledge-graph-object ::= "{" ws "\"nodes\":" ws node-list "," ws "\"edges\":" ws edge-list ws "}"
node-list ::= "[" ws (node-object ("," ws node-object)*)? ws "]"
edge-list ::= "[" ws (edge-object ("," ws edge-object)*)? ws "]"
node-object ::= "{" ws "\"id\":" ws integer "," ws "\"name\":" ws string "," ws "\"type\":" ws string "," ws "\"description\":" ws string ws "}"
edge-object ::= "{" ws "\"source_id\":" ws integer "," ws "\"target_id\":" ws integer "," ws "\"type\":" ws string "," ws "\"description\":" ws string ws "}"
string ::= "\"" ( [^"\\\n] | "\\" ( "\"" | "\\" | "/" | "b" | "f" | "n" | "r" | "t" | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] ) )* "\""
integer ::= [0-9]+
ws ::= [ \t\n]*
'''

def llm(model_name: str, prompt:str, system: Optional[str]=None, schema: Optional[BaseModel] = None, host='localhost'):
    messages = []
    
    if system:
        messages = [ 
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    else:
        messages = [
            {"role": "user", "content": prompt}
        ]
    
    payload = {
        "model": model_name,
        "messages": messages
    }
    
    if schema:
        payload.update({"grammar": GRAMMAR})
        
    server_url = f"http://{host}:8888/v1/chat/completions"
        
    response = requests.post(server_url, 
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(payload))
    
    response.raise_for_status()

    response_data = response.json()
    response_text = response_data['choices'][0]['message']['content'].strip()
    
    if schema:
        try:
            response_text = schema.model_validate_json(response_text)
        except Exception as e:
            print(f"Error validating json: {e}")
            response_text = response_data['choices'][0]['message']['content'].strip()
    
    timings = response_data['timings']
    prompt_per_second = timings['prompt_per_second']
    tokens_per_second = timings['predicted_per_second']
    usage = response_data['usage']
    predicted_tokens = usage['completion_tokens']
    prompt_tokens = usage['prompt_tokens']
    
    return response_text, [model_name, f"{tokens_per_second:.2f}", f"{prompt_per_second:.2f}", predicted_tokens, prompt_tokens]

def unload(host='localhost'):
    response = requests.get(f'http://{host}:8888/unload')
    response.raise_for_status()
    return response
    
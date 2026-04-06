from google import genai
import os
import json
from math import e
from typing import Any
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

def jsonify(string: str):
    encoded = json.loads(string)
    return encoded

def ask_gemini(prompt: str):
    """Call Gemini and return a plain Python dict representing the response.
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        contents = str(prompt)

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=contents
        )
    except Exception as e:
        exception = Exception(f"error: request_failed, message: {str(e)}")
        print(exception)

    return response # type: ignore

def calculate_risk_score(user_info: dict[str, Any] ):
    '''Calculates the risk range of the patient
    '''
    with open("Triage_system/prompt.txt", "r") as f:
        prompt = f.read()
        prompt += str(user_info)
    
    response = ask_gemini(prompt)
    response = response.text # pyright: ignore[reportCallIssue, reportOptionalCall]

    print(response)
    response_dict = jsonify(str(response))
    print(response_dict)
    print(response_dict["Risk Score"])

def calculate_token_reduction(current_token_number:int, risk_score:float) -> int:
    token_reduction = 1+(current_token_number-1) * (1-risk_score)
    reduction = current_token_number - token_reduction
    new_reduction = int(reduction // 1) 
    if 0 < reduction < 3 and risk_score < 0.5:
        return 0
    return new_reduction


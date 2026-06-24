from openai import OpenAI
import os
from library import handler as hdl

client = None

def connectCody():
    global client
    apiKey = os.environ['DEEPSEEK_API_KEY']
    # Deepseek base URL is https://api.deepseek.com
    client = OpenAI(api_key=apiKey, base_url='https://api.deepseek.com')
    return True

def submitCody(lstRecord):
    global client
    llmModel = os.environ['DEEPSEEK_MODEL_NAME']
    lstMessage = hdl.convertMessage(lstRecord)
    response = client.chat.completions.create(
        model=llmModel,
        messages=lstMessage
    )
    result = {
        'role': response.choices[0].message.role,
        'content': response.choices[0].message.content
    }
    return result

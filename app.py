import openai
from openai import OpenAI
import os

from flask import Flask, render_template, request, jsonify

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key = OPENAI_API_KEY)

def get_completion(prompt, model="gpt-4o", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content 

def get_completion_from_messages(messages, model="gpt-4o", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    print(response.choices[0])
    return response.choices[0].message.content

app = Flask(__name__)

# Define the context for the chatbot
context = [{'role': 'system', 'content': """
You are ChatBot, an automated service built to teach Asante Twi ONLY. \ 
You are funny and likes to inject humor in everything. \
You first greet the user, then let them know that it is a great pleasure to welcome them to the great African language. \
Remember that the conversation always starts and ends with you. \
You will primarily interact with the user in English. \
However, please translate anything that the user asks to be translated in Asante Twi. \
When asked to translate, acknowledge what the user has asked in English before translating. \
In that case, it should be formatted such as: \
User: Translate "have you ever attended school?" \
Bot: I see you want me to translate 'Have ever attended school'? It will be translated as 'woako sukuu da"? \
Whenever there is about 10 seconds pause in the conversation, \
inquire from the user if they would like to continue learning or done for now \
Please take your time to provide the best translation \
It is better to receive a translation a few seconds late and accurate \
than too fast and not entirely accurate. \
Also, please remember that you are for Asante Twi ONLY. \
If any user asks you to teach any other language, be clear that you cannot do so, and  \
politely redirect them to learning Twi instead with a translation of what they asked in Asante Twi. \
"""}]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    context.append({'role': 'user', 'content': user_input})
    response = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': response})
    return jsonify({'response': response})

try: 
    if  __name__ == '__main__':
        app.run(debug=True,port=8000)
except:
    print("Exception occured!")
    from werkzeug.serving import run_simple
    run_simple('localhost', 9000, app)
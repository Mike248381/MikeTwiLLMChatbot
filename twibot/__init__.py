#import openai
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

def get_completion_from_messages(messages, model="gpt-4o", temperature=0.2):
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
You are ChatBot, an automated service built to teach Asante Twi ONLY.  
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
\
As you do translations, use the following instructions: \
1. Please remember that you are for Asante Twi ONLY. \
If any user asks you to teach any other language, be clear that you cannot do so, and  \
politely redirect them to learning Twi instead with a translation of what they asked in Asante Twi. \
2. If you are asked to produce any answers to any queries that are not about translation, \
please politely and humorously remind the user that you are only there to help teach Twi. \
For instance, if a user asks "please show me the steps to write a good book", reply to the user \
with a response such as "I am only here to support your Twi mastery, and I would rather keep you on track instead". \
3. However, if you are asked to generate anything with a translation to Twi, then please do. \
The goal is for the user to learn Twi. For instance, a user could ask to produce some common phrases with their Twi translation, \
which you are allowed to do and do well. In addition, you should provide a response if the user clearly states that you should do anything and translate \
such as "please show me the steps to cook jollof rice", your response to let the user know that you can do that if only they need the Twi translation. \
If they agree, you should produce the steps with the corresponding translation for each step in the format \
step 1: [English - Text] \
[Twi - Text] \
step 2: [English - Text] \
[Twi - Text] \
4. Remember that you are not a tool for any other purpose other Twi translation, so anything you're asked that \
is not directly related to translation should receive a response that redirects the user to learning Twi instead. \
For instance, if the user asks "give me the answer of ten percent of 100", respond with something like \
"oh I see you're interested in learning some math. Unfortunately my genius is at Twi. I am happy to translate your question to Twi, though"\
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
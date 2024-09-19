from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
import sqlite3
import pyodbc
import os
import json
import logging
import requests
import openai

app = Flask(__name__)

app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_PERMANENT"] = 'False'
Session(app)



OPEN_AI_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 100
def get_chat_message_exact(query):
    return [
        {
            "role": "user",
            "content": query
        }
    ]


OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_API_URL = "https://api.openai.com/v1/chat/completions"

@app.route("/openairesponse", methods=["POST"])  # Changed to POST
def get_openai_response():
    # Assuming the client sends data in JSON format
    data = request.get_json()  # Use get_json() instead of request.json

    query = data.get('query')
    previous_chat = data.get('previous_chat')
    exact = data.get('exact')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_API_KEY}"
    }
    request_body = {
        "model": OPEN_AI_MODEL,
        "max_tokens": MAX_TOKENS,
        "temperature": 1,
        "messages": get_chat_message_exact(query) if exact else get_chat_message(query, previous_chat)
    }

    response = requests.post(OPEN_API_URL, headers=headers, data=json.dumps(request_body))

    return jsonify(response.json())

def get_chat_message(query, previous_chat):
    logging.info(f"QUERY: {query}, PreviousChat: {previous_chat}")
    
    # Messages formatted as a list of dictionaries for the OpenAI API
    messages = [
        {
            "role": "user",
            "content": query
        },
        {
            "role": "assistant",
            "content": f"Generate a Mermaid code for the requested diagram and only return the code {query} "
                       f"without any explanations or anything. Please keep in mind this previous conversation: '{previous_chat}'"
        }
    ]
    
    return messages
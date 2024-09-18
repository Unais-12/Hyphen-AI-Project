from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
import sqlite3
import pyodbc
import sys
from app import app as application
import os

path = '/home/Unais1/mysite/flask_app.py'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)
app = Flask(__name__)

app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_PERMANENT"] = 'False'
Session(app)

@app.route("/main", method = ["GET"])
def main():
    return "Hello"
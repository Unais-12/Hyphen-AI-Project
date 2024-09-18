from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
import sqlite3
import pyodbc
import sys
import os

app = Flask(__name__)

app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_PERMANENT"] = 'False'
Session(app)

@app.route("/main", methods = ["GET"])
def main():
    return "Hello"
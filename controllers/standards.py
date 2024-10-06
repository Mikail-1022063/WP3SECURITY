from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import sqlite3
import datetime
from datetime import datetime
import string
import random
import bcrypt


def db_connect():
    conn = sqlite3.connect('databases/accessibility_hub.db')
    cursor = conn.cursor()
    return conn, cursor

from flask import Flask
# for markdown purposes -maleko
from flask_simplemde import SimpleMDE





app = Flask(__name__)
# for markdown purposes -maleko
simplemde = SimpleMDE(app)
app.config['SIMPLEMDE_JS_IIFE'] = True
app.config['SIMPLEMDE_USE_CDN'] = True
app.secret_key = "Svet is the best"
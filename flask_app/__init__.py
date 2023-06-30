from flask import Flask
# for markdown purposes -maleko
# from flask_ckeditor import CKEditor
from flask_simplemde import SimpleMDE






app = Flask(__name__)
# for markdown purposes -maleko
# app.config['CKEDITOR_PKG_TYPE'] = 'standard'
# ckeditor = CKEditor(app)
simplemde = SimpleMDE(app)
app.config['SIMPLEMDE_JS_IIFE'] = True
app.config['SIMPLEMDE_USE_CDN'] = True
app.secret_key = "Svet is the best"
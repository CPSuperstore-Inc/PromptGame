from flask import Blueprint

app = Blueprint('filters', __name__, template_folder='templates')

@app.app_template_filter()
def uppercase(text):
    return text.upper()


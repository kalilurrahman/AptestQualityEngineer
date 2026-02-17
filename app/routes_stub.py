from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        # ... logic ...
        pass
    return render_template('generate.html')

@main.route('/agentic')
def agentic():
    return render_template('agentic.html')

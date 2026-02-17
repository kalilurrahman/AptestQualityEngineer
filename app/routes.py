from flask import Blueprint, render_template, request, jsonify, flash
from app.utils import extract_text_from_url, extract_text_from_file, generate_artifacts
import markdown
import json
import os

main = Blueprint('main', __name__)

def load_repo_data():
    filepath = os.path.join('app', 'data', 'repo_data.json')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/generate', methods=['POST'])
def generate():
    api_key = request.form.get('api_key')
    context_type = request.form.get('context_type')
    context_text = ""

    if context_type == 'text':
        context_text = request.form.get('context_text')
    elif context_type == 'url':
        url = request.form.get('context_url')
        context_text = extract_text_from_url(url)
    elif context_type == 'file':
        file = request.files.get('context_file')
        if file:
            context_text = extract_text_from_file(file)

    if not context_text:
        return jsonify({'error': 'No context provided or failed to extract text.'}), 400

    artifacts_md = generate_artifacts(api_key, context_text, context_type)
    artifacts_html = markdown.markdown(artifacts_md, extensions=['tables', 'fenced_code'])
    return render_template('result.html', artifacts=artifacts_html)

@main.route('/repository')
def repository():
    items = load_repo_data()
    return render_template('repository.html', items=items)

@main.route('/repository/<item_id>')
def repo_detail(item_id):
    items = load_repo_data()
    item = items.get(item_id)
    if not item:
        return "Item not found", 404

    # Convert markdown content to HTML
    if 'content' in item:
        item['content_html'] = markdown.markdown(item['content'], extensions=['tables', 'fenced_code'])

    return render_template('repo_detail.html', item=item)

from flask import Blueprint, render_template, request, jsonify, flash
from app.utils import extract_text_from_url, extract_text_from_file, generate_artifacts, generate_test_data_batch
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
    image_data = None

    if context_type == 'text':
        context_text = request.form.get('context_text')

    elif context_type == 'url':
        url = request.form.get('context_url')
        if url:
            context_text = extract_text_from_url(url)
        else:
            return jsonify({'error': 'No URL provided.'}), 400

    elif context_type == 'file':
        if 'context_file' not in request.files:
             return jsonify({'error': 'No file uploaded.'}), 400
        file = request.files['context_file']
        if file.filename == '':
             return jsonify({'error': 'No file selected.'}), 400

        context_text = extract_text_from_file(file)

    elif context_type == 'image':
        if 'context_image' not in request.files:
            return jsonify({'error': 'No image uploaded.'}), 400

        image_file = request.files['context_image']
        if image_file.filename == '':
            return jsonify({'error': 'No image selected.'}), 400

        # Read image bytes
        image_data = image_file.read()
        context_text = "Image analysis requested."

    if not context_text and not image_data:
        return jsonify({'error': 'No context provided or failed to extract content.'}), 400

    # Generate artifacts (pass image_data if present)
    artifacts_md = generate_artifacts(api_key, context_text, context_type, image_data)

    # Check for errors returned as strings
    if artifacts_md.startswith("Error"):
        return jsonify({'error': artifacts_md}), 500

    artifacts_html = markdown.markdown(artifacts_md, extensions=['tables', 'fenced_code'])
    return render_template('result.html', artifacts=artifacts_html, artifacts_md=artifacts_md)

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

@main.route('/test-data')
def test_data():
    return render_template('test_data.html')

@main.route('/generate-test-data', methods=['POST'])
def generate_data():
    api_key = request.form.get('api_key')
    data_type = request.form.get('data_type')
    output_format = request.form.get('format')
    quantity = request.form.get('quantity')
    constraints = request.form.get('constraints')

    if not api_key:
        return jsonify({'error': 'API Key is required'}), 400

    generated_data = generate_test_data_batch(api_key, data_type, output_format, quantity, constraints)

    # Simple error check
    if generated_data and generated_data.startswith("Error"):
         return jsonify({'error': generated_data}), 500

    return render_template('test_data_result.html', data=generated_data, format=output_format)

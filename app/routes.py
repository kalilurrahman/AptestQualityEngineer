from flask import Blueprint, render_template, request, jsonify, flash
from app.utils import extract_text_from_url, extract_text_from_file, generate_artifacts
import markdown
import json
import os
import uuid
import sys

# Add src to path for agentic imports
# This is crucial for imports to work when running from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Lazy import to avoid circular dependencies or initialization issues
try:
    from src.workflows.graph import app as agentic_graph
    # We must import AgentState type for type hinting but it's not strictly runtime required if we use dict
except ImportError:
    agentic_graph = None
    print("Warning: Could not import Agentic QA system. Agentic routes will fail.")

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

# --- Agentic Routes ---

@main.route('/agentic')
def agentic_ui():
    return render_template('agentic.html')

@main.route('/agentic/run', methods=['POST'])
def agentic_run():
    if not agentic_graph:
        return jsonify({"error": "Agentic system not loaded."}), 500

    data = request.json
    api_key = data.get('api_key')
    requirements = data.get('requirements')

    # Set API Key in env for this thread (simplified)
    # In a real production app, pass this via config or state, not global env
    os.environ["GOOGLE_API_KEY"] = api_key

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # Initial State
    state = {
        "user_requirements": requirements,
        "test_plan": [],
        "current_test_context": {},
        "execution_logs": ["Agentic Workflow Initialized..."],
        "screenshots": [],
        "retry_count": 0,
        "final_verdict": "in_progress",
        "current_scenario_index": 0,
        "error": None
    }

    logs = []
    try:
        # Run graph synchronously for demo purposes (in prod, use async/background task)
        # We use .stream() to get updates

        # Note: Depending on LangGraph version, inputs might need to be passed differently.
        # Assuming the standard invocation pattern.

        for event in agentic_graph.stream(state, config=config):
            for key, value in event.items():
                logs.append(f"Completed Step: {key}")
                if isinstance(value, dict) and "execution_logs" in value:
                    logs.extend(value["execution_logs"])
                elif isinstance(value, dict) and "test_plan" in value:
                     logs.append(f"Generated {len(value['test_plan'])} scenarios.")

    except Exception as e:
        logs.append(f"Error executing agent workflow: {str(e)}")

    return jsonify({
        "thread_id": thread_id,
        "status": "completed",
        "logs": logs
    })

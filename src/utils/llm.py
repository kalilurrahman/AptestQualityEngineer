import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
from typing import Optional, List, Any
import json

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# Model Priorities
# Define a hierarchy of models for different capabilities.
# If the first one fails (e.g., rate limit, not found), try the next.
MODEL_REGISTRY = {
    "reasoning": ["gemini-1.5-pro-latest", "gemini-1.5-pro", "gemini-pro"],
    "planning": ["gemini-1.5-pro-latest", "gemini-1.5-pro", "gemini-pro"],
    "coding": ["gemini-1.5-pro-latest", "gemini-1.5-pro", "gemini-1.5-flash"],
    "vision": ["gemini-1.5-flash-latest", "gemini-1.5-flash", "gemini-1.5-pro"],
    "fast": ["gemini-1.5-flash-latest", "gemini-1.5-flash", "gemini-pro"]
}

def get_best_available_model(capability: str = "reasoning") -> str:
    """
    Selects the best available model for the given capability.
    This mimics the "autofix" logic for model pickup.
    """
    candidates = MODEL_REGISTRY.get(capability, MODEL_REGISTRY["reasoning"])

    # In a real rigorous system, we might ping the API to check availability.
    # Here, we return the first one as the primary target, but the `call_llm` function
    # will handle the fallback logic.
    return candidates[0]

def call_llm(
    prompt: str,
    capability: str = "reasoning",
    image_path: Optional[str] = None,
    structured_output_schema: Optional[Any] = None
) -> str:
    """
    Calls the Gemini LLM with the given prompt and capability.
    Handles model fallbacks automatically.

    Args:
        prompt: The text prompt.
        capability: The type of task (reasoning, planning, vision, fast).
        image_path: Path to an image file for multimodal inputs.
        structured_output_schema: A Pydantic model or TypedDict for JSON enforcement.
    """
    if not GOOGLE_API_KEY:
        print(f"[LLM Mock] No API Key found. Returning mock response for {capability}.")
        return mock_response(prompt, capability, structured_output_schema)

    candidates = MODEL_REGISTRY.get(capability, MODEL_REGISTRY["reasoning"])

    last_error = None

    for model_name in candidates:
        try:
            # print(f"[LLM] Attempting with model: {model_name}")

            model_config = {}
            if structured_output_schema:
                model_config["response_mime_type"] = "application/json"
                # For robust schema enforcement, prompt engineering is key along with response_mime_type

            model = genai.GenerativeModel(model_name)

            inputs = [prompt]
            if image_path:
                if os.path.exists(image_path):
                    # Load image
                    try:
                        import PIL.Image
                        img = PIL.Image.open(image_path)
                        inputs.append(img)
                    except ImportError:
                         print("[LLM] PIL not installed, skipping image.")
                else:
                    print(f"[LLM] Warning: Image path {image_path} not found.")

            response = model.generate_content(
                inputs,
                generation_config=model_config
            )

            return response.text
        except Exception as e:
            print(f"[LLM] Error with {model_name}: {e}. Trying next candidate...")
            last_error = e
            time.sleep(1) # Brief pause before retry

    raise Exception(f"All model candidates failed for capability '{capability}'. Last error: {last_error}")

def mock_response(prompt: str, capability: str, schema: Optional[Any] = None) -> str:
    """
    Returns a mock response when no API key is present.
    """
    if "TestPlan" in prompt or capability == "planning":
        return json.dumps({
            "scenarios": [
                {
                    "id": "mock-1",
                    "title": "Mock Login Test",
                    "description": "Verify user can login.",
                    "steps": ["Navigate to https://example.com/login", "Enter user", "Click submit"],
                    "expected_result": "Dashboard visible",
                    "tags": ["smoke"]
                }
            ]
        })
    if "tool" in prompt or capability == "coding":
        # Mocking tool calls logic
        return json.dumps([
            {"tool": "interact_with_ui", "args": {"action": "navigate", "description": "https://example.com/login"}},
            {"tool": "interact_with_ui", "args": {"action": "type", "description": "username field", "value": "testuser"}},
            {"tool": "interact_with_ui", "args": {"action": "click", "description": "login button"}}
        ])

    if capability == "vision":
        return "The screenshot shows a login form with a missing submit button."

    return "Mock LLM Response"

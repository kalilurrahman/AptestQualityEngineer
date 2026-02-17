# Aptest Quality Engineering Tool

An AI-powered application for generating comprehensive Quality Engineering artifacts.

## Features

*   **Generate Test Artifacts**: Creates Test Strategy, Test Cases, Boundary Value Analysis, Test Data, and more using Google Gemini Pro.
*   **Flexible Input**: Accepts text prompts, website URLs, and document uploads (PDF/Text) as context.
*   **Test Case Repository**: Includes a starter library of test strategies for common domains (Netflix, Google News, Car Insurance, etc.).
*   **Modern UI**: Built with Flask and Bootstrap 5.

## Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Populate the starter data:
    ```bash
    python populate_data.py
    ```

## Usage

1.  Run the application:
    ```bash
    python run.py
    ```
2.  Open your browser and navigate to `http://localhost:5000`.
3.  Enter your Google Gemini API Key.
4.  Provide the context (Text, URL, or File) and click "Generate Artifacts".
5.  View, print, or save the generated artifacts.

## Project Structure

*   `app/`: Core application code.
    *   `__init__.py`: Flask app initialization.
    *   `routes.py`: URL routing and view logic.
    *   `utils.py`: Helper functions for LLM integration and text extraction.
    *   `templates/`: HTML templates.
    *   `static/`: CSS and JS files.
    *   `data/`: Data storage (JSON).
*   `run.py`: Entry point.
*   `populate_data.py`: Script to generate starter data.
*   `test_*.py`: Unit and integration tests.

## Requirements

*   Python 3.8+
*   Google Gemini API Key

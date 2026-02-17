# Deployment Guide

This guide provides comprehensive instructions for deploying the **Quality Engineering Artifact Generator** in various environments, from local development to production-ready cloud hosting.

---

## 1. Prerequisites

Before starting, ensure you have the following:

*   **Google Gemini API Key**: Obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).
*   **Git**: Version control system.
*   **Python**: Version 3.9 or higher (for local/cloud deployment).
*   **Docker** (Optional): For containerized deployment.

---

## 2. Local Deployment (Development)

Run the application on your local machine for testing or development.

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/qe-artifact-generator.git
cd qe-artifact-generator
```

### Step 2: Set Up Virtual Environment
Create an isolated Python environment to manage dependencies.

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
Start the Flask development server.
```bash
python run.py
```
Access the app at `http://127.0.0.1:5000`.

---

## 3. Docker Deployment (Containerized)

Package the application as a Docker container for consistent deployment across environments.

### Step 1: Build the Image
From the project root directory:
```bash
docker build -t qe-artifact-generator .
```

### Step 2: Run the Container
Run the container, mapping port 5000 on your host to port 5000 in the container.
```bash
docker run -p 5000:5000 qe-artifact-generator
```
Access the app at `http://localhost:5000`.

---

## 4. Cloud Deployment (Production)

Deploy the application to a cloud provider for public access.

### Option A: Google Cloud Run (Serverless)

1.  **Install Google Cloud SDK**: ensure `gcloud` is installed and authenticated.
2.  **Enable APIs**: Enable Cloud Build and Cloud Run APIs.
3.  **Deploy**:
    ```bash
    gcloud run deploy qe-generator \
      --source . \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated
    ```
4.  **Access**: Use the URL provided by the command output.

### Option B: Render / Heroku / Railway

Most PaaS providers support Python/Docker deployments out of the box.

1.  **Connect Repository**: Link your GitHub repository to the service.
2.  **Build Command**: `pip install -r requirements.txt`
3.  **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT "app:create_app()"`
4.  **Environment Variables**: None required (API Key is input by the user), but ensure `PYTHON_VERSION` is set correctly.

---

## 5. Production Considerations

*   **WSGI Server**: Always use a production WSGI server like **Gunicorn** instead of the Flask development server. The Dockerfile included uses Gunicorn by default.
*   **HTTPS**: Ensure your hosting provider handles SSL/TLS termination (Cloud Run, Heroku, etc., do this automatically).
*   **API Key Security**: The application currently asks the user for their API key. In a private internal deployment, you might modify the code to load the key from an environment variable (`os.environ.get('GEMINI_API_KEY')`) for convenience.

## 6. Troubleshooting

*   **Port In Use**: If `5000` is taken, change the port in `run.py` or the `docker run` command (`-p 8080:5000`).
*   **Missing Dependencies**: Ensure `requirements.txt` is up to date.
*   **API Errors**: Check the Gemini API usage limits and ensure the key has permissions for `gemini-pro` and `gemini-1.5-flash`.

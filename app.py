import json
import requests
from flask import Flask, jsonify, send_from_directory, request
import os

app = Flask(__name__, static_folder="static")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# NOTE: Global storage for prototype - single user only
# Production would use Flask sessions or database
current_file_content = ""


def query_llama(prompt: str, model: str = "llama3.1:8b") -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        resp = requests.post(url, json = payload, timeout = 60)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "No response from model.")
    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to LLM server. Make sure Ollama is running."
    except requests.exceptions.Timeout:
        return "Error: Request to LLM server timed out. The text might be too long."
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"

@app.route("/api/upload", methods=["POST"])
def upload_file():
    global current_file_content
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    filename = file.filename
    if filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    
    try:
        content = file.read().decode('utf-8')

        #check if file is empty
        if not content.strip():
            return jsonify({"error": "File is empty"}), 400

        #check if file is too short
        if len(content) < 50:
            return jsonify({"error": "File too short. Need at least 50 characters."}), 400
        
        current_file_content = content
        return jsonify({"message": "File uploaded successfully", "size": len(content)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/question")
def get_question():
    global current_file_content
    
    if not current_file_content:
        return jsonify({"error": "No file uploaded. Please upload a file first."}), 400
    
    text = current_file_content

    # Prompt the LLM to make ONE MCQ
    final_prompt = (
        text +
        "\n\nUsing the information above, generate ONE multiple-choice question.\n"
        "Format:\n"
        "Question: <your question here>\n"
        "a) <option>\n"
        "b) <option>\n"
        "c) <option>\n"
        "d) <option>\n"
        "Also include the correct answer at the end with a one sentence explanation like:\n"
        "Answer: <letter>\n"
    )

    reply = query_llama(final_prompt)
    return jsonify({"question": reply})

@app.route("/api/definition")
def get_definition():
    global current_file_content
    
    if not current_file_content:
        return jsonify({"error": "No file uploaded. Please upload a file first."}), 400
    
    text = current_file_content

    # Prompt the LLM to define  
    final_prompt = (
        text +
        "\n\nUsing the information above, generate ONE useful definition\n"
    
    )

    reply = query_llama(final_prompt)
    return jsonify({"definition": reply})

@app.route("/api/summarization")
def get_summarization():
    global current_file_content
    
    if not current_file_content:
        return jsonify({"error": "No file uploaded. Please upload a file first."}), 400
    
    text = current_file_content

    # Prompt the LLM to summarize
    final_prompt = (
        text +
        "\n\nUsing the information above, generate a BRIEF summary\n"
    
    )

    reply = query_llama(final_prompt)
    return jsonify({"summarization": reply})

@app.route("/api/simplification")
def get_simplification():
    global current_file_content
    
    if not current_file_content:
        return jsonify({"error": "No file uploaded. Please upload a file first."}), 400
    
    text = current_file_content

    # Prompt the LLM to simplify
    final_prompt = (
        text +
        "\n\nUsing the information above, generate a BRIEF simplification\n"
    
    )

    reply = query_llama(final_prompt)
    return jsonify({"simplification": reply})


@app.route("/")
def index():
    # Serve the frontend
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    # Run Flask dev server
    app.run(host="0.0.0.0", port=8000, debug=True)
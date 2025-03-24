from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import subprocess
import webbrowser
from urllib.parse import parse_qs
import shutil
import sys
import requests
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Serve static files with environment variables injected
@app.route('/')
def serve_index():
    with open('index.html', 'r') as f:
        content = f.read()
        # Inject environment variables
        script_tag = f"""
        <script>
            window.GEMINI_API_KEY = "{os.getenv('GEMINI_API_KEY')}";
        </script>
        """
        # Insert the script tag before the closing </head> tag
        content = content.replace('</head>', f'{script_tag}</head>')
        return content

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/save-csv', methods=['POST'])
def save_csv():
    try:
        data = request.json
        csv_content = data.get('csv_content')
        
        with open('Test.csv', 'w', encoding='utf-8') as f:
            f.write(csv_content)
            
        return jsonify({'message': 'CSV file saved successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Copy the script to the current directory
        script_path = os.path.join(os.path.dirname(__file__), 'text_to_speech.py')
        
        # Run the script with the Python interpreter
        result = subprocess.run(['python', script_path], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode != 0:
            return jsonify({
                'error': 'Script execution failed',
                'stdout': result.stdout,
                'stderr': result.stderr
            }), 500
            
        return jsonify({
            'message': 'Script executed successfully',
            'output': result.stdout
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server running at http://localhost:{port}")
    print(f"Python interpreter: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")
    
    webbrowser.open(f'http://localhost:{port}')
    
    httpd.serve_forever()

if __name__ == '__main__':
    app.run(port=8000)
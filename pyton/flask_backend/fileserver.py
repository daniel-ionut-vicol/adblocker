from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Replace 'your_folder_path' with the actual path to the folder you want to serve
folder_path = 'v8'

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(folder_path, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)

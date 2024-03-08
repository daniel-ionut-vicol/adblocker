import os
import json
import subprocess
import psutil
from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import re
from functools import reduce

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/start_testing', methods=['POST'])
def start_testing():
    data = request.get_json()
    model_path = data.get('model')
    if not model_path:
        return jsonify({'error': 'Model path not provided'}), 400

    # Run the shell script with the model path as an argument
    result = subprocess.run(['/mnt/data/mlserver/adblock/pyton/ultimate_neural_network/automation/start_test.sh', model_path], capture_output=True, text=True)

    # Check the result of the shell script
    if result.returncode != 0:
        # If the shell script failed, return the stderr
        return jsonify({'error': result.stderr}), 500
    else:
        # If the shell script succeeded, return the stdout
        return jsonify({'message': result.stdout}), 200

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    model_path = data.get('model')
    if not model_path:
        return jsonify({'error': 'Model path not provided'}), 400

    # Run the shell script with the model path as an argument
    result = subprocess.run(['/mnt/data/mlserver/adblock/pyton/ultimate_neural_network/automation/convert.sh', model_path], capture_output=True, text=True)

    # Check the result of the shell script
    if result.returncode != 0:
        # If the shell script failed, return the stderr
        return jsonify({'error': result.stderr}), 500
    else:
        # If the shell script succeeded, return the stdout
        return jsonify({'message': result.stdout}), 200

@app.route('/start_tensorboard', methods=['POST'])
def start_tensorboard():
    data = request.get_json()
    logdir = data.get('logdir')
    if not logdir:
        return jsonify({'error': 'Logdir path not provided'}), 400

    # Run the shell script with the model path as an argument
    result = subprocess.run(['/mnt/data/mlserver/adblock/pyton/ultimate_neural_network/automation/start_tensorboard.sh', logdir], capture_output=True, text=True)

    # Check the result of the shell script
    if result.returncode != 0:
        # If the shell script failed, return the stderr
        return jsonify({'error': result.stderr}), 500
    else:
        # If the shell script succeeded, return the stdout
        return jsonify({'message': result.stdout}), 200

# Load the processes from the JSON file
def load_processes():
    try:
        with open('processes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save the processes to the JSON file
def save_processes(processes):
    with open('processes.json', 'w') as f:
        json.dump(processes, f)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/get_logs', methods=['GET'])
def get_logs():
    log_file = '/mnt/data/mlserver/adblock/pyton/ultimate_neural_network/last_training.log'
    try:
        # Read the entire log file
        with open(log_file, 'r') as f:
            log_data = f.read()

        # Remove non-printable characters, but keep newline characters
        log_data = re.sub(r'[^\x20-\x7E\n]+', ' ', log_data)

        # Add newlines between log entries based on a pattern
        log_data = re.sub(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}:)', r'\n\1', log_data)

        # Split the logs into lines
        log_lines = log_data.split('\n')

        # Filter out any empty lines
        log_lines = [line for line in log_lines if line.strip()]

        # Get the first and last 50 lines
        last_50_lines = log_lines[-50:]

        # Combine the lines and return as a response
        return '\n'.join(['...'] + last_50_lines)
    except Exception as e:
        return jsonify({'message': 'Error getting logs: ' + str(e)}), 500

@app.route('/get_evaluation_logs', methods=['GET'])
def get_evaluation_logs():
    log_file = '/mnt/data/mlserver/adblock/pyton/ultimate_neural_network/last_evaluation.log'
    try:
        # Read the entire log file
        with open(log_file, 'r') as f:
            log_data = f.read()

        # Remove non-printable characters, but keep newline characters
        log_data = re.sub(r'[^\x20-\x7E\n]+', ' ', log_data)

        # Add newlines between log entries based on a pattern
        log_data = re.sub(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}:)', r'\n\1', log_data)

        # Split the logs into lines
        log_lines = log_data.split('\n')

        # Filter out any empty lines
        log_lines = [line for line in log_lines if line.strip()]

        # Get the first and last 50 lines
        last_50_lines = log_lines[-50:]

        # Combine the lines and return as a response
        return '\n'.join(['...'] + last_50_lines)
    except Exception as e:
        return jsonify({'message': 'Error getting logs: ' + str(e)}), 500

def list_files(startpath):
    files_folders = {}
    for root, dirs, files in os.walk(startpath):
        path = root.split(os.sep)
        for file in files:
            files_folders[os.path.join(*path, file)] = None
        for dir in dirs:
            files_folders[os.path.join(*path, dir)] = list_files(os.path.join(*path, dir))
    return files_folders

@app.route('/get_models', methods=['GET'])
def get_models():
    models_dir = '/mnt/data/mlserver/cnn_training/models'
    models = get_directory_structure(models_dir)
    return jsonify(models)

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir

@app.route('/hyperparameters')
def hyperparameters():
    with open('/mnt/data/mlserver/adblock/pyton/ultimate_neural_network/config.json', 'r') as f:
        config = json.load(f)
    return jsonify(config)

@app.route('/update_config', methods=['POST'])
def update_config():
    new_config = request.get_json()  # Get the new config from the client

    # Open the config file and update the values
    with open('/mnt/data/mlserver/adblock/pyton/ultimate_neural_network/config.json', 'r+') as f:
        config = json.load(f)
        config.update(new_config)
        f.seek(0)
        f.truncate()
        json.dump(config, f, indent=4)

    return jsonify(config), 200  # Return the updated config

@app.route('/start_training', methods=['POST'])
def start_training():
    # The command to start the training
    command = '/mnt/data/mlserver/adblock/pyton/ultimate_neural_network/automation/start_training.sh'

    try:
        # Execute the command
        process = subprocess.Popen(command, shell=True)

        # Store the process
        process_id = str(process.pid)
        processes = load_processes()
        processes[process_id] = True
        save_processes(processes)

        return jsonify({'message': 'Training started', 'pid': process_id}), 200
    except Exception as e:
        return jsonify({'message': 'Error starting training: ' + str(e)}), 500

processes_to_track = ["training.py", "evaluate.py", "tensorboard"]

@app.route('/processes', methods=['GET'])
def list_processes():
    # Get the list of all running processes
    running_processes = [proc for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time'])]

    # Filter the processes based on the command line
    training_processes = [proc for proc in running_processes if proc.info['cmdline'] is not None and 'python3' in ' '.join(proc.info['cmdline']) and any(cmd in ' '.join(proc.info['cmdline']) for cmd in processes_to_track)]

    # Format the processes information
    processes_info = []
    for proc in training_processes:
        processes_info.append({
            'pid': proc.info['pid'],
            'name': proc.info['name'],
            'start_time': proc.info['create_time'],
            'running_time': time.time() - proc.info['create_time'],
            'cmdline': ' '.join(proc.info['cmdline']),
        })

    return jsonify(processes_info)

@app.route('/stop_process/<string:process_id>', methods=['POST'])
def stop_process(process_id):
    try:
        subprocess.Popen('kill -9 ' + process_id, shell=True)
        return jsonify({'message': f'Process {process_id} has been terminated.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)


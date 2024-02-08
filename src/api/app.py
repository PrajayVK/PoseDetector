from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-script')
def run_script():
    try:
        # Replace 'your_script.py' with the path to your Python script
        output = subprocess.check_output(['python', 'src/api/test.py'])
        return jsonify(message=output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        return jsonify(message=str(e))

if __name__ == '__main__':
    app.run(debug=True)

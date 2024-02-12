from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

@app.route('/run-script')
def run_script():
    script_name = request.args.get('script')  # Get the script name from the query string
    try:
        output = subprocess.check_output(['python', f'src/api/{script_name}.py'])
        return jsonify(message=output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        return jsonify(message=str(e))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    username = 'MohitKambli'
    api_key = '9498e7d162a2714ada74b4257dce08a4dbafb36e'
    remote_path = f'/home/{username}/mysite/Images/{file.filename}'
    file_object = file
    url = f'https://www.pythonanywhere.com/api/v0/user/{username}/files/path{remote_path}'
    headers = {'Authorization': f'Token {api_key}'}
    files = {'content': file_object}
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 201:
        print("File uploaded successfully!")
    else:
        print("Failed to upload file. Error:", response.text)

    import subprocess
    result = subprocess.Popen(['python', 'fetch_colors_from_image.py', file.filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate()
    colors = stdout.decode().rstrip('\n')
    response_output = {'colors': colors}
    return jsonify(response_output)


if __name__ == '__main__':
    app.run(port=7020)

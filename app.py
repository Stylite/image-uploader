import os
from flask import Flask, render_template, request

app = Flask(__name__)

files_folder = os.path.basename('files')
app.config['files_folder'] = files_folder

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    filename = os.path.join(app.config['files_folder'], file.filename)
    file.save(filename)
    return render_template('index.html')
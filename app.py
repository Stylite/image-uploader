import json
import os
import random
import re
import sys
import gevent.monkey

from flask import Flask, redirect, render_template, request, abort

# gevent for async
gevent.monkey.patch_all()

# Configurable Options
debug = any(arg in sys.argv for arg in ['dev', 'development', 'debug'])
storage = os.path.basename('files')
port = 80

app = Flask(__name__)
extension_regex = re.compile(r"\.[a-z0-9]+$", re.IGNORECASE)


def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('authorization') and request.headers.get('authorization') in get_auth_keys():
            return view_function(*args, **kwargs)
        else:
            abort(json.dumps({'status': 401, 'error': 'Invalid authorization key. Message William#2222 or Kromatic#0420 for a key'}))
)

    return decorated_function


@app.route('/')
def index():
    return render_template('index.html')


@require_appkey
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return redirect('/')

    attachment = request.files.get('file', None)

    if not attachment:
        return json.dumps({'status': 400, 'error': 'Missing attachment "file"'})

    extension = extension_regex.search(attachment.filename)

    file_ext = extension.group().lower() if extension else '.png'
    file_name = generate_hex() + file_ext
    file_path = os.path.join(storage, file_name)
    attachment.save(file_path)

    return json.dumps({'status': 200, 'file': file_name})


def generate_hex(length=10):  # Defaults to 10
    return f"%0{length}x" % random.randrange(16**length)


def get_auth_keys():
    try:
        with open('keys.json') as keys:
            data = json.load(keys)
            if not isinstance(data, list):
                print('keys.json must only contain an array of valid auth tokens')
                return []
            else:
                return data
    except FileNotFoundError:
        print('keys.json wasn\'t found in the current directory')
        return []


if __name__ == '__main__':
    if debug:
        print('Webserver launching in debug mode')
        app.run(port=port)
    else:
        app.run(host='0.0.0.0', port=port)

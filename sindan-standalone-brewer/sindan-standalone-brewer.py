from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def list_files():
    directory = os.environ['HOME']+'/sindan-client/macos/log/'
    files = os.listdir(directory)

    data = {}
    for file in files:
        with open(os.path.join(directory, file), 'r') as f:
            content = [line[1:-1].split(',') for line in f.read().splitlines()]
            data[file] = content

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

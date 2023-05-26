import re
import os
from flask import Flask, render_template, jsonify
import json
from collections import deque

app = Flask(__name__)

@app.route('/')
def extract_and_display():
    file_path = './texts/Dialogue.txt'  # Replace with the actual file path
    start_variable = 'Cael'  # Replace with your specified variable
    conversation = deque(maxlen=4) # to send maximum 4 items
    conversation.append("Hello World!")
    conversation.append("Hello World 1!")
    conversation.append("Hello World 2!")
    conversation.append("Hello World 3!")

    with open(file_path, 'r') as file:
        content = file.read()

        # Find the first paragraph starting with the specified variable
        pattern = r'(^{}.*?\n\n)'.format(re.escape(start_variable))
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        if match:
            paragraph = match.group(0)
    paragraph = paragraph.replace('\"', '')
    # add to conversation thread
    data = {'cael_1': conversation[0], 'cael_2': conversation[1], 'knox_1': conversation[2],
            'knox_2': conversation[3], }
    print(paragraph)
    return render_template('index.html', paragraph=json.dumps(paragraph))

# @app.route('/get_paragraph')
# def get_paragraph():
#     paragraph = request.args.get('paragraph', '', type=str)
#     paragraph = jsonify(paragraph=paragraph)
#     print(paragraph)
#     return paragraph


if __name__ == '__main__':
    app.run()
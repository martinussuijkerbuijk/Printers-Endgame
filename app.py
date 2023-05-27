import re
import os
from flask import Flask, render_template, jsonify, Response, stream_with_context
import json
from collections import deque
from time import sleep
import random

app = Flask(__name__)

file_path = './texts/Dialogue.txt'  # Replace with the actual file path

cael = deque(maxlen=2) # to send maximum 2 items
knox = deque(maxlen=2) # to send maximum 2 items

cael.append("Hello World!")
cael.append("Hello World 1!")
knox.append("Hello World 2!")
knox.append("Hello World 3!")

@app.route('/')
def index():
    data = {'cael': list(cael), 'knox': list(knox)}
    return render_template('index.html', paragraph=data)


def extract_name(name):
    with open(file_path, 'r+') as file:
        content = file.read()

        # Find the first paragraph starting with the specified variable
        pattern = r'(^{}.*?\n\n)'.format(re.escape(name))
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        if match:
            paragraph = match.group(0)

            # Remove the paragraph from the content
            content = content.replace(paragraph, '\n', 1)

            # Strip leading newlines from the content
            content = content.lstrip('\n')

            # Move the file cursor to the beginning and truncate the file
            file.seek(0)
            file.truncate()

            # Write the updated content to the file
            file.write(content)

    return paragraph

def paragraph_to_data(paragraph, list_actor, name:str):

    paragraph = paragraph.replace('\"', '')
    # paragraph = paragraph.replace('\n', ' ')
    list_actor.append(paragraph)
    # add to conversation thread
    actor_name = {name: [list_actor[0],list_actor[1]]}
    print(actor_name)
    return actor_name

def actors_to_data(data):
    return data

@app.route('/update_chat')
def update_chat():
    def gen():
        while True:
            cael_par = extract_name('Cael:')
            sleep(1)
            knox_par = extract_name('Knox:')

            cael_dict = paragraph_to_data(cael_par, cael, 'cael')
            knox_dict = paragraph_to_data(knox_par, knox, 'knox')

            data = cael_dict | knox_dict
            print(f"Data is {data}")

            yield f"data: {json.dumps(data)}\n\n"
            sleep(random.randrange(20,30))

    return Response(stream_with_context(gen()), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run()
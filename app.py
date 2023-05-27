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
meta = deque(maxlen=1)

cael.append("Hello World!")
cael.append("Hello World 1!")
knox.append("Hello World 2!")
knox.append("Hello World 3!")

@app.route('/')
def index():
    data = {'cael': list(cael), 'knox': list(knox)}
    return render_template('index.html', paragraph=data)


def extract_name(names):
    with open(file_path, 'r+') as file:
        content = file.read()

        paragraphs = {}

        # Find the first paragraph starting with the specified variable
        for name in names:
            pattern = r'(^{}.*?\n\n)'.format(re.escape(name))
            match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
            if match:
                paragraph = match.group(0)
                paragraphs[name] = paragraph

                # Remove the paragraph from the content
                content = content.replace(paragraph, '\n', 1)

                # Strip leading newlines from the content
                content = content.lstrip('\n')

                # Move the file cursor to the beginning and truncate the file
                file.seek(0)
                file.truncate()

                # Write the updated content to the file
                file.write(content)

        # Find the first paragraph
        match_meta = re.search(r'(.*?\n)', content, re.MULTILINE | re.DOTALL)
        if match_meta:
            paragraph_meta = match_meta.group(0)

        if paragraph_meta.startswith('Cael:') or paragraph_meta.startswith('Knox:'):
            paragraphs['meta'] = ''
        else:
            # If the paragraph doesn't start with 'Cael:' or 'Knox:', handle it accordingly
            # Save the paragraph to a variable, delete it and save the file again
            non_name_paragraph = paragraph_meta  # Saving paragraph to a variable

            # Remove the paragraph from the content
            content = content.replace(non_name_paragraph, '\n', 1)

            # Strip leading newlines from the content
            content = content.lstrip('\n')

            # Move the file cursor to the beginning and truncate the file
            file.seek(0)
            file.truncate()

            # Write the updated content to the file
            file.write(content)
            print(non_name_paragraph)
            paragraphs['meta'] = non_name_paragraph


    return paragraphs


    # return paragraph

def paragraph_to_data(paragraph, list_actor, name:str):

    paragraph = paragraph.replace('\"', '')
    # paragraph = paragraph.replace('\n', ' ')
    list_actor.append(paragraph)
    if len(list_actor) > 1:
        # add to conversation thread
        actor_name = {name: [list_actor[0],list_actor[1]]}
    else:
        actor_name = {name: [list_actor[0]]}
    return actor_name

def actors_to_data(data):
    return data

@app.route('/update_chat')
def update_chat():
    def gen():
        while True:
            paragraphs = extract_name(['Cael:', 'Knox:'])
            print(f"Paragraphs are: ", paragraphs)
            sleep(1)
            # meta_name, meta_content = extract_name()

            dict_cael = paragraph_to_data(paragraphs['Cael:'], cael, 'Cael:')
            dict_knox = paragraph_to_data(paragraphs['Knox:'], knox, 'Knox:')
            dict_meta = paragraph_to_data(paragraphs['meta'], meta, 'meta')

            data = dict_cael | dict_knox | dict_meta
            print(f"Data is {data}")

            yield f"data: {json.dumps(data)}\n\n"
            sleep(random.randrange(10,15))

    return Response(stream_with_context(gen()), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run()
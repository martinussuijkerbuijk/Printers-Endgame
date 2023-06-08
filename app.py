import re
import serial
import adafruit_thermal_printer
from flask import Flask, render_template, jsonify, Response, stream_with_context
import json
from collections import deque
from time import sleep
import random

app = Flask(__name__)

# Connect to UART
uart_cael = serial.Serial("COM1", baudrate=19200, timeout=3000)
uart_knox = serial.Serial("COM2", baudrate=19200, timeout=3000)

#Initialize printer Cael
ThermalPrinter_cael = adafruit_thermal_printer.get_printer_class(2.69)
printer_cael = ThermalPrinter_cael(uart_cael)

#Set parameter to upside down
printer_cael.up_down_mode = True

#Initialize printer Cael
ThermalPrinter_knox = adafruit_thermal_printer.get_printer_class(2.69)
printer_knox = ThermalPrinter_cael(uart_knox)

#Set parameter to upside down
printer_knox.up_down_mode = True

file_path = './texts/Dialogue.txt'  # Replace with the actual file path

cael = deque(maxlen=2) # to send maximum 2 items
knox = deque(maxlen=2) # to send maximum 2 items
meta = deque(maxlen=1)

cael.append("Hello World!")
cael.append("Hello World 1!")
knox.append("Hello World 2!")
knox.append("Hello World 3!")

def connect_test(printer_name):
    printer_name.print('Hello from the thermal Printer! Think about your exhibition Running smooth!')
    printer_name.feed(1)

@app.route('/')
def index():
    data = {'cael': list(cael), 'knox': list(knox)}
    return render_template('index.html', paragraph=data)


def print_text_printer(printer, lines):
    # Print lines in reversed order
    for line in reversed(lines):
        printer.print(line)
    printer.feed(1)


def print_max_line_length(printer, text):
    line_length = 32
    words = text.split()
    current_line_length = 0
    lines = []

    for word in words:
        word_length = len(word)

        if current_line_length + word_length <= line_length:
            # Word fits within the line length
            if not lines:
                lines.append(word)
            else:
                lines[-1] += " " + word
            current_line_length += word_length + 1  # Account for the space after the word
        else:
            # Word doesn't fit within the line length
            lines.append(word)
            current_line_length = word_length + 1  # Account for the space after the word

    print_text_printer(printer, lines)


def extract_name(names):

    with open(file_path, 'r+', encoding='utf-8') as file:

        content = file.read()

        paragraphs = {}
        before_quotes = ""  # Initialize before_quotes

        # Find the first paragraph starting with the specified variable
        for name in names:
            # pattern = r'(^{}.*?\n\n)'.format(re.escape(name))
            pattern = r'(^{}.*?".*?(\n\n|$))'.format(re.escape(name))
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

                before_quotes, rest = paragraph.split('"', 1) # Split at the first quote

                # Print the paragraph to printer
                # if name == 'Cael':
                #     print_max_line_length(printer_cael, rest)
                #     sleep(random.randrange(1, 5))
                # if name == 'Knox':
                #     print_max_line_length(printer_knox, rest)
                #     sleep(1)
                paragraphs[name] = rest

        # Find the first paragraph
        match_meta = re.search(r'(.*?\n)', content, re.MULTILINE | re.DOTALL)
        if match_meta:
            paragraph_meta = match_meta.group(0)

        if paragraph_meta.startswith('Cael:') or paragraph_meta.startswith('Knox:'):
            paragraphs['meta'] = ''
        else:
            if len(before_quotes) > 8:
                paragraphs['meta'] = before_quotes
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
            paragraphs = extract_name(['Cael', 'Knox'])
            print(f"Paragraphs are: ", paragraphs)
            sleep(1)
            # meta_name, meta_content = extract_name()

            dict_cael = paragraph_to_data(paragraphs['Cael'], cael, 'Cael')
            dict_knox = paragraph_to_data(paragraphs['Knox'], knox, 'Knox')
            dict_meta = paragraph_to_data(paragraphs['meta'], meta, 'meta')

            data = dict_cael | dict_knox | dict_meta

            yield f"data: {json.dumps(data)}\n\n"
            # Print the paragraph to printer

            print_max_line_length(printer_cael, paragraphs['Knox'])
            sleep(random.randrange(1, 5))

            print_max_line_length(printer_knox, paragraphs['Cael'])
            sleep(1)

            sleep(random.randrange(25,45))

    return Response(stream_with_context(gen()), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run()
import serial
import adafruit_thermal_printer
import re
from time import sleep
import random

# Connect to UART
uart = serial.Serial("COM1", baudrate=19200, timeout=3000)

#Initialize printer
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
printer = ThermalPrinter(uart)

#Set parameter to upside down
printer.up_down_mode = True


def connect_test(name):
    printer.print('Hello from the thermal Printer! Think about your exhibition Running smooth!')
    printer.feed(1)


def print_text_printer(lines):
    # Print lines in reversed order
    for line in reversed(lines):
        printer.print(line)
    printer.feed(1)


def extract_and_remove_paragraph(file_path, start_variable):
    with open(file_path, 'r+') as file:
        content = file.read()

        # Find the first paragraph starting with the specified variable
        pattern = r'(^{}.*?\n\n)'.format(re.escape(start_variable))
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        if match:
            paragraph = match.group(0)
            print("Extracted paragraph:")
            print(paragraph)

            print_max_line_length(paragraph)

            # Remove the paragraph from the content
            content = content.replace(paragraph, '', 1)

            # Move the file cursor to the beginning and truncate the file
            file.seek(0)
            file.truncate()

            # Write the updated content to the file
            file.write(content)


def print_max_line_length(text):
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

    print_text_printer(lines)
    # return lines



# Example usage
text = "This is a long text that needs to be printed in lines with a maximum of 32 characters."

# Initialize parameters
file_path = './texts/Dialogue.txt'
start_variable = 'Cael'  # Replace with your specified variable

# Run script
if __name__ == '__main__':
    # connect_test('COM2')
    while True:
        extract_and_remove_paragraph(file_path, start_variable)
        sleep(random.randrange(10,30))
    # print_max_line_length(text)



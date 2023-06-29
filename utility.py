import re
import codecs

def convert_lines_to_paragraphs(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    paragraphs = []
    for line in lines:
        paragraph = line.strip()
        if paragraph:
            paragraphs.append(paragraph)

    with open(output_file, 'w') as file:
        file.write('\n\n'.join(paragraphs))

def filter_text_file(file_path):
    # Alternates text file with Knox and Cael
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()

        keywords = ['Knox:', 'Cael:']
        keyword_index = 0

        for line in lines:
            if line.strip().startswith(keywords[keyword_index]):
                file.write(line)
                keyword_index = (keyword_index + 1) % len(keywords)


def count_nonempty_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        count = sum(1 for line in file if line.strip())
    return count


def append_text_file(source_file, destination_file):
    with open(source_file, 'r') as source:
        with open(destination_file, 'a') as destination:
            for line in source:
                destination.write(line)

def format_paragraphs_in_file(input_file, output_file):
    with open(input_file, 'r') as file:
        paragraphs = file.read().split('\n\n')

    formatted_paragraphs = []
    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        formatted_lines = []
        for line in lines:
            if 'Ah, ' in line:
                line = re.sub(r'\([^()]*\)', '', line)  # Remove text within brackets
                line = line.replace('Ah, ', '', 1).capitalize()
            formatted_lines.append(line)
        formatted_paragraphs.append('\n'.join(formatted_lines))

    with open(output_file, 'w') as file:
        file.write('\n\n'.join(formatted_paragraphs))


def within_quotes(input_file, output_file):
    with open(input_file, 'r') as file:
        paragraphs = file.read().split('\n\n')

    formatted_paragraphs = []
    for paragraph in paragraphs:
        if paragraph.startswith(('Knox:', 'Cael:')):
            colon_index = paragraph.index(':')
            text_after_colon = paragraph[colon_index + 1:].strip()
            if not text_after_colon.startswith('"') or not text_after_colon.endswith('"'):
                paragraph = f'{paragraph[:colon_index + 1]} "{text_after_colon}"'
        formatted_paragraphs.append(paragraph)

    with open(output_file, 'w') as file:
        file.write('\n\n'.join(formatted_paragraphs))


def remove_brackets(input_file, output_file):
    with open(input_file, 'r') as file:
        paragraphs = file.read().split('\n\n')

    formatted_paragraphs = []
    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        formatted_lines = []
        within_quotes = False
        for line in lines:
            if line.startswith('"') and line.endswith('"'):
                within_quotes = not within_quotes

            if not within_quotes:
                if line.startswith('Ah, '):
                    line = line[4:].capitalize()

            formatted_lines.append(line)

        formatted_paragraph = '\n'.join(formatted_lines)
        if not re.search(r'\([^()]*\)', formatted_paragraph):
            formatted_paragraphs.append(formatted_paragraph)

    with open(output_file, 'w') as file:
        file.write('\n\n'.join(formatted_paragraphs))


def capitalize_after_double_quote_in_file(input_file, output_file):
    with open(input_file, 'r') as file:
        paragraphs = file.read().split('\n\n')

    capitalized_paragraphs = []
    for paragraph in paragraphs:
        start_index = paragraph.find('"')
        if start_index != -1:
            next_index = start_index + 1
            if next_index < len(paragraph):
                paragraph = paragraph[:next_index] + paragraph[next_index].capitalize() + paragraph[next_index + 1:]
        capitalized_paragraphs.append(paragraph)

    with open(output_file, 'w') as file:
        file.write('\n\n'.join(capitalized_paragraphs))


def convert_ansi_to_utf8(input_file, output_file):
    with codecs.open(input_file, 'r', encoding='ANSI') as source_file:
        content = source_file.read()

    with codecs.open(output_file, 'w', encoding='UTF-8') as target_file:
        target_file.write(content)

input_file = './texts/Dialogue_extra_p.txt'
output_file = './texts/Dialogue_extra_p.txt'
#
# convert_lines_to_paragraphs(input_file, output_file)

# file_path = './texts/Dialogue_adaptive_q.txt'
# filter_text_file(input_file)

# line_count = count_nonempty_lines(output_file)
# print("Number of non-empty lines:", line_count)

# # Append file
source_file_path = './texts/Dialogue_extra_p.txt'
destination_file_path = './texts/Dialogue.txt'

append_text_file(source_file_path, destination_file_path)

# remove_brackets(input_file, output_file)
# capitalize_after_double_quote_in_file(input_file, output_file)
# convert_ansi_to_utf8(input_file, output_file)
# format_paragraphs_in_file(input_file, output_file)
# within_quotes(input_file, output_file)
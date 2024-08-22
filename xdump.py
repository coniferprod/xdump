#!/usr/bin/env python3

import sys

BYTES_PER_LINE = 16
SPACE = ' '

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def make_line(data, offset, options):
    bytes_per_line = options['bytes_per_line']
    lowercase = options['lowercase']

    line = f'{offset:010}: '

    bytes_done = 0
    characters = SPACE
    for b in data:
        line += f'{b:02x} ' if lowercase else f'{b:02X} '
        offset += 1
        bytes_done += 1

        ch = chr(b)
        characters += ch if ch.isprintable() else '.'

    # All data processed, output whitespace to fill out the line
    # if there were less bytes than the full amount.
    while bytes_done < bytes_per_line:
        line += SPACE*3  # for each missing byte
        characters += SPACE
        bytes_done += 1

    line += characters
    return line

def dump(data, options):
    bytes_per_line = options['bytes_per_line']
    line_data = chunks(data, bytes_per_line)

    offset = 0
    for ld in line_data:
        line = make_line(ld, offset, options)
        print(line)
        offset += bytes_per_line

def run(filename, options):
    with open(filename, 'rb') as f:
        data = f.read()

    dump(data, options)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: xdump file')
        sys.exit(1)
    
    filename = sys.argv[1]
    options = {'bytes_per_line': BYTES_PER_LINE, 'lowercase': False}
    run(filename, options)

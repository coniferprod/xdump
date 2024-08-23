#!/usr/bin/env python3

import os
import argparse
import pprint

DEBUG = False
BYTES_PER_LINE = 16
SPACE = ' '

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def make_line(data, offset, options):
    bytes_per_line = options['bytes_per_line']
    uppercase = options['uppercase']

    line = f'{offset:010}: '

    bytes_done = 0
    characters = SPACE
    for b in data:
        line += f'{b:02X} ' if uppercase else f'{b:02x} '
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
    if DEBUG:
        pprint.pprint(options)

    with open(filename, 'rb') as f:
        data = f.read()

    start = options['start_offset']
    length = options['dump_length']
    dump(data[start : start + length], options)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='xdump',
        description='Show hexadecimal dump of file'
    )
    parser.add_argument('filename')  # positional argument
    parser.add_argument('-b', '--bytesperline', type=int, default=BYTES_PER_LINE, help='How many bytes to show per line')
    parser.add_argument('-s', '--start', type=int, help='Offset in file for the start of the dump', default=0)
    parser.add_argument('-l', '--length', type=int, help='Length of dump in bytes from the start offset')
    parser.add_argument('-u', '--uppercase', action=argparse.BooleanOptionalAction, help='Show hex digits in upper case')

    args = parser.parse_args()

    file_stat = os.stat(args.filename)
    length = file_stat.st_size
    if args.length:
        length = args.length

    options = {
        'bytes_per_line': args.bytesperline, 
        'uppercase': args.uppercase,
        'start_offset': args.start,
        'dump_length': length
    }
    run(args.filename, options)

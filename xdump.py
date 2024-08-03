#!/usr/bin/env python3

import sys

BYTES_PER_LINE = 16
SPACE = ' '

def run(filename, options):
    with open(filename, 'rb') as f:
        data = f.read()

    counter = 0
    bytes_done = 0
    print(f'{counter:010}: ', end='')

    bytes_per_line = options['bytes_per_line']
    gap = options['gap']
    lowercase = options['lowercase']

    characters = ''
    for b in data:
        if lowercase:
            print(f'{b:02x} ', end='')
        else:
            print(f'{b:02X} ', end='')
        counter += 1
        bytes_done += 1

        ch = chr(b)
        if ch.isprintable():
            characters += ch
        else:
            characters += '.'

        if gap:
            if bytes_done == bytes_per_line // 2:
                print(SPACE, end='')
                characters += SPACE
        if bytes_done % bytes_per_line == 0:
            print(f'  {characters}')
            bytes_done = 0
            characters = ''
            print(f'{counter:010}: ', end='')

    # All data processed, output whitespace to fill out the line,
    # and then output the rest of the characters.
    while bytes_done < bytes_per_line:
        #print(f'bytes_done = {bytes_done} ')
        print(SPACE*3, end='')
        bytes_done += 1
    else:
        if gap:
            print(SPACE, end='')
    print(f'  {characters}')
    # TODO: Something is off with the gap.

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: xdump file')
        sys.exit(1)
    
    filename = sys.argv[1]
    options = {'bytes_per_line': BYTES_PER_LINE, 'gap': True, 'lowercase': True}
    run(filename, options)

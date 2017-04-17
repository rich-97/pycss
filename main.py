#!/usr/bin/env python

import sys
import re
import os

# Configuarion default.
cfg = {
    'file': None,
    'output_dir': '.',
    'output_file': None,
    'debug': False
}

usage = """
Usage:
    pycss [option] [value] ...

Options:

    --help, -h: Print the usage.
    --file, -f: Set the source file.
    --output-file, -o: Set the output file.
    --output-dir, -d: Set the output directory.
    --debug, -D: Set debuging, the default value is False.
"""


def print_usage():
    print usage
    exit(1)

if len(sys.argv) > 1:
    ARGV = sys.argv
    ARGV.remove(sys.argv[0])
    it = iter(ARGV)
    it.next()
    count = 1

    # Get options.
    for arg in ARGV:
        opt_re = re.match('^-', arg)

        if opt_re:
            opt_str = opt_re.string

            if opt_str == '--file' or opt_str == '-f':
                cfg['file'] = it.next()
                count += 1
            elif opt_str == '--output-file' or opt_str == '-o':
                cfg['output_file'] = it.next()
                count += 1
            elif opt_str == '--output-dir' or opt_str == '-d':
                cfg['output_dir'] = it.next()
                count += 1
            elif opt_str == '--debug' or opt_str == '-D':
                cfg['debug'] = bool(it.next())
                count += 1
            elif opt_str == '--help' or opt_str == '-h':
                print_usage()
            else:
                print 'Option invalid:', opt_str
                print_usage()

        else:
            # This is for StopIteration exception.
            if count < len(ARGV):
                it.next()
                count += 1
else:
    print_usage()


file = cfg.get('file')
output_file = cfg.get('output_file')
output_dir = cfg.get('output_dir')

if re.match('[a-z]*\.pycss', file) is None:
    cfg['file'] = file + '.pycss'

if output_file is None:
    file_basename = os.path.basename(cfg.get('file'))
    cfg['output_file'] = re.sub('\.pycss$', '.css', file_basename)

if re.match('[a-z]*\.css', output_file) is None:
    cfg['output_file'] = output_file + '.css'

if output_dir != '.':
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

src = open(cfg.get('file'), 'r')
pycss = src.read()
src.close()

# Output css source.
out = ''

# Parse.
if len(pycss) > 0:
    lines = re.split('\n', pycss)

    for line in lines:
        if re.match('^\w', line):
            out += line + ' {\n'
        elif re.match('^\W', line):
            terms = line.split()
            spaces = line.count(' ') - 1
            out += ' ' * spaces
            out += terms[0] + ': '
            out += terms[1] + ';'
            out += '\n'
        else:
            out += '}\n'
    
    out = re.sub('}\n$', '', out)
else:
    print 'The source file is empty.'
    exit(1)

output = open(os.path.join(output_dir, cfg.get('output_file')), 'w')
output.write(out)
output.close()

if cfg.get('debug'):
    for item in cfg.items():
        print item[0] + ':', item[1]


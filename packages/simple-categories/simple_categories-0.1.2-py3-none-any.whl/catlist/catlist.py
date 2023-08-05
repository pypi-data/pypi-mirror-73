# coding: utf8
"""
Reads lines from a plaintext file, separated by categories.

Category names are delimited by square brackets as the first and last
characters of the line.

Items in each category are just plain text, one item per line

Any lines before the first category will be assigned to 'uncategorized'

The format is simmilar to .ini files, only you don't have thei 'key'='value'
structure in the items.

Blank lines and lines that begin with '#' are ignored.

Example of a file:
------------------

# the following lines will be assigned to 'uncategorized`

Linux
Windows
MacOS

[Directories]
/home
/usr
/etc

# this line will be ignored

[Files]
README.md
module.py
"""

__title__ = "Simple Categories"
__version__ = "0.1.2"
__license__ = "GNU General Public License v2 or later (GPLv2+)"
__author__ = "Bento Loewenstein"

import sys

def catlist(catfile):
    """
    Returns a dictionary containing the categories and items read from
    the file passed as argument
    """
    fulldata = {}
    plain_text = u''

    # Just make sure the parameters are sane
    if not isinstance(catfile, str):
        raise TypeError('File name must be a string')
    if not catfile:
        raise ValueError('File name can not be empty')

    # Open file read-only and reads all lines
    try:
        plain_text = open(catfile, 'r')
    except OSError:
        print("Could not open file {}".format(catfile), file=sys.stderr)
        raise

    # just in case someone tries to read a file without any valid category
    # or with lines before the first true category, puts the lines on a
    # default category
    cur_category = 'uncategorized'
    for lin in plain_text:
        # let's skip blank line. first strip all spaces, left and right
        lin = lin.strip()
        # decide what to do. If a category line is well formed, create it, otherwise
        # add the line to an existing one
        if not lin or lin[0] == '#':
            continue
        if lin[0] == '[' and lin[-1] == ']':
            cur_category = lin[1:-1]
            # what happens if the category already exists ?
            fulldata.setdefault(cur_category, [])
        else:
            if fulldata.setdefault(cur_category):
                fulldata[cur_category].append(lin)
            else:
                fulldata[cur_category] = [lin]

    return fulldata

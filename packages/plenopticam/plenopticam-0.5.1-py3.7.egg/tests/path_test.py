#!/usr/bin/env python

from os.path import join, abspath, relpath, basename

if __name__ == '__main__':

    print(join('.', 'examples', 'data'))
    print(abspath('.'))
    print(basename(abspath('.')))
    print(relpath('.'))

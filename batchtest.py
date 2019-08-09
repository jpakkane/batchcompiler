#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2019 Jussi Pakkanen
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys, os, subprocess, shutil, random

iface_template = '''export module M{};

// Import statements here.
import M{};
import M{};

export int f{}() {{
  return f{}() + f{}();
}}
'''

root_case = '''export module M{};

export int f{}() {{
    return 1;
}}
'''

class BatchTest:

    def __init__(self):
        if not shutil.which('cl'):
            sys.exit('cl.exe not found, run from the VS tools prompt.')
        self.num_files = 100

    def fnames_for(self, i):
        return ('src{}.ixx'.format(i),
                'M{}.ifc'.format(i),
                'src{}.obj'.format(i))

    def create_files(self):
        if os.path.exists(self.fnames_for(0)[0]):
            print('Sources already exist.')
            return
        for i in range(self.num_files):
            first = i + random.randint(1, 5)
            second = i + random.randint(1, 5)
            first = min(first, self.num_files-1)
            second = min(second, self.num_files-1)
            fnames = self.fnames_for(i)
            if i == self.num_files - 1:
                with open(fnames[0], 'w') as ofile:
                    ofile.write(root_case.format(i, i))
            else:
                with open(fnames[0], 'w') as ofile:
                    ofile.write(iface_template.format(i, first, second, i, first, second))
    def compile(self):
        pass

if __name__ == '__main__':
    bt = BatchTest()
    bt.create_files()
    bt.compile()


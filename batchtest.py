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
        self.cl_cmd = ['cl', '/nologo', '/c', '/experimental:module']
        self.input_sources = set()
        self.waiting_for = {} # Key is module ID, value is sources waiting for said module.

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

    def mark_as_needing(self, trial, missing_mod):
        if missing_mod not in self.waiting_for:
            self.waiting_for[missing_mod] = [trial]
        else:
            self.waiting_for[missing_mod].append(trial)

    def try_compile(self, trial):
        src_name = self.fnames_for(trial)[0]
        cp = subprocess.run(self.cl_cmd + [src_name],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
        if cp.returncode == 0:
            return None
        assert('could not find module' in cp.stdout)
        for message_line in cp.stdout.split('\n'):
            if 'could not find module' in message_line:
                return int(message_line.split("'")[-2][1:])
        sys.exit('Could not find module error message!')

    def module_created(self, modname):
        for new_one in self.waiting_for.pop(modname, []):
            self.input_sources.add(new_one)
        print('Module', modname, 'finished')

    def build(self):
        for i in range(self.num_files):
            # In the real implementation the compiler would have to check
            # here if the input source is up to date. That is, if
            # the output object file exists and is newer than all files
            # it depends on. It might make sense to delete all
            # the output ifc file immediately for all stale files.
            self.input_sources.add(i)
        while len(self.input_sources) > 0:
            trial = self.input_sources.pop()
            missing_mod = self.try_compile(trial)
            if missing_mod is not None:
                self.mark_as_needing(trial, missing_mod)
            else:
                self.module_created(trial)
        if len(self.waiting_for) > 0:
            print(self.waiting_for)
            sys.exit('Could not compile all sources in this target. Bad module dependencies.')

if __name__ == '__main__':
    bt = BatchTest()
    bt.create_files()
    bt.build()


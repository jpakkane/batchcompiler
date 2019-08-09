# Batch compiler for C++ modules feasibility study

A simple Python script that implements the core of [this blog
post](https://nibblestew.blogspot.com/2019/08/building-c-modules-take-n1.html). This
only works with Visual Studio currently, as it ships the most complete
module implementation as of today.

Using it is just a matter of running the script:


    python batchtest.py

This script will fail if you run a localised version of Visual
Studio. It requires all error messages to be in English.

All object files should get created in the correct order without
needing to scan the contents of files.

## Caveats

- This implementation launches two processes (about) per source
  file. In a real implementatio the compilation processes would not
  exit but instead would suspend until other compilation processes
  would finish building modules. This causes a 2x slowdown for this
  script compared to a proper implementation.

- The script uses only one thread for simplicity. A real
  implementation could spawn multiple compilation threads or
  processes.

- This script does not do incremental builds. The source code is
  marked with the location where that check would be needed. This
  approach requires, at the least, modifying the compiler so that it
  can read `.d` dependency files.

- This implementation determines the missing modules by reading the
  compiler's output. In a full implementation there would be some
  different communication mechanism between the work launcher and
  worker threads. But it would be an implementation detail of the
  compiler and would not be exposed to anyone else.

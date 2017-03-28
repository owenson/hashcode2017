#!/bin/bash

#Run as:
#bash run.sh attempt1.py
#bash run.sh attempt2.py
# ...

cd problems
for f in *; do
    echo Processing $f
    pypy ../score.py $f ../solutions/$f.sol
done

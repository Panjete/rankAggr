#!/bin/bash

echo "Processing Condorcet!" 
args=()
while [ "$1" != "" ]; do
    args+=("$1")
    shift
done
python condorcet.py "${args[@]}"
echo "Shell script successfully terminated!
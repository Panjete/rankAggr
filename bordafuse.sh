#!/bin/bash

echo "Processing Bordafuse!" 
args=()
while [ "$1" != "" ]; do
    args+=("$1")
    shift
done
python bordafuse.py "${args[@]}"
echo "Shell script successfully terminated!"
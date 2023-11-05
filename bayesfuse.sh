#!/bin/bash

echo "Processing Bayesfuse!" 
args=()
while [ "$1" != "" ]; do
    args+=("$1")
    shift
done
python bayesfuse.py "${args[@]}"
echo "Shell script successfully terminated!"
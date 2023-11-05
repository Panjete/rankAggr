#!/bin/bash

echo "Processing Bordacount!" 
args=()
while [ "$1" != "" ]; do
    args+=("$1")
    shift
done
python bordacount.py "${args[@]}"
echo "Shell script successfully terminated!
#!/bin/bash

echo "Processing Bordacount Aggregation!" 
args=()
while [ "$1" != "" ]; do
    args+=("$1")
    shift
done
python rrf.py "${args[@]}"
echo "Shell script successfully terminated!
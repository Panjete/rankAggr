#!/bin/bash

echo "Processing Reciprocal Rank Fusion (RRF)!" 
args=()
while [ "$1" != "" ]; do
    args+=("$1")
    shift
done
python rrf.py "${args[@]}"
echo "Shell script successfully terminated!"
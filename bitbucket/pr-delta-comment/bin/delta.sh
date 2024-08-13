#!/bin/bash

# Check if filename is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename="$1"

# Check if file exists
if [ ! -f "$filename" ]; then
    echo "File not found: $filename"
    exit 1
fi

# Search for the last occurrence of the underscore pattern from the snyk-delta output
last_match=$(grep -n '_____________________________' "$filename" | tail -n 1 | cut -d: -f1)

# If no match found, print entire file
if [ -z "$last_match" ]; then
    echo "Invalid file"
    exit 1
else
    # Extract content after the last match
    tail -n +"$((last_match + 1))" "$filename"
fi
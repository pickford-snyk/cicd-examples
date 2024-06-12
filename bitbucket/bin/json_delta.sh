#!/bin/bash

filename="$1"

parse_input() {
    local id=""
    local via=""
    local fixed_in=""
    local fixable_by_upgrade=""
    
    echo "["

    while IFS= read -r line; do
        if [[ "$line" =~ SNYK-JS-([[:alnum:]-]+): ]]; then
            if [ ! -z "$id" ]; then
                # Output the previous node
                echo "{"
                echo "\"Snyk ID\": \"$id\","
                echo "\"Via\": \"$via\","
                echo "\"Fixed in\": \"$fixed_in\","
                echo "\"Fixable by upgrade\": \"$fixable_by_upgrade\""
                echo "},"
            fi
            # Start a new node
            id="${BASH_REMATCH[1]}"
            via=""
            fixed_in=""
            fixable_by_upgrade=""
        elif [[ "$line" =~ Via:\ (.+) ]]; then
            via="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ Fixed\ in:\ (.+) ]]; then
            fixed_in="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ Fixable\ by\ upgrade:\ (.+) ]]; then
            fixable_by_upgrade="${BASH_REMATCH[1]}"
        fi
    done < "$filename"

    # Output the last node
    echo "{"
    echo "\"Snyk ID\": \"$id\","
    echo "\"Via\": \"$via\","
    echo "\"Fixed in\": \"$fixed_in\","
    echo "\"Fixable by upgrade\": \"$fixable_by_upgrade\""
    echo "}"

    echo "]"
}

parse_input